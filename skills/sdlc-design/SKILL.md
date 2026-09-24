---
name: sdlc-design
description: >-
  Writes intent/slug/spec.md from an accepted intent: requirements and design
  in one file. Use after the user accepts an intent, or when they ask for
  requirements, how it should work, a spec, or a design. The playbook collapsed
  requirements and design; there is no separate design.md. Planning only; do
  not implement. On spec approve in this session, read sdlc-apply and execute
  it from the plan step.
license: MIT
metadata:
  author: acourtiol
  version: "1.4"
---

# sdlc-design

Write `intent/<slug>/spec.md` from an accepted intent. Wait for them to approve. On approve, read `sdlc-apply` and execute it from the plan step. Do not implement.

The playbook collapsed requirements and design into one session. The artifact is `spec.md`. Do not write a `design.md`.

## Before you start

Need `intent/<slug>/intent.md` with `status: accepted` (or an accept in this session). If it is still `draft`, go back to `sdlc-plan`.

Commit `intent/<slug>/spec.md` on its own when you write it, and again when a later edit changes it. One concern per commit. The message says why. Do not push unless the user asks.

The named planner subagent is read-only. Dispatch it to research the codebase and return spec markdown. This session writes the file after the user approves. If no subagent is available, research here, still present the draft, still wait. Writing too early skips the gate.

## Steps

1. Resolve slug (the user names it, or the only accepted intent that has no spec).
2. Read `intent.md`. Dispatch planner (read-only): requirements and design that fit this repo, plus policy gotchas. Requirements come back as `### Requirement:` blocks, one SHALL statement each, every one carrying at least one `#### Scenario:` in WHEN / THEN form. Numeric, enum, and validation limits belong in a Scenario THEN, quoted verbatim, not only in Design. A scenario someone can read as a test case is what `sdlc-verify` checks against later.
3. Copy `assets/spec.md` into `intent/<slug>/spec.md` when the draft is complete. Keep `status: draft` until they approve.
4. Ask the user to approve the spec (that starts Build) or to correct it.
5. On approve, set `status: specified`. Then immediately read `sdlc-apply` and execute it from the plan step. If they approve but tell you to stop there, stop.

Next: `sdlc-apply`.
