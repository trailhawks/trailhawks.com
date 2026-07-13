from django.conf import settings
from django.contrib import admin
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.views.static import serve

from health_check.views import HealthCheckView

from sitemaps.races import StaticViewSitemap

sitemaps = {
    "flatpages": FlatPageSitemap,
    "static": StaticViewSitemap,
}

admin.autodiscover()

urlpatterns = [
    path("404/", TemplateView.as_view(template_name="404.html")),
    path("500/", TemplateView.as_view(template_name="500.html")),
    path(
        "faqs/",
        TemplateView.as_view(template_name="faqs.html"),
        name="race_faqs",
    ),
    path(
        "gallery/",
        TemplateView.as_view(template_name="gallery.html"),
        name="race_gallery",
    ),
    path(
        "maps/",
        TemplateView.as_view(template_name="maps.html"),
        name="maps",
    ),
    path(
        "results/",
        TemplateView.as_view(template_name="results.html"),
        name="race_results",
    ),
    # url(r'^signup/$', TemplateView.as_view(template_name='signup.html'), name='race_signup'),
    # url(r'^travel/$', TemplateView.as_view(template_name='travel.html'), name='race_travel'),
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
    path("robots.txt", include("robots.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("", include("favicon.urls")),
    path("admin/", admin.site.urls),
    path("health/", HealthCheckView.as_view(checks=["health_check.Database"])),
]
# Serve user-uploaded media directly through Django. WhiteNoise only handles STATIC_URL,
# so /media/ 404s in production without this. Uploads come from trusted admins.
urlpatterns += [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
urlpatterns += staticfiles_urlpatterns()
