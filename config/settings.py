import os

from environs import Env
from unipath import FSPath as Path


env = Env()

PROJECT_ROOT = Path(__file__).ancestor(2)
TEMPLATE_ROOT = os.path.join(PROJECT_ROOT, 'templates')

DEBUG = env.bool("DJANGO_DEBUG", default=False)
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True
USE_L10N = True

USE_ETAGS = True

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'

DATABASES = {
    "default": env.dj_db_url("DATABASE_URL", default="postgres://postgres@db/postgres")
}

MEDIA_ROOT = PROJECT_ROOT.child('media_root')
MEDIA_URL = '/media/'

STATIC_ROOT = PROJECT_ROOT.child('static_root')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    PROJECT_ROOT.child('assets')
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Template stuff
TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get("SECRET_KEY")

# Template stuff
TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
]

TEMPLATE_DIRS = [
    os.path.join(TEMPLATE_ROOT, 'defaults'),
]

ROOT_URLCONF = 'config.urls'

# Middleware
MIDDLEWARE_CLASSES = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'waffle.middleware.WaffleMiddleware',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.staticfiles',
]

INSTALLED_APPS += [
    'django_comments',
    'markup_deprecated',
    'ajaximage',
    'backupdb',
    'django_extensions',
    'django_gravatar',
    'django_thumbor',
    'djrill',
    'favicon',
    # 'import_export',
    'micawber.contrib.mcdjango',
    'rest_framework',
    'robots',
    'shorturls',
    'simple_open_graph',
    # 'storage_migration',
    'storages',
    'syncr.flickr',
    'syncr.twitter',
    'taggit',
    'waffle',
]

INSTALLED_APPS += [
    'blog',
    'core',
    'events',
    'faq',
    'links',
    'locations',
    'members',
    'news',
    'photos',
    'races',
    'runs',
    'sponsors',
]

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            # 'filters': ['special']
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'trailhawks': {
            'handlers': ['console'],
            'level': 'DEBUG',
            # 'filters': ['special']
        }
    }
}

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

SHORT_BASE_URL = 'https://lth.im/'

SHORTEN_MODELS = {
    'B': 'blog.post',
    'E': 'events.event',
    'F': 'faq.faq',
    'L': 'links.links',
    'M': 'members.member',
    'N': 'news.news',
    'R': 'races.race',
    'U': 'runs.run',
}

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=list())

MACHINE_TAG_NAMESPACE = 'trailhawks'

# Removing deprecation nagging...
DJANGO_MARKUP_IGNORE_WARNINGS = True

# Favicon path
FAVICON_PATH = STATIC_URL + 'ico/favicon.png'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'PAGINATE_BY_PARAM': 'limit',
    # 'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGINATE_BY': 10
}

TWITTER = {
    'username': env("TWITTER_USERNAME", default=""),
    'password': env("TWITTER_PASSWORD", default=""),
}

FLICKR = {
    'key': env("FLICKR_KEY", default=""),
    'secret': env("FLICKR_SECRET", default=""),
    'username': env("FLICKR_USERNAME", default=""),
}

AKISMET_API_KEY = env("AKISMET_API_KEY", default="")
DBBACKUP_POSTGRESQL_BACKUP_COMMANDS = env("DBBACKUP_POSTGRESQL_BACKUP_COMMANDS", default="")
DBBACKUP_S3_ACCESS_KEY = env("DBBACKUP_S3_ACCESS_KEY", default="")
DBBACKUP_S3_BUCKET = env("DBBACKUP_S3_BUCKET", default="")
DBBACKUP_S3_SECRET_KEY = env("DBBACKUP_S3_SECRET_KEY", default="")
DBBACKUP_STORAGE = env("DBBACKUP_STORAGE", default="")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="")
DJRILL_WEBHOOK_SECRET = env("DJRILL_WEBHOOK_SECRET", default="")
EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_PORT = env("EMAIL_PORT", default="")
EMAIL_USE_TLS = env("EMAIL_USE_TLS", default="")
MAILHIDE_PRIVATE_KEY = env("MAILHIDE_PRIVATE_KEY", default="")
MAILHIDE_PUBLIC_KEY = env("MAILHIDE_PUBLIC_KEY", default="")
SERVER_EMAIL = env("SERVER_EMAIL", default="")
THUMBOR_SECURITY_KEY = env("THUMBOR_SECURITY_KEY", default="")
THUMBOR_SERVER = env("THUMBOR_SERVER", default="")
