# ADR-0004: Backend API domain modules layout

- **Status:** Accepted
- **Date:** 2026-08-12
- **Deciders:** Siddhesh Desai

## Context

ADR-0003 defines `apps/` + `libs/` by stack but not how a single product HTTP API hosts multiple business domains, when to add `libs/backend` packages, Spec `001-backend-module-layout` requires one product API process with in-app domain modules. Sibling/ops apps are deferred.

## Decision

1. Place the product HTTP API at **`apps/backend/api`** as a **flat** project root (`main.py`, `core/`, `modules/`—no `src/` wrapper); it is the only product API process in Phase 1.
2. Place business domains as **modules inside that app** (`modules/<name>/`) with layers **routes → services → models → repositories → migrations → clients → public → tests** (see Folder structure). **`models/`** = table/persistence **data shapes only (no business logic)**. **`services/`** = **all business logic** and orchestration, implemented as **classes**. Under **`routes/`**: `inputs/`, `outputs/`, `endpoints/` (one file each), plus root **`registry.py`** to combine routers for `core`—API schemas are **not** the same types as `models/`. Same-module services collaborate via **constructor injection**. Cross-module calls go only through **`public/`** (`inputs/`, `outputs/`, `facets/` — one file each) or `core` orchestration. This specializes constitution Principle I’s “rich domain objects” for Phase 1: behavior lives in service classes rather than on model types.
3. Register domain HTTP routers at one **`core`** wiring point.
4. Add **`libs/backend` packages only** for external-service clients reused in multiple places; otherwise keep `libs/backend` reserved (e.g. `.gitkeep`).
5. **Defer** scaffolding sibling/ops apps (e.g. observability); when added later they belong under `apps/` per ADR-0003, not inside API domain modules.
6. Keep **schema migrations per module** under `modules/<name>/migrations/`; an app-level runner may discover them. Do not use one shared migrations folder as the ownership model for all domains.
7. Keep **tests per module** under `modules/<name>/tests/`, mirroring testable layers (endpoints, services, repositories, clients, public facets). Do not require dedicated tests for models, migrations, or input/output schema files. Thin `api/tests/` only for core wiring.
8. Treat **this ADR** (plus the feature spec’s Domain Design Rules) as the source of truth for create-vs-extend, inter-domain communication, layering, and paths—**no separate `docs/backend-layout.md`**.

## Folder structure

```text
apps/backend/api/                         # flat project root (uv + Nx)
  pyproject.toml
  project.json
  main.py
  core/
    router_registry.py                    # mount domain route registries
  modules/
    <name>/                               # e.g. sample_module
      routes/
        registry.py
        inputs/                           # one input Pydantic per file
        outputs/                          # one output Pydantic per file
        endpoints/                        # one endpoint per file
      services/                           # one service class per file; same-module DI
      models/                             # table shapes only (no business logic)
      repositories/                       # DB access only
      migrations/                         # this module’s schema only
      clients/                            # external systems (not DB)
      public/
        inputs/                           # public I/O (≠ route schemas ≠ models)
        outputs/
        facets/                           # one cross-module facet per file
      tests/                              # this module only
        routes/endpoints/
        services/
        repositories/
        clients/
        public/facets/
        # no dedicated tests for models/, migrations/, or */inputs|outputs
  tests/                                  # core/app wiring only
libs/backend/                             # .gitkeep until multi-place external client
```

Empty reserved folders use `.gitkeep`. Sibling/ops apps under `apps/backend/` are deferred.

## Consequences

### Positive

- Clear home for domains vs shared external clients (`libs/backend` when justified).
- Extractability and reviewability without multiple product API servers.
- uv/Nx membership stays intentional (API package; empty libs until needed).

### Negative / trade-offs

- Modular monolith discipline required (facades/`core` wiring) or boundaries erode.
- Five folder layers can feel heavy for tiny modules; mitigated with `.gitkeep` and thin layers. `repositories/` = DB only; `clients/` = external systems—not a single adapters bucket.
- Anemic models push complexity into services; watch for god-service classes and revisit rich models later if needed.

### Follow-ups

- Scaffolding paths under `apps/backend/api` may now be treated as final per this ADR.
- Later: import-linter (or equivalent) for cross-domain internals; real domains; optional code-bearing workers.

## Alternatives considered

### Domain-per-uv-package under `libs/backend`

Rejected for Phase 1: premature sprawl; contradicted clarification Option B.

### Multiple product HTTP API apps

Rejected: feature requires a single product API process.

### Scaffold Grafana/sibling app in this change

Rejected for now: out of scope; revisit when observability work starts.

### `src/<package>/` nested layout

Rejected for Phase 1: extra nesting without enough payoff for learning navigability; flat `apps/backend/api` preferred.

### Single `adapters/` (or `infrastructure/`) folder

Rejected: mixes DB repositories with external clients; split into `repositories/` and `clients/`.

### Rich behavior on `models/` (DDD-style domain objects)

Rejected for Phase 1 per product owner: models decide tables/shapes only; business logic stays in service classes.

### Single `public.py` facade file

Rejected: use `public/` with `inputs/`, `outputs/`, `facets/`.

### Single app-level `migrations/` ownership for all domains

Rejected: each module owns its `migrations/`; runner may be app-level.
