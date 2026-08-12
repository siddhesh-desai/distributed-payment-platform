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

## Spec-driven features

Use Speckit skills (specify → clarify → plan → tasks → implement / converge / analyze) under `.cursor/skills/speckit-*`. Constitution: `.specify/memory/constitution.md`.

## Architecture decisions

Durable decisions go in `adr/` (see `.cursor/rules/adr.mdc`). Do not put tutorials in ADRs — those belong in `learning/`.

## Pointers

| Concern      | Location          |
| ------------ | ----------------- |
| Learning log | `learning/`       |
| ADRs         | `adr/`            |
| Agent rules  | `.cursor/rules/`  |
| Agent skills | `.cursor/skills/` |
| Speckit      | `.specify/`       |
