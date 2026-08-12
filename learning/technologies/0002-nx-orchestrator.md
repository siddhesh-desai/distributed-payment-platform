---
id: 0002
slug: nx-orchestrator
title: Nx as monorepo task orchestrator
category: technologies
status: taught
taught_on: 2026-08-12
code_refs:
  - nx.json
  - package.json
related:
  - monorepo-workspace-vs-orchestrator
  - uv-workspaces
adr_refs:
  - adr/0002-use-uv-workspaces-and-nx-orchestrator.md
  - adr/0003-monorepo-directory-layout-apps-libs.md
---

# Nx as monorepo task orchestrator

## What

**Nx** is a task runner and monorepo toolkit: project graph, named targets, caching, and (later) generators/plugins for JS apps. Here it **orchestrates**; it does **not** own Python dependency resolution.

## Why

As services multiply, you want `nx test payments`, `nx run-many -t lint`, and eventually affected-only CI — without a bespoke Makefile per service.

## How

Each Python project has a `project.json` with targets that shell into uv:

```text
nx test payments  →  uv run --package payments pytest …
```

`implicitDependencies` links `payments` → `payflow-common` so the graph knows about the workspace edge (Python imports are not auto-inferred by Nx core).

## Where it fits (HLD / LLD)

**Repo/DevEx layer.** Runtime payment flows do not call Nx; CI and local DX do.

## Trade-offs

Root Node install even while product code is Python-first. Manual `project.json` for Python until/unless plugins improve. Avoid Poetry-centric Nx Python plugins while uv is source of truth.

## Production notes

Cache `test`/`lint` via `nx.json` `targetDefaults`. Prefer `NX_DAEMON=false` only when diagnosing graph issues. Frontend can join the same Nx graph under `apps/` later.

## Check your understanding

1. Why can `nx test` succeed while `uv sync --package payments` alone would drop pytest?
   - Because `nx test` will run the test target for the `payments` project, which will include the dependencies for the `payments` project.
2. What is the difference between Nx caching a target and uv locking dependencies?
   - Nx caching a target will cache the result of the target, so that if the target is run again, the result will be returned from the cache instead of being re-run. uv locking dependencies will lock the dependencies for the workspace, so that if the dependencies are changed, the workspace will be updated to the new dependencies.
3. Why set `implicitDependencies: ["payflow-common"]` on `payments`?
   - Because the `payments` project depends on the `payflow-common` package, and the `payflow-common` package is a member of the workspace, so the `payments` project should be implicitly dependent on the `payflow-common` package.

## Code in this repo

- Workspace config: `nx.json`, root `package.json`
- No Nx projects yet — add `project.json` under each app/lib when those are decided

## Further practice (optional)

After the first service + shared lib exist, run `nx graph` and confirm `implicitDependencies`.
