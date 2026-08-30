# ADR-0007: Use Docker Compose for local development

- **Status:** Accepted
- **Date:** 2026-08-29
- **Deciders:** Siddhesh Desai

## Context

PayFlow needs a repeatable local stack: at least PostgreSQL (ADR-0006) and the product API (`apps/backend/api`). Developers may already run host Postgres on port 5432. Full production topology (orchestrators, managed DB, HA) is out of scope for day-to-day local development; Compose is the local stand-in. Later local deps (Redis, Kafka) should join the same Compose project rather than inventing a second runner.

## Decision

1. Use **Docker Compose** as the standard **local development** runtime for PayFlow dependencies and, for the default path, the **API process** as well.
2. Place Compose at repo root as **`docker-compose.yml`**, plus **`.env.example`** for local defaults. Add service Dockerfiles under the owning app (e.g. `apps/backend/api/Dockerfile`) — not a custom Postgres image unless extensions later require it.
3. **Phase 1 services** in Compose:
   - **`postgres`**: official `postgres:16`; host port **`5433`→`5432`**; named volume; `pg_isready` healthcheck; bootstrap only DB name/user/password via env. Business schema via migrations (ADR-0008).
   - **`api`**: build from `apps/backend/api` Dockerfile; depends on Postgres healthy; publish app HTTP port (e.g. **`8000`**); `DATABASE_URL` (or equivalent) uses the Compose **service hostname** `postgres` and port **`5432`** on the Compose network.
4. Grow the same Compose file later for Redis, Kafka, workers, etc., as those ADRs land.
5. **Optional escape hatch:** run the API on the host with `uv`/`nx` against Compose-only Postgres (`localhost:5433`) for faster iteration; Compose remains the documented default full stack.

## Consequences

### Positive

- One command brings up API + DB with correct DNS between containers.
- Isolated from host Postgres; port `5433` avoids the common conflict.
- Same entry point for future local infra services.

### Negative / trade-offs

- Requires Docker Desktop (or compatible engine).
- API-in-Docker reload/debug UX is slightly heavier than pure host `uvicorn`; mitigated by the host-run escape hatch.
- Compose is not production deployment; do not treat it as HA or a substitute for managed Postgres.

### Follow-ups

- Accept ADR-0006 and ADR-0008 before implementing the first slice end-to-end.
- Document migrate-then-serve (or an init/migrate step) for the `api` service without implying silent prod auto-migrate.

## Alternatives considered

### Compose for Postgres only; API always on the host

Rejected as the **default**: full-stack newcomers miss networking/DSN differences; host-run remains an allowed escape hatch, not the primary story.

### Reuse the developer’s host Postgres on 5432

Rejected: shared/unowned data; not reproducible for other machines/CI.

### Custom Postgres Dockerfile from day one

Rejected: unnecessary until nonstandard extensions or init beyond env bootstrap.

### `infra/docker-compose.yml` only (no root file)

Rejected for Phase 1: root `docker-compose.yml` is the usual local DX; revisit if infra sprawl justifies a subdirectory.

### Docker Compose as production deploy

Rejected: local/dev parity only; production deploy is a later decision (e.g. cloud/K8s).
