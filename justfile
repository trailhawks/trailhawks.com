compose := "docker-compose run --rm --no-deps web"
manage := compose + " python manage.py"
TAILWIND_CSS_VERSION := "latest"

@_default:
    just --list

@bump:
    bumpver update
    git push origin main

@build:
    docker-compose build
    docker images | grep trailhawks

@check:
    {{manage}} check --deploy

# opens a console
@console:
    {{compose}} /bin/bash

@djcodemod:
    djcodemod run --deprecated-in 3.1 .

@down:
    docker-compose down

@fmt:
    -isort --project=black .
    -black .
    -djhtml --tabwidth=4 --in-place \
        templates/**/**/*.html \
        templates/**/**/**/*.html \
        templates/**/**/**/**/*.html
    -rustywind --write ./templates/tailwind/

@import_from_ultrasignup:
    {{manage}} import_from_ultrasignup 53172
    # just run import_from_ultrasignup 53173
    # just run import_from_ultrasignup 53174

    # 2020
    # just run import_from_ultrasignup 73780

    # # 2019
    # just run import_from_ultrasignup 63105
    # just run import_from_ultrasignup 63106
    # just run import_from_ultrasignup 63107

    # # 2018
    # just run import_from_ultrasignup 53172
    # just run import_from_ultrasignup 53173
    # just run import_from_ultrasignup 53174

    # # 2017
    # just run import_from_ultrasignup 43955
    # just run import_from_ultrasignup 43957
    # just run import_from_ultrasignup 43956

    # # 2016
    # just run import_from_ultrasignup 36684
    # just run import_from_ultrasignup 36685

@lint:
    -black --check --diff .
    -isort --check --diff --project=black .
    -unimport --check --diff .
    -vulture --min-confidence=80 .
    # -curlylint templates
    # -rustywind --dry-run ./templates/tailwind/

@logs +ARGS="":
    docker-compose logs {{ARGS}}

@makemigrations:
    {{manage}} makemigrations

@migrate:
    {{manage}} migrate

@pip-compile:
    pip install --upgrade -r requirements/requirements.in
    pip-compile requirements/requirements.in
    {{compose}} \
        pip install \
            --upgrade \
            --requirement ./requirements/requirements.in && \
        pip-compile \
            ./requirements/requirements.in \
            --output-file ./requirements/requirements.txt

@run +ARGS="--help":
    {{manage}} {{ARGS}}

@server:
    docker-compose up -d db
    {{manage}} migrate --noinput
    docker-compose up web

@static:
    npx -p tailwindcss@{{TAILWIND_CSS_VERSION}} tailwindcss build \
        ./frontend/index.css \
        --config ./frontend/tailwind.config.js \
        --output ./assets/css/tailwind.css

    {{manage}} collectstatic --noinput

@test:
    {{compose}} pytest

@up:
    docker-compose up -d
