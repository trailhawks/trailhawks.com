from .views import SponsorDetailView, SponsorListView
from django.urls import path


urlpatterns = [
    path("", SponsorListView.as_view(), name="sponsor_list"),
    path("<int:pk>/", SponsorDetailView.as_view(), name="sponsor_detail"),
]
