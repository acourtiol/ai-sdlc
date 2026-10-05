---
name: sdlc-plan
description: >-
  Capture a new product change in its intent.md. Use for a feature or
  product change after exploration, before design or implementation.
license: MIT
metadata:
  author: acourtiol
  version: "2.8"
---

# sdlc-plan

Write `intent/<slug>/intent.md` from the user's idea, preserving their wording for the outcome. In a normal run, wait for acceptance; an explicitly authorized autonomous queue may accept an existing draft after the confidence assessment below. On acceptance, read `sdlc-design` and execute it.

Preserve requested capabilities as product outcomes: explicit automation, named providers or integrations, and requested data coverage stay requirements, not optional implementation details. Keep short decisive user wording or a source excerpt in Proposed outcome when it could be easy to lose. Do not move a requested outcome into Out of scope without explicit user acceptance; unrequested implementation non-goals may clarify the boundary. Autonomous approval cannot authorize reducing the outcome. If access, credentials, or a dependency is unavailable, record the blocker and continue useful authorized work, but leave the requested capability blocked until it is delivered or the user explicitly accepts a different outcome after seeing the tradeoff. For critical automation or integrations, include an observable end-to-end scenario; a manual fallback does not prove it.

Check added scope as well as missing scope. Additional screens, required inputs, acknowledgements, reconfirmation steps or gates beyond the requested flow are product decisions, not routine implementation details. Trace each to an explicit user request or an evidenced binding constraint in existing artifacts; broad autonomy, generic product goals and agent-authored requirements do not supply that authority. Autonomous approval cannot expand the accepted outcome. Keep necessary internal validation, security and error handling tied to the changed flow, but do not turn known external limits into an unrequested user ceremony. If a new product decision is genuinely needed and authority is missing, present the concrete tradeoff before implementing it. An agent-created guard is not justification for another feature needed solely to configure that guard. Size the solution to the stated users and deployment; do not assume organizational approval, compliance administration or future multi-user needs. Prefer the smallest design that delivers the complete requested behavior.

## Before you start

Resolve `assets/` and `scripts/` against this skill's installed directory supplied by the host, not the product repo. Commands use `python3` as an example; choose an available Python 3.8+ interpreter and quote resolved paths. Load a required next skill through the host or its installed `SKILL.md`; if it or its resources are unavailable, hand off at that gate rather than inventing them.

Triage before you write. A feasibility question is a spike: answer it, do not open an intent. A bounded bug or behavior-preserving refactor of an existing flow goes to `sdlc-fix`, without an intent. An intent is for work that changes what the product does. File count alone does not decide the path. Use `sdlc-explore` for a shapeless idea; when routing is ambiguous, take the heavier path. Record evidence of the problem or `not checked`.

Keep a small, well-understood new behavior compact within the same intent/spec/plan gates: one clear outcome and the few scenarios and steps needed to prove it. Do not create extra documents to make a small change look substantial. For a broad request, identify the earliest independently useful outcome and its actual prerequisites before bundling adjacent features. Prefer a complete user-visible delivery over a foundation spanning all future surfaces; shared infrastructure alone is not that outcome. Balance earlier usefulness against repeated review/migration/release cost. When the user authorizes decomposition, capture a bounded delivery intent referencing the existing parent outcome and remaining obligations; do not mark the parent complete or move its undelivered requirements out of scope. Do not create a child for every implementation box.

An active intent does not block capturing an independent request; honor explicit user sequencing and concurrency limits. Use separate intent paths/ownership and inspect dependencies or overlapping contracts/resources before assigning parallel implementation. Queue competing work for the same owner or mutable boundary; explicit reprioritization checkpoints that owner before switching. Keep one integration owner and serialized landing/release, without changing a candidate under review. Keep the interview and narrow source lookups here. Delegate bounded independent research only when parallel work or saved context outweighs startup and coordination. Reuse a researcher for related reads; provide paths and questions instead of the full conversation. Use completion notifications where available; otherwise wait meaningfully while doing independent work, without repeated status polling.

