from django.contrib import admin
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from blog.models import Post
from config import __version__
from core.views import (
    AboutView,
    HomepageAView,
    HomepageBView,
    HomepageCView,
    HomepageView,
    HumansView,
    StyleGuideView,
    ThanksView,
)
from members.views import officer_list
from news.models import News
from photos.apis import PhotoViewSet, RandomPhotoViewSet
from races.models import Race
from sitemaps.default import StaticViewSitemap

blog_dict = {
    "queryset": Post.objects.public(),
    "date_field": "publish",
}

news_dict = {
    "queryset": News.objects.public(),
    "date_field": "pub_date",
}

race_dict = {
    "queryset": Race.objects.all(),
    "date_field": "start_datetime",
}

sitemaps = {
    "static": StaticViewSitemap,
    "flatpages": FlatPageSitemap,
    "news": GenericSitemap(news_dict, priority=0.6),
    "race": GenericSitemap(race_dict, priority=0.6),
    "blog": GenericSitemap(blog_dict, priority=0.6),
}

router = DefaultRouter()

router.register(r"photos", PhotoViewSet)
router.register(r"random_photos", RandomPhotoViewSet)

admin_header = f"Trail Hawks v{__version__}"
admin.site.enable_nav_sidebar = False
admin.site.site_header = admin_header
admin.site.site_title = admin_header


urlpatterns = [
    path("", HomepageView.as_view(), name="homepage"),
    path("demo/a/", HomepageAView.as_view(), name="homepage_demo_a"),
    path("demo/b/", HomepageBView.as_view(), name="homepage_demo_b"),
    path("demo/c/", HomepageCView.as_view(), name="homepage_demo_c"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", officer_list, name="contact"),
    path("contact/thanks/", ThanksView.as_view(), name="thanks"),
    path("styleguide/", StyleGuideView.as_view(), name="styleguide"),
    path("blog/", include("blog.urls")),
    path("events/", include("events.urls")),
    path("faq/", include("faq.urls")),
    path("links/", include("links.urls")),
    path("members/", include("members.urls")),
    path("news/", include("news.urls")),
    path("photos/", include("photos.urls")),
    path("races/", include("races.urls")),
    path("runs/", include("runs.urls")),
    path("sponsors/", include("sponsors.urls")),
    path("ajaximage/", include("ajaximage.urls")),
    path("api/v1/", include(router.urls)),
    path("humans.txt", HumansView.as_view()),
    path("robots.txt", include("robots.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("404/", TemplateView.as_view(template_name="404.html")),
    path("500/", TemplateView.as_view(template_name="500.html")),
    path("", include("favicon.urls")),
    path("admin/", admin.site.urls),
    path("health/", include("health_check.urls")),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
