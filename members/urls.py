from django.urls import path

from .views import MemberDetailView, MemberEmailPreview, MemberListView, member_list

urlpatterns = [
    path("", MemberListView.as_view(), name="member_list"),
    path("preview/", MemberEmailPreview.as_view(), name="member_email_preview"),
    path("<int:pk>/", MemberDetailView.as_view(), name="member_detail"),
    path("member_list/", member_list, name="admin_member_list"),
]
