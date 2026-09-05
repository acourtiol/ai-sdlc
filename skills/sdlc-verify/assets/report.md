---
slug: example-slug
verified: 2026-01-01
verdict: pass
---

# Report: short name

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

The diff follows the Design section of `spec.md` and the patterns already in this
repo.

## Findings

Each one tagged and pinned to a location. When you are unsure of severity, pick
the lower one.

- CRITICAL — blocks done. `path/to/file.ts:42`
- WARNING — should fix. `path/to/file.ts:88`
- SUGGESTION — worth fixing. `path/to/file.ts:120`

## Not checked

Which checks you skipped and why, so nobody reads silence as a pass.

## Verdict

Pass or fail, one line, matching `verdict` in the frontmatter. Anything left over
that needs its own intent.
