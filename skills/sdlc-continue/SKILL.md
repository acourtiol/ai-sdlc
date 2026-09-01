---
name: sdlc-continue
description: >-
  Resumes an in-progress change by reading intent/slug/ and running the next
  unapproved gate (accept intent, approve spec, approve plan, implement, or
  verify). Use when the user says continue, next, resume, or pick up a feature
  that already has an intent folder.
license: MIT
metadata:
  author: acourtiol
  version: "1.1"
---

# sdlc-continue

Pick up `intent/<slug>/` and run the next gate. Do not skip gates. Do not start a new slug.

Skipping a gate looks fast and produces a spec nobody accepted.

## Before you start

If `openspec/` has open changes and there is no `intent/` work, use OpenSpec instead.

Do not commit unless the user asks.

One slug at a time. If several exist, ask which.

## Next gate

Read frontmatter `status` on the files that exist. Follow that row's skill `SKILL.md`. Stop at the next human gate unless the user already approved a later one and asked to keep going.

| State | Next |
| --- | --- |
| no `intent/<slug>/` | `sdlc-plan` (wrong skill unless they named a new idea) |
| `intent.md` is `draft` | present it; on accept set `accepted` |
| `intent.md` is `accepted`, no spec | `sdlc-design` |
| `spec.md` is `draft` | ask to approve; on approve set `specified` |
| spec `specified`, no plan | `sdlc-apply` from the plan step |
| `plan.md` is `draft` | ask to approve the plan |
| plan `planned`, code not done | `sdlc-apply` implement step (coder) |
| code done, not verified | `sdlc-verify` |
| verified, statuses not `done` | ask to mark `done`; reviewer is a separate named agent |
