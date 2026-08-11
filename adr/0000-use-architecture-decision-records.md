# ADR-0000: Use Architecture Decision Records

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Siddhesh Desai

## Context

PayFlow will make many irreversible or costly-to-reverse choices (datastores, messaging, idempotency, Spec Kit vs alternatives). Without a stable place for rationale, the same debates recur and agents/humans rediscover “why” from code alone.

## Decision

Record significant architecture decisions as Markdown ADRs under `adr/`, using the Nygard-style sections (Context, Decision, Consequences) plus Alternatives, numbered `NNNN-kebab-case.md`, one decision per file.

## Consequences

### Positive

- Decisions are reviewable in PRs alongside code.
- Stable IDs for linking from specs, PRs, and later ADRs.
- Constitution waivers and specialized defaults have an explicit home.

### Negative / trade-offs

- Small process overhead for significant choices.
- Discipline required to keep ADRs short and not turn them into design docs.

### Follow-ups

- Conventions live in `.cursor/rules/adr.mdc`.

## Alternatives considered

### Wiki or Confluence-only ADRs

Rejected: drifts from the repo; weaker PR review and grep discoverability.

### No formal ADRs

Rejected: rationale stays tribal; Spec Kit and constitution waivers need citable records.
