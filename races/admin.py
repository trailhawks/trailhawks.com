from dateutil.relativedelta import relativedelta
from django.contrib import admin
from django.template.defaultfilters import slugify
from num2words import num2words
from titlecase import titlecase

from .models import (
    Race,
    Racer,
    RaceType,
    Registration,
    Report,
    Result,
)
from faq.admin import FaqInline
from links.admin import LinksInline
from news.admin import NewsInline
from sponsors.admin import SponsorInline


def migrate_race(modeladmin, request, queryset):
    for race in queryset.all():
        race.pk = None
        race.number = race.number + 1
        race.annual = titlecase(
            "{} Annual".format(num2words(race.number, ordinal=True))
        )
        race.slug = "{}-{}".format(slugify(race.title), race.number)
        race.active = False
        race.start_datetime = race.start_datetime + relativedelta(years=1)
        race.save()


migrate_race.short_description = "Duplicate the race for the next year"


def set_location_to_clinton(modeladmin, request, queryset):
    queryset.update(location=2)


set_location_to_clinton.short_description = "Set location to Clinton Lake"


def set_location_to_river_trails(modeladmin, request, queryset):
    queryset.update(location=1)


set_location_to_river_trails.short_description = "Set location to the River Trails"


def set_location_to_olathe_pc(modeladmin, request, queryset):
    queryset.update(location=4)


set_location_to_olathe_pc.short_description = (
    "Set location to the Olathe Prairie Center"
)


class RaceDirectorInline(admin.StackedInline):
    model = Race.race_directors.through
    raw_id_fields = ("member",)
    extra = 0


class RegistrationInline(admin.TabularInline):
    model = Registration
    extra = 0


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ["description", "race", "reg_date", "end_date", "reg_cost"]
    raw_id_fields = ["race"]


class RaceAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title", "annual"]}
    list_display = ("title", "number", "annual", "active", "start_datetime")
    list_filter = ("active", "start_datetime", "number", "annual", "location")
    ordering = ["-start_datetime"]
    raw_id_fields = ["background"]
    save_on_top = True
    search_fields = ("title", "slogan", "description", "slogan")
    actions = [
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
    raw_id_fields = ("racer", "race")
    search_fields = ("time", "place")


class RacerAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "gender", "email", "trailhawk")
    list_filter = ("gender",)
    ordering = ["last_name", "first_name"]
    raw_id_fields = ["trailhawk"]
    search_fields = ("first_name", "last_name")


class ReportAdmin(admin.ModelAdmin):
    list_display = ["title", "racer"]
    raw_id_fields = ["race", "racer"]


class RaceTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]


admin.site.register(Race, RaceAdmin)
admin.site.register(RaceType, RaceTypeAdmin)
admin.site.register(Racer, RacerAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Registration, RegistrationAdmin)
