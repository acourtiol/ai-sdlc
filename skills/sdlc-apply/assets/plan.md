---
status: draft
slug: example-slug
spec: spec.md
base_commit: pending
spec_digest: pending
approved_by: pending
approved_digest: pending
---

# Plan: short name

## Files that change

Exact paths. New vs edit. One line each on what changes.

## Order of work

Replace this guidance with task boxes only. Use numeric prefixes for coherent,
reviewable changes, each with a focused check and commit; do not split by individual
file, tool call, or bookkeeping. Keep one implementer on related work. Remove every
example before approval.

- [ ] 1.1 What changes — verify: command, test, or observable behavior
- [ ] 1.2 Next step in this area — verify: ...
- [ ] 2.1 First step in the next area — verify: ...

## Risks

Carry each applicable spec Gotcha here with its concrete failure case and a
matching check in Order of work or Proof. Include only relevant migration,
external-API, compatibility, security, safety, or accessibility checks. Write
`None.` if no applicable risks were identified.

## Proof

The end-to-end evidence that the whole spec is met. Name each check's scope and
owner: focused checks per slice, one final full change-appropriate gate owned by the
fresh verifier. Consolidate overlapping gates before approval; map shared checks
to requirements/scenarios. Record cheap prerequisites before expensive integration
proof and the focused reassessment after two failures of the same class. An earlier
full gate needs a repository requirement or concrete integration risk.

## Review route

Name the fresh verifier subagent or separate fresh-session handoff capability,
the environment it can inspect, and any access needed. An autonomous run needs
a verifier dispatchable before implementation begins.

## Decision review

For autonomous approval only: decision, confidence, evidence for explicit outcome
and constraints, current-source support, contracts and important failure modes,
and unresolved assumptions/conflicts. At high confidence, explain why a challenge
was skipped. Otherwise record the focused challenge, checked evidence, resolution,
and residual uncertainty. Reference still-valid upstream evidence without copying
it. Remove this guidance before approval.
