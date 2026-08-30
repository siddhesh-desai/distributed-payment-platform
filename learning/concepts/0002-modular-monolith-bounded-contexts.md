---
id: 0002
slug: modular-monolith-bounded-contexts
title: Modular monolith and bounded contexts
category: concepts
status: taught
taught_on: 2026-08-12
code_refs:
  - apps/backend/api/modules/sample_module/
  - apps/backend/api/core/router_registry.py
related:
  - fastapi-router-composition
  - domain-module-layering
adr_refs:
  - adr/0004-backend-api-domain-modules.md
---

# Modular monolith and bounded contexts

## What

A **modular monolith** is one deployable process that hosts multiple **bounded contexts** (business domains) as internal modules with explicit boundaries—not one big shared “utils soup,” and not separate microservices yet.

A **bounded context** owns a coherent slice of the domain language and data. Cross-context collaboration goes through a published surface (`public/`), not by reaching into another module’s internals.

## Why

Payments platforms grow many domains (payments, ledger, risk, …). Starting as separate services too early adds ops cost without clarity. Starting as a tangled single package makes later splits painful. Modules inside one API give clear ownership now and a migration path later.

## How

```text
Client
  │
  ▼
API process (apps/backend/api)
  │
  ▼
core/router_registry
  │
  ▼
sample_module  (+ future modules…)
```

- One HTTP process: `apps/backend/api`
- Domains live under `modules/<name>/` and import as `modules.<name>` (e.g. `modules.sample_module`).
- Create vs extend: same capability → extend; new capability/language → new module

## Where it fits (HLD / LLD)

HLD: single product API box. LLD: folders + `public/` rules = the boundary mechanism.

## Trade-offs

| Approach         | When                                              |
| ---------------- | ------------------------------------------------- |
| Modular monolith | Default for learning / early product              |
| Microservices    | Independent scale, team, failure domain justified |
| Big ball of mud  | Never as intentional design                       |

## Production notes

Boundaries are social + structural: CI ownership, import rules, and reviews matter as much as folders.

## Check your understanding

1. Why must a new domain’s router be registered in `core`, not imported from inside `sample_module`?
2. When would “ledger posting” be a new module vs a payment field?

## Code in this repo

- `sample_module` — demonstrator domain with hello endpoint
- `core/router_registry.py` — sole composition point for module routers

## Further practice (optional)

Sketch create-vs-extend for a fictional “chargeback” brief using only ADR-0004.
