.PHONY: install
## Install the dependencies
install:
	poetry install

.PHONY: build
## Build the image
build:
	docker-compose build

.PHONY: up
## Start the container
up:
	docker-compose up

.PHONY: enter
## Enter the fastapi container
enter:
	docker-compose exec fastapi bash

.PHONY: lint
## Run pre-commit checks
lint:
	pre-commit run --all-files

.PHONY: test
## Run tests
test:
	pytest

.PHONY: makemigrations
## Generate migrations
makemigrations:
	alembic revision --autogenerate

.PHONY: migrate
## Run migrations
migrate:
	alembic upgrade head
