---
name: sdlc-continue
description: >-
  Resumes an in-progress change by reading intent/slug/ and running the next
  unapproved gate (accept intent, approve spec, approve plan, implement, verify,
  or archive). Use when the user says continue, next, resume, what's in flight,
  or pick up a feature that already has an intent folder.
license: MIT
metadata:
  author: acourtiol
  version: "1.2"
---

# sdlc-continue

Pick up `intent/<slug>/` and run the next gate. Do not skip gates. Do not start a new slug.

Skipping a gate looks fast and produces a spec nobody accepted.

## Before you start

Do not commit unless the user asks.

If `scripts/status.sh` exists next to this file, run it with the product repository as the working directory (`sh <this-skill-dir>/scripts/status.sh`). If the script is missing, list `intent/*/` yourself using the table below, skipping `intent/archive/`.

One slug at a time. If several exist, ask which. `intent/archive/` is the archive, not a slug: skip it when you list them.

Say which slug you picked and how to name a different one.

## Next gate

Read frontmatter `status` on the files that exist, from disk rather than from anything earlier in the conversation. Follow that row's skill `SKILL.md`. Stop at the next human gate unless the user already approved a later one and asked to keep going.

| State | Next |
| --- | --- |
| no `intent/<slug>/` | `sdlc-plan` (wrong skill unless they named a new idea) |
| `intent.md` is `draft` | present it; on accept set `accepted` |
| `intent.md` is `accepted`, no spec | `sdlc-design` |
| `spec.md` is `draft` | ask to approve; on approve set `specified` |
| spec `specified`, no plan | `sdlc-apply` from the plan step |
| `plan.md` is `draft` | ask to approve the plan |
| plan `planned`, boxes unticked | `sdlc-apply` implement step (coder), from the first unticked box |
| every box ticked, no `report.md` | `sdlc-verify` |
| verified, statuses not `done` | ask to mark `done`; reviewer is a separate named agent |
| `report.md` present, statuses `done` | `sdlc-archive` |

Report where the work stands as `N/M boxes ticked` when `plan.md` exists.
