#!/usr/bin/env bash

set -eo pipefail

python manage.py collectstatic --noinput
python manage.py migrate --noinput
