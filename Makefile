.PHONY: build
build: docker

.PHONY: docker
docker:
	docker-compose build

.PHONY: migrate
migrate:
	docker-compose run --rm web python manage.py migrate

.PHONY: static
static:
	docker-compose run --rm web python manage.py collectstatic
