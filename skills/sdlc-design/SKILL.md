---
name: sdlc-design
description: >-
  Writes intent/slug/spec.md from an accepted intent: requirements and design
  in one file. Use after the user accepts an intent, or when they ask for a
  spec or design. The Anthropic playbook has no separate design.md. Planning
  only; do not implement.
license: MIT
metadata:
  author: acourtiol
  version: "1.1"
---

# sdlc-design

Write `intent/<slug>/spec.md` from an accepted intent. Stop so they can approve. Leave plan and code for `sdlc-apply`.

Anthropic collapsed requirements and design into one session. The artifact is `spec.md`. Do not write a `design.md`. That filename is OpenSpec, not this playbook.

## Before you start

If `openspec/` has open changes, stop and use OpenSpec (`openspec` binary, never `npx openspec`).

Need `intent/<slug>/intent.md` with `status: accepted` (or an accept in this session). If it is still `draft`, go back to `sdlc-plan`.

Do not commit unless the user asks.

The named planner subagent is read-only. Dispatch it to research the codebase and return spec markdown. This session writes the file after the user approves. If no subagent is available, research here, still present the draft, still wait. Writing too early skips the gate.

## Steps

1. Resolve slug (the user names it, or the only accepted intent that has no spec).
2. Read `intent.md`. Dispatch planner (read-only): requirements and design that fit this repo, plus policy gotchas.
3. Copy `assets/spec.md` into `intent/<slug>/spec.md` when the draft is complete. Keep `status: draft` until they approve.
4. Ask the user to approve the spec (that starts Build) or to correct it.
5. On approve, set `status: specified`. Do not start `sdlc-apply` unless they ask.

Next: `sdlc-apply`.
