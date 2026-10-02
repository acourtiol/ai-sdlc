---
name: sdlc-apply
description: >-
  Plan and implement a specified intent, then hand it to independent
  verification. Use when the user asks to build an accepted product change.
license: MIT
metadata:
  author: acourtiol
  version: "2.3"
---

# sdlc-apply

Write `intent/<slug>/plan.md`, obtain the applicable approval, implement, then verify. Do not push or deploy unless the user asks. Archive only through `sdlc-archive` after valid completion.

## Before you start

Need `intent/<slug>/spec.md` with `status: specified` or session approval. Resolve choices that could change architecture, safety, or acceptance before planning/resuming. Research repo answers; a remaining material choice needs an answer or explicitly approved default. Otherwise return to design for correction/reapproval, reopening an existing plan to `draft` too. Lower-impact questions with an owner/default do not block.

The workflow authorizes owned artifact and verified slice commits unless the user/host restricts them. Before writing, record repo, branch, HEAD, staged and dirty/untracked paths. Isolate overlapping/unowned work in a clean worktree or stop; never reset, stash, or absorb it. Stage only owned paths/hunks. Use Conventional Commits (`type(scope): imperative summary`, optional scope), a blank line, and a sentence on why; mark breaking changes with `!` or `BREAKING CHANGE:`. Do not push unless asked.

Prepare a straightforward plan here; use a read-only planner only when independent research or complexity justifies the handoff. This session writes and commits the draft. Approval changes it to `planned` before implementation. A normal run waits for the user; autonomous approval follows the confidence rule below.

Keep one active implementation lane per product repo: this session implements by default, or one delegated implementer owns the whole related change. Parallel research is read-only. Do not start another implementation while the current change is being implemented or verified, even with disjoint files: migrations, contracts, and test/browser resources can still overlap. Queue new requests unless the user explicitly reprioritizes; checkpoint the current lane before switching. Reuse researchers for bounded questions, use completion notifications, and avoid status polling.

Review the stable completed feature once through a fresh `sdlc-verify` context, covering both source coherence and behavior. Do not routinely dispatch a planner, per-box reviewer, and then another full verifier. A targeted interim review is justified by a concrete unresolved high-impact assumption or a failure; record that reason and scope its follow-up to changed findings. Repository or user requirements for stronger review remain binding.

A material change to approved steps, scope, risk response, or proof reopens the plan to `draft` and needs fresh human or authorized autonomous approval before code. Record small execution deviations in the report; do not use that to bypass approval.

## Keep the thread across compaction

`intent.md`, `spec.md`, `plan.md`, the code, and tests are the source of truth. Update `plan.md` for implementation decisions and deviations under its existing rule; do not use a handoff file to bypass the approved plan. Use optional `intent/<slug>/context.md` only for current consequential facts absent from them: unresolved assumptions, ownership or blockers, the exact next action, and links to evidence. Aim for 500–1,000 words or fewer; replace superseded entries rather than append a session journal. Git and reports preserve detailed history. Do not duplicate artifacts or test receipts, or claim an unchecked step is complete.

Checkpoint consequential changes before a handoff, long risky investigation, or unfinished turn. Include context with the next slice when practical; commit it alone when needed for a safe resumption. Do not checkpoint every routine tool result. Do not push unless asked. On resumption, reconcile context against files/Git and remove stale/transferred entries. Context is a handoff, never approval or verification evidence.

Keep the plan operative too: replace superseded rationale and Decision review entries rather than append checkpoint/review chronology. Usually aim for 1,000–2,000 words, exceeding that when current scope needs it. Preserve task text/check states, base, requirements, applicable constraints, proof, ownership, and unresolved risks; Git and existing reports keep history. Compact an oversized plan through draft/reapproval while implementation or repair is still pending; do not reopen a completed plan merely for size. update dependent bindings and invalidate stale reports. Human-gated runs need approval; authorized autonomous runs may reapprove unchanged decisions from fresh evidence without another challenge. Leave completed/archived records intact.

## Confidence and challenge

High confidence requires all four: explicit outcome/constraints; current-source support; evidence for relevant contracts and important failure modes; no unresolved material assumption or conflicting evidence. Privacy, migrations, concurrency, and irreversible behavior need stronger evidence. Agreement or a stated probability is insufficient.

Record confidence and evidence under Decision review for autonomous approval. At high confidence, skip the challenger. Otherwise send one fresh, read-only challenger the strongest unresolved assumption, check citations, resolve objections, and record residual uncertainty. Missing preference/authority needs the user. Carry valid evidence across gates; challenge only changed material uncertainty, with bounded repair follow-ups. Artifact edits still require reapproval and dependent digest reconciliation.

## Work and validation granularity

Make each box a coherent change with a meaningful observable check; do not make boxes for individual tool calls, files, or bookkeeping. Keep ordered dependencies and a verified commit per box. Use focused affected tests, typechecks, and relevant browser checks within boxes. Do not require independent reviews merely to tick each box; use the implementer's observed focused checks unless the approved plan or a concrete unresolved risk requires an interim review.

The fresh final verifier owns one full change-appropriate gate on the completed snapshot. Run a full gate earlier only when repository instructions or integration risk require it. Record each command's scope and owner in Proof; map requirements and scenarios to shared checks instead of repeating a suite for each scenario. Consolidate overlapping checks before plan approval. An existing approved plan's required proof cannot be silently dropped: reconcile and reapprove it first.

