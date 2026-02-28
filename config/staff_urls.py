from django.urls import path

from config.staff_views import RaceCRUDView, RunCRUDView, StaffDashboardView

app_name = "staff"

urlpatterns = [
    path("", StaffDashboardView.as_view(), name="dashboard"),
    *RaceCRUDView.get_urls(),
    *RunCRUDView.get_urls(),
]
