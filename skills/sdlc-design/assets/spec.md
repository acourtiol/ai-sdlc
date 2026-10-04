---
status: draft
slug: example-slug
intent: intent.md
intent_digest: pending
approved_by: pending
approved_digest: pending
---

# Spec: short name

## Requirements

What the system must do. Testable. Not file paths. One block per requirement,
each with at least one scenario. Trace the accepted outcome and material
constraints to these requirements; preserve user-provided examples and limits.
Check both missing outcomes and added product behavior against decisive user
wording and evidenced binding constraints. Agent-authored requirements alone
do not authorize extra scope; keep that trace here without a separate document.

### Requirement: short name

The system SHALL do the observable thing.

#### Scenario: short name

- **WHEN** the trigger
- **THEN** the observable outcome
- **AND** any further outcome

## Design

How it fits the existing codebase: surfaces, data, APIs, ownership. For a changed
shared contract or state invariant, name affected existing callers/writers and
link their retained behavior or approved change to scenarios. At affected provider/runtime
boundaries, identify established adapters/error parsers and the source, version-matched
documentation or authorized response evidence supporting consequential assumptions.
For stateful flows, scenarios cover relevant transitions and persisted results after
failure, retry or reload; an immediate response alone may hide rolled-back state.

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

## Decision review

For autonomous approval only: decision, confidence, evidence for explicit outcome
and constraints, current-source support, contracts and important failure modes,
and unresolved assumptions/conflicts. At high confidence, explain why a challenge
was skipped. Otherwise record the focused challenge, checked evidence, resolution,
and residual uncertainty. Reference still-valid upstream evidence without copying
it. Remove this guidance before approval.
