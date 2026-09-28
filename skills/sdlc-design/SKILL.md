---
name: sdlc-design
description: >-
  Write requirements and design in intent/<slug>/spec.md after an accepted
  intent. Use when the user requests a spec or design for an existing intent.
license: MIT
metadata:
  author: acourtiol
  version: "2.1"
---

# sdlc-design

Write `intent/<slug>/spec.md` from an accepted intent. In a normal run, wait for approval; an explicitly authorized autonomous queue may approve after its independent decision review. On approval, read `sdlc-apply` and execute it from the plan step. Do not implement.

Keep requirements and design in `spec.md`. Do not write a `design.md`.

## Before you start

Need `intent/<slug>/intent.md` with `status: accepted` (or an accept in this session). If it is still `draft`, go back to `sdlc-plan`. An existing draft spec may be resumed here; revise it rather than copying the template over it.

Invoking this workflow normally authorizes commits for its own artifacts, subject to explicit user restrictions and host policy. Before writing, record the repository, branch, HEAD, staged paths, and working-tree/untracked paths. Use a clean isolated worktree if existing work would overlap or be absorbed; otherwise stop the commit and explain the conflict. Never reset or stash someone else's changes. Stage only this concern. Use an imperative commit subject, a blank line, and one sentence on why. Do not push unless asked.

The named planner subagent is read-only. Dispatch it to research the codebase and return spec markdown. This session writes and commits the draft. Use subagents for independent research when their benefit exceeds coordination cost. A normal run waits for human approval. An explicitly authorized autonomous run uses the decision review below.

## Steps

1. Resolve slug (the user names it, or the only accepted intent with no spec or a draft spec).
2. Read `intent.md`, the existing `spec.md` if present, and any `context.md`; verify contextual claims against the product repository and carry forward only unresolved facts relevant to the design. Dispatch planner (read-only): requirements and design that fit the product repository, plus policy gotchas. Preserve valid decisions in an existing spec. Requirements come back as `### Requirement:` blocks, one SHALL statement each, every one carrying at least one `#### Scenario:` in WHEN / THEN form. Numeric, enum, and validation limits belong in a Scenario THEN, quoted verbatim, not only in Design. A scenario someone can read as a test case is what `sdlc-verify` checks against later.
3. Copy `assets/spec.md` into `intent/<slug>/spec.md` only when creating it; otherwise revise the existing draft. Keep `status: draft` until approval. Set `intent_digest` to the current accepted intent's `approved_digest`; a mismatch means the intent changed and must be reconciled first. Remove from `context.md` anything now captured in `spec.md`; remove the file if nothing remains. Commit these edits before the next step.
4. Before approval, check unresolved choices that could materially change architecture, safety behavior, or acceptance criteria. Research answers available in the repo. In a normal run, ask the user about decisions that only they can make, revise and commit the draft, then seek approval. An explicit proposed default may be accepted in the spec review; an owner alone is insufficient. Lower-impact questions may carry an owner or default.
5. In an autonomous run, give a fresh, read-only research subagent the intent, draft spec, relevant source, and decision under review. Ask for the strongest counterargument, alternative, failure case, and evidence that could falsify the proposal. Check its citations against source. Record the choice, counterargument, evidence, dissent, and residual uncertainty under Decision review. The orchestrator chooses a defensible option within the accepted intent; agreement among agents is not proof. If a choice needs a preference or authority absent from the intent, leave the spec draft, record the blocker, and let the queue continue to another independent intent.
6. On human approval or a completed autonomous decision review, set `approved_by: human` or `autonomous`, compute `approved_digest` with `python3 <this-skill-dir>/scripts/fingerprint.py intent/<slug>/spec.md`, set `status: specified`, and commit. Then read `sdlc-apply` and execute it from the plan step. A material spec edit after this point reopens spec and plan to `draft` and invalidates a prior passing report. Recompute dependent digests only after reconciling and reapproving. If the user tells you to stop after approval, stop.

If a previously `specified` spec needs a blocking correction, return it to `draft` and commit the revision. If a plan already exists, return its status to `draft` in the same commit. After spec reapproval, `sdlc-apply` must reconcile and reapprove the plan before implementation resumes.

Next: `sdlc-apply`.
