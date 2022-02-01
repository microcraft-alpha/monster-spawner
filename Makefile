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

.PHONY: rebuild
## Build and start the container
rebuild:
	docker-compose up --build

.PHONY: enter
## Enter the fastapi container
enter:
	docker-compose exec fastapi bash

.PHONY: lint
## Run pre-commit checks
lint:
	poetry run pre-commit run --all-files

.PHONY: test
## Run tests
test:
	poetry run pytest

.PHONY: makemigrations
## Generate migrations
makemigrations:
	poetry run alembic revision --autogenerate

.PHONY: migrate
## Run migrations
migrate:
	poetry run alembic upgrade head
