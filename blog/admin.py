from django.contrib import admin
from django.db import models
from pagedown.widgets import AdminPagedownWidget

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": AdminPagedownWidget},
    }
    ordering = ["-publish"]
    list_display = ("title", "status", "author", "publish")
    list_filter = ("status", "publish")
    prepopulated_fields = {"slug": ["title"]}
    raw_id_fields = ("author",)
    search_fields = ("title", "tease", "body")
