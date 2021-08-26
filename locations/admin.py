from django.contrib import admin
from django.db import models
from pagedown.widgets import AdminPagedownWidget

from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": AdminPagedownWidget},
    }
    prepopulated_fields = {"slug": ["name"]}
    list_display = ("name", "latitude", "longitude", "zoom")
