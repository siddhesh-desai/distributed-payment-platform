# ADR-0002: Use uv workspaces and Nx as orchestrator

- **Status:** Accepted
- **Date:** 2026-08-12
- **Deciders:** Siddhesh Desai

## Context

PayFlow is a greenfield monorepo: Python microservices and shared libs first; frontend and CLI later. We need (1) consistent Python dependency resolution across packages and (2) a way to run lint/test/build across many projects without hand-rolled scripts forever.

## Decision

- Use **uv workspaces** as the Python package/dependency layer (shared lockfile, local path deps).
- Use **Nx** as the task orchestrator (project graph, named targets, caching; later frontend/CLI).
- Keep Python deps owned by uv; Nx targets shell into `uv run` / `uv sync`. Do not use Poetry-centric Nx Python plugins as the source of truth.

## Consequences

### Positive

- One Python version contract (`uv.lock`) across services/libs without installing every package on every deploy.
- Orchestration ready before the JS surface exists; same `nx test` / `nx run-many` story later for web/CLI.
- Clear separation: uv = install/link; Nx = run/cache.

### Negative / trade-offs

- Two tools to learn; Nx needs manual `project.json` (and deps) for Python until plugins mature.
- Root Node install for Nx even while the product is Python-first.
- Workspace-wide resolves can force version alignment across services (usually desirable; occasional overrides needed).

### Follow-ups

- Add frontend under `apps/` with pnpm or Nx JS plugins when that work starts.
- Revisit Pants (or heavier Nx CI features) only if affected-only / remote-cache pain is measured.

## Alternatives considered

### uv only (no orchestrator)

Rejected for now: fine for a single service, but we already plan many services plus frontend/CLI; Nx from day one avoids a later glue rewrite.

### Nx-first with @nxlv/python (Poetry)

Rejected: Python-first repo; uv is the chosen package manager. Orchestrator must call uv, not replace it.

### Pants or Bazel

Rejected for greenfield learning scale: high build-system tax before domain complexity justifies it.

### Turborepo

Rejected: JS/TS-oriented; weak fit as primary orchestrator for Python services.
