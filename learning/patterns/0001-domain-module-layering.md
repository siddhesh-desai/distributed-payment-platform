---
id: 0001
slug: domain-module-layering
title: Domain module layering (routes → public facades → services → …)
category: patterns
status: taught
taught_on: 2026-08-12
updated_on: 2026-08-30
code_refs:
  - apps/backend/api/modules/sample_module/routes/
  - apps/backend/api/modules/sample_module/public/facades/
  - apps/backend/api/modules/sample_module/services/
  - apps/backend/api/modules/sample_module/repositories/
related:
  - modular-monolith-bounded-contexts
adr_refs:
  - adr/0004-backend-api-domain-modules.md
  - adr/0010-domain-module-call-path-facades-and-naming.md
---

# Domain module layering

## What

Each domain module uses a fixed call path (ADR-0010):

**routes → public facades → use-case services → repositories → models**

- **routes**: HTTP only — `requests/`, `responses/`, `endpoints/` + `registry.py`; import **only** `public/`
- **public/facades**: published API; one facade, many methods; each method → one use-case service
- **services**: one use-case class per file; direct params (no `services/inputs|outputs`)
- **models**: table shapes only; **repositories**: DB access only
- **public/inputs|outputs**: optional cross-module DTOs only

## Why

Without this, endpoints grow DB/business logic; callers import private types; fat services mix many use cases. Facades give one entry for HTTP and other modules.

## How

Hello path:

1. `routes/endpoints/get_hello.py` → `HelloFacade.say_hello()`
2. `services/hello_service.py` — greeting logic

DB sample path:

1. `models/sample_item.py` → `repositories/sample_item_repository.py`
2. `services/sample_items_list_service.py` — list use case
3. `public/facades/sample_item_facade.py` — `SampleItemFacade.list_items(db)` (static)
4. `routes/endpoints/get_sample_items.py` — `GET /sample/items`

## Where it fits (HLD / LLD)

LLD inside each `modules/<name>/`. Same facade surface for same-module HTTP and cross-module callers.

## Trade-offs

Extra hop (endpoint → facade → service). Anemic models + use-case services keep Phase 1 clear.

## Production notes

Do not put business rules in route handlers. Do not import `services/` or `repositories/` from routes or other modules.

## Check your understanding

1. Why must `HelloResponse` live under `routes/responses/` instead of `models/`?
2. What may a route import from another (or the same) module’s internals?

## Code in this repo

`get_hello` → `HelloFacade` → `HelloService`.  
`get_sample_items` → `SampleItemFacade` → `SampleItemsListService` → `SampleItemRepository`.

## Further practice (optional)

Add `SampleItemsCreateService` and a `create_item` method on `SampleItemFacade`.
