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
    docker-compose run --rm web python manage.py check --deploy

# opens a console
@console:
    {{compose}} /bin/bash

@djcodemod:
    djcodemod run --deprecated-in 3.0 .
    djcodemod run --removed-in 3.0 .

@down:
    docker-compose down

@import_from_ultrasignup:
    just run import_from_ultrasignup 53172
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
    curlylint templates

@makemigrations:
    docker-compose run --rm web python manage.py makemigrations

@migrate:
    docker-compose run --rm web python manage.py migrate

@pip-compile:
    pip install --upgrade -r requirements/requirements.in
    pip-compile requirements/requirements.in
    docker-compose run --rm web \
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
    @npx -p tailwindcss@{{TAILWIND_CSS_VERSION}} tailwindcss build \
        ./frontend/index.css \
        --config ./frontend/tailwind.config.js \
        --output ./assets/css/tailwind.css

    @docker-compose run --rm web python manage.py collectstatic --noinput

@test:
    docker-compose run --rm web pytest

@up:
    # docker-compose build
    # docker-compose run --rm web python manage.py check
    # docker-compose run --rm web python manage.py makemigrations
    # docker-compose run --rm web python manage.py migrate
    # docker-compose down
    docker-compose up -d
    # docker-compose logs -f
