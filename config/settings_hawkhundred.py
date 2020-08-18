import os

from config.settings import *


SITE_ID = 2

ROOT_URLCONF = "config.urls_hawkhundred"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(TEMPLATE_ROOT, "hawkhundred.com"),
            os.path.join(TEMPLATE_ROOT, "race_defaults"),
            os.path.join(TEMPLATE_ROOT, "defaults"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]