Before an expensive container, restore, migration, or browser integration run, check cheap prerequisites in the isolated environment: candidate identity, dependencies, ports, fixture/schema readiness, and probe behavior relevant to that run. After two failures of the same class, stop repeating the full gate and reassess the cause with a focused reproduction. This does not authorize production access or waive required proof.

Before planning code, check implementation and intended delivery baselines. Under existing Risks/Proof, record prerequisite contracts, commits/migrations, their owner/order, and shared validation resources where relevant. Compare the intended target checkout with those prerequisites before promising a bounded release; disjoint source paths do not establish deployability. Resolve or explicitly sequence missing dependencies early. If release is outside scope, record local-only evidence and outstanding release prerequisites; do not infer production permission or block valid local work on unrequested operational checks.

## Steps

1. Resolve slug. Read `intent.md`, `spec.md`, existing `plan.md`, and `context.md` when present; reconcile the latter with current files and git state. Preserve verified work and the original implementation base when revising a draft plan.
2. Prepare the plan here or with the justified read-only planner: files that change, coherent order of work, risks, and proportionate proof. Map each applicable spec Gotcha to Risks and an observable task/Proof check. Keep checks change-specific and the plan usable without the chat.
3. Write `intent/<slug>/plan.md` from `assets/plan.md` if absent, or reconcile an existing draft plan with the approved spec. Use `status: draft`; a new plan has `base_commit: pending`. Set `spec_digest` to the approved spec digest. Every step under Order of work is a `- [ ]` box ending in its own `— verify:` clause. Include relevant rollout, migration, recovery, and observation in Proof; archive does not claim release. Commit the draft.
4. Before implementation, confirm that this host can arrange a fresh subagent verifier or an explicit separate fresh-session handoff with the same artifact inputs. Record the stable review boundary, route, and required environment in Review route. When dispatch supports `fork_turns`, explicitly set `fork_turns: "none"`; otherwise use its equivalent fresh-context setting or a separate session. Never rely on inherited/default conversation history for independent review. For an unattended run, a verifier must be dispatchable within the run; otherwise mark the slug blocked before code. Confirm a clean committed implementation checkout can be provided for verification. In a normal run, ask the user to approve the plan. In an autonomous run, assess confidence and challenge only unresolved material uncertainty. Record evidence and rationale under Decision review; carry supported spec decisions forward. Block if required evidence or a needed challenger is unavailable, or no defensible decision fits the authorized outcome.
5. On approval, record the full current `git rev-parse HEAD` as `base_commit` only if its value is `pending`; retain an existing valid base when reapproving a revised plan. Set `approved_by: human` or `autonomous`, compute `approved_digest` with `python3 <this-skill-dir>/scripts/fingerprint.py intent/<slug>/plan.md`, set `status: planned`, and commit. The digest normalizes task checkbox state but binds task text, proof, risks, dependency digest, and base commit. Then implement from the first unticked box. For a bugfix, establish a failing reproduction before changing application code when practical; never edit a test merely to manufacture a pass.
6. Tick a box only once you have run its verify clause and seen it pass. A step partially done, deferred, or narrowed stays `- [ ]`. Commit that coherent slice, including its ticked box, before the next box. Several edits and focused checks can belong to one box; do not add commits for routine tool actions.
7. After the last box, immediately run `sdlc-verify` in an independent review context. Require clean committed in-scope implementation and a report bound to the reviewed HEAD and approved artifact digests. Check the returned report content before its single report-only commit; return format or missing-evidence findings to the same verifier for a narrow correction while the report remains uncommitted, without editing its verdict yourself. When available, run `python3 <sdlc-continue-dir>/scripts/validator.py validate <slug>` before committing to detect content errors (a pending report still fails the one-report-commit freshness check), then rerun after the report-only commit and require success before accepting a pass. A committed report correction must replace only an owned, unshared report-only tip after its verifier repairs the content; never amend the reviewed candidate or append a second report commit. If that repair is unsafe, obtain fresh verification at the current clean committed candidate. Source or semantic artifact changes always require fresh verification. Do not call the work done from test results alone.
8. If the report fails or has CRITICAL, fix the findings and commit before re-verification. Keep the failing report until a fresh verifier replaces it; never flip its verdict. Count prior failures in Git as well as this run and change ineffective repair strategies. After two failures of the same class, reassess with a focused reproduction before another full review; after three failed repairs of the same unresolved issue, stop that slug with concrete findings. A blocked verification is a capability or environment recovery task, not evidence of incorrect behavior; do not mark done or archive.
9. On a valid fresh pass, a normal run asks before marking statuses `done`. An explicitly authorized autonomous run may set them to `done` and invoke `sdlc-archive` after its deterministic check passes.

If the plan is already `planned` and the user says implement, run the readiness and freshness checks and resume at the first unticked box. If it is `draft`, reconcile and reapprove before code, retaining an existing valid `base_commit`. If a report already failed or has CRITICAL, use step 8.

When you stop before the last box, say where the work stands as `N/M boxes ticked` and name the first unticked one. `sdlc-continue` picks up from there.
