import csv
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from races.models import Race, Result
from runs.models import Run

from .forms import ContactForm
from .models import Member, Term


class MemberDetailView(DetailView):
    model = Member
    navitem = "members"


class MemberEmailPreview(TemplateView):
    template_name = "emails/renewal.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["first_name"] = "Trailhawks"
        context["expire_date"] = datetime.now()
        return context


class MemberListView(ListView):
    queryset = Member.objects.current()
    navitem = "members"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_officers"] = Term.objects.current().order_by("office__order")
        context["previous_officers"] = Term.objects.previous().order_by("office__order")
        context["run_leaders"] = Run.objects.active()
        context["race_leaders"] = Race.objects.all()
        return context


def officer_list(request):
    officer_ids = Term.objects.current().values_list("member__id", flat=True)
    officers = Member.objects.filter(id__in=officer_ids)

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "[Trailhawks]: %s" % form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["sender"]
            cc_myself = form.cleaned_data["cc_myself"]
            recipients = [officer.email for officer in officers if officer.email]
            if cc_myself:
                recipients.append(sender)

            if recipients:
                message_html = loader.render_to_string(
                    "emails/contact_message.html",
                    {"body": message, "sender": sender, "subject": subject},
                )
                message_text = loader.render_to_string(
                    "emails/contact_message.txt",
                    {"body": message, "sender": sender, "subject": subject},
                )

                try:
                    msg = EmailMultiAlternatives(subject, message_text, "no-reply@trailhawks.com", recipients)
                    msg.attach_alternative(message_html, "text/html")
                    msg.send()
                except Exception:
                    pass

            return HttpResponseRedirect(reverse("thanks"))
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})


class MemberExport(TemplateView):
    content_type = "text/csv"


@login_required
def member_list(request):
    if request.GET.get("plain"):
        response = HttpResponse(content_type="text/plain")
    else:
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=member_list.csv"

    current_site = Site.objects.get_current()

    members = Member.objects.all().order_by("-date_paid")
    member_list = csv.writer(response)
    member_list.writerow(
        [
            "id",
            "First Name",
            "Hawk Name",
            "Last Name",
            "Gender",
            "Club Officer Title",
            "Address",
            "Address2",
            "City",
            "State",
            "Zip",
            "Email Address",
            "Date paid",
            "Member Since",
            "Dues Due",
            "Website Admin Url",
        ]
    )

    for member in members:
        member_list.writerow(
            [
                member.id,
                member.first_name,
                f'"{member.hawk_name}"',
                member.last_name,
                member.gender,
                # member.get_gender_display(),
                # member.get_position(),
                "",
                member.address,
                member.address2,
                member.city,
                member.state,
                member.zip,
                member.email,
                member.date_paid,
                member.member_since,
                member.date_expires,
                "http://" + current_site.domain + reverse("admin:members_member_change", args=[member.pk]),
            ]
        )

    return response


class MemberResultCsvListView(ListView):
    queryset = Member.objects.all()

    def get(self, *args, **kwargs):
        members = self.get_queryset().all()

        if self.request.GET.get("plain"):
            response = HttpResponse(content_type="text/plain")
        else:
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = "attachment; filename=member_results.csv"

        results = (
            Result.objects.filter(racer__trailhawk__in=members)
            .select_related("race", "race_type", "racer", "racer__trailhawk")
            .order_by(
                "race__name",
                "race__start_datetime__year",
                "race_type__name",
                "dq",
                "dnf",
                "dns",
                "time",
            )
        )

        result_list = csv.writer(response)
        result_list.writerow(
            [
                "racer.trailhawkracer.trailhawk.date_paid",
                "racer.trailhawk.member_since",
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
                    result.racer.trailhawk,
                    result.racer.trailhawk.date_paid,
                    result.racer.trailhawk.member_since,
                    result.race.title,
                    result.race.start_datetime.year,
                    result.race_type.name,
                    result.bib_number,
                    result.racer.full_name,
                    result.racer.get_gender_display(),
                    time,
                    result.place,
                ]
            )

        return response
