from __future__ import annotations

from django.http import HttpResponse
from django.views.generic.base import View

from config import __version__


class VersionView(View):
    def get(self, request):
        return HttpResponse(__version__, content_type="text/plain")
