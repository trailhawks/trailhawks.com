from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.db import models
from pagedown.widgets import AdminPagedownWidget

from .models import News


class NewsInline(GenericStackedInline):
    formfield_overrides = {
        models.TextField: {"widget": AdminPagedownWidget},
    }
    model = News
    extra = 0


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": AdminPagedownWidget},
    }
    prepopulated_fields = {"slug": ["title"]}
    list_display = ["title", "pub_date", "status", "content_type", "object_id"]
    list_filter = ["pub_date", "status"]
    fieldsets = (
        (
            None,
            {"fields": ("pub_date", "title", "slug", "body", "status", "alert_status")},
        ),
        (
            "Advanced options",
            {"classes": ("collapse",), "fields": ("content_type", "object_id")},
        ),
    )
