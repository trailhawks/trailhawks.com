from django.contrib import admin

from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
    list_display = ("name", "latitude", "longitude", "zoom")
