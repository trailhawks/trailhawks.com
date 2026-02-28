import csv
import json
import re

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView, dates
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .agents import apply_race_changes, compute_race_diff, run_chat_agent, run_race_agent
from .forms import RaceAgentForm
from .models import Race, Racer, Result, Series
from .schemas import RaceAgentResult


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
            response["Content-Disposition"] = f"attachment; filename={race.slug}_{race.start_datetime.year}_results.csv"

        results = Result.objects.filter(race=race).order_by("race_type__name", "dq", "dnf", "dns", "time")

        result_list = csv.writer(response)
        result_list.writerow(
            [
                "race.title",
                "race.start_datetime.year",
                "race_type.name",
                "racer.bib_number",
                "racer.full_name",
                "racer.gender",
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
                    result.race_type.name,
                    result.race.start_datetime.year,
                    result.bib_number,
                    result.racer.full_name,
                    result.racer.gender,
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


class SeriesResultCsvDetail(DetailView):
    queryset = Series.objects.all()
    template_name = "races/race_result.html"

    def get(self, *args, **kwargs):
        series = self.get_object()

        if self.request.GET.get("plain"):
            response = HttpResponse(content_type="text/plain")
        else:
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = f"attachment; filename={series.slug}_results.csv"

        results = Result.objects.filter(race__in=series.races.all()).order_by(
            "race__name",
            "race__start_datetime__year",
            "race_type__name",
            "dq",
            "dnf",
            "dns",
            "time",
        )

        result_list = csv.writer(response)
        result_list.writerow(
            [
                "race.title",
                "race.start_datetime.year",
                "race_type.name",
                "racer.bib_number",
                "racer.full_name",
                "racer.gender",
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
                    result.race_type.name,
                    result.bib_number,
                    result.racer.full_name,
                    result.racer.gender,
                    time,
                    result.place,
                ]
            )

        return response


class RaceAgentView(LoginRequiredMixin, FormView):
    template_name = "races/race_agent.html"
    form_class = RaceAgentForm

    def post(self, request, *args, **kwargs):
        # Phase 2: confirm and apply
        if request.POST.get("confirm"):
            race_pk = request.POST.get("race_pk")
            agent_result_json = request.POST.get("agent_result_json")
            try:
                race = Race.objects.get(pk=race_pk)
                result = RaceAgentResult.model_validate_json(agent_result_json)
                changes = compute_race_diff(race, result)
                apply_race_changes(race, changes)
                messages.success(request, f"Applied {len(changes)} change(s) to {race}.")
            except Race.DoesNotExist:
                messages.error(request, "Race not found.")
            except Exception as e:
                messages.error(request, f"Error applying changes: {e}")
            return redirect("race_agent")

        # Phase 1: fetch and preview
        form = self.get_form()
        if form.is_valid():
            race = form.cleaned_data["race"]
            url = form.cleaned_data["url"]
            try:
                result = run_race_agent(url)
                changes = compute_race_diff(race, result)
                if not changes:
                    messages.info(request, "No changes detected from the provided URL.")
                    return redirect("race_agent")
                context = self.get_context_data(
                    form=form,
                    changes=changes,
                    race=race,
                    agent_result_json=result.model_dump_json(),
                )
                return self.render_to_response(context)
            except Exception as e:
                messages.error(request, f"Error fetching race data: {e}")
                return redirect("race_agent")
        return self.form_invalid(form)


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class RaceChatView(StaffRequiredMixin, TemplateView):
    template_name = "races/race_chat.html"

    def get_race(self):
        return Race.objects.get(pk=self.kwargs["pk"])

    def session_key(self):
        return f"race_chat_history_{self.kwargs['pk']}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        race = self.get_race()
        context["race"] = race
        context["chat_history"] = self.request.session.get(self.session_key(), [])
        return context

    def post(self, request, *args, **kwargs):
        race = self.get_race()
        session_key = self.session_key()

        # Handle clearing chat history
        if request.POST.get("clear_chat"):
            request.session.pop(session_key, None)
            return redirect("race_chat", pk=race.pk)

        user_message = request.POST.get("message", "").strip()
        if not user_message:
            return redirect("race_chat", pk=race.pk)

        chat_history = request.session.get(session_key, [])
        chat_history.append({"role": "user", "content": user_message})

        try:
            response_text = run_chat_agent(race, user_message)

            # Check for JSON update blocks in the response
            updates = self._extract_updates(response_text)
            applied_fields = []
            if updates:
                for field, value in updates.items():
                    if field in [
                        "title",
                        "annual",
                        "number",
                        "slogan",
                        "description",
                        "distance",
                        "unit",
                        "start_datetime",
                        "course_map",
                        "cut_off",
                        "reg_url",
                        "reg_description",
                        "ultrasignup_id",
                        "awards",
                        "discounts",
                        "lodging",
                        "packet_pickup",
                        "facebook_url",
                        "facebook_event_url",
                        "race_type",
                        "active",
                    ]:
                        if field in ("unit", "race_type", "number"):
                            value = int(value) if value is not None else None
                        elif field == "active":
                            value = value if isinstance(value, bool) else str(value).lower() == "true"
                        setattr(race, field, value)
                        applied_fields.append(field)
                if applied_fields:
                    race.save(update_fields=applied_fields)
                    response_text += f"\n\n_Applied updates to: {', '.join(applied_fields)}_"

            chat_history.append({"role": "assistant", "content": response_text})

        except Exception as e:
            chat_history.append({"role": "assistant", "content": f"Error: {e}"})

        request.session[session_key] = chat_history
        return redirect("race_chat", pk=race.pk)

    def _extract_updates(self, text: str) -> dict:
        """Extract JSON update block from agent response."""
        match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(1))
                return data.get("updates", {})
            except (json.JSONDecodeError, AttributeError):
                pass
        return {}
