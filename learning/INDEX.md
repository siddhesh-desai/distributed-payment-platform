# Learning index

> Agents: scan this table before introducing new concepts. Add a row when a topic is planned or taught. One slug = one topic.

| Slug                               | Category     | Status | Entry                                                                                                      | Code refs                                                  | Notes                                   |
| ---------------------------------- | ------------ | ------ | ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | --------------------------------------- |
| monorepo-workspace-vs-orchestrator | concepts     | taught | [concepts/0001-monorepo-workspace-vs-orchestrator.md](concepts/0001-monorepo-workspace-vs-orchestrator.md) | `pyproject.toml`, `nx.json`, `apps/`, `libs/`              | uv = workspace; Nx = orchestrator       |
| modular-monolith-bounded-contexts  | concepts     | taught | [concepts/0002-modular-monolith-bounded-contexts.md](concepts/0002-modular-monolith-bounded-contexts.md)   | `apps/backend/api/modules/`, `core/`                       | One API process; domains as modules     |
| domain-module-layering             | patterns     | taught | [patterns/0001-domain-module-layering.md](patterns/0001-domain-module-layering.md)                         | `modules/sample_module/`                                   | routes→facades→services; ADR-0010       |
| type-checking-imports              | techniques   | taught | [techniques/0001-type-checking-imports.md](techniques/0001-type-checking-imports.md)                       | `IdModelMixin`, `session.py`, services                     | `TYPE_CHECKING` + future annotations    |
| orm-model-auto-discovery           | techniques   | taught | [techniques/0002-orm-model-auto-discovery.md](techniques/0002-orm-model-auto-discovery.md)                 | `core/alembic/import_module_models.py`, `env.py`           | Importlib walk of modules/*/models      |
| twelve-factor-config               | patterns     | taught | [patterns/0002-twelve-factor-config.md](patterns/0002-twelve-factor-config.md)                             | `core/settings/`, `.env.example`                           | Env-backed DSN / pool                   |
| uv-workspaces                      | technologies | taught | [technologies/0001-uv-workspaces.md](technologies/0001-uv-workspaces.md)                                   | `pyproject.toml`, `uv.lock`                                | members include `apps/backend/api`      |
| nx-orchestrator                    | technologies | taught | [technologies/0002-nx-orchestrator.md](technologies/0002-nx-orchestrator.md)                               | `nx.json`, `package.json`, `api/project.json`              | Targets call `uv run`                   |
| fastapi-router-composition         | technologies | taught | [technologies/0003-fastapi-router-composition.md](technologies/0003-fastapi-router-composition.md)         | `main.py`, `core/router_registry.py`                       | Module registries mounted in core       |
| fastapi-depends                    | technologies | taught | [technologies/0010-fastapi-depends.md](technologies/0010-fastapi-depends.md)                               | `core/db/session.py`, `get_sample_items`                   | Depends + get_db request lifecycle      |
| postgresql-primary-store           | technologies | taught | [technologies/0004-postgresql-primary-store.md](technologies/0004-postgresql-primary-store.md)             | `docker-compose.yml`, `core/db/`                           | Postgres 16; host port 5433             |
| docker-compose-local-dev           | technologies | taught | [technologies/0005-docker-compose-local-dev.md](technologies/0005-docker-compose-local-dev.md)             | `docker-compose.yml`, `api/Dockerfile`                     | api + postgres local stack              |
| sqlalchemy-orm                     | technologies | taught | [technologies/0006-sqlalchemy-orm.md](technologies/0006-sqlalchemy-orm.md)                                 | `models/sample_item.py`, `repositories/`                   | SQLAlchemy 2 + session dependency       |
| sqlalchemy-sync-vs-async           | technologies | taught | [technologies/0011-sqlalchemy-sync-vs-async.md](technologies/0011-sqlalchemy-sync-vs-async.md)             | `core/db/engine.py`, `session.py`, `psycopg`               | Sync Session stack; when async wins     |
| alembic-migrations                 | technologies | taught | [technologies/0007-alembic-migrations.md](technologies/0007-alembic-migrations.md)                         | `core/alembic/env.py`, `migrations/0001_*`                 | Per-module migrations; app-level runner |
| uv-init-backend-libs               | technologies | taught | [technologies/0008-uv-init-backend-libs.md](technologies/0008-uv-init-backend-libs.md)                     | `tools/scripts/init-backend-lib.sh`                        | `uv init --lib` under libs/backend      |
| ruff-isort-import-sorting          | technologies | taught | [technologies/0009-ruff-isort-import-sorting.md](technologies/0009-ruff-isort-import-sorting.md)           | `pyproject.toml`, `.vscode/settings.json`                  | Ruff `I` = isort; organize on save      |

## Planned learning tracks (suggested order)

### Foundations

- [x] service-boundaries-and-bounded-contexts _(see modular-monolith-bounded-contexts)_
- [ ] api-contracts-and-versioning
- [ ] dependency-injection-and-ports-adapters _(FastAPI piece: [fastapi-depends](technologies/0010-fastapi-depends.md); broader ports/adapters still planned)_

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
