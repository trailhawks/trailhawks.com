#!/bin/sh
uv run -m manage migrate --noinput
uv run -m manage collectstatic --noinput
# uv run -m manage prodserver web
uv run uwsgi \
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
