---
name: pr-review
description: >-
  Pre-merge review of PayFlow PRs and branch changes against constitution,
  learn-first, ADRs, OO design, tests, naming, formatting, and production
  patterns. Use when the user asks to review a PR, pre-merge review, merge
  readiness, /pr-review, or to check whether changes are safe to merge.
---

# PayFlow pre-merge PR review

Report-only by default. Do **not** fix findings unless the user explicitly asks.

## When to run

Triggers: “review PR”, “pre-merge review”, “merge readiness”, `/pr-review`, or a PR URL/number.

Default scope: **branch changes** vs merge-base with `main` (committed + staged + unstaged).  
If the user asks for uncommitted-only → review working tree only.  
If given a PR URL/number → resolve with `gh`, ensure the head branch is checked out (ask before stash), then review.

## Mandatory inputs to load

Before judging, read (or re-read) and apply:

| Source           | Path                                                                      |
| ---------------- | ------------------------------------------------------------------------- |
| Constitution     | `.cursor/rules/constitution.mdc`                                          |
| Learn-first      | `.cursor/skills/learn-first/SKILL.md`, `.cursor/rules/learning-first.mdc` |
| Dev workflow     | `.cursor/skills/dev-workflow/SKILL.md`                                    |
| Repo conventions | `.cursor/rules/repo-conventions.mdc`                                      |
| ADR rules        | `.cursor/rules/adr.mdc`                                                   |
| Agent entry      | `AGENTS.md`                                                               |
| Learning index   | `learning/INDEX.md`                                                       |
| Relevant ADRs    | `adr/` (new/changed + any decision the diff depends on)                   |

Also follow any other project skills the change touches (e.g. learn-first gate already required for new topics).

## Review workflow

```
1. Diff     → collect changed files (gh pr diff / git diff merge-base)
2. Context  → load rules/skills/INDEX + related ADRs/learning entries
3. Axes     → score every axis below against the diff (not the whole repo)
4. Design   → ask: better HLD or LLD for this feature?
5. Verdict  → merge gate from severities
6. Report   → template below; no auto-fix
```

## Severity

| Level      | Meaning                                                                   | Merge impact                    |
| ---------- | ------------------------------------------------------------------------- | ------------------------------- |
| `critical` | Correctness, security, payment invariants, constitution hard fails        | Blocks merge                    |
| `high`     | Missing required learn/ADR/tests for the change; major OO/boundary breach | Blocks merge                    |
| `medium`   | Real gap (coverage hole, weak pattern, incomplete ADR) — should fix soon  | Caveat; prefer fix before merge |
| `low`      | Maintainability, minor naming/format inconsistency                        | Optional before merge           |
| `nit`      | Taste / micro-style                                                       | Optional                        |

**Merge gate:** any `critical` or `high` → **Do not merge**. Else **Merge with caveats** (list medium+) or **Merge ready** (only low/nit or clean).

## Review axes

Check **each** axis. Skip an axis only if the diff cannot touch it; say so briefly.

### 1. Rules & skills compliance

- Change followed learn-first → ADR (if needed) → implement → learning log sequence
- No Speckit `specs/` / `.specify/` recreation unless an optional skill asked for it
- Constitution principles not waived without ADR + tracked removal
- Layout matches accepted ADRs (`apps/`, `libs/`, uv + Nx)

### 2. Object-oriented design

- Domain/app logic in objects: encapsulated state, clear responsibilities, constructor DI
- Composition over inheritance; one job per type/file
- Ports (interfaces/ABCs) for persistence, messaging, providers — no hidden globals/service locators
- Entrypoints (routes, `main`, CLI) stay thin and delegate
- No god objects, procedural domain logic, or speculative dead code

### 3. Learning coverage

- Diff introduces concepts/tech/patterns/techniques → must appear in `learning/` + INDEX as **taught**, **unless** the user explicitly said they already know the topic
- Code refs / mapping present when a lesson was claimed
- Flag “code without lesson” and “lesson without code_refs” as `high` when the topic is clearly new

### 4. ADRs

- Durable decisions (store, broker, layout, consistency, constitution waiver) have an ADR
- Status workflow respected (no Accepted-dependent code without acceptance)
- Context → Decision → Consequences → Alternatives present; one decision per file
- Missing ADR for a durable choice in the diff → `high` / `critical` by impact

### 5. HLD / LLD fitness

- Bounded context / module boundaries respected
- Propose a **better** HLD or LLD only when clearly superior for _this_ change (trade-offs, not bikeshedding)
- Pattern suggestions → `medium` (or `high` if current design will be hard to unwind)

### 6. Correctness & bugs

- Logic errors, edge cases, race/idempotency gaps, illegal state transitions
- Payment paths: invariants, double-entry, exactly-once effect under retry (constitution VI)
- Simulation-only: no real money / PAN / CVV

### 7. Tests (complete coverage expectation)

For changed behavior, require intentional coverage — not only happy path:

| Kind       | Expect                                                             |
| ---------- | ------------------------------------------------------------------ |
| Positive   | Primary success paths                                              |
| Negative   | Validation failures, not-found, authZ denials, illegal transitions |
| Boundary   | Empty, max size, zero/negative money, timezone/idempotency keys    |
| Invariant  | Money/ledger/idempotency assertions where relevant                 |
| Regression | Bugfix should lock the failure mode                                |

Unit vs integration per constitution II. Missing tests for new behavior → at least `high`. Thin smoke-only where negatives matter → `medium`/`high`.

### 8. Naming & formatting

- Names reveal domain intent; consistent module/route/service vocabulary
- Matches existing project style (Python/TS as applicable); CI format/lint clean for touched files
- No cryptic abbreviations, misleading types, or route/DTO drift from API vocabulary

### 9. Enterprise / production patterns

When the change touches runtime surfaces, check for (or explicit deferral + ADR):

- Health/readiness, structured JSON logs, metrics (latency/errors)
- Timeouts on outbound calls; bounded retries; DLQ/poison handling if messaging
- Secrets from env only; no secrets/PII in logs
- Idempotency / correlation ID behavior for mutating APIs
- Migration/rollback notes for topology/store/contract changes
- Error bodies machine-readable and safe (constitution III)

Gaps on money-path or new public API → `high`/`critical`; otherwise `medium` if deferred without note.

## Output format

```markdown
# Pre-merge review

**Verdict:** Do not merge | Merge with caveats | Merge ready
**Scope:** <branch vs main | PR #N | uncommitted>
**Summary:** <2–4 sentences>

## Findings

| Severity | Axis | Location    | Finding | Suggestion |
| -------- | ---- | ----------- | ------- | ---------- |
| critical | …    | `path:line` | …       | …          |

## Architecture (HLD/LLD)

- <fit assessment + better pattern if any>

## Learning & ADR gaps

- Learning: <ok | missing entries/topics>
- ADRs: <ok | missing/Proposed-only issues>

## Tests

- Covered: <positive/negative/boundary/invariant notes>
- Missing: <list>

## Merge blockers

- <critical/high only, or “None”>
```

Sort findings by severity (critical → nit). Prefer concrete `file:line` locations. No policy dumps — cite the rule/skill name only when it clarifies the finding.

## Anti-patterns for the reviewer

- Reviewing untouched legacy code unrelated to the diff
- Demanding Speckit artifacts
- Treating every design preference as `critical`
- Auto-fixing or opening follow-up PRs unless asked
- Skipping learning/ADR axes because “it’s just code”

## Optional deeper checklist

For axis detail examples, see [checklist.md](checklist.md).
