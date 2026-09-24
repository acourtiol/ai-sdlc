---
name: sdlc-apply
description: >-
  Writes intent/slug/plan.md, waits for plan approval, implements, then always
  runs sdlc-verify by dispatching a verifier subagent. Apply is not finished
  without report.md. Use when the user is ready to build a specified intent, or
  says implement, apply, build it, or code this feature. Do not write code
  before the plan is approved. Do not skip verify. Do not verify in the
  implementing session. Do not archive. On fail or CRITICAL, fix then re-verify
  (cap 3); never skip verify to archive.
license: MIT
metadata:
  author: acourtiol
  version: "1.5"
---

# sdlc-apply

Write `intent/<slug>/plan.md`, wait for approve, then implement, then verify. Do not push, deploy, or archive unless the user asks.

A plan someone else could implement, written before the diff, is cheaper to correct than a finished PR.

## Before you start

Need `intent/<slug>/spec.md` with `status: specified` (or an approve in this session).

Do not commit unless the user asks.

The named planner is read-only: it returns plan markdown. This session writes `plan.md` after the user approves. The named coder implements only after `plan.md` is `planned`.

If implementation departs from the plan, update `plan.md` in the same change (same commit if they asked to commit). Later review checks the diff against the plan.

## Steps

1. Resolve slug. Read `intent.md` and `spec.md`.
2. Dispatch planner (read-only): files that change, order of work, risks, proof. Someone who missed the chat should still be able to implement from the plan.
3. Write `intent/<slug>/plan.md` from `assets/plan.md` (`status: draft`). Every step under Order of work is a `- [ ]` box ending in its own `— verify:` clause. Ask the user to approve the plan.
4. On approve, set `status: planned`. Then dispatch coder (or implement here) against that plan, starting at the first unticked box. Smallest correct change. Real tests, not placeholders. If the approved plan is a bugfix, first add or extend a test that fails for the reported reason, run it, and see the fail. Only then change application code. Do not edit that test to make it pass. New behavior is not a bugfix: the failing-test-first sequence is not required.
5. Tick a box only once you have run its verify clause and seen it pass. A step that is partially done, deferred, or narrowed stays `- [ ]`.
6. After the last Order of work box is ticked, **immediately read `sdlc-verify` and execute it**. Dispatch the verifier subagent per that skill; do not verify in this session. Apply is not finished without a valid isolated `intent/<slug>/report.md`. Do not stop at “tests passed.” Do not call the work done. Do not archive. Verify is not optional and is not a later `sdlc-continue` pick-up.
7. After `report.md` exists: if `verdict: fail` or Findings has CRITICAL, fix those findings (smallest correct change). Leave the failing report on disk; do not rewrite it to look green. Then run `sdlc-verify` again: dispatch a new verifier subagent with fresh context, same isolation rules. Count each `sdlc-verify` execution in this run (step 6 plus each re-run). After 3, if it still fails or still has CRITICAL: stop, show what remains, and wait. Do not archive. Do not mark `done`.
8. If `verdict: pass` and no CRITICAL: ask before setting statuses `done`. Do not archive.

If the plan is already `planned` and the user says implement, skip to step 4. If `report.md` already exists with `verdict: fail` or CRITICAL, skip to step 7.

When you stop before the last box, say where the work stands as `N/M boxes ticked` and name the first unticked one. `sdlc-continue` picks up from there.
