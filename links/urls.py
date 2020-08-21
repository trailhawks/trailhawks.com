from .views import LinkDetailView, LinkListView
from django.urls import path


urlpatterns = [
    path("", LinkListView.as_view(), name="link_list"),
    path("<int:pk>/", LinkDetailView.as_view(), name="link_detail"),
]
