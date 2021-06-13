from django.urls import path, re_path

from .views import EventDetailView, EventListView

urlpatterns = [
    path("", EventListView.as_view(), name="event_list"),
    re_path(r"^(?P<slug>[-\w]+)/$", EventDetailView.as_view(), name="event_detail"),
]
