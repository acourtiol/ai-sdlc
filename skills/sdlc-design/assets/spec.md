---
status: draft
slug: example-slug
intent: intent.md
---

# Spec: short name

## Requirements

What the system must do. Testable. Not file paths. One block per requirement,
each with at least one scenario.

### Requirement: short name

The system SHALL do the observable thing.

#### Scenario: short name

- **WHEN** the trigger
- **THEN** the observable outcome
- **AND** any further outcome

## Design

How it fits the existing codebase: surfaces, data, APIs, ownership.

## Gotchas / policy flags

List only applicable failure cases and constraints: security, auth and permissions,
PII, safety, persistent-data migration, external APIs, compatibility, and
accessibility for affected user flows. Say what could fail and point to the
requirement or scenario that covers it. Write `None.` if none apply.

## Open questions carried forward

Unresolved items from intent.md, plus new ones. Lower-impact items may carry an
owner or a default. A choice that could materially change architecture, safety
behavior, or acceptance criteria needs an answer or an explicit proposed default
called out for approval; an owner alone does not resolve it.
