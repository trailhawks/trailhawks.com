from django.urls import path

from .views import (
    member_list,
    MemberDetailView,
    MemberEmailPreview,
    MemberListView,
    MemberResultCsvDetail,
)

urlpatterns = [
    path("", MemberListView.as_view(), name="member_list"),
    path("preview/", MemberEmailPreview.as_view(), name="member_email_preview"),
    path("<int:pk>/", MemberDetailView.as_view(), name="member_detail"),
    path("member_list/", member_list, name="admin_member_list"),
    path(
        "csv/",
        MemberResultCsvDetail.as_view(),
        name="admin_member_csv_list",
    ),
]
