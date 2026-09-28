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

Replace this guidance with task boxes only. Group by area using numeric prefixes;
each box carries the check that closes it. Remove every example before approval.

- [ ] 1.1 What changes — verify: command, test, or observable behavior
- [ ] 1.2 Next step in this area — verify: ...
- [ ] 2.1 First step in the next area — verify: ...

## Risks

Carry each applicable spec Gotcha here with its concrete failure case and a
matching check in Order of work or Proof. Include only relevant migration,
external-API, compatibility, security, safety, or accessibility checks. Write
`None.` if no applicable risks were identified.

## Proof

The end-to-end evidence that the whole spec is met, not the per-step verifies
above. Tests, commands, or screenshots.

## Review route

Name the fresh verifier subagent or separate fresh-session handoff capability,
the environment it can inspect, and any access needed. An autonomous run needs
a verifier dispatchable before implementation begins.

## Decision review

For autonomous approval only: material choice, strongest counterargument from a
fresh research subagent, evidence checked, decision, and remaining uncertainty.
