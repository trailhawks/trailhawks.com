from django.urls import path

from . import views

urlpatterns = [
    path("", views.PostArchive.as_view(), name="blog_list"),
    path(
        "<int:year>/<str:month>/<int:day>/<slug:slug>/",
        views.PostDateDetail.as_view(),
        name="blog_detail",
    ),
]
