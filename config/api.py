from datetime import date, datetime

from ninja import NinjaAPI, Schema

from blog.models import Post
from events.models import Event
from members.models import Member
from news.models import News
from races.models import Race, Racer
from runs.models import Run
from sponsors.models import Sponsor

api = NinjaAPI(title="Trail Hawks API", version="2.0", urls_namespace="api")


# Schemas


class RaceSchema(Schema):
    id: int
    title: str
    slug: str
    description: str | None = None
    distance: str | None = None
    start_datetime: datetime | None = None
    annual: str | None = None
    number: int | None = None
    slogan: str | None = None
    race_type: int | None = None
    unit: int | None = None
    active: bool = True
    awards: str | None = None
    cut_off: str | None = None
    course_map: str | None = None
    reg_url: str | None = None
    reg_description: str | None = None
    ultrasignup_id: str | None = None
    discounts: str | None = None
    lodging: str | None = None
    packet_pickup: str | None = None
    facebook_url: str | None = None
    facebook_event_url: str | None = None


class RunSchema(Schema):
    id: int
    name: str
    slug: str
    day_of_week: int | None = None
    location: str | None = None
    run_time: str | None = None
    details: str | None = None
    active: bool

    @staticmethod
    def resolve_location(obj):
        return str(obj.location) if obj.location else None


class MemberSchema(Schema):
    id: int
    first_name: str
    last_name: str
    hawk_name: str | None = None
    gender: str | None = None
    member_since: date | None = None


class RacerSchema(Schema):
    id: int
    first_name: str
    last_name: str
    gender: str | None = None
    city: str | None = None
    state: str | None = None


class NewsSchema(Schema):
    id: int
    title: str
    body: str
    pub_date: datetime | None = None


class PostSchema(Schema):
    id: int
    title: str
    slug: str
    publish: datetime | None = None


class EventSchema(Schema):
    id: int
    title: str
    body: str


class SponsorSchema(Schema):
    id: int
    name: str
    url: str | None = None
    active: bool


# Endpoints


@api.get("/races/", response=list[RaceSchema])
def list_races(request):
    return Race.objects.all()


@api.get("/races/{race_id}/", response=RaceSchema)
def get_race(request, race_id: int):
    return Race.objects.get(pk=race_id)


@api.get("/runs/", response=list[RunSchema])
def list_runs(request):
    return Run.objects.all()


@api.get("/members/", response=list[MemberSchema])
def list_members(request):
    return Member.objects.current()


@api.get("/racers/", response=list[RacerSchema])
def list_racers(request):
    return Racer.objects.all()


@api.get("/news/", response=list[NewsSchema])
def list_news(request):
    return News.objects.public()


@api.get("/blog/", response=list[PostSchema])
def list_posts(request):
    return Post.objects.public()


@api.get("/events/", response=list[EventSchema])
def list_events(request):
    return Event.objects.public()


@api.get("/sponsors/", response=list[SponsorSchema])
def list_sponsors(request):
    return Sponsor.objects.filter(active=True)
