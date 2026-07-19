.PHONY: install lint format test test-unit test-api test-integration test-eval test-network coverage compose-up compose-down smoke docs

install:
	pip install -e '.[dev]'

lint:
	ruff check src tests

format:
	ruff format src tests
	ruff check --fix src tests

test:
	pytest

test-unit:
	pytest tests/unit

test-api:
	pytest tests/api

test-integration:
	pytest tests/integration

test-eval:
	pytest tests/eval

test-network:
	ENABLE_NETWORK_TESTS=1 pytest tests/network

coverage:
	pytest --cov=recallops --cov-report=term-missing --cov-report=html

compose-up:
	docker compose up -d postgres qdrant

compose-down:
	docker compose down

smoke:
	python scripts/smoke.py

docs:
	mkdocs build
