.PHONY: install dev test lint check clean

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=mindclash

lint:
	ruff check mindclash/ tests/

check:
	mindclash check

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete
