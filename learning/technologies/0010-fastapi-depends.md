---
id: 0010
slug: fastapi-depends
title: FastAPI Depends (dependency injection) from zero
category: technologies
status: taught
taught_on: 2026-08-30
code_refs:
  - apps/backend/api/core/db/session.py
  - apps/backend/api/modules/sample_module/routes/endpoints/get_sample_items.py
  - apps/backend/api/modules/sample_module/tests/routes/endpoints/test_get_sample_items.py
related:
  - fastapi-router-composition
  - sqlalchemy-orm
  - domain-module-layering
  - type-checking-imports
adr_refs:
  - adr/0010-domain-module-call-path-facades-and-naming.md
---

# FastAPI Depends (dependency injection) from zero

## What

**Dependency injection (DI)** means: a function does not create every collaborator itself; a framework (or caller) **provides** them.

In FastAPI, **`Depends(...)`** marks a route (or other dependency) parameter as “resolve this for me.” The client does **not** send it in the URL/body. FastAPI calls your dependency function, then passes the result into the endpoint.

```python
db: Annotated[Session, Depends(get_db)]
```

Read it as:

| Piece | Meaning |
| --- | --- |
| `db` | Parameter name inside the endpoint |
| `Session` | Type of the value (typing / docs / IDE) |
| `Depends(get_db)` | **How** FastAPI obtains that value: call `get_db` |

Older equivalent: `db: Session = Depends(get_db)`. Prefer **`Annotated[..., Depends(...)]`** (current FastAPI style).

## Why

Without DI for the DB session:

- Every endpoint opens/closes sessions differently → leaks, forgotten `close()`, inconsistent rollback.
- Tests cannot swap a fake DB without rewriting the handler.
- Nested needs (auth user + db + settings) duplicate setup code.

`Depends` centralizes **setup + teardown**, keeps routes thin, and enables **`dependency_overrides`** in tests.

## How — mental model

```text
HTTP request
    │
    ▼
FastAPI matches route (e.g. GET /sample/items)
    │
    ▼
Build dependency graph for the endpoint parameters
    │
    ├─ path/query/body  ← from the HTTP message
    └─ Depends(...)     ← call Python callables (server-side)
            │
            ▼
        get_db() runs until yield  →  Session created
            │
            ▼
        get_sample_items(db=Session)
            │
            ▼
        response (or exception)
            │
            ▼
        resume get_db after yield
            ├─ on error: rollback + re-raise
            └─ finally: close()
```

**Order that matters:**

1. Dependency **setup** (code before `yield`)
2. Endpoint body
3. Dependency **teardown** (code after `yield`) — always for generators, even when the endpoint raises

If the endpoint raises, there is **no successful return**; teardown still runs, then FastAPI turns the error into an HTTP error response.

## End-to-end in this repo

### 1. Dependency: `get_db`

```python
# apps/backend/api/core/db/session.py
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
```

- **Before `yield`:** open a SQLAlchemy `Session` (unit of work for this request).
- **`yield db`:** pause; FastAPI injects this object as `db`.
- **After `yield`:** clean up. `except` rolls back a failed unit of work; `finally` always closes.

`finally` alone closes. `except` + `rollback` avoids leaving the connection in a bad transactional state after errors. We do **not** auto-`commit()` here — write use-cases commit explicitly when we add them.

### 2. Endpoint declares the dependency

```python
# modules/sample_module/routes/endpoints/get_sample_items.py
@router.get("/items", response_model=list[SampleItemResponse])
def get_sample_items(
    db: Annotated[Session, Depends(get_db)],
) -> list[SampleItemResponse]:
    items = SampleItemFacade.list_items(db)
    ...
```

Flow for one request:

```text
get_db → yield Session
  → SampleItemFacade.list_items(db)          # static facade
    → SampleItemsListService(db)
      → SampleItemRepository(db)
        → SQL SELECT
  → map rows to SampleItemResponse
→ get_db teardown (rollback if needed, close)
```

Per ADR-0010, the route depends on **infra** (`get_db`) and **public facades**, not on services/repositories directly.

### 3. What is *not* in the HTTP contract

`db` does not appear as a query param or JSON field. OpenAPI may show security/other deps specially; a plain `get_db` is internal wiring.

## Generator deps vs plain return deps

| Style | Example | Teardown |
| --- | --- | --- |
| **Return** | `def get_settings() -> Settings: return Settings()` | None — fire and forget |
| **Yield** | `get_db` above | Code after `yield` runs after the request work |

Use **yield** when you must release resources (DB sessions, file locks, connections).

## Extra things you should know

### Sub-dependencies (nesting)

A dependency can itself declare `Depends`:

```python
def get_current_user(db: Annotated[Session, Depends(get_db)]) -> User:
    ...

def get_sample_items(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
): ...
```

FastAPI builds a graph. **`get_db` is called once per request** even if two deps need it (request-scoped cache of dependency results).

### Sync vs async

