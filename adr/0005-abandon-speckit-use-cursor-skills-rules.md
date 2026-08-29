# ADR-0005: Abandon Speckit; use agent skills and rules

- **Status:** Accepted
- **Date:** 2026-08-29
- **Deciders:** Siddhesh Desai

## Context

ADR-0001 adopted GitHub Spec Kit for greenfield spec-driven work. In practice the specify → plan → tasks → implement pipeline added ceremony without enough speed for a learning-first repo. Durable needs are teaching (`learning/`), architecture decisions (`adr/`), and non-negotiable engineering principles — not a multi-artifact Speckit tree in-repo.

## Decision

Abandon Speckit as the primary workflow. Delete `.specify/`, Speckit agent skills, and feature `specs/` artifacts. Govern via always-apply agent rules (constitution, learn-first, repo conventions, ADRs) and skills (`learn-first`, thin `dev-workflow`) under `.cursor/rules/` and `.cursor/skills/`. Spec-based development may return later as an optional agent skill, not as a living Speckit install.

## Consequences

### Positive

- Faster path: teach → (ADR if needed) → implement → log.
- Principles stay enforced through `.cursor/rules/constitution.mdc`.
- Less process surface for agents and humans to keep in sync.
- IDE-agnostic: any agent that reads those paths can follow them.

### Negative / trade-offs

- No mandatory written feature spec/plan/tasks for every change; large work relies on Plan mode (or equivalent) and judgment.
- Historical Speckit feature folders under `specs/` are removed (intent retained in code, ADRs, and `learning/`).

### Follow-ups

- Optional future skill for lightweight feature specs when a change needs stronger SDD.

## Alternatives considered

### Keep Speckit; use it only for large features

Rejected: the install and skills still create default overhead and conflicting agent guidance.

### Switch to OpenSpec

Rejected for now: still a framework install; we prefer agent-native rules/skills until SDD pain returns.
