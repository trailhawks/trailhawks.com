set dotenv-load := false

compose := "docker-compose run --rm --no-deps web"
manage := compose + " python -m manage"
TAILWIND_CSS_VERSION := "latest"

@_default:
    just --list

@fmt:
    just --fmt --unstable

@bump:
    bumpver update --allow-dirty
    git push origin main

@build *ARGS:
    docker-compose build {{ ARGS }}

@check:
    {{ manage }} check --deploy

# opens a console
@console:
    {{ compose }} /bin/bash

@down:
    docker-compose down

@import_from_ultrasignup:
    {{ manage }} import_from_ultrasignup --race=53172
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

@lint *ARGS:
    just pre-commit run --all-files {{ ARGS }}

@logs +ARGS="":
    docker-compose logs {{ ARGS }}

@makemigrations:
    {{ manage }} makemigrations

@migrate:
    {{ manage }} migrate

# Compile new python dependencies
@lock *ARGS:
    docker-compose run \
        --rm web \
            bash -c "uv pip compile {{ ARGS }} ./requirements.in \
                --output-file ./requirements.txt"

# Python linting
@pre-commit *ARGS:
    pre-commit {{ ARGS }}

@run +ARGS="--help":
    {{ manage }} {{ ARGS }}

@scrape:
    just spatula scrape

@scrape-test:
    just spatula test

@spatula +ARGS="scrape":
    rm -rf _scrapes/*
    {{ compose }} spatula {{ ARGS }} --fastmode scrapers.scrape_ultrasignup.RaceListFromDjango

@server:
    docker-compose up -d db
    {{ manage }} migrate --noinput
    docker-compose up web

@static:
    npx -p tailwindcss@{{ TAILWIND_CSS_VERSION }} tailwindcss build \
        ./frontend/index.css \
        --config ./frontend/tailwind.config.js \
        --output ./assets/css/tailwind.css

    {{ manage }} collectstatic --noinput

@test:
    {{ compose }} pytest

@up *ARGS:
    docker-compose up {{ ARGS }}

# Upgrade existing Python dependencies to their latest versions
@upgrade:
    just lock --upgrade

# new...

# Remove current application services
@remove:
    ...

# Start all services
@start *ARGS="--detach":
    docker-compose up {{ ARGS }}

# Restart all services
@restart:
    docker-compose restart

@status:
    docker-compose ps

# Stop all services
@stop:
    docker-compose down

# Tail service logs
@tail:
    just logs --follow

# dump database to file
pg_dump file='db.dump':
    docker compose run \
        --no-deps \
        --rm \
        db \
        pg_dump \
            --dbname "${DATABASE_URL:=postgres://postgres@db/postgres}" \
            --file /src/{{ file }} \
            --format=c \
            --verbose

# restore database dump from file
pg_restore file='db.dump':
    docker compose run \
        --no-deps \
        --rm \
        db \
        pg_restore \
            --clean \
            --dbname "${DATABASE_URL:=postgres://postgres@db/postgres}" \
            --if-exists \
            --no-owner \
            --verbose \
            /src/{{ file }}