The workflow authorizes owned artifact commits unless the user or host restricts them. Before the first write, record the repository, branch, HEAD, staged paths, and working-tree/untracked paths. Reuse an owned checkout first; default new worktrees to `<agreed-project-workspace>/.worktrees/`. Never move a live checkout. If an affected file contains someone else's work or the index has unrelated staged changes, use a clean isolated worktree when feasible; otherwise stop the commit and explain the ownership conflict. Never reset, stash, or absorb unrelated work; stage only owned paths/hunks. Use Conventional Commits (`type(scope): imperative summary`, optional scope), a blank line, and a sentence on why; mark breaking changes with `!` or `BREAKING CHANGE:`. Do not push unless asked. A step that writes or edits and leaves those paths dirty is not done.

## Confidence and challenge

High confidence requires all four: explicit outcome/constraints; current-source support; evidence for relevant contracts and important failure modes; no unresolved material assumption or conflicting evidence. Privacy, migrations, concurrency, and irreversible behavior need stronger evidence. Agreement or a stated probability is insufficient.

Record confidence and evidence under Decision review for autonomous approval. At high confidence, skip the challenger. Otherwise send one fresh, read-only challenger the strongest unresolved assumption, check citations, resolve objections, and record residual uncertainty. Missing preference/authority needs the user. Carry valid evidence across gates; challenge only changed material uncertainty, with bounded repair follow-ups. Artifact edits still require reapproval and dependent digest reconciliation.

## Steps

1. Before the interview, read applicable instructions in the product repository and list `intent/*/` (skip `intent/archive/`); use those as constraints, do not copy them into `intent.md`. Read `context.md` if exploration left one; check relevant current claims against the repo. Keep only unresolved facts absent from the artifacts, next action, and evidence links; aim for 500–1,000 words or fewer. Preserve superseded detail in Git rather than copying its chronology forward. Then interview until the idea is concrete: what cannot be done today, what shows the problem is real (or `not checked`), who is affected, what better looks like, constraints, out of scope. Ask one question at a time when a missing answer would change the file.
2. Derive a kebab-case slug. If `intent/<slug>/` already has only `context.md` from exploration, reuse it. If it has an `intent.md`, pick another slug or hand off to `sdlc-continue`. If `intent/archive/*-<slug>/` exists, that name shipped before: say so and pick a slug that does not collide with the history. `intent/archive/` is the archive, never a slug.
3. Copy `assets/intent.md` into `intent/<slug>/intent.md`. Fill every section, including Evidence. Frontmatter starts with `status: draft`, `approved_by: pending`, and `approved_digest: pending`. Do not migrate existing consumer intents that lack Evidence. Remove from `context.md` anything now captured in `intent.md`; remove the file if nothing remains. Commit these edits before the next step.
4. Show the path and a short summary. Ask the user to accept (that starts Design) or to correct it. If they correct the file, commit that edit before you continue.
5. On acceptance set `approved_by: human`, compute `approved_digest` with `python3 <this-skill-dir>/scripts/fingerprint.py intent/<slug>/intent.md`, set `status: accepted`, and commit that edit. The digest covers the approved content while excluding the status and digest fields themselves. If the user's accepted outcome or constraints later change, return intent to `draft` and downstream spec and plan to `draft`; a previous report cannot close the changed work. Then immediately read `sdlc-design` and execute it unless told to stop.

An explicit autonomous run starts **after** an `intent.md` exists. `sdlc-continue` may accept its draft on standing authorization after the confidence assessment and any needed challenge. Set `approved_by: autonomous` before computing the digest. If required evidence or a needed challenger is unavailable, or no defensible choice fits the outcome, leave it draft and record the blocker. The orchestrator owns the decision; a research agent cannot grant authority.

Next: `sdlc-design`.
