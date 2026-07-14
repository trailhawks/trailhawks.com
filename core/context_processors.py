from django.conf import settings


def google_maps(request):
    """Expose the Google Maps API key to templates that render a map."""
    return {"GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY}
