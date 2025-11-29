.PHONY: build
build:
	./build.sh

.PHONY: dev
dev:
	uv run manage.py runserver

.PHONY: render-start
render-start:
	gunicorn task_manager.wsgi

.PHONY: install
install:
	uv sync
