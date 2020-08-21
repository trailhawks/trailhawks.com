from . import views
from django.urls import path, re_path


urlpatterns = [
    path("", views.PhotoListView.as_view(), name="photo_list"),
    path("review/", views.PhotoReview.as_view(), name="photo_review_list"),
    path("groups/", views.PhotoSetListView.as_view(), name="photoset_list"),
    re_path(
        r"^(?P<slug>[-_\w]+)/$", views.PhotoDetailView.as_view(), name="photo_detail"
    ),
    re_path(
        r"^groups/(?P<flickr_id>[-_\w]+)/$",
        views.PhotoSetDetailView.as_view(),
        name="photoset_detail",
    ),
]
