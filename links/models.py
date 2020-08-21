from __future__ import unicode_literals

from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from six import python_2_unicode_compatible


@python_2_unicode_compatible
class Links(models.Model):
    name = models.CharField(max_length=250)
    link = models.URLField(help_text="URL to link")
    description = models.TextField()

    content_type = models.ForeignKey(
        "contenttypes.ContentType", on_delete=models.CASCADE, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ("name",)
        verbose_name = _("Link")
        verbose_name_plural = _("Links")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("link_detail", kwargs={"pk": self.pk})
