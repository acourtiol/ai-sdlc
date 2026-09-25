---
slug: example-slug
verified: pending
verdict: pending
isolation: pending
---

# Report: short name

## Change inspected

Base commit, HEAD, committed change range, working-tree and untracked paths.
State how a base was derived for an older plan.

## What shipped

What the change actually does now, read from the diff and the ticked plan rather
than from the session that wrote it. Name the surfaces and the requirements each
one satisfies.

## Deviations from plan

Where the implementation departed from `plan.md`, and why. "None" is an answer.

## Verification

### Completeness

Every box in `plan.md` ticked. Every requirement in `spec.md` has evidence.

### Correctness

Each scenario: what you ran or drove, what you observed. The proposed outcome in
`intent.md` is the bar, not green tests. A user-facing pass needs a
human-observable moment (what was driven or shown, and what a person would see).

### Coherence

Review the full change range for logic, security, regressions, error handling,
and architectural fit against `spec.md`, `plan.md`, and existing patterns.

## Findings

Write `None.` or list each finding as `- CRITICAL`, `- WARNING`, or
`- SUGGESTION`, pinned to a `file:line`. State what would settle uncertain impact.

## Not checked

Which checks you skipped and why, so nobody reads silence as a pass.

## Verdict

Pass or fail, one line, matching `verdict` in the frontmatter. Anything left over
that needs its own intent.
