from django.contrib import admin

from faq.admin import FaqInline
from news.admin import NewsInline

from .models import Run


@admin.register(Run)
class RunAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
    list_display = ["name", "day_of_week", "active", "run_time"]
    list_filter = ["day_of_week", "run_time", "location"]
    raw_id_fields = ["contact"]
    inlines = (
        NewsInline,
        FaqInline,
    )
