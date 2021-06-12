from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from six import python_2_unicode_compatible


class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()

    content_type = models.ForeignKey(
        "contenttypes.ContentType", on_delete=models.CASCADE, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ("-content_type",)
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")

    def __str__(self):
        return self.question

    def get_absolute_url(self):
        return reverse("faq_detail", kwargs={"pk": self.pk})
