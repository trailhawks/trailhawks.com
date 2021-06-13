from django.urls import path, re_path

from .views import RunDetail, RunList

urlpatterns = [
    path("", RunList.as_view(), name="run_list"),
    re_path(r"^(?P<slug>[-\w]+)/$", RunDetail.as_view(), name="run_detail"),
]
