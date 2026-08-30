# PayFlow API (`apps/backend/api`)

Single **product HTTP API** process for PayFlow (modular monolith). Domain code lives under `modules/<name>/`; process composition lives under `core/`.

## Layout (SoT)

Authoritative rules: [`adr/0004-backend-api-domain-modules.md`](../../../adr/0004-backend-api-domain-modules.md) (Accepted).

| Question                         | Answer                                                                          |
| -------------------------------- | ------------------------------------------------------------------------------- |
| Where is the product API?        | This package only — `apps/backend/api/` (flat; no `src/`)                       |
| Where does a domain go?          | `modules/<name>/` with ADR-0004 layers                                          |
| How are HTTP routes composed?    | Only via `core/router_registry.py` including each module’s `routes/registry.py` |
| Sibling/ops apps (e.g. Grafana)? | Deferred — not under `apps/backend/` for this feature                           |

## Deferred (scaffold)

Ops/auth/error envelope (structured JSON logs, metrics, readiness, uniform error bodies, AuthN/Z) are deferred until the first real domain lands. Soft `GET /health` is process-level only.

## Local stack (Docker Compose)

From repo root (Postgres on host **5433** so a Mac Postgres on 5432 is untouched):

```bash
cp -n .env.example .env
# Edit .env: set POSTGRES_PASSWORD to a local-only value (required; never commit .env).
docker compose up --build
```

- API: http://localhost:8000  
- Sample DB read: `GET /sample/items`  
- Health: `GET /health` (liveness only; DB readiness / structured logs / metrics deferred)

Compose runs migrations (`alembic -c core/alembic/alembic.ini upgrade heads`) then uvicorn. See ADRs 0006–0008.

## Host-run API (escape hatch)

```bash
# from repo root — Postgres via Compose only
cp -n .env.example .env   # then set POSTGRES_PASSWORD in .env
docker compose up postgres -d
uv sync
# Host API talks to localhost:5433 — set POSTGRES_HOST=localhost POSTGRES_PORT=5433 in .env (or export).
nx run api:migrate
uv run --directory apps/backend/api uvicorn main:app --reload --port 8000
# or: nx serve api
```

## Test / lint / migrations

```bash
nx test api
nx lint api
# Write revision files (autogenerate against live DB) — review before apply.
# Use zero-padded --rev-id so files sort as 0001_*, 0002_*, …:
nx run api:makemigrations -- --rev-id 0002 -m "describe change"
# Apply pending revisions to the database:
nx run api:migrate
```

## SC-010 decision drill (layout rules)

Using only ADR-0004:

1. “Add refund status field on payment” → **extend** the payment-like domain (same bounded context).
2. “Add ledger posting for settled payments” → **new** ledger domain (different capability; `public/` when payments need to call it).
3. “Add hello-world style ping in sample” → **extend** `sample_module`.

**Result**: pass (3/3 matches expected).
