from django.urls import path

from . import views

urlpatterns = [
    path("", views.PhotoListView.as_view(), name="photo_list"),
    path("review/", views.PhotoReview.as_view(), name="photo_review_list"),
    path("groups/", views.PhotoSetListView.as_view(), name="photoset_list"),
    path("<slug:slug>/", views.PhotoDetailView.as_view(), name="photo_detail"),
    path(
        "groups/<str:flickr_id>/",
        views.PhotoSetDetailView.as_view(),
        name="photoset_detail",
    ),
]
