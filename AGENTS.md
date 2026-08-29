# AGENTS.md

Instructions for AI agents working in this repository.

## Project intent

This repo is a **learning-first** distributed payments platform (PayFlow). Prefer teaching and durable understanding over shipping features in silence.

## Learn-first (required)

1. Read `learning/INDEX.md` before introducing unfamiliar concepts, technologies, patterns, or techniques
2. If not marked **taught**: teach in depth → gate on confirmation → then implement
3. After coding: update the learning entry + INDEX; map code back to the lesson
4. Full workflow: `.cursor/skills/learn-first/SKILL.md` and `.cursor/rules/learning-first.mdc`

Skip the gate only for mechanical edits with no new concepts, or when the user says they already know the topic.

## Lean development flow

Default path (no mandatory feature spec/plan/tasks artifacts):

1. Scan `learning/INDEX.md` → teach and gate on new topics
2. If durable decision: ADR **Proposed** → human accept → **Accepted**
3. Implement (use Plan mode or equivalent only when large or ambiguous)
4. Update `learning/` + INDEX; explain how code maps to the lesson

Details: `.cursor/skills/dev-workflow/SKILL.md`. Constitution and quality gates: `.cursor/rules/constitution.mdc`. Repo layout/tooling: `.cursor/rules/repo-conventions.mdc`.

## Architecture decisions

Durable decisions go in `adr/` (see `.cursor/rules/adr.mdc`). Do not put tutorials in ADRs — those belong in `learning/`.

### ADR → review → implement (required)

For stack, layout, datastore, broker, or other durable choices:

1. **Write** the ADR with status `Proposed` (teach first if the topic is new)
2. **Stop** and wait for explicit human review / acceptance
3. Mark the ADR `Accepted` only after confirmation
4. **Then** implement code, path moves, and config that depend on it

Never bundle “ADR + implementation” into one unconfirmed step. A yes to “shall we proceed?” on a lesson is not acceptance of an unwritten or unread ADR.

## Pointers

| Concern          | Location                            |
| ---------------- | ----------------------------------- |
| Learning log     | `learning/`                         |
| ADRs             | `adr/`                              |
| Constitution     | `.cursor/rules/constitution.mdc`    |
| Agent rules      | `.cursor/rules/`                    |
| Agent skills     | `.cursor/skills/`                   |
| Pre-merge review | `.cursor/skills/pr-review/SKILL.md` |
