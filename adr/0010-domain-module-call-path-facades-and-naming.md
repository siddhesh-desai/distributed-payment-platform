# ADR-0010: Domain module call path, facades, and naming

- **Status:** Accepted
- **Date:** 2026-08-30
- **Deciders:** Siddhesh Desai
- **Amends:** [ADR-0004](0004-backend-api-domain-modules.md) (in-module call path, `public/` role, service DTO folders, naming)

## Context

ADR-0004 places domains under `modules/<name>/` and allows same-module `routes → services`, with `public/facets` mainly for cross-module callers. That splits entry points and encourages fat, multi-use-case service classes plus optional `services/inputs|outputs` DTO trees. We need one published surface for HTTP and other modules, use-case-sized services with direct parameters, and explicit file/symbol naming so agents and humans do not invent parallel conventions. This ADR renames that published surface from **facet** to **facade** (`public/facades/`).

## Decision

Adopt the following as the source of truth for **in-module request flow**, **`public/` usage**, **package exports**, and **naming** inside `apps/backend/api/modules/<name>/`. Where this conflicts with ADR-0004, **this ADR wins**.

### Call path (models → API)

```text
HTTP endpoint (routes/endpoints)
  → public facade method (public/facades)
  → use-case service (services)
    → repository(ies) (repositories)
      → ORM model (models)
        → PostgreSQL
```

Rules:

1. **Routes** depend only on **`public/`** (facades; and public inputs/outputs when those exist for cross-module or non-HTTP contracts). Routes **must not** import `services/`, `repositories/`, or `models/` (except purely for typing only if unavoidable—prefer public/return types and route response schemas).
2. **One facade** exposes **many methods**; each method delegates to **one use-case service** composed inside the facade (facade may hold many services).
3. **Use-case services** own business logic; they compose **repositories** from a `Session` (or later ports). They do **not** take repositories as constructor args from callers.
4. **Repositories** own persistence only; prefer shared `BaseRepository` helpers where applicable.
5. **Models** are table shapes only (no business logic)—unchanged from ADR-0004 / ADR-0009.
6. **Cross-module** callers use the same **`public/facades`** (and public I/O types)—no reaching into another module’s `services/` or `repositories/`.

### Folder roles (amended)

| Folder | Role |
| --- | --- |
| `models/` | ORM table shapes |
| `repositories/` | DB access; one primary entity repository per file |
| `services/` | **One use-case service class per file**; **no** `services/inputs/` or `services/outputs/` |
| `public/facades/` | Published API; one facade class per aggregate/capability file |
| `public/inputs/`, `public/outputs/` | Optional **cross-module** DTOs only (≠ route schemas ≠ models) |
| `routes/endpoints/` | One HTTP endpoint (or tightly coupled handler pair) per file |
| `routes/requests/`, `routes/responses/` | HTTP schemas only |
| `routes/registry.py` | Combine routers for `core` |
| `migrations/`, `clients/`, `tests/` | As ADR-0004 (tests mirror endpoints, services, repositories, clients, public facades) |

### Package exports (`__init__.py` / `__all__`)

1. Every package that exposes types (`models`, `repositories`, `services`, `public/facades`, `routes/responses`, …) **re-exports** public names in its `__init__.py` with **relative** imports and an explicit `__all__`.
2. Callers import from the **package**, not the leaf module file (`from modules.x.models import SampleItem`, not `...models.sample_item import SampleItem`). Same rule as `.cursor/rules/python-imports.mdc`.
3. Facade package is the routes’ dependency: e.g. `from modules.sample_module.public.facades import SampleItemFacade`.

### Naming — types

| Kind | Pattern | Example |
| --- | --- | --- |
| Model | `<Entity>` | `SampleItem` |
| Repository | `<Entity>Repository` | `SampleItemRepository` |
| Use-case service | `<Entity\|Resource><Action>Service` | `SampleItemsListService` |
| Facade | `<Entity\|Resource>Facade` | `SampleItemFacade` |
| Facade method | verb_phrase matching the use case | `list_items` → `SampleItemsListService` |
| HTTP response/request | `<Name>Response` / `<Name>Request` | `SampleItemResponse` |
| Endpoint Depends | `db` (or other infra) via FastAPI `Depends` | `get_db` — call facade static methods directly |


### Naming — files

| Kind | File name | Notes |
| --- | --- | --- |
| Model | `sample_item.py` | snake_case of type |
| Repository | `sample_item_repository.py` | |
| Use-case service | `sample_items_list_service.py` | matches type; action in the name |
| Facade | `sample_item_facade.py` | |
| Endpoint | `get_sample_items.py` | `<http_verb>_<resource>.py` |
| Route response | `sample_item_response.py` | |
| Migration | `0001_create_sample_items.py` | ordered prefix (existing Alembic convention) |
| Test | `tests/<layer>/…/test_<stem>.py` | mirror source stem |

### Service & facade shape

- Service `__init__(self, db: Session)` (or explicit ports later); compose repos as attributes.
- Service methods use **direct parameters and return annotations**—no mandatory input/output DTO classes under `services/`.
- Facade methods are **`@staticmethod`**; pass `db` (and other args) into each method that needs them. Construct the use-case service inside the method — **do not** require instantiating the facade.
- Endpoints map facade results → `routes/responses` schemas.

### Example (normative)

```text
SampleItem (model)
  ← SampleItemRepository
    ← SampleItemsListService.list_items()
      ← SampleItemFacade.list_items(db)
        ← GET routes/endpoints/get_sample_items.py
```

## Consequences

### Positive

- Single entry surface for HTTP and other modules.
- Use-case services stay small; facades group related operations without becoming god services.
- Naming/file rules are agent-enforceable; `__all__` defines the public surface.

### Negative / trade-offs

- Extra hop (endpoint → facade → service) for every call.
- ADR-0004’s “routes may construct services” and `services/inputs|outputs` are retired—existing sample module must be migrated after acceptance.
- Dense convention surface; violations need lint/review discipline (import-linter later).

### Follow-ups

- Done for `sample_module` (facades + `SampleItemsListService`); keep ADR-0004 status note pointing at this amend.
## Alternatives considered

### Routes keep calling services; facades only cross-module

Rejected: two entry styles; HTTP still coupled to internal service types.

### One facade ↔ one service

Rejected: forces either god services or facade explosion; owner prefers one facade, many use-case services.

### Keep `services/inputs` and `services/outputs`

Rejected for use-case services: prefer direct parameters; public I/O remains available for cross-module contracts only.
