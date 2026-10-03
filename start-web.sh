#!/bin/sh
uv run -m manage migrate --noinput
uv run -m manage collectstatic --noinput
# uwsgi serves the site directly, not through django-prodserver. `exec`
# hands the container's stop signal to uwsgi so it shuts down cleanly
# instead of being killed after the stop timeout.
exec uv run uwsgi \
    --buffer-size=8196 \
    --chdir=/src \
    --enable-threads \
    --harakiri=180 \
    --http-socket=:8000 \
    --http-timeout=180 \
    --log-x-forwarded-for \
    --master \
    --max-requests=5000 \
    --module=config.wsgi \
    --need-app \
    --offload-threads=2 \
    --post-buffering=4096 \
    --processes=1 \
    --static-map=/media=/src/media_root \
    --strict \
    --threads=2 \
    --thunder-lock \
    --vacuum
