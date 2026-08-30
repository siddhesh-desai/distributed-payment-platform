# ADR-0008: Use SQLAlchemy 2 and Alembic for ORM and migrations

- **Status:** Accepted
- **Date:** 2026-08-29
- **Deciders:** Siddhesh Desai

## Context

ADR-0004 places persistence shapes in `models/`, DB access in `repositories/`, and **per-module** `migrations/`, with an optional app-level runner. The first vertical slice needs: connect the API to Postgres, evolve schema safely, and expose a sample GET that reads via the ORM stack. Learners are new to Alembic; the tool choice should be standard for Python + FastAPI.

## Decision

1. Use **SQLAlchemy 2.x** as the ORM / SQL toolkit for `apps/backend/api` (models + engine/session wiring in `core`, repositories use sessions).
2. Use **Alembic** for schema migrations. Each domain keeps revisions under `modules/<name>/migrations/` per ADR-0004; an **app-level Alembic runner/config** discovers and applies them in a defined order.
3. Drive DB connectivity from **environment-backed settings** (DSN, pool size, timeouts); do not auto-run migrations on every API startup in production-shaped deploys — prefer an explicit migrate command/target (local Compose DX per ADR-0007 may document migrate-then-serve without implying the same for prod).
4. First slice: a **disposable sample table** in `sample_module`, repository + service, and a **GET** endpoint that returns row(s) from the DB. Removal later is another migration, not a silent drop.

## Consequences

### Positive

- Industry-default Python stack; maps cleanly to ADR-0004 layers.
- Versioned schema for every environment; sample table proves the path end-to-end.

### Negative / trade-offs

- Multi-module Alembic layout needs a clear runner convention (more than a single default `alembic/` tree).
- ORM misuse (lazy loads in wrong places, huge sessions) is a teaching risk — keep repositories thin.

### Follow-ups

- Teach Alembic revision/upgrade workflow when implementing (not blocked on a separate ADR).
- Add `psycopg` (v3) or equivalent driver as the Postgres DBAPI dependency.
- Tests: prefer deterministic DB tests (later Testcontainers or Compose-backed integration); unit-test services with fakes where appropriate.

## Alternatives considered

### Raw `psycopg` SQL only (no ORM)

Rejected for Phase 1 default: slower domain modeling; revisit for specific hot paths if measured.

### Django ORM / Tortoise / SQLModel as primary

Rejected: SQLAlchemy 2 is the common FastAPI companion; SQLModel optional later, not the ownership model.

### Single shared `migrations/` package for all domains

Rejected: conflicts with ADR-0004 module ownership.
