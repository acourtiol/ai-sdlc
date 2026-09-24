---
name: sdlc-continue
description: >-
  Resumes an in-progress change by reading intent/slug/ and running the next
  unapproved gate (accept intent, approve spec, approve plan, implement, verify,
  or archive). After apply, next is isolated sdlc-verify (verifier subagent, not
  in-session judgment) — do not skip verify, do not archive. Fail or CRITICAL →
  apply (fix) then isolated re-verify, never skip verify to archive. On accept
  or approve in this session, start the next skill unless they tell you to
  stop. Use when the user says continue, next, resume, what's in flight, or
  pick up a feature that already has an intent folder.
license: MIT
metadata:
  author: acourtiol
  version: "1.5"
---

# sdlc-continue

Pick up `intent/<slug>/` and run the next gate. Do not skip gates. Do not start a new slug. Never skip verify to archive.

Skipping a gate looks fast and produces a spec nobody accepted.

## Before you start

This skill does not commit. The skill you run commits its own artifact. Do not push unless the user asks.

If `scripts/status.sh` exists next to this file, run it with the product repository as the working directory (`sh <this-skill-dir>/scripts/status.sh`). Follow its `next:` line; if that is apply-then-verify, read `sdlc-apply` (it re-runs verify). If the script is missing, list `intent/*/` yourself using the table below, skipping `intent/archive/`. When next is verify, that means isolated `sdlc-verify` (dispatch a verifier subagent), not in-session judgment.

One slug at a time. If several exist, ask which. `intent/archive/` is the archive, not a slug: skip it when you list them.

Say which slug you picked and how to name a different one.

## Next gate

Read frontmatter `status` on the files that exist, from disk rather than from anything earlier in the conversation. Follow that row's skill `SKILL.md`. Stop at the next human gate. After they accept or approve in this session, follow that skill's after-approve handover unless they tell you to stop there.

| State | Next |
| --- | --- |
| no `intent/<slug>/` | `sdlc-plan` (wrong skill unless they named a new idea) |
| `intent.md` is `draft` | present it; on accept set `accepted`, then read `sdlc-design` and execute it |
| `intent.md` is `accepted`, no spec | `sdlc-design` |
| `spec.md` is `draft` | ask to approve; on approve set `specified`, then read `sdlc-apply` and execute it from the plan step |
| spec `specified`, no plan | `sdlc-apply` from the plan step |
| `plan.md` is `draft` | ask to approve; on approve set `planned`, then read `sdlc-apply` and execute it from the implement step |
| plan `planned`, boxes unticked | `sdlc-apply` implement step (coder), from the first unticked box — that skill runs isolated `sdlc-verify` after the last box |
| every box ticked, no `report.md` | isolated `sdlc-verify`: dispatch a verifier subagent (mandatory; not in-session judgment; never skip to archive) |
| `report.md` with `verdict: fail` or CRITICAL | `sdlc-apply` (fix findings), then isolated `sdlc-verify` (new subagent; not optional); do not archive |
| `verdict: pass`, no CRITICAL, statuses not `done` | ask to mark `done`; reviewer is a separate named agent |
| `report.md` `verdict: pass`, no CRITICAL, statuses `done` | `sdlc-archive` |

Report where the work stands as `N/M boxes ticked` when `plan.md` exists.
