---
name: sdlc-design
description: >-
  Write requirements and design in spec.md after an accepted
  intent. Use when the user requests a spec or design for an existing intent.
license: MIT
metadata:
  author: acourtiol
  version: "2.5"
---

# sdlc-design

Write `intent/<slug>/spec.md` from an accepted intent. In a normal run, wait for approval; an explicitly authorized autonomous queue may approve after the confidence assessment below. On approval, read `sdlc-apply` and execute it from the plan step. Do not implement.

Keep requirements and design in `spec.md`. Do not write a `design.md`. Trace the accepted outcome and each material constraint to observable requirements/scenarios; use the user's concrete examples and limits where provided. Do not silently replace the wanted behavior with an easier implementation. Carry missing product decisions forward for resolution, not invented defaults.

## Before you start

Resolve `assets/` and `scripts/` against this skill's installed directory supplied by the host, not the product repo. Commands use `python3` as an example; choose an available Python 3.8+ interpreter and quote resolved paths. Load a required next skill through the host or its installed `SKILL.md`; if it or its resources are unavailable, hand off at that gate rather than inventing them.

Need `intent/<slug>/intent.md` with `status: accepted` (or an accept in this session). If it is still `draft`, go back to `sdlc-plan`. An existing draft spec may be resumed here; revise it rather than copying the template over it.

The workflow authorizes owned artifact commits unless the user or host restricts them. Before writing, record the repository, branch, HEAD, staged paths, and working-tree/untracked paths. Use a clean isolated worktree if existing work would overlap or be absorbed; otherwise stop the commit and explain the conflict. Never reset or stash someone else's changes. Stage only this concern. Use Conventional Commits (`type(scope): imperative summary`, optional scope), a blank line, and a sentence on why; mark breaking changes with `!` or `BREAKING CHANGE:`. Do not push unless asked.

Keep code implementation to one active lane per product repo; parallel design research is read-only, and added requests do not start another writer. Write a straightforward spec here. Delegate bounded read-only research when substantial independent work justifies the handoff; use its evidence to write the artifact here. Reuse researchers for related questions, pass bounded inputs, and use completion notifications instead of repeatedly polling. A normal run waits for human approval; autonomous approval follows the confidence rule below.

## Confidence and challenge

High confidence requires all four: explicit outcome/constraints; current-source support; evidence for relevant contracts and important failure modes; no unresolved material assumption or conflicting evidence. Privacy, migrations, concurrency, and irreversible behavior need stronger evidence. Agreement or a stated probability is insufficient.

Record confidence and evidence under Decision review for autonomous approval. At high confidence, skip the challenger. Otherwise send one fresh, read-only challenger the strongest unresolved assumption, check citations, resolve objections, and record residual uncertainty. Missing preference/authority needs the user. Carry valid evidence across gates; challenge only changed material uncertainty, with bounded repair follow-ups. Artifact edits still require reapproval and dependent digest reconciliation.

## Steps

1. Resolve slug (the user names it, or the only accepted intent with no spec or a draft spec).
2. Read `intent.md`, the existing `spec.md` if present, and any `context.md`; verify contextual claims against the product repository and carry forward only unresolved facts relevant to the design. Prepare requirements, design, and applicable policy gotchas here, using bounded read-only research when justified. Preserve valid decisions in an existing spec; replace superseded rationale instead of appending review chronology. Check prerequisite contracts/migrations and the intended delivery baseline in Design/Gotchas before choosing an approach; label unrequested release proof as outstanding, not implicit permission. Use `### Requirement:` blocks with one SHALL each and at least one `#### Scenario:` in WHEN / THEN form. Quote numeric/enum/validation limits verbatim in Scenario THEN, not only Design; these scenarios are the verifier's test cases.
3. Copy `assets/spec.md` into `intent/<slug>/spec.md` only when creating it; otherwise revise the existing draft. Keep `status: draft` until approval. Set `intent_digest` to the current accepted intent's `approved_digest`; a mismatch means the intent changed and must be reconciled first. Compact `context.md` to unresolved facts absent from the artifacts, next action, and evidence links; aim for 500–1,000 words or fewer. Remove transferred or superseded entries, preserving history in Git; remove the file if empty. Commit these edits before the next step.
4. Before approval, check unresolved choices that could materially change architecture, safety behavior, or acceptance criteria. Research answers available in the repo. In a normal run, ask the user about decisions that only they can make, revise and commit the draft, then seek approval. An explicit proposed default may be accepted in the spec review; an owner alone is insufficient. Lower-impact questions may carry an owner or default.
5. In an autonomous run, assess confidence for new or changed material decisions. Record supporting evidence and any needed challenge under Decision review. Keep established decisions unless current evidence invalidates them; do not challenge them again just because this is a new gate. If a choice needs missing preference, authority, or evidence, leave the spec draft and record the blocker for the queue.
6. On human approval or a completed autonomous decision review, set `approved_by: human` or `autonomous`, compute `approved_digest` with `python3 <this-skill-dir>/scripts/fingerprint.py intent/<slug>/spec.md`, set `status: specified`, and commit. Then read `sdlc-apply` and execute it from the plan step. A material spec edit after this point reopens spec and plan to `draft` and invalidates a prior passing report. Recompute dependent digests only after reconciling and reapproving. If the user tells you to stop after approval, stop.

If a previously `specified` spec needs a blocking correction, return it to `draft` and commit the revision. If a plan already exists, return its status to `draft` in the same commit. After spec reapproval, `sdlc-apply` must reconcile and reapprove the plan before implementation resumes.

Next: `sdlc-apply`.
