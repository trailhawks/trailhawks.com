from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from .models import Sponsor


def set_homepage_to_true(modeladmin, request, queryset):
    queryset.update(homepage=True)


def set_homepage_to_false(modeladmin, request, queryset):
    queryset.update(homepage=False)


def set_active_to_true(modeladmin, request, queryset):
    queryset.update(active=True)


def set_active_to_false(modeladmin, request, queryset):
    queryset.update(active=False)


class SponsorInline(GenericStackedInline):
    model = Sponsor
    extra = 0


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    actions = [
        set_active_to_false,
        set_active_to_true,
        set_homepage_to_false,
        set_homepage_to_true,
    ]
    prepopulated_fields = {"slug": ["name"]}
    list_display = ("name", "active", "homepage", "content_type", "object_id")
    list_filter = (
        "active",
        "homepage",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "slug",
                    "active",
                    "homepage",
                    "url",
                    "address",
                    "phone",
                    "email",
                    "logo",
                    "discount_detail",
                )
            },
        ),
        (
            "Advanced options",
            {"classes": ("collapse",), "fields": ("content_type", "object_id")},
        ),
    )
