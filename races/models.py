from ajaximage.fields import AjaxImageField
from django.db import models
from django.template.defaultfilters import title
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from num2words import num2words

from core.models import MachineTagMixin

from .managers import RaceManager


class Race(MachineTagMixin):
    """Race model."""

    KM = 1
    MI = 2
    UNIT_CHOICES = (
        (KM, _("Kilometers")),
        (MI, _("Miles")),
    )
    RUN = 1
    BIKE = 2
    SWIM = 3
    DISCIPLINE_CHOICES = (
        (RUN, _("Run")),
        (BIKE, _("Bike")),
        (SWIM, _("Swim")),
    )
    title = models.CharField(
        max_length=200,
        help_text='Title of event. If there are multiple races assoiated to an "event", make two events.',
    )
    active = models.BooleanField(default=True)
    number = models.IntegerField(blank=True, null=True)
    annual = models.CharField(max_length=32, blank=True, null=True)
    slug = models.SlugField(
        unique=True,
        blank=True,
        help_text="Suggested value automatically generated from title and annual. Must be unique.",
    )

    slogan = models.CharField(max_length=300, blank=True, null=True)

    logo = AjaxImageField(
        upload_to="races/logos",
        blank=True,
        null=True,
        help_text="The logo image is on the top of the race page.",
    )

    # background = AjaxImageField(upload_to='races/backgrounds', blank=True, null=True,
    #                             help_text='Optional background photo')
    background = models.ForeignKey(
        "flickr.Photo",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="The background image is used on the homepage. If a background image is not provided, the logo image will be used.",
    )

    race_type = models.IntegerField(choices=DISCIPLINE_CHOICES, default=RUN, blank=True, null=True)
    sponsors = models.ManyToManyField("sponsors.Sponsor", related_name="sponsors")
    race_directors = models.ManyToManyField("members.Member")
    awards = models.TextField(blank=True, null=True)
    distance = models.CharField(max_length=100, blank=True, null=True, help_text="eg 26.2")
    unit = models.IntegerField(choices=UNIT_CHOICES, default=KM, blank=True, null=True)
    start_datetime = models.DateTimeField(verbose_name="Start Date and Time")
    description = models.TextField(blank=True)
    location = models.ForeignKey("locations.Location", on_delete=models.CASCADE, blank=True, null=True)
    course_map = models.URLField(blank=True, null=True, help_text="Link to course map if avail.")
    cut_off = models.CharField(max_length=75, null=True, blank=True, help_text="eg: 13 hours")
    reg_url = models.URLField(
        blank=True,
        null=True,
        help_text="Link to registartion flyer or to registration URL for online signup.",
    )
    reg_description = models.TextField(blank=True, null=True)
    ultrasignup_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="This should be the ID of your UltraSignup.com ?did=",
    )
    entry_form = models.FileField(upload_to="races/entry_forms", null=True, blank=True)
    discounts = models.TextField(
        blank=True,
        null=True,
        help_text="Describe discounts for the race if they exist.",
    )
    lodging = models.URLField(blank=True, null=True, help_text="Link to lodging information")
    packet_pickup = models.TextField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True, help_text="Link to Facebook page")
    facebook_event_url = models.URLField(blank=True, null=True, help_text="Link to Facebook Event page")

    objects = RaceManager()

    class Meta:
        ordering = ["-start_datetime"]
        verbose_name = _("Race")
        verbose_name_plural = _("Races")

    def save(self, *args, **kwargs):
        if not self.slug:
            year = self.start_datetime.strftime("%Y")
            if self.title.endswith(year):
                self.slug = slugify(self.title)
            else:
                self.slug = slugify(f"{self.title} {year}")
        else:
            self.slug = slugify(self.slug)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name()

    def get_absolute_url(self):
        return reverse(
            "race_detail",
            kwargs={
                "year": self.start_datetime.strftime("%Y"),
                "month": self.start_datetime.strftime("%b").lower(),
                "day": self.start_datetime.strftime("%d"),
                "slug": self.slug,
            },
        )

    def get_full_name(self):
        name = f"{self.title}"
        if self.number:
            number = num2words(self.number, ordinal=True)
            if self.number == 1:
                name = f"Inaugural {self.title}"
            else:
                name = f"{number} Annual {self.title}"
        elif self.annual:
            name = f"{self.annual} {self.title}"
        return title(name)

    @cached_property
    def ical_uid(self):
        return f"race-{self.pk}@trailhawks.com"

    @cached_property
    def get_overall_results(self):
        return self.result_set.all().order_by("race_type", "time")

    @cached_property
    def get_race_reports(self):
        return self.report_set.all()

    @cached_property
    def is_finished(self):
        return not self.result_set.count() == 0


