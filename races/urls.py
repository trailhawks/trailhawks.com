from django.urls import path

from races import feeds
from races import views

urlpatterns = [
    path("", views.RaceIndex.as_view(), name="race_index"),
    path(
        "<int:year>/<str:month>/<int:day>/<slug:slug>/",
        views.RaceDateDetail.as_view(),
        name="race_detail",
    ),
    path(
        "<int:year>/<str:month>/<int:day>/<slug:slug>/results/",
        views.RaceResultDetail.as_view(),
        name="race_result_detail",
    ),
    path(
        "<int:year>/<str:month>/<int:day>/<slug:slug>/results/csv/",
        views.RaceResultCsvDetail.as_view(),
        name="race_result_csv_detail",
    ),
    path("agent/", views.RaceAgentView.as_view(), name="race_agent"),
    path("agent/<int:pk>/", views.RaceAgentView.as_view(), name="race_agent_pk"),
    path("chat/<int:pk>/", views.RaceChatView.as_view(), name="race_chat"),
    path("ical/", feeds.RaceFeed(), name="race_ical"),
    path("racers/<int:pk>/", views.RacerDetail.as_view(), name="racer_detail"),
    path(
        "series/<slug:slug>/csv/",
        views.SeriesResultCsvDetail.as_view(),
        name="series_results_index",
    ),
]
