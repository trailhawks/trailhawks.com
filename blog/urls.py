
from . import views
from django.urls import path, re_path


urlpatterns = [
    path('', views.PostArchive.as_view(), name="blog_list"),
    re_path(r"^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$",
        views.PostDateDetail.as_view(),
        name="blog_detail",
    ),
]
