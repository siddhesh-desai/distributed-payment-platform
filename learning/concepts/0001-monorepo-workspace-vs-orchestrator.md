---
id: 0001
slug: monorepo-workspace-vs-orchestrator
title: Monorepo workspace vs orchestrator
category: concepts
status: taught
taught_on: 2026-08-12
code_refs:
  - pyproject.toml
  - nx.json
  - apps/
  - libs/
related:
  - uv-workspaces
  - nx-orchestrator
adr_refs:
  - adr/0002-use-uv-workspaces-and-nx-orchestrator.md
  - adr/0003-monorepo-directory-layout-apps-libs.md
---

# Monorepo workspace vs orchestrator

## What

A **monorepo** holds many deployables and libraries in one git repo. Two layers are easy to confuse:

- **Workspace / package manager** — resolves and links dependencies (versions, local packages).
- **Orchestrator** — runs tasks across projects (`test`, `lint`, `build`) with a project graph and optional caching.

## Why

Without a workspace, sibling services pin conflicting versions of the same library and shared code is awkward to link. Without an orchestrator, every service reinvents scripts and CI matrices as the repo grows.

## How

```text
uv.lock / workspace members     →  "which versions / what can import what"
Nx project.json targets         →  "how we run test/lint for each project"
Deploy image for one service    →  only that service’s dependency tree
```

A shared lockfile is a **version contract**, not “install every package on every server.”

## Where it fits (HLD / LLD)

**HLD:** repo topology (`apps/{backend,frontend}/`, `libs/{backend,frontend}/`). **LLD:** per-project `pyproject.toml` + `project.json` targets.

## Trade-offs

Two tools (uv + Nx) vs one heavy build system (Pants/Bazel). More concepts early; less ceremony than Bazel for a learning greenfield.

## Production notes

CI should sync the workspace with the right groups (`--all-packages --group dev` for test), then `nx run-many` / affected. Production images should install **one** package’s tree (`uv sync --package <svc>`), not the whole monorepo’s dev tools.

## Check your understanding

1. Can two services share one lockfile but ship different installed packages? How?
   - Yes, if the services are in the same workspace and the packages are different.
2. What breaks if `payments` and `ledger` pin different `httpx` versions with no workspace resolve?
   - The services will pin conflicting versions of httpx, which will break the build.
3. Why might `uv sync --package payments` remove pytest from a local `.venv`?
   - Because the `payments` service may have a different version of pytest than the root workspace, and `uv sync --package payments` will install the version of pytest that is specified in the `payments` service's `pyproject.toml` file.

## Code in this repo

- Layout: `apps/{backend,frontend}/`, `libs/{backend,frontend}/` (ADR-0003); members TBD
- Workspace root: `pyproject.toml` (uv); orchestrator: `nx.json` + per-project `project.json` when apps exist

## Further practice (optional)

When the first backend service and shared lib land, wire `{ workspace = true }` and `nx test <name>`.
