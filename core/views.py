from django.views.generic import TemplateView
from runs.models import Run


class AboutView(TemplateView):
    template_name = "about.html"
    navitem = "about"


class HomepageView(TemplateView):
    template_name = "homepage.html"
    navitem = "home"

    def get_context_data(self, **kwargs):
        runs = Run.objects.active().order_by("day_of_week")
        context = super().get_context_data(**kwargs)
        context["use_bootstrap"] = True if self.request.GET.get("bootstrap") else False
        context["runs"] = runs
        return context


class HumansView(TemplateView):
    content_type = "text/plain"
    template_name = "humans.txt"


class StyleGuideView(TemplateView):
    template_name = "styleguide.html"
    navitem = "styleguide"


class ThanksView(TemplateView):
    template_name = "thanks.html"
    navitem = "thanks"
