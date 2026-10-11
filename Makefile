.PHONY: install run migrate check typecheck lint lint-check flake8 format test

install:
	uv sync
run:
	uv run python manage.py runserver
migrate:
	uv run python manage.py migrate
check:
	uv run python manage.py check
typecheck:
	uv run mypy .
lint:
	uv run ruff check . --fix
lint-check:
	uv run ruff check .
flake8:
	uv run flake8 .
format:
	uv run ruff format .
test:
	uv run pytest
