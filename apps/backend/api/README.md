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

## Run / test

```bash
# from repo root
uv sync
uv run --directory apps/backend/api uvicorn main:app --reload --port 8000
# or: nx serve api

nx test api
nx lint api
```

## SC-010 decision drill (layout rules)

Using only ADR-0004:

1. “Add refund status field on payment” → **extend** the payment-like domain (same bounded context).
2. “Add ledger posting for settled payments” → **new** ledger domain (different capability; `public/` when payments need to call it).
3. “Add hello-world style ping in sample” → **extend** `sample_module`.

**Result**: pass (3/3 matches expected).
