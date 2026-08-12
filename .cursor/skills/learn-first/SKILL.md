---
name: learn-first
description: >-
  Teach-first coding workflow for this learning-oriented repo. Before
  writing or introducing code that uses unfamiliar concepts, technologies,
  patterns, or techniques, teach them in depth, check learning/INDEX.md, gate on
  learner confirmation, then implement and log. Use whenever generating new
  code, introducing a library/tool, explaining architecture (HLD/LLD),
  microservices communication, production practices, or when the user mentions
  learning, teaching, learning log, or "teach me first".
---

# Learn-First Workflow

Primary goal: the user is building to **learn**. Code is the vehicle; understanding is the product.

## When this skill applies

Apply on every change that introduces something not yet marked **taught** in `learning/INDEX.md` — libraries, protocols, patterns, infra, testing approaches, non-obvious language techniques.

Skip teaching only when the topic is already **taught**, or the user explicitly says “I know X, skip teaching”.

## Mandatory sequence (do not reorder)

```
1. Scan   → read learning/INDEX.md
2. Detect → list NEW concepts this change will introduce
3. Teach  → in-depth lesson BEFORE writing the new code
4. Gate   → ask learner to confirm / go deeper / proceed
5. Code   → implement only after confirmation (or explicit skip)
6. Log    → write/update learning entry + INDEX
7. Explain→ map the new code back to the concepts just taught
```

If multiple new topics appear, teach the **critical path** first (usually 1–3). Park the rest as upcoming lessons.

## Depth bar (not surface-level)

Every lesson MUST cover:

1. **What** — precise definition
2. **Why** — problem it solves; failure mode without it
3. **How** — mental model, key components, data/control flow
4. **Fit** — HLD vs LLD; which layer/service boundary
5. **Trade-offs** — costs, alternatives, when NOT to use it
6. **Production** — ops, failure, observability, security if relevant
7. **Check your understanding** — 2–4 non-trivial questions

Prefer diagrams, concrete examples, and wrong-vs-right comparisons.

## Paths

| Artifact                  | Path                                                    |
| ------------------------- | ------------------------------------------------------- |
| Index                     | `learning/INDEX.md`                                     |
| Template                  | `learning/_template.md`                                 |
| Entries                   | `learning/{concepts,technologies,patterns,techniques}/` |
| Decisions (not tutorials) | `adr/`                                                  |

## Gate phrasing

After teaching, stop and ask:

> I’ve taught **\<topic\>**. Want me to go deeper on any part, or shall we proceed to implement?

Do not dump large unfamiliar code in the same turn as the first lesson unless confirmed.

**Exception:** tiny mechanical edits with zero new concepts — no gate; briefly say why.

## After coding

1. Point to files/symbols that embody the concept
2. Write/update the learning entry (`status: taught`, `code_refs`)
3. Update `learning/INDEX.md`
4. Optionally note related upcoming topics

## Optional accelerators (offer when useful)

- **Explain-back**: ask the learner to restate; correct gaps before coding
- **Vertical slice**: smallest end-to-end use of the idea after the lesson
- **Alternatives → ADR**: teach the comparison, then write/link an ADR
- **Failure-as-lesson**: name the failure mode and log it if new
- **Blast radius**: prefer one major new technology per session/PR

## Anti-patterns

- Vague one-paragraph “teaching” then hundreds of lines of code
- Skipping the INDEX check
- Logging without teaching (or teaching without logging)
- “Just read the docs” instead of teaching
- Introducing many new technologies in one unscoped change

## Entry / INDEX details

See [teaching-guide.md](teaching-guide.md).
