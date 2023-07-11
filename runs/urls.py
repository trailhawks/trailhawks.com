from django.urls import path

from .views import RunDetail, RunList

urlpatterns = [
    path("", RunList.as_view(), name="run_list"),
    path("<slug:slug>/", RunDetail.as_view(), name="run_detail"),
]
