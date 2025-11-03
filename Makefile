.PHONY: help sync test test-fast test-verbose clean installer

help:
	@echo "Available commands:"
	@echo "  make sync         - Sync dependencies using uv"
	@echo "  make test         - Run all tests with coverage"
	@echo "  make test-fast    - Run tests until first failure"
	@echo "  make test-verbose - Run tests with extra verbosity"
	@echo "  make clean        - Clean build artifacts and cache"
	@echo "  make installer    - Build installer with PyInstaller"

sync:
	uv sync

test:
	uv run pytest

test-fast:
	uv run pytest -x

test-verbose:
	uv run pytest -vv

clean:
	rm -rf dist/ build/ .pytest_cache/ htmlcov/ .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

installer:
	uv run python -m PyInstaller --clean --noconfirm weather_app.spec
