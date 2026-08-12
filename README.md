# distributed-payment-platform

PayFlow — a production-style distributed payment simulation for practicing high-level design, low-level design, microservice communication, and operational practices (idempotency, ledgers, events, retries, observability).

## Status

Greenfield. Spec-driven process and decision records are in place; application services are not built yet.

## Repository layout

| Path        | Purpose                                               |
| ----------- | ----------------------------------------------------- |
| `adr/`      | Architecture Decision Records                         |
| `learning/` | Learning log (concepts taught while building)         |
| `.specify/` | Speckit constitution, templates, and feature workflow |
| `.cursor/`  | Cursor rules and skills for this repo                 |

## Spec-driven development

Feature work follows Speckit: constitution → specify → plan → tasks → implement. Governance lives in `.specify/memory/constitution.md`.

## Architecture decisions

See `adr/` for accepted choices (e.g. Speckit over OpenSpec). New durable stack or consistency decisions should land as ADRs before large implementation.

## Contributing (humans)

1. Prefer small, reviewable changes aligned with the constitution
2. Record non-obvious decisions in `adr/`
3. Keep `learning/INDEX.md` accurate if you were taught something new while implementing
