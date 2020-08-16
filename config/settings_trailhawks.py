import os

from config.settings import *


SITE_ID = 1

ROOT_URLCONF = "config.urls"

TEMPLATE_DIRS = [
    os.path.join(TEMPLATE_ROOT, "defaults"),
]
