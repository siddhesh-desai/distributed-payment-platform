---
name: dev-workflow
description: >-
  Lean PayFlow development flow without Speckit. Use when starting feature
  work, deciding whether to teach, write an ADR, use Plan mode, or implement
  directly. Prefer this over recreating spec/plan/tasks artifact trees.
---

# Lean development workflow

Primary goal remains **learning**. Speed comes from skipping Speckit ceremony, not from skipping teaching or ADRs.

## Default sequence

```
1. Scan   → learning/INDEX.md
2. Teach  → if topic not taught (learn-first skill); gate on confirmation
3. ADR    → if durable decision; Proposed → human accept → Accepted
4. Scope  → Plan mode (or equivalent) only when large or ambiguous
5. Code   → implement under apps/ / libs/ per accepted layout ADRs
6. Log    → learning entry + INDEX; map code to the lesson
```

## When to do what

| Situation                                               | Action                                                                    |
| ------------------------------------------------------- | ------------------------------------------------------------------------- |
| New concept/tech/pattern                                | Teach first (`learn-first`); do not dump unfamiliar code in the same turn |
| Stack, layout, datastore, broker, consistency semantics | ADR Proposed → wait → Accepted → then code                                |
| Small, clear change; topics already taught              | Implement directly                                                        |
| Large or ambiguous multi-file design                    | Use Plan mode (or equivalent); still no mandatory `specs/` tree           |
| Mechanical edit, zero new concepts                      | Skip teach gate; briefly say why                                          |

## Do not

- Recreate Speckit `spec.md` / `plan.md` / `tasks.md` / `.specify/` unless a future optional skill explicitly requests lightweight SDD
- Bundle ADR acceptance with “shall we proceed?” on a lesson
- Skip constitution principles in `.cursor/rules/constitution.mdc`

## Pointers

| Concern          | Path                                  |
| ---------------- | ------------------------------------- |
| Learn-first      | `.cursor/skills/learn-first/SKILL.md` |
| Pre-merge review | `.cursor/skills/pr-review/SKILL.md`   |
| Constitution     | `.cursor/rules/constitution.mdc`      |
| ADRs             | `.cursor/rules/adr.mdc`, `adr/`       |
| Repo conventions | `.cursor/rules/repo-conventions.mdc`  |
| Agent entry      | `AGENTS.md`                           |