class Racer(MachineTagMixin):
    """Racer model."""

    MALE = 1
    FEMALE = 2
    GENDER_CHOICES = (
        (MALE, "Man"),
        (FEMALE, "Woman"),
    )

    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    trailhawk = models.OneToOneField(
        "members.Member",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="If racer is a trailhawk select profile.",
    )
    email = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=13, blank=True, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES)
    birth_date = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=40, null=True, blank=True)
    state = models.CharField(max_length=40, null=True, blank=True)
    country = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = _("Racer")
        verbose_name_plural = _("Racers")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("racer_detail", kwargs={"pk": self.pk})

    def get_machine_tags(self):
        machine_tags = super().get_machine_tags()
        try:
            if self.trailhawk:
                machine_tags += self.trailhawk.get_machine_tags()
        except IndexError:
            pass
        return machine_tags

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def get_results(self):
        return Result.objects.filter(racer=self)

    @property
    def age(self):
        TODAY = timezone.today()
        return TODAY.year - self.birth_date.year

    @property
    def get_gender(self):
        for num, gender in self.GENDER_CHOICES:
            if num == self.gender:
                return gender


class RaceType(models.Model):
    """Race Type model."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Report(models.Model):
    """Report model."""

    report = models.URLField(help_text="Link to race report")
    title = models.CharField(max_length=200)
    race = models.ForeignKey("races.Race", on_delete=models.CASCADE)
    racer = models.ForeignKey("races.Racer", on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")

    def __str__(self):
        return self.title


class Registration(models.Model):
    """Registration model."""

    race = models.ForeignKey("races.Race", on_delete=models.CASCADE)
    description = models.CharField(max_length=100, blank=True, null=True)
    reg_date = models.DateField("Registration Date")
    end_date = models.DateField("End Date", blank=True, null=True)
    reg_cost = models.IntegerField("Registration Cost")

    class Meta:
        verbose_name = _("Registration Dates")
        verbose_name_plural = _("Registration Dates")

    def __str__(self):
        return f"{self.race.title} {self.reg_date}"

    @property
    def has_expired(self):
        if self.end_date:
            return timezone.now() < self.end_date
        return False


class Result(models.Model):
    """Result model."""

    racer = models.ForeignKey("races.Racer", on_delete=models.CASCADE)
    race = models.ForeignKey("races.Race", on_delete=models.CASCADE)
    race_type = models.ForeignKey(
        "races.RaceType",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="For races with multiple race types.",
    )
    bib_number = models.IntegerField(blank=True, null=True)
    time = models.CharField(max_length=20, null=True, blank=True)
    place = models.TextField(
        null=True,
        blank=True,
        help_text="Ex. First Overall Man or First Masters Woman",
    )
    course_record = models.BooleanField(default=False)
    dq = models.BooleanField("Disqualified", default=False)
    dns = models.BooleanField("Did not Start", default=False)
    dnf = models.BooleanField("Did not Finish", default=False)
    import_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ("time",)
        verbose_name = _("Result")
        verbose_name_plural = _("Results")

    def __str__(self):
        return f"{self.racer} - {self.race.title} - {self.time}"

    def save(self, *args, **kwargs):
        if self.time:
            if "cr" in self.time.lower():
                self.course_record = True

            if "dnf" in self.time.lower():
                self.dnf = True

            if "dns" in self.time.lower():
                self.dns = True

        return super().save(*args, **kwargs)


class Series(models.Model):
    """Series model."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    races = models.ManyToManyField("races.Race", related_name="series")

    class Meta:
        verbose_name = _("Series")
        verbose_name_plural = _("Series")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
