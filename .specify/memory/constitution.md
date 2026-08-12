<!--
Sync Impact Report
- Version change: 1.0.0 → 1.1.0
- Modified principles: none (I–VI unchanged)
- Modified sections:
  - Development Workflow & Quality Gates — Speckit sequence, learn-first,
    ADR Proposed→Accepted→implement, monorepo tooling/layout ADRs
  - Quality Constraints — explicit deference to ADR-0002/0003 for stack/layout
- Added sections: none
- Removed sections: none
- Follow-up TODOs: none
-->

# PayFlow Constitution

## Core Principles

### I. Code Quality, Organization & Readability

Every change MUST leave the codebase clearer than it found it.
Code MUST be organized by bounded context and service boundary, not by
ad-hoc convenience. Public modules MUST expose a small, intentional surface;
internal details MUST stay private to their package.

All application and domain code MUST be object-oriented. Behavior MUST live
in classes (or equivalent language types with encapsulation), with clear
responsibilities, constructors/factories for creation, and instance methods
for operations. Domain concepts (Payment, LedgerEntry, OutboxMessage,
WebhookDelivery, etc.) MUST be modeled as objects, not as ad-hoc dicts or
loose procedural scripts.

Mandatory OO practices:

- Encapsulation: state MUST be owned by objects; callers MUST use defined
  interfaces, not reach into internals
- Single responsibility per class; god classes MUST be split before merge
- Prefer composition for wiring collaborators; inheritance only for true
  is-a relationships with shared behavioral contracts
- Interfaces/abstract base types MUST define ports for persistence,
  messaging, and external providers so implementations stay swappable
- Dependency injection (constructor injection) MUST be used for
  collaborators; hidden global/service-locator state MUST NOT be introduced

Procedural or functional modules are allowed only as thin entrypoints
(main/bootstrap, framework route adapters, one-line CLI shims) that
immediately delegate into objects. Scripts that implement business rules
inline MUST NOT merge. Anemic “DTO-only” layers that push all logic into
unstructured functions MUST NOT substitute for real domain objects.

Naming MUST reveal domain intent (payment, ledger, webhook, outbox) without
abbreviation noise. Functions and types MUST do one job; files that mix
unrelated concerns MUST be split before merge. Dead code, commented-out
blocks, and speculative abstractions MUST NOT ship.

Readability is a merge gate: reviewers MUST reject cryptic control flow,
god objects, unexplained magic numbers, and procedural domain logic.
Shared conventions (formatting, lint rules, import style) MUST be enforced
mechanically via CI. Prefer straightforward production patterns over
cleverness; complexity MUST be justified in the PR description.

**Rationale**: Readable, object-oriented structure keeps payment complexity
and correctness reviewable as the system grows.

### II. Testing Standards

No PR MAY merge without automated tests that cover the behavior it changes.
Tests MUST be deterministic, isolated from shared mutable state, and runnable
in CI without manual setup beyond documented project bootstrap.

Unit tests are the default for domain logic, validation, and pure
transforms. Integration tests are strongly encouraged for persistence,
messaging, and cross-service contracts, but they are NOT mandatory for every
change. When integration tests are omitted, the PR MUST state how risk is
covered (unit coverage of invariants, contract stubs, or a follow-up task).

Money-path and correctness-critical code (idempotency, ledger posting,
status transitions, outbox publish) MUST include tests that assert the
invariant, not only the happy path. Flaky tests MUST be fixed or quarantined
with an owner; they MUST NOT be ignored indefinitely.

**Rationale**: Merge-gated tests protect invariants without mandating full
TDD ceremony; integration depth scales with risk.

### III. User Experience Consistency

Phase 1 clients are HTTP APIs. Every public API MUST present a consistent
contract: stable resource shapes, predictable error envelopes, uniform
pagination/filtering where lists exist, and documented status codes.
Breaking response or error-shape changes MUST be versioned or explicitly
migrated.

Idempotency, correlation/request IDs, and authentication failures MUST
behave the same way across services. Error bodies MUST be machine-readable
and safe to show to API consumers (no stack traces or secrets).

When CLI or UI surfaces are added later, they MUST reuse the same domain
vocabulary, status model, and error semantics as the API—no parallel
“friendly” meanings that diverge from the API contract.

**Rationale**: Consistency is the product UX for an API-first platform;
CLI/UI inherit that contract rather than inventing a second one.

### IV. Performance Requirements

Performance work MUST be measured, not assumed. Each service MUST define
and track quantitative budgets; regressions that breach budgets MUST block
release unless an ADR documents a temporary waiver with an expiry.

Default budgets for synchronous public APIs under nominal local/staging
load (single-region, warm process, dataset size documented in the test
plan):

| Metric                                                 | Budget                                |
| ------------------------------------------------------ | ------------------------------------- |
| Health/readiness endpoints                             | p99 ≤ 50 ms                           |
| Read APIs (get/list by key)                            | p99 ≤ 200 ms                          |
| Write APIs (create/update payment-like commands)       | p99 ≤ 500 ms                          |
| Sustained command throughput (single service instance) | ≥ 100 req/s without error-rate > 0.1% |

Background consumers MUST process without unbounded lag growth under the
documented publish rate for that environment; consumer lag alerts MUST fire
when lag exceeds 60 seconds for more than 5 consecutive minutes.

N+1 queries, unbounded list endpoints, and missing timeouts on outbound
calls are defects. Every external call MUST use an explicit timeout
(default ≤ 3 s unless an ADR sets otherwise). Caching and async offload
are allowed only when correctness (especially ledger and idempotency)
remains intact.

