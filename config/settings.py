import os

import environs

env = environs.Env()

BASE_DIR = environs.Path(__file__).parent.parent

TEMPLATE_ROOT = BASE_DIR.joinpath("templates", "bootstrap4")

DEBUG = env.bool("DJANGO_DEBUG", default=False)

ADMINS = ()

MANAGERS = ADMINS

TIME_ZONE = "America/Chicago"

LANGUAGE_CODE = "en-us"

SITE_ID = 1

USE_I18N = True
USE_L10N = True

USE_ETAGS = True

TIME_ZONE = "America/Chicago"
LANGUAGE_CODE = "en-us"

DATABASES = {
    "default": env.dj_db_url("DATABASE_URL", default="postgres://postgres@db/postgres")
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

MEDIA_ROOT = str(BASE_DIR.joinpath("media_root"))
MEDIA_URL = "/media/"

STATIC_ROOT = str(BASE_DIR.joinpath("static_root"))
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(BASE_DIR.joinpath("assets"))]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get("SECRET_KEY")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(TEMPLATE_ROOT.joinpath("defaults"))],
        "APP_DIRS": True,
        "OPTIONS": {
            "builtins": [
                "heroicons.templatetags.heroicons",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

ROOT_URLCONF = "config.urls"

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.flatpages",
    "django.contrib.humanize",
    "django.contrib.messages",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "django.contrib.staticfiles",
]

INSTALLED_APPS += [
    # "storages",
    "ajaximage",
    "django_q",
    # "django_tailwind_cli",
    "django_thumbor",
    "favicon",
    "heroicons",
    "markdownify.apps.MarkdownifyConfig",
    "micawber.contrib.mcdjango",
    "rest_framework",
    "robots",
    "simple_open_graph",
    "syncr.flickr",
    "syncr.twitter",
    "taggit",
]

INSTALLED_APPS += [
    "blog",
    "core",
    "events",
    "faq",
    "links",
    "locations",
    "members",
    "news",
    "photos",
    "races",
    "runs",
    "sponsors",
]

# Logging

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": True,
#     "formatters": {
#         "verbose": {
#             "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
#         },
#         "simple": {"format": "%(levelname)s %(message)s"},
#     },
#     "handlers": {
#         "null": {"level": "DEBUG", "class": "logging.NullHandler"},
#         "console": {
#             "level": "DEBUG",
#             "class": "logging.StreamHandler",
#             "formatter": "verbose",
#         },
#         "mail_admins": {
#             "level": "ERROR",
#             "class": "django.utils.log.AdminEmailHandler",
#             # 'filters': ['special']
#         },
#     },
#     "loggers": {
#         "django": {"handlers": ["null"], "propagate": True, "level": "INFO"},
#         "django.request": {
#             "handlers": ["mail_admins"],
#             "level": "ERROR",
#             "propagate": False,
#         },
#         "trailhawks": {
#             "handlers": ["console"],
#             "level": "DEBUG",
#             # 'filters': ['special']
#         },
#     },
# }

TEST_RUNNER = "django.test.runner.DiscoverRunner"

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=list())

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=list())

MACHINE_TAG_NAMESPACE = "trailhawks"

# Removing deprecation nagging...
DJANGO_MARKUP_IGNORE_WARNINGS = True

# Favicon path
FAVICON_PATH = STATIC_URL + "ico/favicon.png"

REST_FRAMEWORK = {
    # "DEFAULT_FILTER_BACKENDS": ("rest_framework.filters.DjangoFilterBackend",),
    "PAGINATE_BY_PARAM": "limit",
    # 'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    "PAGINATE_BY": 10,
}

TWITTER = {
    "username": env("TWITTER_USERNAME", default=""),
    "password": env("TWITTER_PASSWORD", default=""),
}

FLICKR = {
    "key": env("FLICKR_KEY", default=""),
    "secret": env("FLICKR_SECRET", default=""),
    "username": env("FLICKR_USERNAME", default=""),
}

DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="")
EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_PORT = env("EMAIL_PORT", default="")
EMAIL_USE_TLS = env("EMAIL_USE_TLS", default="")
# PAGEDOWN_IMAGE_UPLOAD_ENABLED = env.bool("PAGEDOWN_IMAGE_UPLOAD_ENABLED", default=True)
# PAGEDOWN_IMAGE_UPLOAD_UNIQUE = env.bool("PAGEDOWN_IMAGE_UPLOAD_UNIQUE", default=True)
RUNSIGNUP_KEY = env("RUNSIGNUP_KEY", default="")
RUNSIGNUP_SECRET = env("RUNSIGNUP_SECRET", default="")
RUNSIGNUP_URL = env("RUNSIGNUP_URL", default="")
SERVER_EMAIL = env("SERVER_EMAIL", default="")
THUMBOR_SECURITY_KEY = env("THUMBOR_SECURITY_KEY", default="")
THUMBOR_SERVER = env("THUMBOR_SERVER", default="")

# Django-Q settings

Q_CLUSTER = {
    "bulk": 10,
    "name": "DjangORM",
    "orm": "default",
    "queue_limit": 50,
    "retry": 120,
    "timeout": 90,
    "workers": 4,
}


MARKDOWNIFY = {
    "default": {
        "WHITELIST_TAGS": [
            "a",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "img",
            "p",
            "strong",
        ],
    },
}
