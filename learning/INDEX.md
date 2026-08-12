# Learning index

> Agents: scan this table before introducing new concepts. Add a row when a topic is planned or taught. One slug = one topic.

| Slug                               | Category     | Status | Entry                                                                                                      | Code refs                                     | Notes                                     |
| ---------------------------------- | ------------ | ------ | ---------------------------------------------------------------------------------------------------------- | --------------------------------------------- | ----------------------------------------- |
| monorepo-workspace-vs-orchestrator | concepts     | taught | [concepts/0001-monorepo-workspace-vs-orchestrator.md](concepts/0001-monorepo-workspace-vs-orchestrator.md) | `pyproject.toml`, `nx.json`, `apps/`, `libs/` | uv = workspace; Nx = orchestrator         |
| uv-workspaces                      | technologies | taught | [technologies/0001-uv-workspaces.md](technologies/0001-uv-workspaces.md)                                   | `pyproject.toml`, `uv.lock`                   | members empty until apps/libs decided     |
| nx-orchestrator                    | technologies | taught | [technologies/0002-nx-orchestrator.md](technologies/0002-nx-orchestrator.md)                               | `nx.json`, `package.json`                     | Targets call `uv run` when projects exist |

## Planned learning tracks (suggested order)

Use these as a backlog; promote into the table when work starts.

### Foundations

- [ ] service-boundaries-and-bounded-contexts
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
