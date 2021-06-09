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

@djcodemod:
    djcodemod run --deprecated-in 3.0 .
    djcodemod run --removed-in 3.0 .

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

@up:
    # docker-compose build
    # docker-compose run --rm web python manage.py check
    # docker-compose run --rm web python manage.py makemigrations
    # docker-compose run --rm web python manage.py migrate
    # docker-compose down
    docker-compose up -d
    # docker-compose logs -f
