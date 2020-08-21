.PHONY: build
build: docker

.PHONY: bump
bump:
	bumpversion patch
	git push origin main

.PHONY: build
build:
	docker-compose build
	docker images | grep trailhawks

.PHONY: check
check:
	docker-compose run --rm web python manage.py check --deploy

.PHONY: djcodemod
djcodemod:
	djcodemod run --deprecated-in 3.0 .
	djcodemod run --removed-in 3.0 .

.PHONY: docker
docker:
	docker-compose build

.PHONY: lint
lint:
	curlylint templates

.PHONY: makemigrations
makemigrations:
	docker-compose run --rm web python manage.py makemigrations

.PHONY: migrate
migrate:
	docker-compose run --rm web python manage.py migrate

.PHONY: pip-compile
pip-compile:
	pip-compile requirements/requirements.in

.PHONY: static
static:
	@npx -p tailwindcss@1.7.3 tailwindcss build ./frontend/index.css \
		--config ./frontend/tailwind.config.js \
		--output ./assets/css/tailwind.css

	@docker-compose run --rm web python manage.py collectstatic --noinput

.PHONY: up
up:
	docker-compose build
	docker-compose run --rm web python manage.py check
	docker-compose run --rm web python manage.py makemigrations
	docker-compose run --rm web python manage.py migrate
	docker-compose down
	docker-compose up -d
	docker-compose logs -f
