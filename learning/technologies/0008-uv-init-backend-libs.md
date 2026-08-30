---
id: 0008
slug: uv-init-backend-libs
title: Scaffold backend libs with uv init (flat snake_case)
category: technologies
status: taught
taught_on: 2026-08-29
code_refs:
  - tools/scripts/init-backend-lib.sh
  - libs/backend/payflow_common/
related:
  - uv-workspaces
  - nx-orchestrator
adr_refs:
  - adr/0009-libs-backend-common-orm-base.md
---

# Scaffold backend libs with `uv init` (flat snake_case)

## What

New backend libs live at **`libs/backend/<snake_name>/`** where **`<snake_name>` == the Python import package**. No `src/` directory.

```text
libs/backend/payflow_common/
  pyproject.toml          # dist name payflow-common
  project.json
  payflow_common/         # import payflow_common
    __init__.py
    models/
  tests/
```

## Why

`src/` adds a layer without payoff here. Matching folder ↔ import name avoids `common` vs `payflow_common` drift.

## How

```bash
npm run g:backend-lib -- payflow_payments_client
# or: ./tools/scripts/init-backend-lib.sh payflow_payments_client

uv sync --all-packages
```

The script runs `uv init --lib`, moves the package out of `src/`, and uses hatchling for the flat layout.

## Where it fits (HLD / LLD)

Repo tooling. Apps depend via `{ workspace = true }`.

## Trade-offs

Slightly customizes uv’s default `src/` layout — intentional for consistency.

## Check your understanding

1. Why is the folder `payflow_common` instead of `common`?
2. What does the script do after `uv init` regarding `src/`?

## Code in this repo

`tools/scripts/init-backend-lib.sh`; first lib `libs/backend/payflow_common`.
