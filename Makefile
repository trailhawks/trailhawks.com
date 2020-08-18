.PHONY: build
build: docker

.PHONY: bump
bump:
	bumpversion patch
	git push origin main

.PHONY: build
build:
	docker-compose build

.PHONY: check
check:
	docker-compose run --rm web python manage.py check

.PHONY: docker
docker:
	docker-compose build

.PHONY: makemigrations
makemigrations:
	docker-compose run --rm web python manage.py makemigrations

.PHONY: migrate
migrate:
	docker-compose run --rm web python manage.py migrate

.PHONY: static
static:
	docker-compose run --rm web python manage.py collectstatic --noinput

.PHONY: up
up:
	docker-compose build
	docker-compose run --rm web python manage.py check
	docker-compose run --rm web python manage.py makemigrations
	docker-compose run --rm web python manage.py migrate
	docker-compose down
	docker-compose up -d
	docker-compose logs -f
