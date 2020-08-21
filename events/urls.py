
from .views import EventDetailView, EventListView
from django.urls import path, re_path


urlpatterns = [
    path('', EventListView.as_view(), name="event_list"),
    re_path(r"^(?P<slug>[-\w]+)/$", EventDetailView.as_view(), name="event_detail"),
]
