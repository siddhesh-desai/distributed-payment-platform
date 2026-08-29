# distributed-payment-platform

PayFlow — a production-style distributed payment simulation for practicing high-level design, low-level design, microservice communication, and operational practices (idempotency, ledgers, events, retries, observability).

## Status

Greenfield. Learn-first process, ADRs, agent rules/skills, and monorepo tooling (uv + Nx) are in place. Backend API module layout is underway under `apps/backend/api/`.

## Monorepo tooling

| Layer           | Tool              | Role                              |
| --------------- | ----------------- | --------------------------------- |
| Python packages | **uv workspaces** | Install, lock, link local libs    |
| Orchestration   | **Nx**            | `test` / `lint` / graph / caching |

### Bootstrap

```bash
uv sync --group dev
npm install --registry=https://registry.npmjs.org/
```

### Common commands

```bash
uv sync --group dev
nx graph
# After apps/libs exist:
# uv sync --all-packages --group dev
# nx test <project>
# nx run-many -t test
```

## Repository layout

| Path             | Purpose                                       |
| ---------------- | --------------------------------------------- |
| `apps/backend/`  | Deployable backend services                   |
| `apps/frontend/` | Deployable frontend apps (TBD)                |
| `libs/backend/`  | Shared backend packages (TBD)                 |
| `libs/frontend/` | Shared frontend packages (TBD)                |
| `adr/`           | Architecture Decision Records                 |
| `learning/`      | Learning log (concepts taught while building) |
| `.cursor/`       | Agent rules and skills for this repo          |

## How we work

- **Learn-first**: teach unfamiliar topics → confirm → implement → log in `learning/`
- **ADRs**: durable stack/layout/consistency decisions under `adr/` (Proposed → accept → implement)
- **Constitution**: engineering principles in `.cursor/rules/constitution.mdc`
- **Lean flow**: no mandatory Speckit feature artifacts; Plan mode (or equivalent) when work is large or ambiguous

## Architecture decisions

See `adr/` for accepted choices. New durable stack or consistency decisions: write ADR as **Proposed** → review/accept → then implement.

## Contributing (humans)

1. Prefer small, reviewable changes aligned with the constitution
2. Record non-obvious decisions in `adr/`
3. Keep `learning/INDEX.md` accurate if you were taught something new while implementing
