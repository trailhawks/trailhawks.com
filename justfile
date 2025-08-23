# Disable automatic .env file loading (we handle env vars explicitly)
set dotenv-load := false

# Define reusable command prefixes for Docker operations
compose := "docker compose run --rm --no-deps web"
manage := compose + " python -m manage"
TAILWIND_CSS_VERSION := "latest"

# Show all available recipes when just is run without arguments
@_default:
    just --list

# Format the justfile using just's built-in formatter
@fmt:
    just --fmt --unstable

# Bump version, commit, and push to main branch
@bump:
    bumpver update --allow-dirty
    git push origin main

# Build Docker containers (accepts additional docker compose build arguments)
@build *ARGS:
    docker compose build {{ ARGS }}

# Run Django deployment checks
@check:
    {{ manage }} check --deploy

# Open an interactive bash shell in the web container
@console:
    {{ compose }} /bin/bash

# Stop and remove all Docker containers
@down:
    docker compose down

# Import race results from UltraSignup (currently set for 2018 races)
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

# Run pre-commit hooks on all files
@lint *ARGS:
    uv --quiet tool run --with pre-commit-uv pre-commit run {{ ARGS }} --all-files

# Update pre-commit hooks to their latest versions
@lint-update:
    uv --quiet tool run --with pre-commit-uv pre-commit autoupdate

# View Docker container logs (accepts docker compose logs arguments)
@logs +ARGS="":
    docker compose logs {{ ARGS }}

# Create new Django database migrations
@makemigrations:
    {{ manage }} makemigrations

# Apply Django database migrations
@migrate:
    {{ manage }} migrate

# Compile Python dependencies from requirements.in to requirements.txt
@lock *ARGS:
    docker compose run \
        --rm web \
            bash -c "uv pip compile {{ ARGS }} ./requirements.in \
                --output-file ./requirements.txt"

# Execute Django management commands (default: show help)
@run +ARGS="--help":
    {{ manage }} {{ ARGS }}

# Scrape race data from UltraSignup using Spatula
@scrape:
    just spatula scrape

# Test the Spatula scraper without saving data
@scrape-test:
    just spatula test

# Run Spatula scraper with custom arguments (clears cache first)
@spatula +ARGS="scrape":
    rm -rf _scrapes/*
    {{ compose }} spatula {{ ARGS }} --fastmode scrapers.scrape_ultrasignup.RaceListFromDjango

# Start development server (database, migrations, then web server)
@server:
    docker compose up -d db
    {{ manage }} migrate --noinput
    docker compose up web

# Build Tailwind CSS and collect Django static files
@static:
    npx -p tailwindcss@{{ TAILWIND_CSS_VERSION }} tailwindcss build \
        ./frontend/index.css \
        --config ./frontend/tailwind.config.js \
        --output ./assets/css/tailwind.css

    {{ manage }} collectstatic --noinput

# Run pytest test suite in Docker
@test:
    {{ compose }} pytest

# Start Docker containers (accepts docker compose up arguments)
@up *ARGS:
    docker compose up {{ ARGS }}

# Upgrade all Python dependencies to their latest versions
@upgrade:
    just lock --upgrade

# === Additional Docker Management Recipes ===

# Remove current application services (placeholder - needs implementation)
@remove:
    ...

# Start all services in detached mode by default
@start *ARGS="--detach":
    docker compose up {{ ARGS }}

# Restart all running Docker services
@restart:
    docker compose restart

# Show status of all Docker containers
@status:
    docker compose ps

# Stop all services without removing containers
@stop:
    docker compose down

# Tail service logs with auto-follow
@tail:
    just logs --follow

# Export PostgreSQL database to compressed dump file
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

# Import PostgreSQL database from dump file (WARNING: destroys existing data)
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
