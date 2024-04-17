from django.contrib import admin

from faq.admin import FaqInline
from news.admin import NewsInline

from .models import Run


@admin.register(Run)
class RunAdmin(admin.ModelAdmin):
    filter_horizontal = ["leaders"]
    inlines = [NewsInline, FaqInline]
    list_display = ["name", "day_of_week", "run_time", "active", "location"]
    list_filter = ["day_of_week", "run_time", "location"]
    ordering = ["day_of_week"]
    prepopulated_fields = {"slug": ["name"]}
    raw_id_fields = ["contact"]
