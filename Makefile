.PHONY: build
build:
	./build.sh

.PHONY: collectstatic
collectstatic:
	echo 'stub for collectstatic'

.PHONY: create_venv
create_venv:
	uv venv

.PHONY: activate_venv
activate_venv:
	source .venv/bin/activate

.PHONY: create_migrations
create_migrations:
	uv run manage.py makemigrations

.PHONY: run_migrations
run_migrations:
	uv run manage.py migrate

.PHONY: dev
dev:
	uv run manage.py runserver

.PHONY: render-start
render-start:
	gunicorn task_manager.wsgi

.PHONY: lint
lint:
	@uv run ruff check --fix task_manager/

.PHONY: install
install:
	uv sync

.PHONY: test
test:
	uv run manage.py test

.PHONY: test_coverage
test_coverage:
	uv run coverage run manage.py test

.PHONY: coverage_report
coverage_report: test_coverage
	uv run coverage html
