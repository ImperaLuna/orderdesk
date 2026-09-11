.PHONY: install run test lint typecheck migrate revision seed

install:
	uv sync

run:
	uv run uvicorn app.main:app --reload

test:
	uv run pytest -q

lint:
	uv run ruff check . && uv run ruff format --check .

typecheck:
	uv run mypy app

migrate:
	uv run alembic upgrade head

revision:
	uv run alembic revision --autogenerate -m "$(m)"

seed:
	uv run python -m scripts.seed
