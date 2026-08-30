---
id: 0011
slug: sqlalchemy-sync-vs-async
title: SQLAlchemy sync vs async DB access
category: technologies
status: taught
taught_on: 2026-08-30
code_refs:
  - apps/backend/api/core/db/engine.py
  - apps/backend/api/core/db/session.py
  - apps/backend/api/pyproject.toml
  - apps/backend/api/modules/sample_module/routes/endpoints/get_sample_items.py
related:
  - sqlalchemy-orm
  - fastapi-depends
  - postgresql-primary-store
adr_refs:
  - adr/0008-use-sqlalchemy-and-alembic.md
---

# SQLAlchemy sync vs async DB access

## What we use now (PayFlow API)

**Fully synchronous** database access:

| Piece | Choice |
| --- | --- |
| Engine | `sqlalchemy.create_engine` → sync `Engine` |
| Session | `sessionmaker` → sync `Session` |
| Driver | **`psycopg`** (v3, sync) — not `asyncpg` |
| FastAPI routes | `def` (sync), not `async def` |
| DI | `get_db` yields a sync `Session` |

There is **no** `create_async_engine`, `AsyncSession`, or `asyncpg` in this app today.

## What “sync” vs “async” means for the DB

### Sync (what we have)

```text
request thread/worker
  → run endpoint
  → db.execute / session.scalars(...)
  → Python waits (blocks) until Postgres answers
  → continue
```

The calling thread is **occupied** for the whole round-trip to Postgres (network + query time).

### Async (alternative stack)

```text
event-loop worker
  → await session.execute(...)
  → release the loop while waiting on the socket
  → other coroutines can run
  → resume when Postgres responds
```

You need the **async** SQLAlchemy API plus an **async driver** (for Postgres usually `asyncpg`, or `psycopg` in async mode).

Rough pairing:

| Mode | Engine API | Session | Typical Postgres driver |
| --- | --- | --- | --- |
| Sync | `create_engine` | `Session` | `psycopg` / `psycopg2` |
| Async | `create_async_engine` | `AsyncSession` | `asyncpg` or async `psycopg` |

DSN shapes differ (`postgresql+psycopg://…` vs `postgresql+asyncpg://…`).

## How FastAPI fits (important)

FastAPI / Starlette run on an **async event loop** (uvicorn).

- **`async def` endpoint:** runs on the event loop. If you call **blocking** sync SQLAlchemy here, you **block the loop** → other requests on that worker stall. Bad mix.
- **`def` endpoint (sync):** FastAPI runs it in a **threadpool**. Blocking DB I/O is OK; the loop keeps accepting other work on other threads/workers.

So our combo is coherent:

```text
sync def route  +  sync Session  +  psycopg
```

The “better” async story is also coherent only as a set:

```text
async def route  +  AsyncSession  +  asyncpg (or async psycopg)
```

**Half-migrating** (async route + sync Session) is a common production footgun.

## Why we chose sync (for now)

1. **Learning clarity** — one mental model: call → wait → result. No `await`, greenlet nuances, or dual session types.
2. **Stack simplicity** — Alembic, most SQLAlchemy tutorials, and our repositories use sync `Session` naturally.
3. **Workload fit (Phase 1)** — modular monolith, modest concurrency; sync + threadpool + connection pool is enough to learn payments domain mechanics.
4. **Fewer moving parts** — no async session lifecycle rules (`await db.commit()`, `run_sync` for legacy sync ORM bits, etc.).

This is a **pragmatic Phase 1 choice**, not a claim that sync is always superior.

## What is “better”?

There is no universal winner. Optimize for **constraint**:

### Sync is often better when

- Team / codebase is sync-first (us today).
- Concurrency is moderate; vertical scale / more uvicorn workers is acceptable.
- Most time is **CPU or business logic**, not thousands of concurrent idle-on-DB waits.
- You want simpler debugging and one Session API.

### Async is often better when

- **Very high concurrency** of I/O-bound requests (many open connections waiting on DB/HTTP).
- You already standardize on `async def` everywhere (HTTP clients, queues, websockets).
- You want fewer OS threads per concurrent wait (memory / context-switch pressure).

### Async is *not* automatically faster

- A single query’s latency to Postgres is similar.
- Async shines at **overlapping many waits** on one process.
- Misused async (blocking calls in `async def`) is **worse** than honest sync `def`.
- Extra complexity: cancellations, task lifetimes, testing async, library support.

## End-to-end pictures

### Ours (sync)

```text
uvicorn (event loop)
  → schedules sync endpoint on threadpool
  → get_db: SessionLocal()  (checkout from sync pool)
  → Facade → Service → Repository → session.scalars(...)
  → psycopg talks to Postgres (thread blocked until done)
  → response
  → get_db finally: close (return conn to pool)
```

### Async alternative (not in repo)

```text
uvicorn (event loop)
  → async endpoint on the loop
  → async get_db: AsyncSession
  → await session.execute(...)
  → asyncpg waits without blocking the loop
  → await commit/rollback; aclose session
```

## Production notes

- **Pool size × workers × threads** matters more than sync/async slogans. Exhausted pools → timeouts regardless of API style.
- Prefer **one style end-to-end** in a service. Dual stacks double cognitive load.
- If you adopt async later: migrate engine, session, driver, routes, and tests together; consider an ADR.
- Alembic migrations stay sync in almost all setups even if the app runtime is async.

## Check your understanding

1. Why is `async def` + sync `session.query(...)` dangerous?
    - Because the `await` will block the event loop, and the `session.query(...)` will block the thread.
2. Does async make a single `SELECT` return faster? Why / why not?
    - No, a single `SELECT` return is similar in latency.
3. What three pieces must change together to go async in this API?
    - The engine, the session, and the driver.
4. Where does a sync FastAPI route actually run while waiting on Postgres?
    - In the threadpool.

## Code in this repo

- Sync engine: `core/db/engine.py` (`create_engine`)
- Sync session + `get_db`: `core/db/session.py`
- Driver dep: `psycopg[binary]` in `apps/backend/api/pyproject.toml`
- Sync route: `get_sample_items` (`def`, not `async def`)

## Further practice (optional)

Sketch (do not implement unless ADR’d) an `async` `get_db` signature and list every file that would need to change for a real cutover.
