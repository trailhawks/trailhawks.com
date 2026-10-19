from django.apps import AppConfig


class RacesConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "races"

    def ready(self):
        from . import checks  # noqa: F401  (registers system checks)
