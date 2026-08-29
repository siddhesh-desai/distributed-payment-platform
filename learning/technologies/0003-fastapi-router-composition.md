---
id: 0003
slug: fastapi-router-composition
title: FastAPI router composition
category: technologies
status: taught
taught_on: 2026-08-12
code_refs:
  - apps/backend/api/main.py
  - apps/backend/api/core/router_registry.py
  - apps/backend/api/modules/sample_module/routes/registry.py
related:
  - modular-monolith-bounded-contexts
adr_refs:
  - adr/0004-backend-api-domain-modules.md
---

# FastAPI router composition

## What

FastAPI apps mount **`APIRouter`** instances. Composition = include module routers into one app router, then include that on the `FastAPI` app.

## Why

Keeps domain HTTP definitions next to the domain while the process still exposes one OpenAPI surface and one ASGI app.

## How

```text
main.py  →  include core.api_router
core/router_registry.py  →  include sample (and future module) registries
modules/*/routes/registry.py  →  include endpoint routers (prefix/tags)
```

Run: `uvicorn main:app` with cwd/package root `apps/backend/api`.

## Where it fits (HLD / LLD)

Process entry (`main`) vs domain registries vs endpoint files.

## Trade-offs

Central `core` registry is a small chokepoint (good for visibility). Alternatives: auto-discovery (harder to review).

## Production notes

Prefixes (`/sample`) belong on the module registry so paths stay stable when endpoints move files.

## Check your understanding

1. What file must change to expose a brand-new module’s routes?
2. Why not import `get_hello` directly from `main.py`?

## Code in this repo

`GET /sample/hello` is registered sample → core → main. `GET /health` sits on `main` as process-level soft health.

## Further practice (optional)

Add a second module and register it with one line in `core/router_registry.py`.
