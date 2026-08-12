# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]

**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command; its definition describes the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.12 via uv, TypeScript later or NEEDS CLARIFICATION]

**Primary Dependencies**: [e.g., FastAPI with uv or NEEDS CLARIFICATION]

**Storage**: [if applicable, e.g., PostgreSQL or N/A]

**Testing**: [e.g., pytest via `nx test <project>` / `uv run pytest` or NEEDS CLARIFICATION]

**Target Platform**: [e.g., Linux server containers or NEEDS CLARIFICATION]

**Project Type**: [e.g., backend service under apps/backend/, shared lib under libs/backend/ or NEEDS CLARIFICATION]

**Performance Goals**: [align with constitution IV budgets or NEEDS CLARIFICATION]

**Constraints**: [domain-specific; must honor accepted ADRs and constitution or NEEDS CLARIFICATION]

**Scale/Scope**: [domain-specific or NEEDS CLARIFICATION]

## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

[Gates determined based on constitution file]

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

<!--
  Default monorepo layout for this Speckit setup. Replace placeholders with the
  concrete apps/libs this feature touches. If accepted ADRs define a different
  tree, follow those ADRs instead.
-->

```text
apps/
  backend/
    <service>/                 # one deployable Python service
  frontend/
    <app>/                     # when UI work is in scope
      …
libs/
  backend/
    <package>/                 # shared Python library
  frontend/
    <package>/                 # shared frontend package when needed
      …
```

**Structure Decision**: Document the selected structure from accepted layout/tooling
ADRs (typical: `apps/{backend,frontend}/`, `libs/{backend,frontend}/`). List which
concrete service/lib folders this feature creates or changes.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation                  | Why Needed         | Simpler Alternative Rejected Because |
| -------------------------- | ------------------ | ------------------------------------ |
| [e.g., 4th project]        | [current need]     | [why 3 projects insufficient]        |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient]  |
