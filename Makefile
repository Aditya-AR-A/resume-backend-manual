.PHONY: help setup install run test clean lint format

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Set up the development environment
	./setup.sh

install: ## Install dependencies
	pip install -r requirements.txt

run: ## Run the application
	python -m app.main

run-reload: ## Run the application with auto-reload
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test: ## Run tests
	pytest tests/ -v

test-cov: ## Run tests with coverage
	pytest tests/ -v --cov=app --cov-report=html

clean: ## Clean up generated files
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf logs/
	rm -f complete.log
	rm -f session_*.log

lint: ## Run linting
	flake8 app/ tests/
	black --check app/ tests/
	isort --check-only app/ tests/

format: ## Format code
	black app/ tests/
	isort app/ tests/

docs: ## Generate API documentation
	@echo "API documentation available at: http://localhost:8000/docs"
	@echo "Redoc documentation at: http://localhost:8000/redoc"

check: ## Run all checks (lint, test, type check)
	make lint
	make test
	mypy app/ --ignore-missing-imports

dev: ## Run in development mode
	make run-reload
