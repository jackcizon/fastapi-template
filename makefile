.PHONY: all lint format type test coverage pre_commit docs

all: pre_commit coverage

lint:
	poetry run ruff check src/ tests/

format:
	poetry run ruff format src/ tests/

type:
	poetry run mypy --config-file mypy.ini

test:
	poetry run pytest -q

coverage:
	poetry run coverage run -m pytest -q
	poetry run coverage report -m
	poetry run coverage html

pre_commit:
	poetry run pre-commit run -a

docs:
	sphinx-autobuild docs docs/_build/html