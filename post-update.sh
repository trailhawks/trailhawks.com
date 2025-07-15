#!/usr/bin/env bash

set -eo pipefail

python -m manage showmigrations --plan --skip-checks
python -m manage migrate --noinput --skip-checks
python -m manage collectstatic --noinput --skip-checks
