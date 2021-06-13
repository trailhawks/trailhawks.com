from django.urls import path

from .views import FaqDetailView, FaqListView

urlpatterns = [
    path("", FaqListView.as_view(), name="faq_list"),
    path("<int:pk>/", FaqDetailView.as_view(), name="faq_detail"),
]
