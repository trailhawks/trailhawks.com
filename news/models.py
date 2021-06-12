from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.urls import reverse

from .managers import NewsManager
from django.utils.translation import gettext_lazy as _


ALERT_CHOICES = (
    ("", _("Default no style.")),
    ("success", _("success")),
    ("info", _("info")),
    ("warning", _("warning")),
    ("danger", _("danger")),
)


class News(models.Model):
    """News model."""

    STATUS_DRAFT = 1
    STATUS_PUBLIC = 2
    STATUS_CHOICES = (
        (STATUS_DRAFT, _("Draft")),
        (STATUS_PUBLIC, _("Public")),
    )
    pub_date = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=250)
    slug = models.SlugField(blank=True, null=True)
    body = models.TextField()
    status = models.IntegerField(
        _("status"), choices=STATUS_CHOICES, default=STATUS_PUBLIC
    )
    alert_status = models.CharField(
        max_length=50, choices=ALERT_CHOICES, default="", blank=True
    )

    # show in main news feed? handy for race results...
    content_type = models.ForeignKey(
        "contenttypes.ContentType", on_delete=models.CASCADE, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    objects = NewsManager()

    class Meta:
        get_latest_by = "pub_date"
        ordering = ("-pub_date",)
        unique_together = (("slug", "pub_date"),)
        verbose_name = _("news")
        verbose_name_plural = _("news")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        now = timezone.now()

        if not self.pub_date and self.status == self.STATUS_PUBLIC:
            self.pub_date = now

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("news_detail", kwargs={"pk": self.pk})

    def get_previous_news(self):
        return self.get_previous_by_publish(status__gte=self.STATUS_PUBLIC)

    def get_next_news(self):
        return self.get_next_by_publish(status__gte=self.STATUS_PUBLIC)