**Rationale**: Quantitative budgets make performance reviewable; defaults
are portfolio-realistic and may be tightened per service via ADR.

### V. Production Practices

PayFlow MUST be operable like production even though it is a sandbox.
Services MUST expose health and readiness probes, structured logs
(JSON), and metrics sufficient to diagnose latency, errors, and queue lag.
Secrets MUST come from environment or a secret manager—never committed.

Deployable units MUST run via containers with immutable image tags in
shared environments. Configuration MUST be explicit and environment-scoped.
Retries MUST use bounded backoff; poison messages MUST land in a DLQ (or
equivalent) with enough context to replay safely.

Changes that affect runtime topology, data stores, or public contracts MUST
include migration/rollback notes in the PR. Observability gaps for new
failure modes MUST be closed in the same change set when feasible.

**Rationale**: Production practice is the learning goal; sandbox scope does
not excuse missing operability.

### VI. Security & Payment Domain Correctness

This platform MUST remain a simulation: it MUST NOT process real money or
store real card PAN/CVV. Test fixtures MUST use clearly fake credentials
and tokens.

Security baseline (non-negotiable):

- Authenticate and authorize every non-public endpoint
- Validate and bound all inputs
- Encrypt data in transit (TLS in shared/deployed environments)
- Hash or tokenize sensitive secrets at rest; never log secrets, API keys,
  or full payment instrument data
- Apply least privilege to service credentials and datastore roles

Payment-domain correctness (non-negotiable):

- Mutating payment operations MUST be idempotent under client-supplied keys
- Ledger updates MUST preserve double-entry invariants (debits = credits)
- Status transitions MUST follow an explicit state machine; illegal
  transitions MUST fail closed
- Exactly-once _effect_ MUST be preserved under at-least-once delivery
  (idempotent consumers / dedupe)
- Fraud, refund, and webhook side effects MUST NOT double-apply on retry

Security or correctness shortcuts in “temporary” code MUST NOT merge
without an ADR and a tracked removal date.

**Rationale**: Security and ledger correctness are the trust surface of a
payment platform; sandbox status raises the bar for realism, not lowers it.

## Quality Constraints

- Constitution principles supersede informal preference and convenience.
- Specs, plans, and tasks MUST NOT introduce behavior that violates these
  principles; conflicts require a constitution amendment or an ADR waiver.
- Language/runtime and datastore choices MAY evolve, but MUST preserve
  testability, observability, object-oriented structure, and the
  security/correctness rules above.
- Free/open-source or free-tier infrastructure is preferred when it does
  not compromise the principles.
- Monorepo tooling and directory layout MUST follow accepted ADRs unless
  superseded: uv workspaces + Nx orchestrator (ADR-0002); `apps/` and
  `libs/` split by `backend`/`frontend` (ADR-0003). Plans and tasks MUST
  place new code under those trees.

## Development Workflow & Quality Gates

1. Spec-driven flow for non-trivial features (Speckit skills):
   specify → clarify (as needed) → plan → tasks → analyze (recommended) →
   implement → converge (if gaps remain). Checklist / taskstoissues as needed.
2. Learn-first (required alongside Speckit): before introducing unfamiliar
   concepts, technologies, patterns, or techniques, follow
   `.cursor/skills/learn-first/SKILL.md` — teach → gate on confirmation →
   then code; update `learning/` + INDEX after coding. Speckit implement
   MUST NOT skip this gate.
3. Durable stack/layout/datastore/broker decisions: write ADR as
   **Proposed** → explicit human accept → mark **Accepted** → only then
   implement dependent code (see `.cursor/rules/adr.mdc` and `AGENTS.md`).
4. Every PR MUST include tests for changed behavior and MUST pass lint,
   type/format checks (where configured), and CI. Prefer `nx` targets that
   shell into `uv run` for Python projects.
5. Reviewers MUST verify principles I–VI relevant to the diff; payment-path
   and security-sensitive changes require explicit invariant review;
   structural reviews MUST reject procedural domain logic (I).
6. Integration tests SHOULD accompany persistence, messaging, and contract
   changes; omission requires a written risk note.
7. Performance-sensitive changes SHOULD include measurement (benchmark,
   load snippet, or before/after metrics) against the budgets in IV.
8. ADRs MUST live under `adr/` and MUST document architecture decisions
   that waive or specialize constitution defaults (timeouts, budgets,
   delivery semantics).

## Governance

This constitution is the highest process authority for PayFlow engineering
practice. Amendments MUST:

1. Update `.specify/memory/constitution.md` with a Sync Impact Report
2. Bump **Version** using semantic versioning:
   - MAJOR: remove/redefine a principle in a backward-incompatible way
   - MINOR: add a principle/section or materially expand guidance
   - PATCH: clarifications, wording, non-semantic refinements
3. Set **Last Amended** to the amendment date (ISO 8601)
4. Keep **Ratified** as the original adoption date unless the document is
   deliberately re-ratified

Version bumps apply only when a prior version has already been committed
(or otherwise published as a baseline). While the constitution, a feature
spec, plan, tasks file, ADR, or related Spec Kit artifact is still
uncommitted draft work on the same change set, editors MUST refine it
in place WITHOUT incrementing its version. Bump the version on the first
commit that introduces that revision relative to the last committed
baseline—not on every intermediate edit before commit.

Compliance is expected on every PR and agent-driven change. Material
violations discovered after merge MUST be tracked and remediated; silent
drift is not allowed. Runtime guidance for agents and humans MUST align
with this document; when guidance conflicts, this constitution wins until
amended.

**Version**: 1.1.0 | **Ratified**: 2026-08-11 | **Last Amended**: 2026-08-12
