from django.contrib import admin
from django.contrib.contenttypes import generic

from .models import News


class NewsInline(generic.GenericStackedInline):
    model = News
    extra = 0


class NewsAdmin(admin.ModelAdmin):
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


admin.site.register(News, NewsAdmin)
