from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.db import models
from pagedown.widgets import AdminPagedownWidget

from .models import Links


class LinksInline(GenericStackedInline):
    model = Links
    extra = 0


@admin.register(Links)
class LinksAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": AdminPagedownWidget},
    }
    list_display = ("name", "content_type", "object_id")
    fieldsets = (
        (None, {"fields": ("name", "link", "description")}),
        (
            "Advanced options",
            {"classes": ("collapse",), "fields": ("content_type", "object_id")},
        ),
    )
