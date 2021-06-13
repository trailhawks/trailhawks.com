from config.settings import *

SITE_ID = 2

ROOT_URLCONF = "config.urls_hawkhundred"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            str(TEMPLATE_ROOT.joinpath("hawkhundred.com")),
            str(TEMPLATE_ROOT.joinpath("race_defaults")),
            str(TEMPLATE_ROOT.joinpath("defaults")),
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
