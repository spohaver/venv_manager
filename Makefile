# Makefile for venv-manager project

.PHONY: help install test clean lint format check-format

# Default target
help:
	@echo "Available targets:"
	@echo "  install      - Install the package in development mode"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linting checks"
	@echo "  format       - Format code with black"
	@echo "  check-format - Check if code is formatted correctly"
	@echo "  clean        - Clean up build artifacts"
	@echo "  demo         - Run a demo of the tool"

# Install in development mode
install:
	pip install -e .
	pip install -r requirements-dev.txt

# Run tests
test:
	python -m pytest tests/ -v

# Run linting
lint:
	flake8 *.py tests/
	mypy *.py --ignore-missing-imports

# Format code
format:
	black *.py tests/

# Check formatting
check-format:
	black --check *.py tests/

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete
	rm -f venv_shell .venvlocation

# Demo the tool
demo:
	@echo "=== Virtual Environment Manager Demo ==="
	@echo "1. Showing help:"
	./venv-manager --help
	@echo ""
	@echo "2. Listing existing environments:"
	./venv-manager list || echo "No environments found"
	@echo ""
	@echo "3. Demo complete - try creating an environment with:"
	@echo "   ./venv-manager --name demo-env"