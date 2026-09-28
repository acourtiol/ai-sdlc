---
name: sdlc-apply
description: >-
  Plan and implement a specified intent, then hand it to independent
  verification. Use when the user asks to build an accepted product change.
license: MIT
metadata:
  author: acourtiol
  version: "2.0"
---

# sdlc-apply

Write `intent/<slug>/plan.md`, obtain the applicable approval, implement, then verify. Do not push or deploy unless the user asks. Archive only through `sdlc-archive` after valid completion.

A plan someone else could implement, written before the diff, is cheaper to correct than a finished PR.

## Before you start

Need `intent/<slug>/spec.md` with `status: specified` (or an approve in this session). Before planning or resuming implementation, check for unresolved choices that could materially change architecture, safety behavior, or acceptance criteria. Research what the repo can settle. If one remains without an answer or an explicit default accepted at spec approval, do not create or implement a plan: return to `sdlc-design` for a draft correction and reapproval. If a plan exists, return it to `draft` too; do not use its old approval after the spec changes. Lower-impact questions with an owner or default do not block planning.

Invoking this workflow normally authorizes commits for its own artifacts and verified implementation slices, subject to explicit user restrictions and host policy. Before writing, record repository, branch, HEAD, staged paths, and working-tree/untracked paths. Use a clean isolated worktree if existing work could be absorbed or overlap; otherwise stop the commit and explain the conflict. Never reset or stash someone else's changes. Stage only owned paths or hunks. Use an imperative commit subject, a blank line, and one sentence on why. Do not push unless asked.

The named planner is read-only: it returns plan markdown. This session writes and commits the draft `plan.md`. Approval changes it to `planned`; only then may implementation begin. A normal run waits for the user. An explicitly authorized autonomous run follows the decision review below.

Use subagents for independent research when their benefit exceeds coordination cost. Implementation stays in order: one box, its verify clause, its commit, then the next. Work that shares files stays in one session. Independent verification requires a fresh subagent or a separate fresh session under `sdlc-verify`; the implementing session cannot supply a passing verdict.

If implementation needs a material change to the approved plan's steps, scope, risk response, or proof, reopen the plan to `draft` and seek fresh human or authorized autonomous approval before implementing that change. A small execution detail can be recorded as a deviation in the report without changing the approved plan. Do not hide a material change as a routine deviation.

## Keep the thread across compaction

`intent.md`, `spec.md`, `plan.md`, the code, and tests are the source of truth. Update `plan.md` for implementation decisions and deviations under its existing rule; do not use a handoff file to bypass the approved plan. For consequential work in progress that belongs in none of them, use optional `intent/<slug>/context.md`: verified findings with paths or commands, assumptions marked as such, a blocker or failed approach and why, and the exact next action for the first unticked box. Do not repeat the plan, paste chat history, or claim a box is complete before its verify clause passes.

Checkpoint as a finding or decision emerges, before a long tool call or handoff, and before ending an unfinished turn; a compaction warning may come too late. Commit a standalone context update if no implementation slice is ready, staging only that file. Otherwise commit it with the slice. Do not push unless asked. On starting or resuming, read `context.md` if present, compare it with the current files and git state, and remove stale or transferred entries. `context.md` is a handoff aid, not an approval, a task ledger, or verification evidence.

## Steps

1. Resolve slug. Read `intent.md`, `spec.md`, existing `plan.md`, and `context.md` when present; reconcile the latter with current files and git state. Preserve verified work and the original implementation base when revising a draft plan.
2. Dispatch planner (read-only): files that change, order of work, risks, proof. Carry each applicable spec Gotcha into Risks and a matching Order of work verify clause or Proof check with observable evidence. Keep checks specific to the change; do not add a universal checklist. Someone who missed the chat should still be able to implement from the plan.
3. Write `intent/<slug>/plan.md` from `assets/plan.md` if absent, or reconcile an existing draft plan with the approved spec. Use `status: draft`; a new plan has `base_commit: pending`. Set `spec_digest` to the approved spec digest. Every step under Order of work is a `- [ ]` box ending in its own `— verify:` clause. Proof should include any relevant rollout prerequisite, migration, recovery, and post-release observation; archive closes the change record, not the release. Commit the draft.
4. Before implementation, confirm that this host can arrange a fresh subagent verifier or an explicit separate fresh-session handoff with the same artifact inputs. Record the route and required environment in the plan's Review route section. For an unattended run, a verifier must be dispatchable within the run; otherwise mark the slug blocked before code. Confirm a clean committed implementation checkout can be provided for verification. In a normal run, ask the user to approve the plan. In an autonomous run, give a fresh read-only research subagent the intent, spec, draft plan, and relevant source; ask for the strongest counterargument, alternative, failure case, and falsifying evidence for material choices. Check cited evidence, record the decision and remaining uncertainty under Decision review, and block the slug only if no defensible decision fits the authorized outcome.
5. On approval, record the full current `git rev-parse HEAD` as `base_commit` only if its value is `pending`; retain an existing valid base when reapproving a revised plan. Set `approved_by: human` or `autonomous`, compute `approved_digest` with `python3 <this-skill-dir>/scripts/fingerprint.py intent/<slug>/plan.md`, set `status: planned`, and commit. The digest normalizes task checkbox state but binds task text, proof, risks, dependency digest, and base commit. Then implement from the first unticked box. For a bugfix, establish a failing reproduction before changing application code when practical; never edit a test merely to manufacture a pass.
6. Tick a box only once you have run its verify clause and seen it pass. A step partially done, deferred, or narrowed stays `- [ ]`. Commit that finished slice, including the ticked box, before the next box. Do not batch slices.
7. After the last box, immediately run `sdlc-verify` in an independent review context. Require clean committed in-scope implementation and a report bound to the reviewed HEAD and approved artifact digests. Do not call the work done from test results alone.
8. If the report fails or has CRITICAL, fix the findings and commit before re-verification. Leave the failing report as recorded history until the new verifier replaces it with a new result; do not edit it to flip a verdict. Count prior failed attempts visible in Git history as well as this run, and change an ineffective repair strategy rather than repeating it. After three attempts for the same unresolved issue, stop that slug with concrete findings. A blocked verification is a capability or environment recovery task, not evidence of incorrect behavior; do not mark done or archive.
9. On a valid fresh pass, a normal run asks before marking statuses `done`. An explicitly authorized autonomous run may set them to `done` and invoke `sdlc-archive` after its deterministic check passes.

If the plan is already `planned` and the user says implement, run the readiness and freshness checks and resume at the first unticked box. If it is `draft`, reconcile and reapprove before code, retaining an existing valid `base_commit`. If a report already failed or has CRITICAL, use step 8.

When you stop before the last box, say where the work stands as `N/M boxes ticked` and name the first unticked one. `sdlc-continue` picks up from there.
