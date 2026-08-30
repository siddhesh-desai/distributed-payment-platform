---
id: 0005
slug: docker-compose-local-dev
title: Docker Compose for local development
category: technologies
status: taught
taught_on: 2026-08-29
code_refs:
  - docker-compose.yml
  - apps/backend/api/Dockerfile
  - apps/backend/api/scripts/docker-entrypoint.sh
  - .env.example
related:
  - postgresql-primary-store
  - alembic-migrations
adr_refs:
  - adr/0007-use-docker-compose-for-local-development.md
---

# Docker Compose for local development

## What

**Docker Compose** declares multi-container local stacks (services, ports, volumes, env, healthchecks) from one YAML file.

## Why

Reproducible API + Postgres without fighting host installs; correct DNS between containers (`api` → `postgres`).

## How

```text
docker compose up --build
  → postgres (healthy) → api build → entrypoint: alembic upgrade heads → uvicorn
```

Escape hatch: Compose Postgres only; run API on host against `localhost:5433`.

## Where it fits (HLD / LLD)

Local/dev runtime only — not production deploy. Later Redis/Kafka join the same Compose project.

## Trade-offs

Requires Docker. API-in-container reload is heavier than host `uvicorn`; escape hatch covers that.

## Production notes

Compose ≠ HA/managed DB. Do not treat local passwords/ports as prod.

## Check your understanding

1. Inside Compose, why is the DSN host `postgres` not `localhost`?
   - To avoid conflicts with a host Postgres on 5432.

2. What does `depends_on: condition: service_healthy` prevent?
   - It prevents the API from starting up before the Postgres server is healthy.

## Code in this repo

Root `docker-compose.yml` (`postgres` + `api`); requires `POSTGRES_PASSWORD` from gitignored `.env` (see `.env.example`). `apps/backend/api/Dockerfile` copies workspace root lockfile + `apps/backend/api` + `libs/backend` then `uv sync --package payflow-api`; entrypoint migrate-then-serve.
