# ADR-0009: Shared `libs/backend/payflow_common` ORM base (uv workspace libs)

- **Status:** Accepted
- **Date:** 2026-08-29
- **Deciders:** Siddhesh Desai

## Context

ADR-0004 §4 restricts `libs/backend` to **external-service clients** reused in multiple places. We want a shared SQLAlchemy declarative base plus reusable column mixins so every domain model inherits the same conventions, under import path `payflow_common.models.*`. That is cross-cutting persistence infrastructure, not an HTTP client — so §4 must be extended. New backend libs should be created with the workspace’s standard Python tool (**`uv init`**), not a hand-rolled scaffold.

## Decision

1. **Amend ADR-0004 §4:** `libs/backend` may hold (a) multi-place **external clients**, and (b) small **shared backend infrastructure** packages that multiple backend apps/modules must import unchanged (ORM base/mixins, shared helpers). Domain business logic stays in `apps/…/modules/`, not in libs.
2. Add uv workspace package **`libs/backend/payflow_common`** (folder name = import name **`payflow_common`**; dist **`payflow-common`**) with models under **`payflow_common.models`**:
   - **`OrmBaseModel`** — SQLAlchemy 2 `DeclarativeBase` subclass (single metadata registry).
   - Mixins named **`*ModelMixin`** (e.g. **`IdModelMixin`**, later `AuditModelMixin`) under `payflow_common.models.mixins`.
3. Domain models inherit mixins + base, e.g. `class SampleItem(IdModelMixin, OrmBaseModel): …`. App `core/db/` keeps **engine/session** only; it does **not** own the declarative base.
4. **Naming:** do **not** use bare `BaseModel` (Pydantic clash). Use **`OrmBaseModel`** for the declarative class and **`XxxModelMixin`** for mixins.
5. **Scaffold new backend libs with `uv init --lib`**, then flatten so layout is `libs/backend/<snake_name>/<snake_name>/` (no `src/`; folder == import package). Optional wrapper: `tools/scripts/init-backend-lib.sh` / `npm run g:backend-lib`. **Do not** maintain a custom Nx file-template generator.

## Consequences

### Positive

- One place for shared ORM columns/behavior; consistent naming (`OrmBaseModel` / `*ModelMixin`).
- Lib creation uses the same tool as the rest of the Python monorepo (`uv`).
- Aligns with ADR-0003 `libs/backend`; ready for workers later.

### Negative / trade-offs

- Extra workspace member + path dep for the API.
- Over-sharing risk if domain fields creep into `payflow_common` — keep mixins cross-cutting only.
- Flattening uv’s default `src/` layout is intentional so folder name == import name with no extra layer.
- Amends ADR-0004 libs policy (note “see ADR-0009” on §4).

### Follow-ups

- `libs/backend/payflow_common` + `SampleItem` on `OrmBaseModel` / `IdModelMixin` (done).
- Add `AuditModelMixin` only when a real domain needs timestamps.

## Alternatives considered

### Keep declarative base in `apps/backend/api/core/db/`

Rejected as long-term home: reusable lib requested; second process would duplicate.

### Name the class `BaseModel` or `OrmBase`

`BaseModel` rejected (Pydantic clash). `OrmBase` superseded by requested **`OrmBaseModel`** for consistency with `*ModelMixin`.

### Custom Nx generator with file templates

Rejected (revised): prefer **`uv init --lib`** as the source of truth; avoid a second scaffolding stack to maintain.

### Speculative full mixin suite on day one

Rejected: add `IdModelMixin` when useful; other mixins when first needed.
