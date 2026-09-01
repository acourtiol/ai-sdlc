---
name: sdlc-continue
description: >-
  Resumes an in-progress AI-native SDLC change by reading intent/<slug>/ and
  running the next unapproved gate (accept intent, approve spec, approve plan,
  implement, or verify). Use when the user says continue, next, or resume a
  feature that already has an intent/ folder.
license: MIT
metadata:
  author: acourtiol
  version: "1.0"
---

# sdlc-continue

Pick up `intent/<slug>/` and run the next gate. Do not skip gates. Do not start a new slug.

## House rules

- If the repo has `openspec/` with open changes and no `intent/` work, use OpenSpec instead.
- Do not commit unless the user asks.
- One slug at a time. If several exist, ask which.

## Next-gate table

Read frontmatter `status` on the files that exist:

| State | Next |
| --- | --- |
| no `intent/<slug>/` | `sdlc-plan` (this is the wrong skill unless they named a new idea) |
| `intent.md` is `draft` | present it; on accept set `accepted`, then stop or continue to design if they asked to keep going |
| `intent.md` is `accepted`, no spec | `sdlc-design` |
| `spec.md` is `draft` | ask to approve; on approve set `specified` |
| spec `specified`, no plan | `sdlc-apply` from the plan step |
| `plan.md` is `draft` | ask to approve the plan |
| plan `planned`, code not done | `sdlc-apply` implement step (coder) |
| code done, not verified | `sdlc-verify` |
| verified, statuses not `done` | ask to mark `done`; reviewer is a separate named agent |

Follow that skill's `SKILL.md` for the chosen row. Then stop at the next human gate unless the user said to keep going through a later gate they already approved.
