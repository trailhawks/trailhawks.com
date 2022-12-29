#!/usr/bin/env bash
#
# This script is used to start our Django WSGI process (gunicorn in this case)
# for use with docker-compose.  In deployed or production scenarios you would
# not necessarily use this exact setup.
#

python manage.py collectstatic --noinput

# gunicorn -c config/gunicorn.conf.py --log-level INFO -b 0.0.0.0:8000 config.wsgi
python manage.py runserver 0.0.0.0:8000
