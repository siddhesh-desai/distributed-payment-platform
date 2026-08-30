# ADR-0006: Use PostgreSQL as primary store

- **Status:** Accepted
- **Date:** 2026-08-29
- **Deciders:** Siddhesh Desai

## Context

PayFlow Phase 1 needs a durable system of record for domain data (later: users, payments, ledger). The roadmap assumes PostgreSQL. Locally, a host Postgres already occupies port 5432, so any local PayFlow instance must not collide with it. Constitution requires money-path correctness (transactions, constraints, idempotency) that a shared SQL database supports well.

## Decision

1. Use **PostgreSQL** as the primary relational store for `apps/backend/api` (and later backend apps that need the same system of record).
2. Pin a **major version** in local infra (target **16**) and prefer the same major in shared/deployed environments when chosen later.
3. Application access is via a **DSN / settings from the environment** (12-factor config); no hardcoded production credentials in source.
4. Managed Postgres + backups/PITR for shared/deployed envs is **deferred**; local Docker Compose (ADR-0007) is the Phase 1 stand-in.

## Consequences

### Positive

- Strong transactional semantics, constraints, and tooling for payment/ledger learning.
- Clear mental model: one primary SQL store before Redis/Kafka.

### Negative / trade-offs

- Local ops depend on Docker (or equivalent) alongside any existing host Postgres.
- Connection limits and pooling must be respected as the API scales (app pool × replicas < `max_connections`).

### Follow-ups

- Accept ADR-0007 (Compose) and ADR-0008 (SQLAlchemy + Alembic) before implementing connectivity and schema.
- Later: managed provider, TLS, least-privilege roles, PgBouncer if connection pressure appears.

## Alternatives considered

### SQLite for local / early Phase 1

Rejected: weak fit for concurrency, locking, and production-parity learning for payments.

### Multiple primary databases per domain from day one

Rejected: premature; modular monolith shares one Postgres with per-module schema ownership (ADR-0004).
