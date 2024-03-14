from ajaximage.fields import AjaxImageField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import SponsorManager


class Sponsor(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(
        blank=True,
        null=True,
        help_text="Suggested value automatically generated from name. Must be unique.",
    )
    url = models.URLField(help_text="URL to website")
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    logo = AjaxImageField(upload_to="sponsors", blank=True, null=True)
    discount_detail = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=False)
    homepage = models.BooleanField("Show on homepage?", default=False)

    content_type = models.ForeignKey("contenttypes.ContentType", on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    objects = SponsorManager()

    class Meta:
        verbose_name = _("Sponsor")
        verbose_name_plural = _("Sponsors")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("sponsor_detail", kwargs={"pk": self.pk})
