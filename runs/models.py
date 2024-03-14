from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from core.models import MachineTagMixin

from .managers import RunManager


class Run(MachineTagMixin):
    """Run model."""

    DAY_OF_WEEK = (
        (0, _("Monday")),
        (1, _("Tuesday")),
        (2, _("Wednesday")),
        (3, _("Thursday")),
        (4, _("Friday")),
        (5, _("Saturday")),
        (6, _("Sunday")),
    )
    name = models.CharField(max_length=50)
    slug = models.SlugField(
        unique=True,
        help_text="Suggested value automatically generated from title. Must be unique.",
    )
    day_of_week = models.IntegerField(choices=DAY_OF_WEEK, default=0)
    run_time = models.CharField(max_length=25, help_text="Time of run (ex. 6:30 PM)")
    location = models.ForeignKey("locations.Location", on_delete=models.CASCADE, blank=True, null=True)
    details = models.TextField()
    contact = models.ForeignKey("members.Member", on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    objects = RunManager()

    class Meta:
        ordering = ["day_of_week"]
        verbose_name = _("Run")
        verbose_name_plural = _("Runs")

    def __str__(self):
        return f"{self.get_day_of_week_display()}: {self.name}"

    def get_absolute_url(self):
        return reverse("run_detail", kwargs={"slug": self.slug})
