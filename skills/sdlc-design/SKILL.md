---
name: sdlc-design
description: >-
  Writes intent/slug/spec.md from an accepted intent: requirements and design
  in one file. Use after the user accepts an intent, or when they ask for
  requirements, how it should work, a spec, or a design. The playbook collapsed
  requirements and design; there is no separate design.md. Planning only; do
  not implement. Commit spec.md in the same step that writes it; do not wait
  to be asked to commit. Do not push unless asked. On spec approve in this
  session, read sdlc-apply and execute it from the plan step.
license: MIT
metadata:
  author: acourtiol
  version: "1.5"
---

# sdlc-design

Write `intent/<slug>/spec.md` from an accepted intent. Wait for them to approve. On approve, read `sdlc-apply` and execute it from the plan step. Do not implement.

The playbook collapsed requirements and design into one session. The artifact is `spec.md`. Do not write a `design.md`.

## Before you start

Need `intent/<slug>/intent.md` with `status: accepted` (or an accept in this session). If it is still `draft`, go back to `sdlc-plan`. An existing draft spec may be resumed here; revise it rather than copying the template over it.

Using this skill is the user asking you to commit. Do not wait for a later message that says commit. A host rule that says commit only when asked is already satisfied. Stage only this concern. The message is an imperative subject, a blank line, and one sentence on why, passed with a heredoc. Do not push unless the user asks. A step that writes or edits and leaves those paths dirty is not done.

The named planner subagent is read-only. Dispatch it to research the codebase and return spec markdown. This session writes and commits the draft for the user's review; approval changes its status to `specified`. Use subagents to parallelize work and preserve context when it matters: independent research goes out together and comes back as findings, so this session keeps the draft and the approval gate. A narrow lookup stays here. If no subagent is available, research here, still present the draft, still wait. Implementing before approval skips the gate.

## Steps

1. Resolve slug (the user names it, or the only accepted intent with no spec or a draft spec).
2. Read `intent.md`, the existing `spec.md` if present, and any `context.md`; verify contextual claims against the repo and carry forward only unresolved facts relevant to the design. Dispatch planner (read-only): requirements and design that fit this repo, plus policy gotchas. Preserve valid decisions in an existing spec. Requirements come back as `### Requirement:` blocks, one SHALL statement each, every one carrying at least one `#### Scenario:` in WHEN / THEN form. Numeric, enum, and validation limits belong in a Scenario THEN, quoted verbatim, not only in Design. A scenario someone can read as a test case is what `sdlc-verify` checks against later.
3. Copy `assets/spec.md` into `intent/<slug>/spec.md` only when creating it; otherwise revise the existing draft. Keep `status: draft` until approval. Remove from `context.md` anything now captured in `spec.md`; remove the file if nothing remains. Commit these edits before the next step.
4. Before asking for approval, check whether any unresolved choice could materially change architecture, safety behavior, or acceptance criteria. Research answers available in the repo. For a decision only the user can make, ask one question at a time, revise and commit the draft, then check again. An explicit proposed default may be approved with the spec if called out; an owner alone is not enough. Lower-impact questions may carry forward with an owner or default. Ask the user to approve the ready spec (that starts Build) or correct it. Commit corrections before continuing.
5. On approve, set `status: specified` and commit that edit. Then immediately read `sdlc-apply` and execute it from the plan step. If they approve but tell you to stop there, stop. The approve commit still happens.

If a previously `specified` spec needs a blocking correction, return it to `draft` and commit the revision. If a plan already exists, return its status to `draft` in the same commit: its approval depended on the old spec. After spec reapproval, `sdlc-apply` must reconcile and reapprove that plan before implementation resumes.

Next: `sdlc-apply`.
