---
id: 0001
slug: uv-workspaces
title: uv workspaces for Python packages
category: technologies
status: taught
taught_on: 2026-08-12
code_refs:
  - pyproject.toml
  - uv.lock
  - apps/backend/
  - libs/backend/
related:
  - monorepo-workspace-vs-orchestrator
  - nx-orchestrator
adr_refs:
  - adr/0002-use-uv-workspaces-and-nx-orchestrator.md
  - adr/0003-monorepo-directory-layout-apps-libs.md
---

# uv workspaces for Python packages

## What

**uv** is a fast Python package manager. A **uv workspace** declares multiple member projects under one root; they share a single **`uv.lock`** resolve and can depend on each other with `{ workspace = true }`.

## Why

Microservices need shared libraries without publishing to PyPI on every change, and without each service drifting to incompatible third-party versions.

## How

1. Root `pyproject.toml` lists `[tool.uv.workspace] members`.
2. Each member has its own `[project]` metadata and deps.
3. `uv lock` / `uv sync` resolve the whole graph once.
4. `uv sync --package payments` installs **that** package’s tree (deploy-shaped).
5. `uv sync --all-packages --group dev` installs members + root dev tools (local/CI).

## Where it fits (HLD / LLD)

Owns the **Python dependency boundary** for all backend libs/services. Does not replace service boundaries or runtime messaging.

## Trade-offs

Workspace resolve forces version alignment (good for consistency; occasional overrides needed). uv does not provide affected-only test selection — that’s Nx/Pants territory.

## Production notes

Commit `uv.lock`. Build images with package-scoped sync so pytest/ruff from the root `dev` group do not ship. Prefer `requires-python` pinned at the workspace floor (here `>=3.12`).

## Check your understanding

1. What does `[tool.uv.sources] payflow-common = { workspace = true }` do?
   - It tells uv that the `payflow-common` package is a member of the workspace and should be included in the workspace resolve.
2. Why keep the workspace root `[tool.uv] package = false`?
   - Because the workspace root is not an installable package, it should not be included in the workspace resolve.
3. When would you use `--package` vs `--all-packages`?
   - You would use `--package` to install the dependencies for a specific package in the workspace. You would use `--all-packages` to install the dependencies for all packages in the workspace.

## Code in this repo

- Root workspace: `pyproject.toml` (`members = []` until backend apps/libs are decided)
- Paths reserved: `apps/backend/*`, `libs/backend/*`

## Further practice (optional)

After the first members land, compare `uv sync --package <svc> --dry-run` with `uv sync --all-packages --group dev`.
