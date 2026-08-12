# Learning log

This folder is the **source of truth for what has been taught** in this project.

Agents must check `INDEX.md` before introducing unfamiliar concepts. If a topic is not marked **taught**, they teach it in depth first, then implement, then log it here.

## Layout

| Path            | Purpose                            |
| --------------- | ---------------------------------- |
| `INDEX.md`      | Fast scan of all topics + status   |
| `_template.md`  | Copy for new entries               |
| `concepts/`     | Distributed systems / domain ideas |
| `technologies/` | Named tools and libraries          |
| `patterns/`     | Architecture & design patterns     |
| `techniques/`   | Concrete LLD / coding techniques   |

## Status values

- `planned` — on the roadmap, not taught yet
- `teaching` — lesson in progress this session
- `taught` — deep lesson delivered (and usually code exists)
- `needs-review` — revisit later

## How you use this as a learner

1. When an agent proposes something new, expect a real lesson + “ready to proceed?”
2. Answer honestly — ask for more depth or say you already know it
3. Skim entries after a session to reinforce
4. Use `needs-review` topics as a revision queue

## Practices that improve learning + building

Already wired into agent rules/skills:

- Teach → gate → implement → log
- In-depth lessons (not one-liners) + check-your-understanding questions
- INDEX as the “already taught?” source of truth
- Separate ADRs (why we chose X) from learning entries (how X works)

Optional habits (use when they help):

1. **Vertical slice after each lesson** — smallest working end-to-end path that uses the concept, not a big-bang rewrite
2. **Alternatives before ADR** — when choosing Kafka vs Rabbit, Postgres vs …, insist on a short compare lesson, then write the ADR
3. **Revision queue** — mark shaky topics `needs-review`; periodically ask the agent to quiz you from those entries
4. **Explain-back** — after a lesson, you explain the concept in your own words in chat; agent corrects gaps before coding
5. **Blast-radius limit** — one new major technology per PR/session when possible
6. **Debug as curriculum** — when something breaks, treat the failure mode as a lesson and log it (timeouts, poison messages, duplicate charges, etc.)
