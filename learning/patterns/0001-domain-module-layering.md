---
id: 0001
slug: domain-module-layering
title: Domain module layering (routes → services → models → …)
category: patterns
status: taught
taught_on: 2026-08-12
code_refs:
  - apps/backend/api/modules/sample_module/routes/
  - apps/backend/api/modules/sample_module/services/hello_service.py
  - apps/backend/api/modules/sample_module/public/
related:
  - modular-monolith-bounded-contexts
adr_refs:
  - adr/0004-backend-api-domain-modules.md
---

# Domain module layering

## What

Each domain module uses a fixed layer stack:

**routes → services → models → repositories → migrations → clients → public → tests**

- **routes**: HTTP only — `inputs/`, `outputs/`, `endpoints/` (one file each) + `registry.py`
- **services**: **all business logic** as classes; same-module deps via constructor injection
- **models**: table/persistence **shapes only** (anemic for Phase 1)
- **public**: cross-module contract (`inputs/`, `outputs/`, `facets/`) — not route schemas, not models

## Why

Without layering, endpoints grow DB calls and business rules; other modules import private types; tests become end-to-end only. Clear layers make “where does this go?” answerable.

## How

Hello path today:

1. `routes/endpoints/get_hello.py` — HTTP adapter; constructs `HelloService`
2. `services/hello_service.py` — greeting logic (instance method)
3. `routes/outputs/hello_output.py` — response schema ≠ table model

Unused layers stay as folders + `.gitkeep` until needed (no fake DB).

## Where it fits (HLD / LLD)

LLD inside each `modules/<name>/`. Cross-module LLD uses `public/` only.

## Trade-offs

Anemic models + service classes specialize constitution “rich domain objects” for Phase 1 clarity. Rich models can return later with an ADR if needed.

## Production notes

Do not put business rules in route handlers or Pydantic schemas. Do not share ORM models as public API types.

## Check your understanding

1. Why must `HelloResponse` live under `routes/outputs/` instead of `models/`?
2. What may call another module’s repository?

## Code in this repo

`sample_module` hello implements routes + services: the endpoint constructs `HelloService()` and calls `say_hello()` (same-module constructor DI). Other layers are empty placeholders matching ADR-0004.

## Further practice (optional)

Add a second same-module service and inject it into `HelloService` via the constructor.
