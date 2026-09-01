---
name: sdlc-apply
description: >-
  Writes intent/slug/plan.md, waits for plan approval, then implements. Use
  when the user is ready to build a specified intent, or says implement, apply,
  or code this feature. Do not write code before the plan is approved.
license: MIT
metadata:
  author: acourtiol
  version: "1.1"
---

# sdlc-apply

Write `intent/<slug>/plan.md`, wait for approve, then implement. Stop at test and review. Do not push or deploy unless the user asks.

A plan someone else could implement, written before the diff, is cheaper to correct than a finished PR.

## Before you start

If `openspec/` has open changes, stop and use OpenSpec (`openspec` binary, never `npx openspec`).

Need `intent/<slug>/spec.md` with `status: specified` (or an approve in this session).

Do not commit unless the user asks.

The named planner is read-only: it returns plan markdown. This session writes `plan.md` after the user approves. The named coder implements only after `plan.md` is `planned`.

If implementation departs from the plan, update `plan.md` in the same change (same commit if they asked to commit). Later review checks the diff against the plan.

Do not add `production-gate.sh` or `bands.yaml` here. Those belong in a product repo that asked for a deploy hook.

## Steps

1. Resolve slug. Read `intent.md` and `spec.md`.
2. Dispatch planner (read-only): files that change, order of work, risks, proof. Someone who missed the chat should still be able to implement from the plan.
3. Write `intent/<slug>/plan.md` from `assets/plan.md` (`status: draft`). Ask the user to approve the plan.
4. On approve, set `status: planned`. Then dispatch coder (or implement here) against that plan. Smallest correct change. Real tests, not placeholders.
5. After code, `sdlc-verify` is next. Do not call the work done without evidence.

If the plan is already `planned` and the user says implement, skip to step 4.
