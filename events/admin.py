from django.contrib import admin

from faq.admin import FaqInline
from links.admin import LinksInline
from news.admin import NewsInline
from sponsors.admin import SponsorInline

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    list_display = ("title", "status")
    list_filter = ("status",)
    filter_horizontal = ("races",)
    save_on_top = True
    inlines = (
        FaqInline,
        NewsInline,
        LinksInline,
        SponsorInline,
    )
