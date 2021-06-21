import csv

from django.http import HttpResponse
from django.views.generic import TemplateView, dates
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Race, Racer, Result


class RaceMixin:
    queryset = Race.objects.all()
    date_field = "start_datetime"
    allow_future = True
    navitem = "races"


class RaceIndex(TemplateView):
    template_name = "races/races.html"
    navitem = "races"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["completed_races"] = Race.objects.complete().order_by("-start_datetime")
        context["upcoming_races"] = Race.objects.upcoming().order_by("start_datetime")
        return context


# class RaceIndex(RaceMixin, dates.ArchiveIndexView):
#    make_object_list = True
#    pass


class RaceUpcomingList(ListView):
    queryset = Race.objects.upcoming()
    template_name = "races/upcoming.html"
    navitem = "races"


class RaceYear(RaceMixin, dates.YearArchiveView):
    pass


class RaceMonth(RaceMixin, dates.MonthArchiveView):
    pass


class RaceDay(RaceMixin, dates.DayArchiveView):
    pass


class RaceDateDetail(RaceMixin, dates.DateDetailView):
    queryset = Race.objects.all()


class RaceResultDetail(RaceMixin, dates.DateDetailView):
    queryset = Race.objects.all()
    template_name = "races/race_result.html"


class RaceResultCsvDetail(RaceMixin, dates.DateDetailView):
    queryset = Race.objects.all()
    template_name = "races/race_result.html"

    def get(self, *args, **kwargs):
        race = self.get_object()

        if self.request.GET.get("plain"):
            response = HttpResponse(content_type="text/plain")
        else:
            response = HttpResponse(content_type="text/csv")
            response[
                "Content-Disposition"
            ] = f"attachment; filename={race.slug}_{race.start_datetime.year}_results.csv"

        results = Result.objects.filter(race=race).order_by("dq", "dnf", "dns", "time")

        result_list = csv.writer(response)
        result_list.writerow(
            [
                "race.title",
                "race.start_datetime.year",
                "racer.bib_number",
                "racer.full_name",
                "time",
                "place",
            ]
        )

        for result in results:
            time = str(result.time).replace(",", ":")
            if result.dq:
                time = "DQ"
            elif result.dns:
                time = "DNS"
            elif result.dnf:
                time = "DNF"

            result_list.writerow(
                [
                    result.race.title,
                    result.race.start_datetime.year,
                    result.bib_number,
                    result.racer.full_name,
                    time,
                    result.place,
                ]
            )

        return response


class RacerDetail(DetailView):
    model = Racer
    navitem = "races"


class RacerList(ListView):
    model = Racer
    navitem = "races"
