---
id: 0002
slug: twelve-factor-config
title: Twelve-factor config (env-backed settings)
category: patterns
status: taught
taught_on: 2026-08-29
code_refs:
  - apps/backend/api/core/settings/
  - .env.example
  - docker-compose.yml
related:
  - postgresql-primary-store
  - docker-compose-local-dev
adr_refs:
  - adr/0006-use-postgresql-as-primary-store.md
---

# Twelve-factor config (env-backed settings)

## What

[Twelve-Factor](https://12factor.net/) **Factor III — Config**: config that varies by environment lives in the **environment**, not in code.

## Why

Same image/binary for local/staging/prod; secrets stay out of git; Compose can inject a different DSN than host-run.

## How

`pydantic-settings` `Settings` reads discrete `POSTGRES_*` knobs (user/password/db/host/port/pool) and builds the SQLAlchemy URL. Defaults suit host-run (`localhost:5433`). Compose sets `POSTGRES_HOST=postgres` and `POSTGRES_PORT=5432`.

## Where it fits (HLD / LLD)

Process wiring in `core/settings/` (composed groups → `Settings`); domains never hardcode hosts/passwords.

## Trade-offs

Too many env knobs become opaque — keep a small documented set (`.env.example`).

## Production notes

Secret manager in shared envs; never commit real `.env`.

## Check your understanding

1. Why is putting the DB password in a service class a 12-factor violation?
   - The password is a secret that should not be stored in the code.
2. Why can Compose and host-run use different `POSTGRES_HOST` values?
   - The Compose service name `postgres` is different from the host-run `localhost`.

## Code in this repo

`core/settings/` (`database.py` + composed `Settings`) + root `.env.example`; Compose passes `POSTGRES_*`.
