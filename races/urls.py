from . import views
from .feeds import RaceFeed
from django.urls import path, re_path


urlpatterns = [
    path("", views.RaceIndex.as_view(), name="race_index"),
    re_path(
        r"^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$",
        views.RaceDateDetail.as_view(),
        name="race_detail",
    ),
    re_path(
        r"^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/results/$",
        views.RaceResultDetail.as_view(),
        name="race_result_detail",
    ),
    path("ical/", RaceFeed(), name="race_ical"),
    re_path(
        r"^racers/(?P<pk>[-\w]+)/$", views.RacerDetail.as_view(), name="racer_detail"
    ),
]
