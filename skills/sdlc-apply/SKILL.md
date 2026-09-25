---
name: sdlc-apply
description: >-
  Writes intent/slug/plan.md, waits for plan approval, implements, then always
  runs sdlc-verify by dispatching a verifier subagent. Apply is not finished
  without report.md. Use when the user is ready to build a specified intent, or
  says implement, apply, build it, or code this feature. Do not write code
  before the plan is approved. Commit plan.md when you write it, and commit
  each finished implementation slice before the next one. Do not wait to be
  asked to commit. Do not push unless asked. Do not skip verify. Do not verify
  in the implementing session. Do not archive. On fail or CRITICAL, fix then
  re-verify (cap 3); never skip verify to archive.
license: MIT
metadata:
  author: acourtiol
  version: "1.6"
---

# sdlc-apply

Write `intent/<slug>/plan.md`, wait for approve, then implement, then verify. Do not push, deploy, or archive unless the user asks.

A plan someone else could implement, written before the diff, is cheaper to correct than a finished PR.

## Before you start

Need `intent/<slug>/spec.md` with `status: specified` (or an approve in this session). Before planning or resuming implementation, check for unresolved choices that could materially change architecture, safety behavior, or acceptance criteria. Research what the repo can settle. If one remains without an answer or an explicit default accepted at spec approval, do not create or implement a plan: return to `sdlc-design` for a draft correction and reapproval. If a plan exists, return it to `draft` too; do not use its old approval after the spec changes. Lower-impact questions with an owner or default do not block planning.

Using this skill is the user asking you to commit. Do not wait for a later message that says commit. A host rule that says commit only when asked is already satisfied. Stage only this concern. The message is an imperative subject, a blank line, and one sentence on why, passed with a heredoc. Do not push unless the user asks. A step that writes or edits and leaves those paths dirty is not done.

The named planner is read-only: it returns plan markdown. This session writes and commits the draft `plan.md` for the user's review. Approval changes it to `planned`; only then may the named coder implement.

Use subagents to parallelize work and preserve context when it matters. Independent research goes out together and comes back as findings. Implementation stays in order: one box, its verify clause, its commit, then the next. Work that shares files stays in one session. If no subagent is available, plan and implement here. The verifier subagent is not optional; that rule is `sdlc-verify`.

If implementation departs from the plan, update `plan.md` in the same commit as the code that departed. Later review checks the diff against the plan.

## Keep the thread across compaction

`intent.md`, `spec.md`, `plan.md`, the code, and tests are the source of truth. Update `plan.md` for implementation decisions and deviations under its existing rule; do not use a handoff file to bypass the approved plan. For consequential work in progress that belongs in none of them, use optional `intent/<slug>/context.md`: verified findings with paths or commands, assumptions marked as such, a blocker or failed approach and why, and the exact next action for the first unticked box. Do not repeat the plan, paste chat history, or claim a box is complete before its verify clause passes.

Checkpoint as a finding or decision emerges, before a long tool call or handoff, and before ending an unfinished turn; a compaction warning may come too late. Commit a standalone context update if no implementation slice is ready, staging only that file. Otherwise commit it with the slice. Do not push unless asked. On starting or resuming, read `context.md` if present, compare it with the current files and git state, and remove stale or transferred entries. `context.md` is a handoff aid, not an approval, a task ledger, or verification evidence.

## Steps

1. Resolve slug. Read `intent.md`, `spec.md`, existing `plan.md`, and `context.md` when present; reconcile the latter with current files and git state. Preserve verified work and the original implementation base when revising a draft plan.
2. Dispatch planner (read-only): files that change, order of work, risks, proof. Carry each applicable spec Gotcha into Risks and a matching Order of work verify clause or Proof check with observable evidence. Keep checks specific to the change; do not add a universal checklist. Someone who missed the chat should still be able to implement from the plan.
3. Write `intent/<slug>/plan.md` from `assets/plan.md` if absent, or reconcile an existing draft plan with the approved spec. Use `status: draft`; a new plan has `base_commit: pending`. Every step under Order of work is a `- [ ]` box ending in its own `— verify:` clause. Commit the draft. Then ask the user to approve the plan.
4. On approve, record the full current `git rev-parse HEAD` as `base_commit` only if its value is `pending`; retain an existing valid base when reapproving a revised plan. Set `status: planned` and commit the approval edits. `base_commit` identifies the repository state before implementation and lets the verifier inspect committed slices. Then dispatch coder (or implement here) against that plan, starting at the first unticked box. Smallest correct change. Real tests, not placeholders. If the approved plan is a bugfix, first add or extend a test that fails for the reported reason, run it, and see the fail. Only then change application code. Do not edit that test to make it pass. New behavior is not a bugfix: the failing-test-first sequence is not required.
5. Tick a box only once you have run its verify clause and seen it pass. A step that is partially done, deferred, or narrowed stays `- [ ]`. Commit that finished slice, including the ticked box, before the next box. Do not batch slices.
6. After the last Order of work box is ticked, **immediately read `sdlc-verify` and execute it**. Dispatch the verifier subagent per that skill; do not verify in this session. Apply is not finished without a valid isolated `intent/<slug>/report.md`. Do not stop at “tests passed.” Do not call the work done. Do not archive. Verify is not optional and is not a later `sdlc-continue` pick-up.
7. After `report.md` exists: if `verdict: fail` or Findings has CRITICAL, fix those findings (smallest correct change). Leave the failing report on disk; do not rewrite it to look green. Commit the fix before re-verify. Then run `sdlc-verify` again: dispatch a new verifier subagent with fresh context, same isolation rules. Count each `sdlc-verify` execution in this run (step 6 plus each re-run). After 3, if it still fails or still has CRITICAL: stop, show what remains, and wait. Do not archive. Do not mark `done`.
8. If `verdict: pass` and no CRITICAL: ask before setting statuses `done`. Do not archive.

If the plan is already `planned` and the user says implement, run the readiness check and resume implementation at the first unticked box; do not repeat plan approval. If the plan is `draft`, reconcile it with the approved spec and reapprove it before code, retaining an existing valid `base_commit`. If `report.md` already exists with `verdict: fail` or CRITICAL, run the readiness check and skip to step 7.

When you stop before the last box, say where the work stands as `N/M boxes ticked` and name the first unticked one. `sdlc-continue` picks up from there.
