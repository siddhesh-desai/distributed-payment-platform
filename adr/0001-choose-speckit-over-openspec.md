# ADR-0001: Choose Spec Kit over OpenSpec

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Siddhesh Desai

## Context

PayFlow is a greenfield, production-style distributed payment simulation. We need a spec-driven workflow so AI-assisted implementation stays aligned with correctness requirements (idempotency, double-entry ledgering, event delivery, retries).

Two leading options:

|             | **GitHub Spec Kit**                                         | **OpenSpec**                                           |
| ----------- | ----------------------------------------------------------- | ------------------------------------------------------ |
| Primary fit | Greenfield / 0→1                                            | Brownfield / iterative change                          |
| Workflow    | Constitution → specify → clarify → plan → tasks → implement | Propose → apply → sync → archive (delta-based)         |
| Spec model  | Full feature specs + governance constitution                | Living source-of-truth + ADDED/MODIFIED/REMOVED deltas |
| Overhead    | Higher upfront ceremony                                     | Lower friction per change                              |

## Decision

Adopt **GitHub Spec Kit** as the primary spec-driven development framework for PayFlow.

## Consequences

### Positive

- Clear checkpoints before implementation; less vibe-coding on critical paths.
- Non-negotiables live in one constitution and are reusable across features.
- Feature work decomposes into reviewable specs, plans, and tasks.

### Negative / trade-offs

- More process overhead than OpenSpec for small changes.
- As the codebase matures into mostly brownfield iteration, Spec Kit may feel heavier than delta-based change tracking.

### Follow-ups

- If ongoing work becomes predominantly brownfield and Spec Kit overhead dominates, revisit OpenSpec (or a hybrid) in a new ADR. Prefer sticking to one framework until that pain is real.

## Alternatives considered

### OpenSpec

Rejected for now: excellent for documenting deltas against an existing system, but we do not yet have a living behavior baseline to delta against. Lower ceremony is less valuable than strong upfront structure at this stage.

### No formal SDD framework

Rejected: the domain and architecture are complex enough that informal prompts alone are likely to drift from invariants and phase boundaries.
