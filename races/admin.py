from dateutil.relativedelta import relativedelta
from django.contrib import admin
from django.utils.text import slugify
from django.urls import reverse
from django.utils.html import format_html
from num2words import num2words
from titlecase import titlecase

from faq.admin import FaqInline
from links.admin import LinksInline
from news.admin import NewsInline
from sponsors.admin import SponsorInline

from .models import Race, Racer, RaceType, Registration, Report, Result, Series


@admin.action(description="Fix slug fields")
def fix_slug_fields(modeladmin, request, queryset):
    for race in queryset.all():
        race.slug = slugify(f"{race.slug}")
        race.save(update_fields=["slug"])


@admin.action(description="Duplicate the race for the next year")
def migrate_race(modeladmin, request, queryset):
    for race in queryset.all():
        # track existing events since m2ms aren't automatically copied...
        events = race.events.all()

        race.pk = None
        if race.number:
            race.number = race.number + 1
        else:
            race.number = 1

        race.annual = titlecase(f"{num2words(race.number, ordinal=True)} Annual")
        race.slug = slugify("{} {}".format(race.title, race.annual or ""))
        race.active = False
        race.start_datetime = race.start_datetime + relativedelta(years=1)
        race.save()

        # update m2ms...
        for event in events:
            race.events.add(event.pk)


@admin.action(description="Set location to Clinton Lake")
def set_location_to_clinton(modeladmin, request, queryset):
    queryset.update(location=2)


@admin.action(description="Set location to the River Trails")
def set_location_to_river_trails(modeladmin, request, queryset):
    queryset.update(location=1)


@admin.action(description="Set location to the Olathe Prairie Center")
def set_location_to_olathe_pc(modeladmin, request, queryset):
    queryset.update(location=4)


class RaceDirectorInline(admin.StackedInline):
    model = Race.race_directors.through
    raw_id_fields = ("member",)
    extra = 0


class RegistrationInline(admin.TabularInline):
    model = Registration
    extra = 0


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title", "annual"]}
    list_display = [
        "title",
        "number",
        "annual",
        "active",
        "start_datetime",
        "ultrasignup_id",
        "reg_url",
        "download_csv_results",
    ]
    list_editable = ["ultrasignup_id"]
    list_filter = ["active", "start_datetime", "number", "annual", "location"]
    ordering = ["-start_datetime"]
    raw_id_fields = ["background"]
    save_on_top = True
    search_fields = ["title", "slogan", "description", "slogan"]
    actions = [
        fix_slug_fields,
        migrate_race,
        set_location_to_clinton,
        set_location_to_river_trails,
        set_location_to_olathe_pc,
    ]
    inlines = (
        RaceDirectorInline,
        RegistrationInline,
        NewsInline,
        FaqInline,
        SponsorInline,
        LinksInline,
    )
    exclude = (
        "race_directors",
        "sponsors",
    )

    @admin.display(description="Race Results")
    def download_csv_results(self, obj):
        if obj.result_set.exists():
            url = reverse(
                "race_result_csv_detail",
                kwargs={
                    "year": obj.start_datetime.strftime("%Y"),
                    "month": obj.start_datetime.strftime("%b").lower(),
                    "day": obj.start_datetime.strftime("%d"),
                    "slug": obj.slug,
                },
            )
            return format_html(f'<a href="{url}">Download CSV</a>')
        return None


@admin.register(RaceType)
class RaceTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]


@admin.register(Racer)
class RacerAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "gender", "email", "trailhawk")
    list_filter = ("gender",)
    ordering = ["last_name", "first_name"]
    raw_id_fields = ["trailhawk"]
    search_fields = ("first_name", "last_name")


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ["description", "race", "reg_date", "end_date", "reg_cost"]
    raw_id_fields = ["race"]


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["title", "racer"]
    raw_id_fields = ["race", "racer"]


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        "race",
        "race_type",
        "racer",
        "time",
        "place",
        "course_record",
        "dns",
        "dnf",
        "dq",
    )
    list_filter = ("race_type", "course_record", "dns", "dnf", "dq", "race")
    ordering = [
        "race",
        "time",
        "race_type",
    ]
    raw_id_fields = ("racer", "race")
    search_fields = ("time", "place")


@admin.register(Series)
class SeriesTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "download_csv_results"]
    filter_horizontal = ("races",)

    @admin.display(description="Race Results")
    def download_csv_results(self, obj):
        if obj.races.exists():
            url = reverse(
                "series_results_index",
                kwargs={"slug": obj.slug},
            )
            return format_html(
                f'<a href="{url}">Download {obj.races.count()} Races (CSV)</a>'
            )
        return None
