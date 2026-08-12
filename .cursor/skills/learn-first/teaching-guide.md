# Teaching guide (depth checklist)

Use this when writing the in-chat lesson and the `learning/` entry.

## Lesson structure (chat)

```markdown
### Concept: <Name>

**What** — …
**Why** — problem + what breaks without it
**How** — mental model (diagram if useful)
**Fit** — HLD / LLD / which service or layer
**Trade-offs** — vs alternatives; when not to use
**Production** — failure modes, metrics, security notes
**Check your understanding**

1. …
2. …
```

## Entry frontmatter fields

```yaml
---
id: 0001
slug: idempotency-keys
title: Idempotency keys for payment APIs
category: patterns # concepts | technologies | patterns | techniques
status: taught # planned | teaching | taught | needs-review
taught_on: 2026-08-12
code_refs:
  - services/payments/src/...
related:
  - exactly-once-vs-at-least-once
  - transactional-outbox
adr_refs: []
---
```

## Category guide

| Folder          | Use for                                                       |
| --------------- | ------------------------------------------------------------- |
| `concepts/`     | Domain/distributed-systems ideas (consistency, CAP, saga)     |
| `technologies/` | Named tools/libs (Kafka, Postgres, OpenTelemetry)             |
| `patterns/`     | Named design/architecture patterns (outbox, CQRS)             |
| `techniques/`   | Concrete coding/LLD techniques (constructor DI, typed errors) |

## INDEX row format

```markdown
| Slug             | Category | Status | Entry                             | Code refs    |
| ---------------- | -------- | ------ | --------------------------------- | ------------ |
| idempotency-keys | patterns | taught | patterns/0001-idempotency-keys.md | payments API |
```

## Quality bar for “taught”

Mark **taught** only when:

- In-depth lesson was delivered in chat (or user confirmed prior knowledge)
- Entry file exists with What/Why/How/Trade-offs
- At least one `code_refs` path once code lands (can be empty briefly during teach-only)

Mark **needs-review** if the learner struggled or asked to revisit later.
