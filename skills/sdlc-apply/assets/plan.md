---
status: draft
slug: example-slug
spec: spec.md
base_commit: pending
---

# Plan: short name

## Files that change

Exact paths. New vs edit. One line each on what changes.

## Order of work

Build and verify order, not a task dump. Group by area, number within the group.
Each box carries the check that closes it.

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
