from .views import NewsDetail, NewsList
from django.urls import path


urlpatterns = [
    path("", NewsList.as_view(), name="news_list"),
    path("<int:pk>/", NewsDetail.as_view(), name="news_detail"),
]