- Sync `def get_db` / sync endpoint: fine for typical SQLAlchemy sync sessions (threadpool in ASGI).
- `async def` deps/endpoints: use when you await async I/O (async engine/session). Do not mix “async endpoint + blocking ORM” carelessly — it blocks the event loop.

This repo currently uses **sync** `Session` + sync routes.

### `dependency_overrides` (tests)

```python
app.dependency_overrides[get_db] = lambda: fake_session
# call TestClient...
app.dependency_overrides.clear()
```

Swap real DB for a fake without changing the route. Alternative used in our sample test: **patch the facade** so the route never hits the DB; that also works, but overriding `get_db` is the pure DI approach.

### Class-based dependencies

```python
class Pagination:
    def __init__(self, skip: int = 0, limit: int = 10):
        self.skip, self.limit = skip, limit

def list_x(p: Annotated[Pagination, Depends()]): ...
```

FastAPI treats callable classes as deps (`Depends()` with no args uses the type). Useful for shared query parsing.

### Security helpers are deps too

`OAuth2PasswordBearer`, API-key headers, etc. are built on the same `Depends` mechanism. Auth is “just” a dependency that may raise `HTTPException(401)`.

### App / router-level dependencies

```python
APIRouter(dependencies=[Depends(require_auth)])
```

Runs for every route on that router — good for “all payment routes need auth.”

### Lifespan vs `Depends`

- **`Depends`:** per-request (or per-call) collaborators.
- **Lifespan / startup:** process-wide resources (engine, connection pool). Our `engine` is created at import/startup; **`get_db` only creates a Session from the pool**, not a new engine per request.

### Common pitfalls

1. **`TYPE_CHECKING`-only `Session` on a FastAPI param** — with `from __future__ import annotations`, FastAPI must still resolve the type for injection. Prefer a **runtime** import of `Session` on endpoints that use `Annotated[Session, Depends(get_db)]` (as we do in `get_sample_items`).
2. **Calling `SessionLocal()` inside the route** — works for that line, but you lose automatic rollback/close, overrides, and shared request scope. Prefer `Depends(get_db)`.
3. **Forgetting `raise` after rollback** — always re-raise so FastAPI still returns 500/your handler error.
4. **Committing in `get_db` on success** — optional “unit of work” style; we keep commits in write services so reads stay side-effect free.
5. **Assuming order of sibling deps** — don’t rely on side effects between two independent deps; keep them pure given their inputs.

## Where it fits (HLD / LLD)

- **HLD:** HTTP adapter layer receives a request-scoped DB handle from the platform, then calls the module’s public facade.
- **LLD:** FastAPI DI graph + SQLAlchemy session lifecycle in `core/db`; domain code receives `db: Session` as a normal argument (facade → service → repository).

Related broader topic (planned): general **ports & adapters / DI** beyond FastAPI — same idea, different frameworks.

## Trade-offs

| Approach | Pros | Cons |
| --- | --- | --- |
| `Depends(get_db)` | Lifecycle, overrides, shared per request | Magic for newcomers; must learn generator teardown |
| Manual `SessionLocal()` in route | Obvious | Easy to leak; hard to test; duplicated |
| Context var / thread-local session | Hidden “current db” | Implicit; fights explicit DI; harder to reason about |

We choose **explicit `Depends` + pass `db` down** (ADR-0010 naming: parameter `db`).

## Production notes

- One session per request is the default safe story; do not store `db` on globals or long-lived objects.
- Pool exhaustion often shows up as hung requests — ensure `close()` always runs (`finally`).
- Log/monitor rollback paths on 5xx to spot failing units of work.
- Timeouts on DB statements still matter; DI does not replace them.

## Check your understanding

1. If `SampleItemFacade.list_items` raises, does the endpoint’s `return [...]` run? What runs in `get_db`?
    - No, the endpoint's `return [...]` does not run. The `get_db` teardown runs, including the `rollback` and `close` methods.
2. Why list both `Session` and `Depends(get_db)` in `Annotated`?
    - Because the `Session` type is the runtime type of the value, and the `Depends(get_db)` is the way to get the value.
3. Two dependencies both need `get_db` on one request — how many `SessionLocal()` calls?
    - One `SessionLocal()` call.
4. What is the difference between overriding `get_db` in tests vs patching `SampleItemFacade.list_items`?
    - Overriding `get_db` in tests is the pure DI approach, while patching `SampleItemFacade.list_items` is a test-specific approach.

## Code in this repo

- Dependency: `apps/backend/api/core/db/session.py` → `get_db`
- Export: `from core.db import get_db`
- Consumer: `modules/sample_module/routes/endpoints/get_sample_items.py` → `SampleItemFacade.list_items(db)`
- Test (facade patch style): `modules/sample_module/tests/routes/endpoints/test_get_sample_items.py`

## Further practice (optional)

1. Rewrite the route test to use `app.dependency_overrides[get_db]` with a fake session instead of patching the facade.
2. Add a nested dep `get_sample_item_facade`-style that only wraps nothing (static facade) — or a future auth dep that also `Depends(get_db)`.
