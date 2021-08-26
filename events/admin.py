from django.contrib import admin
from django.db import models
from pagedown.widgets import AdminPagedownWidget

from faq.admin import FaqInline
from links.admin import LinksInline
from news.admin import NewsInline
from sponsors.admin import SponsorInline

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": AdminPagedownWidget},
    }
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
