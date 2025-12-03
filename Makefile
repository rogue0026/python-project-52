.PHONY: build
build:
	./build.sh

.PHONY: collectstatic
collectstatic:
	echo 'stub for collectstatic'

.PHONY: makemigrations
makemigrations:
	uv run manage.py makemigrations

.PHONY: migrate
migrate: makemigrations
	uv run manage.py migrate

.PHONY: dev
dev:
	uv run manage.py runserver

.PHONY: render-start
render-start:
	gunicorn task_manager.wsgi

.PHONY: install
install:
	uv sync

.PHONY: lint
lint:
	@uv run ruff check --fix task_manager/
