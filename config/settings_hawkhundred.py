import os

from config.settings import *


SITE_ID = 2

ROOT_URLCONF = "config.urls_hawkhundred"

TEMPLATE_DIRS = [
    os.path.join(TEMPLATE_ROOT, "hawkhundred.com"),
    os.path.join(TEMPLATE_ROOT, "race_defaults"),
    os.path.join(TEMPLATE_ROOT, "defaults"),
]
