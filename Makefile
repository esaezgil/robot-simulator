.DEFAULT_GOAL := check
POETRY := poetry
SRC := robot_simulator tests

.PHONY: install lint format format-check typecheck test coverage check fix clean

install:
	$(POETRY) install

lint:
	$(POETRY) run flake8 $(SRC)

format:
	$(POETRY) run isort $(SRC)
	$(POETRY) run black $(SRC)

format-check:
	$(POETRY) run isort --check-only $(SRC)
	$(POETRY) run black --check $(SRC)

typecheck:
	$(POETRY) run mypy $(SRC)

test:
	$(POETRY) run pytest

coverage:
	$(POETRY) run coverage run --source=robot_simulator -m pytest
	$(POETRY) run coverage report

fix: format

check: lint format-check typecheck test

clean:
	find . -type d -name '__pycache__' -prune -exec rm -rf {} +
	rm -rf .pytest_cache .mypy_cache htmlcov
	rm -f .coverage coverage.xml
