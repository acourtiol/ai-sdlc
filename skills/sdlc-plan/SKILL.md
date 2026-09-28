---
name: sdlc-plan
description: >-
  Capture a new product change as intent/<slug>/intent.md. Use for a feature or
  product change after exploration, before design or implementation.
license: MIT
metadata:
  author: acourtiol
  version: "2.1"
---

# sdlc-plan

Write `intent/<slug>/intent.md` from the user's idea. In a normal run, wait for acceptance; an explicitly authorized autonomous queue may accept an existing draft after its independent decision review. On acceptance, read `sdlc-design` and execute it.

The originator should see their own words in the file. A proto-spec they can correct is faster than a ticket they did not write.

## Before you start

Triage before you write. A feasibility question is a spike: answer it, do not open an intent. A bounded bug or behavior-preserving refactor of an existing flow goes to `sdlc-fix`, without an intent. An intent is for work that changes what the product does. File count alone does not decide the path. When two readings are plausible, take the heavier one. If the idea is still shapeless, `sdlc-explore` first. Ask what shows the problem is real, or write `not checked`, even if explore was skipped.

Keep a small, well-understood new behavior compact within the same intent/spec/plan gates: one clear outcome and the few scenarios and steps needed to prove it. Do not create extra documents to make a small change look substantial.

Use subagents to parallelize work and preserve context when it matters. The interview stays in this session. Independent codebase reads that would bury it go out and come back as findings. If no subagent is available, read here.

Invoking this workflow normally authorizes commits for its own artifacts, subject to explicit user restrictions and host policy. Before the first write, record the repository, branch, HEAD, staged paths, and working-tree/untracked paths. If an affected file contains someone else's work or the index has unrelated staged changes, use a clean isolated worktree when feasible; otherwise stop the commit and explain the ownership conflict. Never reset, stash, or absorb that work. Stage only this concern. Use an imperative commit subject, a blank line, and one sentence on why. Do not push unless asked. A step that writes or edits and leaves those paths dirty is not done.

## Steps

1. Before the interview, read applicable instructions in the product repository and list `intent/*/` (skip `intent/archive/`); use those as constraints, do not copy them into `intent.md`. Read `context.md` if exploration left one for this idea; verify its claims against the repo and use only what is still current. Then interview until the idea is concrete: what cannot be done today, what shows the problem is real (or `not checked`), who is affected, what better looks like, constraints, out of scope. Ask one question at a time when a missing answer would change the file.
2. Derive a kebab-case slug. If `intent/<slug>/` already has only `context.md` from exploration, reuse it. If it has an `intent.md`, pick another slug or hand off to `sdlc-continue`. If `intent/archive/*-<slug>/` exists, that name shipped before: say so and pick a slug that does not collide with the history. `intent/archive/` is the archive, never a slug.
3. Copy `assets/intent.md` into `intent/<slug>/intent.md`. Fill every section, including Evidence. Frontmatter starts with `status: draft`, `approved_by: pending`, and `approved_digest: pending`. Do not migrate existing consumer intents that lack Evidence. Remove from `context.md` anything now captured in `intent.md`; remove the file if nothing remains. Commit these edits before the next step.
4. Show the path and a short summary. Ask the user to accept (that starts Design) or to correct it. If they correct the file, commit that edit before you continue.
5. If they accept in this session, set `approved_by: human`, compute `approved_digest` with `python3 <this-skill-dir>/scripts/fingerprint.py intent/<slug>/intent.md`, set `status: accepted`, and commit that edit. The digest covers the approved content while excluding the status and digest fields themselves. If the user's accepted outcome or constraints later change, return intent to `draft` and downstream spec and plan to `draft`; a previous report cannot close the changed work. Then immediately read `sdlc-design` and execute it unless told to stop.

An explicit autonomous run starts **after** an `intent.md` exists. `sdlc-continue` may accept its draft intent on the user's standing authorization, but only after a fresh research subagent challenges material decisions and the orchestrator records its evidence, objections, and resolution under Decision review. Set `approved_by: autonomous` before computing the digest. If the challenge cannot be performed or no defensible choice fits the stated outcome, leave it draft and mark that slug blocked for the queue. The research agent advises; it does not grant authority.

Next: `sdlc-design`.
