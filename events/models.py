from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import MachineTagMixin

from .managers import EventManager


class Event(MachineTagMixin):
    """Event model."""

    STATUS_DRAFT = 1
    STATUS_PUBLIC = 2
    STATUS_CHOICES = (
        (STATUS_DRAFT, _("Draft")),
        (STATUS_PUBLIC, _("Public")),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(blank=True, null=True)
    body = models.TextField(blank=True)
    status = models.IntegerField(_("status"), choices=STATUS_CHOICES, default=STATUS_PUBLIC)
    facebook_url = models.URLField(blank=True, null=True, help_text="Link to Facebook page")
    facebook_event_url = models.URLField(blank=True, null=True, help_text="Link to Facebook Event page")
    races = models.ManyToManyField("races.Race", related_name="events")

    objects = EventManager()

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        now = timezone.now()

        if self.status == self.STATUS_PUBLIC:
            self.pub_date = now

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("event_detail", kwargs={"slug": self.slug})
