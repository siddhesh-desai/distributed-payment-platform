# ADR-0003: Monorepo directory layout (apps + libs by stack)

- **Status:** Accepted
- **Date:** 2026-08-12
- **Deciders:** Siddhesh Desai

## Context

PayFlow needs a monorepo layout that scales to many backend services, frontend apps, and shared libraries without mixing stacks at the top level.

## Decision

Use this root layout:

```text
apps/
  backend/          # deployable backend services (one folder per service)
  frontend/         # deployable frontend apps (one folder per app)
libs/
  backend/          # shared backend packages (one folder per package)
  frontend/         # shared frontend packages (one folder per package)
```

uv workspace members and Nx project paths follow this tree. Tooling choice (uv + Nx) remains ADR-0002.

## Consequences

### Positive

- Clear stack split (`backend` vs `frontend`) under both apps and libs.
- One folder per deployable / package; easy to add services without renaming roots.
- Matches how polyglot monorepos usually grow.

### Negative / trade-offs

- Deeper paths than a flat `apps/` + `libs/` (no stack subfolders).

### Follow-ups

- Place future CLI under the appropriate `apps/` stack folder when that work starts (not decided here beyond “lives under `apps/`”).

## Alternatives considered

### Flat `services/` + `packages/` roots

Rejected: does not mirror the planned frontend surface; two naming schemes later.

### `apps/<name>` with language tags only

Rejected: backend vs frontend grouping is the primary navigation axis requested.
