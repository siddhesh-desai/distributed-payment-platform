# PR review checklist (detail)

Use when a finding needs a sharper bar. Primary instructions stay in `SKILL.md`.

## OO smells

- [ ] Service/repository/client responsibilities mixed in one type
- [ ] Business rules in route handlers or Free functions that own state
- [ ] Concrete infra imported into domain core (skip ports)
- [ ] Inheritance trees for behavior variation (prefer strategy/composition)
- [ ] Module reaches into another module’s internals (not `public/`)

## Learning smells

- [ ] New library/pattern in diff with no INDEX row
- [ ] INDEX says taught but entry lacks `code_refs` for this change
- [ ] User did **not** say “I know X” and teaching was skipped
- [ ] ADR used as a tutorial substitute (should be `learning/`)

## ADR smells

- [ ] New datastore/broker/layout/consistency semantics without ADR
- [ ] Code depends on ADR still `Proposed`
- [ ] Accepted ADR decision silently contradicted
- [ ] Multi-decision ADR or missing alternatives

## Test matrix (per changed behavior)

| Scenario      | Ask                                                      |
| ------------- | -------------------------------------------------------- |
| Positive      | Does the main success path assert the real outcome?      |
| Negative      | Invalid input / unauthorized / conflict / not found?     |
| Boundary      | Empty collections, max limits, money zero/precision?     |
| Idempotency   | Replay same key — same effect, no double apply?          |
| State machine | Illegal transition fails closed?                         |
| Concurrency   | Optimistic lock / unique constraint covered if relevant? |
| Contract      | Response shape/status stable and documented?             |

## Naming & format

- [ ] Types/files match existing module vocabulary (`routes`, `services`, `repositories`, …)
- [ ] HTTP paths and DTO names align with API UX consistency
- [ ] Formatter/linter clean on touched files
- [ ] No unused imports / dead stubs left “for later” without need

## Production patterns

| Surface      | Expect                                                 |
| ------------ | ------------------------------------------------------ |
| New HTTP API | Validation, stable errors, idempotency if mutating     |
| Outbound I/O | Explicit timeout ≤ constitution default unless ADR     |
| Messaging    | Retry bound, poison → DLQ context                      |
| Persistence  | Migration + rollback note when schema/topology changes |
| Ops          | Logging fields useful for correlation; no secrets      |
| Security     | AuthN/Z on non-public; fake fixtures only for cards    |

## HLD / LLD prompts

Ask only against the feature in the diff:

1. Is the bounded context right, or is this splitting/joining the wrong seam?
2. Is sync HTTP enough, or do we need async/outbox for the consistency story?
3. Is the module layering (route → service → port → adapter) intact?
4. Would a simpler pattern (fewer types) or a stricter one (explicit port) reduce risk?

Document the recommendation with trade-offs; severity from unwind cost.
