from django.views.generic import TemplateView
from blog.models import Post
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

        context["photos"] = [
            {"caption": "", "description": "", "large_url": "/img/races/CactusRoulette-2023-JK-5986-X5.jpg"},
            {"caption": "", "description": "", "large_url": "/img/races/CactusRoulette-2023-RM-2687-X5.jpg"},
            {"caption": "", "description": "", "large_url": "/img/races/Hawk-2023-KM-2349-X5.jpg"},
            {"caption": "", "description": "", "large_url": "/img/races/Hawk-2023-RM-7805-X5.jpg"},
            {"caption": "", "description": "", "large_url": "/img/races/NightHawk-2023-EM-2759-X5.jpg"},
            {"caption": "", "description": "", "large_url": "/img/races/NightHawk-KM-2021-6003-X5.jpg"},
            {"caption": "", "description": "", "large_url": "/img/races/PiDay-2022-KM-8015-X5.jpg"},
            {"caption": "", "description": "", "large_url": "/img/races/PiDay-2023-KM-8486-X5.jpg"},
            {"caption": "", "description": "", "large_url": "/img/races/SandersSaunter-2023-AR-0637-X5.jpg"},
            # {"caption": "", "description": "", "large_url": "/img/races/SandersSaunter-2023-AR-2491-X4.jpg"},
        ]
        context["use_bootstrap"] = True if self.request.GET.get("bootstrap") else False
        context["runs"] = runs
        context["latest_post"] = Post.objects.public().first()
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
