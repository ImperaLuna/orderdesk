# orderdesk

Order management service. FastAPI, SQLAlchemy 2 (async), Alembic, Pydantic v2.

## Quick start

```bash
uv sync
cp .env.example .env
uv run alembic upgrade head
uv run python -m scripts.seed
uv run uvicorn app.main:app --reload
```

Docs at http://localhost:8000/docs.

Postgres via Docker:

```bash
docker compose up -d db
export DATABASE_URL=postgresql+asyncpg://orderdesk:orderdesk@localhost:5432/orderdesk
```

## Layout

```
app/
  core/         settings, logging, id generation
  db/           engine, session, declarative base
  models/       SQLAlchemy ORM models
  schemas/      Pydantic request/response models
  repositories/ data access, one class per aggregate
  services/     business logic
  api/v1/       routers
alembic/        migrations
docs/adr/       architecture decision records
tests/
```

## Identifier strategy

See [ADR-0002](docs/adr/0002-identifier-strategy.md). Short version:

| Table         | ID type |
|---------------|---------|
| users         | UUIDv4  |
| api_keys      | UUIDv4  |
| orders        | UUIDv7  |
| order_events  | UUIDv7  |

## Commands

```bash
make test
make lint
make typecheck
make migrate
```
