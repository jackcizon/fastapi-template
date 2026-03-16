.PHONY: all lint format type test coverage pre_commit commit changelog

# all: lint format type test coverage pre_commit
all: lint format type pre_commit

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

commit:
	cz commit

changelog:
	cz changelog