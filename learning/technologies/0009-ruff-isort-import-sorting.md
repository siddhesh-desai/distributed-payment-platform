---
id: 0009
slug: ruff-isort-import-sorting
title: Ruff I rules as isort (lint + IDE on save)
category: technologies
status: taught
taught_on: 2026-08-29
code_refs:
  - pyproject.toml
  - .vscode/settings.json
  - .vscode/extensions.json
related:
  - uv-workspaces
adr_refs: []
---

# Ruff I rules as isort (lint + IDE on save)

## What

**Import sorting** (historically the `isort` tool) groups and orders Python imports: future, stdlib, third-party, first-party. **Ruff’s `I` lint rules** implement the same policy inside Ruff (`ruff check` / organize-imports), so one tool owns lint + import order.

## Why

Unsorted imports create noisy diffs and local/CI drift. Auto-organize on save keeps every edit aligned with `nx lint` without a second CLI (`isort`) that can fight Ruff.

## How

```text
pyproject.toml  →  [tool.ruff.lint] select includes "I"
                →  known-first-party: payflow_common, core, modules, main
Save .py file   →  Ruff extension: organizeImports + format
CI / nx lint    →  uv run … ruff check .
```

Package `pyproject.toml` files `extend` the workspace root so `I` (and other selects) stay consistent.

Default section order (no custom bands): third-party → first-party. Workspace libs and app packages share the first-party group via `known-first-party`.

Example grouping in an API module:

```python
from sqlalchemy.orm import Session

from core.db.session import get_db
from payflow_common.models import OrmBaseModel
```

## Where it fits (HLD / LLD)

Workspace tooling / DX — not a domain concern. Applies to all Python under `apps/backend` and `libs/backend`.

## Trade-offs

- **Ruff `I` only** — one config, fast; preferred here.
- **Standalone isort + Ruff** — redundant; configs can disagree unless mirrored carefully.
- **Custom isort sections** (e.g. a separate band for libs) — extra clarity, more config to maintain; we keep the default first-party group instead.
- IDE settings live in committed `.vscode/` so the team shares them; personal overrides still win in user settings if needed.

## Production notes

Pin Ruff via the uv workspace. Add new import roots (`payflow_*`, `core`, …) to `known-first-party` when they appear. Do not ship the Ruff extension into runtime images — editor-only.

## Check your understanding

1. Why prefer Ruff `I` over adding the `isort` package alongside Ruff?
2. What goes wrong if `payflow_common` is omitted from `known-first-party`?
3. How does organize-on-save relate to `nx lint`?

## Code in this repo

- Root `[tool.ruff.lint]` / `[tool.ruff.lint.isort]` in `pyproject.toml`; packages extend it
- `.vscode/settings.json` — format + organize imports on save via Ruff
- `.vscode/extensions.json` — recommends `charliermarsh.ruff`

## Further practice (optional)

Intentionally scramble imports in a module, save, and confirm the Ruff extension restores isort order; then run `nx lint api` with no I001 left.
