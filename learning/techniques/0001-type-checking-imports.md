---
id: 0004
slug: type-checking-imports
title: TYPE_CHECKING imports for type-only dependencies
category: techniques
status: taught
taught_on: 2026-08-29
code_refs:
  - apps/backend/api/core/db/session.py
  - apps/backend/api/modules/sample_module/services/sample_item_service.py
  - apps/backend/api/modules/sample_module/routes/endpoints/get_sample_items.py
  - .cursor/rules/python-imports.mdc
related:
  - sqlalchemy-orm
  - domain-module-layering
adr_refs: []
---

# TYPE_CHECKING imports

## What

`typing.TYPE_CHECKING` is `True` only while type checkers run. Imports inside `if TYPE_CHECKING:` are skipped at runtime.

## Why

Avoid loading heavy / circular modules just to satisfy annotations. Faster imports and fewer cycles.

## How

```python
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column  # Mapped stays runtime for SQLAlchemy

if TYPE_CHECKING:
    from sqlalchemy.orm import Session  # annotation-only
```

`from __future__ import annotations` makes annotations lazy so annotation-only names are not required at runtime.

## Where it fits

Repo-wide Python technique (apps + libs). Rule: `.cursor/rules/python-imports.mdc`.

## Trade-offs

Easy to misplace a runtime symbol under `TYPE_CHECKING` (e.g. `select(Model)` still needs `Model` at runtime).  
**SQLAlchemy `Mapped` must stay a normal import** on mapped classes/mixins.

## Check your understanding

1. Why must `SampleItem` stay a normal import in a repository that calls `select(SampleItem)`?
   - Because `SampleItem` is a runtime symbol, and we need to be able to use it at runtime.
2. Why pair this pattern with `from __future__ import annotations`?
   - Because we want to be able to use annotations at runtime, but we don't want to load the module at runtime.

## Code in this repo

See `get_db`, `SampleItemsListService`, `get_sample_items` (`Session` under `TYPE_CHECKING` where annotation-only).
`IdModelMixin` keeps `Mapped` as a runtime import (SQLAlchemy requirement).
