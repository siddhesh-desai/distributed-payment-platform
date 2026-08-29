# Learning index

> Agents: scan this table before introducing new concepts. Add a row when a topic is planned or taught. One slug = one topic.

| Slug                               | Category     | Status | Entry                                                                                                      | Code refs                                     | Notes                                   |
| ---------------------------------- | ------------ | ------ | ---------------------------------------------------------------------------------------------------------- | --------------------------------------------- | --------------------------------------- |
| monorepo-workspace-vs-orchestrator | concepts     | taught | [concepts/0001-monorepo-workspace-vs-orchestrator.md](concepts/0001-monorepo-workspace-vs-orchestrator.md) | `pyproject.toml`, `nx.json`, `apps/`, `libs/` | uv = workspace; Nx = orchestrator       |
| modular-monolith-bounded-contexts  | concepts     | taught | [concepts/0002-modular-monolith-bounded-contexts.md](concepts/0002-modular-monolith-bounded-contexts.md)   | `apps/backend/api/modules/`, `core/`          | One API process; domains as modules     |
| domain-module-layering             | patterns     | taught | [patterns/0001-domain-module-layering.md](patterns/0001-domain-module-layering.md)                         | `modules/sample_module/`                      | routes→services→…; public/ cross-module |
| uv-workspaces                      | technologies | taught | [technologies/0001-uv-workspaces.md](technologies/0001-uv-workspaces.md)                                   | `pyproject.toml`, `uv.lock`                   | members include `apps/backend/api`      |
| nx-orchestrator                    | technologies | taught | [technologies/0002-nx-orchestrator.md](technologies/0002-nx-orchestrator.md)                               | `nx.json`, `package.json`, `api/project.json` | Targets call `uv run`                   |
| fastapi-router-composition         | technologies | taught | [technologies/0003-fastapi-router-composition.md](technologies/0003-fastapi-router-composition.md)         | `main.py`, `core/router_registry.py`          | Module registries mounted in core       |

## Planned learning tracks (suggested order)

Use these as a backlog; promote into the table when work starts.

### Foundations

- [x] service-boundaries-and-bounded-contexts _(see modular-monolith-bounded-contexts)_
- [ ] api-contracts-and-versioning
- [ ] dependency-injection-and-ports-adapters

### Reliability & money movement

- [ ] idempotency-keys
- [ ] at-least-once-delivery-and-dedup
- [ ] transactional-outbox
- [ ] saga-vs-orchestration-choreography

### Communication

- [ ] sync-vs-async-integration
- [ ] event-driven-basics
- [ ] gRPC-or-REST-tradeoffs _(pick when ADR lands)_

### Production practices

- [ ] structured-logging-and-correlation-ids
- [ ] metrics-traces-alerts
- [ ] timeouts-retries-backoff-jitter
- [ ] secrets-and-least-privilege

### Testing

- [ ] unit-vs-integration-vs-contract-tests
- [ ] testcontainers-or-local-stack _(when chosen)_

Update checkboxes and the table as topics move to **taught**.
