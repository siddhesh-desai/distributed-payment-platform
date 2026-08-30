---
id: 0004
slug: postgresql-primary-store
title: PostgreSQL as primary store
category: technologies
status: taught
taught_on: 2026-08-29
code_refs:
  - docker-compose.yml
  - apps/backend/api/core/settings/
  - apps/backend/api/core/db/
related:
  - docker-compose-local-dev
  - sqlalchemy-orm
  - alembic-migrations
  - twelve-factor-config
adr_refs:
  - adr/0006-use-postgresql-as-primary-store.md
---

# PostgreSQL as primary store

## What

**PostgreSQL** is a relational database. PayFlow uses it as the **system of record** for durable domain data (transactions, constraints, later ledger/idempotency).

## Why

Payments need ACID transactions, unique constraints, and predictable concurrency. A shared SQL store is the right Phase 1 foundation before Redis/Kafka.

## How

- Local: Compose service `postgres` (`postgres:16`), host port **5433→5432** so a Mac Postgres on 5432 is untouched.
- App: discrete DB settings → SQLAlchemy URL (psycopg); business schema via Alembic, not image init DDL.

## Where it fits (HLD / LLD)

HLD: primary store for the modular monolith API. LLD: `models/` + `repositories/` + `migrations/` per module; engine/session in `core/`.

## Trade-offs

Strong consistency and tooling vs ops cost (connections, backups, migrations). SQLite rejected for concurrency/production-parity learning.

## Production notes

Prefer managed Postgres + backups/PITR later; least-privilege roles; TLS; watch `max_connections` vs app pool × replicas. Local Compose is not HA.

## Check your understanding

1. Why map host **5433** instead of 5432 in Compose?
   - To avoid conflicts with a host Postgres on 5432.
2. Who owns `max_connections` vs `postgres_pool_size`?
   - `max_connections` is owned by the Postgres server and `postgres_pool_size` is owned by the application.

## Code in this repo

`docker-compose.yml` runs Postgres 16 on 5433; `core/settings/` defaults host DSN to `localhost:5433`; Compose API uses hostname `postgres:5432`.
