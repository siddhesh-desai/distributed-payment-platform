---
id: 0002
slug: orm-model-auto-discovery
title: Auto-discover domain ORM modules for Alembic metadata
category: techniques
status: taught
taught_on: 2026-08-30
code_refs:
  - apps/backend/api/core/alembic/import_module_models.py
  - apps/backend/api/core/alembic/env.py
related:
  - alembic-migrations
  - sqlalchemy-orm
  - domain-module-layering
adr_refs:
  - adr/0004-backend-api-domain-modules.md
---

# Auto-discover domain ORM modules for Alembic metadata

## What

**Model auto-discovery** walks `modules/<name>/models/**/*.py`, imports each module, and relies on declarative class definition to register tables on shared `OrmBaseModel.metadata` — so Alembic autogenerate sees every domain table without a hand-maintained import list in `env.py`.

## Why

Explicit `from modules.…models… import Model` in `env.py` grows with every table and is easy to forget. Missing imports → empty/partial metadata → autogenerate misses tables or proposes wrong drops.

## How

```text
modules/<domain>/models/*.py
        │
        ▼
import_module_models()   # importlib per dotted path
        │
        ▼
OrmBaseModel.metadata    # tables registered as classes load
        │
        ▼
alembic env target_metadata / autogenerate
```

Convention: put ORM modules under `models/` (skip `_*.py`). New domains get discovery for free once files land there.

## Where it fits (HLD / LLD)

App-level migration runner (`core/alembic`) + domain-owned models (ADR-0004). Discovery is infrastructure, not domain logic.

## Trade-offs

| Approach | Pros | Cons |
| -------- | ---- | ---- |
| Auto-discover (chosen) | No env.py churn per model | Import errors / side effects if a models file is heavy or misnamed |
| Explicit barrel | Clear, greppable | Easy to forget a model |
| Hand migrations only | No metadata load needed | Weaker autogenerate |

## Production notes

Keep `models/` packages side-effect light (table defs only). Fail loud if an import raises — better than silent incomplete metadata. Review autogenerate diffs; discovery does not replace migration review.

## Check your understanding

1. Why does importing the file matter more than listing table names in Alembic config?
2. What happens if a new model lives outside `modules/*/models/`?
3. Why skip `_*.py`?

## Code in this repo

`discover_model_module_names` + `import_module_models` in `core/alembic/import_module_models.py`; `env.py` calls `import_module_models()` before `target_metadata = OrmBaseModel.metadata`.

Unit coverage for this helper is not kept under `api/tests/` (ADR-0004: module tests only). Validate discovery manually or via migration/autogenerate workflows when changing it.

## Further practice (optional)

Add a second dummy model under a new module’s `models/` and confirm it appears in `OrmBaseModel.metadata.tables` after `import_module_models()`.
