---
id: 0007
slug: alembic-migrations
title: Alembic schema migrations
category: technologies
status: taught
taught_on: 2026-08-29
code_refs:
  - apps/backend/api/core/alembic/alembic.ini
  - apps/backend/api/core/alembic/env.py
  - apps/backend/api/modules/sample_module/migrations/0001_create_sample_items.py
related:
  - sqlalchemy-orm
  - docker-compose-local-dev
  - domain-module-layering
  - orm-model-auto-discovery
adr_refs:
  - adr/0004-backend-api-domain-modules.md
  - adr/0008-use-sqlalchemy-and-alembic.md
---

# Alembic schema migrations

## What

**Alembic** versions database schema changes. Each **revision** has `upgrade()` / `downgrade()` and links via `down_revision`. Alembic records applied revisions in `alembic_version`.

## Why

Without migrations, environments drift and rollbacks are guesswork — unacceptable once money tables exist.

## How (mental model)

```text
core/alembic/alembic.ini + env.py   ← app-level runner
modules/<name>/migrations/          ← per-module revisions (ADR-0004)
nx run api:makemigrations -- --rev-id 0002 -m "msg"  ← write 0002_*.py (autogenerate)
nx run api:migrate                                   ← alembic upgrade heads
```

- **Revision**: one change set; **file + id** use zero-padded numbers (`0001_create_sample_items.py`, `revision = "0001"`) so listings always sort.
- **Branch label**: e.g. `sample_module` — keeps module lineages clear when many modules have roots.
- **makemigrations** (Nx): Django-style “create files” — pass `--rev-id 0002` (next number) with `-m "…"`. Needs a reachable DB; **always review** the generated file.
- **migrate** (Nx / Compose): Django-style “apply” — `alembic upgrade heads`.
- **env.py**: sets DB URL from settings; discovers `modules/*/migrations`; auto-imports `modules/*/models/**` so `OrmBaseModel.metadata` is complete for autogenerate.
- **alembic.ini `version_locations`**: required so `history`/`revision` see module dirs (those commands do not always rely only on env discovery). Config lives in `core/alembic/` next to `env.py`; invoke with `-c core/alembic/alembic.ini`.

First sample revision creates `sample_items` and seeds one row (disposable later via a drop migration).

## Where it fits (HLD / LLD)

Schema ownership stays with the domain module; runner is app-level (`nx run api:migrate` / Compose entrypoint).

## Trade-offs

Multi-module version locations need discipline (update `version_locations` when adding a module’s first migration). Autogenerate helps but review by hand — especially for money-path tables.

## Production notes

Prefer explicit migrate in deploy pipelines, not silent auto-migrate on every API start. Expand/contract for zero-downtime later.

## Check your understanding

1. Why both `alembic.ini` `version_locations` and discovery in `env.py`?
   - To ensure that the migrations are discovered by Alembic.
2. Why `upgrade heads` (plural) instead of `head`?
   - To apply all the migrations that have been created.
3. How do you remove the sample table safely later?
   - By creating a drop migration and applying it.

## Code in this repo

`0001_create_sample_items.py`; Nx targets `api:makemigrations` / `api:migrate`; Compose entrypoint runs `upgrade heads` before uvicorn.
