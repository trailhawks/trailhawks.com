from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.db import models
from pagedown.widgets import AdminPagedownWidget

from .models import FAQ


class FaqInline(GenericStackedInline):
    model = FAQ
    extra = 0


@admin.register(FAQ)
class FaqAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": AdminPagedownWidget},
    }
    list_display = ("question", "content_type", "get_object_name")
    fieldsets = (
        (None, {"fields": ("question", "answer")}),
        (
            "Advanced options",
            {"classes": ("collapse",), "fields": ("content_type", "object_id")},
        ),
    )

    @admin.display(description="associated object")
    def get_object_name(self, obj):
        if obj.content_object and len(str(obj.content_object)):
            return obj.content_object
