.PHONY: install install-dev test lint format clean build publish help

help:
	@echo "Available commands:"
	@echo "  make install       - Install package"
	@echo "  make install-dev   - Install package with dev dependencies"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linting checks"
	@echo "  make format        - Format code with black and isort"
	@echo "  make clean         - Remove build artifacts"
	@echo "  make build         - Build distribution packages"
	@echo "  make publish       - Publish to PyPI (requires credentials)"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest --cov=lean_tearsheet --cov-report=term-missing --cov-report=html

lint:
	black --check --line-length 79 src/ tests/
	flake8 --max-line-length 79 --extend-ignore=E203 src/ tests/
	isort --check-only --profile black --line-length 79 src/ tests/
	mypy src/

format:
	black --line-length 79 src/ tests/
	isort --profile black --line-length 79 src/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

publish: build
	twine upload dist/*
