---
id: 0006
slug: sqlalchemy-orm
title: SQLAlchemy 2 ORM
category: technologies
status: taught
taught_on: 2026-08-29
code_refs:
  - libs/backend/payflow_common/payflow_common/models/
  - apps/backend/api/core/db/
  - apps/backend/api/modules/sample_module/models/sample_item.py
  - apps/backend/api/modules/sample_module/repositories/sample_item_repository.py
related:
  - alembic-migrations
  - domain-module-layering
  - postgresql-primary-store
  - sqlalchemy-sync-vs-async
adr_refs:
  - adr/0008-use-sqlalchemy-and-alembic.md
---

# SQLAlchemy 2 ORM

## What

**SQLAlchemy 2** is Python’s standard SQL toolkit + ORM. Models map classes to tables; sessions execute queries.

## Why

Repositories stay readable; types and relationships scale better than ad-hoc SQL strings for domain work (raw SQL still OK for hot paths later).

## How

```text
Settings (POSTGRES_*) → database_url → create_engine → SessionLocal
Model (DeclarativeBase) → Repository(session) → Service → route maps to Pydantic response
```

`get_db` is a FastAPI dependency yielding a request-scoped SQLAlchemy `Session`.

## Where it fits (HLD / LLD)

LLD: `models/` shapes only; `repositories/` DB access; never expose ORM models as public HTTP schemas.

## Trade-offs

ORM misuse (lazy loads, huge sessions) hurts. Keep repositories thin; map to route outputs explicitly.

## Production notes

`pool_pre_ping=True`; size pools so instances × pool < Postgres `max_connections`; set timeouts via settings.

## Check your understanding

1. Why is `SampleItemResponse` not the same class as `SampleItem`?
   - Because `SampleItemResponse` is the HTTP response schema (Pydantic); `SampleItem` is the ORM table shape.
2. Where should a `SELECT` live — service or repository?
   - A `SELECT` should live in the repository.

## Code in this repo

`SampleItem` model + `SampleItemRepository.list_all` + `GET /sample/items` via `SampleItemService`.
