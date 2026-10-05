---
name: sdlc-continue
description: >-
  Resume an existing intent at its next gate, or process all open intents
  sequentially when the user explicitly requests an autonomous run.
license: MIT
metadata:
  author: acourtiol
  version: "2.11"
---

# sdlc-continue

Read artifacts and run the next gate for one slug. Skip `intent/archive/`; never create an intent here. “Run all open intents autonomously” explicitly enables the queue below; ordinary continue is human-gated.

## Preflight

Resolve this skill's installed directory from the host's skill path; its `assets/` and `scripts/` paths are relative to that directory, not the product repo. Commands use `python3` as an example: select an available Python 3.8+ interpreter and quote resolved paths. Run `python3 "<this-skill-dir>/scripts/validator.py" route` in the product repo (`status.sh` is an optional POSIX wrapper). Follow `next:` after repairing/reapproving malformed or stale artifacts; validation cannot prove claimed behavior. Direct commands are `python3 <this-skill-dir>/scripts/validator.py validate <slug>` and `archive-check <slug>` (adds done statuses). Load the next owning skill by the host's supported mechanism or read its installed `SKILL.md` and needed local resources directly. No slash-command or skill-invocation API is assumed. If that skill or its resources cannot be resolved, hand off with the required skill, artifact path, and next gate; do not improvise its template or review.

Before edits and between slugs, record repo/branch/HEAD and staged/dirty/untracked paths. Reuse the current owning checkout by default; isolate concrete overlap or provide a clean review candidate only when needed. Never reset, stash, or absorb others' changes. Resumable checkouts and retained receipts use persistent, non-cache storage; temporary directories are disposable. For an agent-created checkout, use the agreed project workspace's `.worktrees/<purpose>` by default, anchoring the root once from the initial workspace to avoid nested worktree areas. Ensure the location is excluded from Git tracking and relevant source/test discovery before creation, applying the project's targeted exclusion convention if needed. Keep host-managed isolation when required and record its path and reason. On resumption, check cited evidence still exists before reuse.

Use Conventional Commits (`type(scope): imperative summary`, optional scope), a blank line, and a sentence on why; mark breaking changes with `!` or `BREAKING CHANGE:`.

Read any `context.md`, then check relevant current claims against source, artifacts, and Git. Compact context to unresolved facts absent from artifacts, next action, and evidence links; aim for 500–1,000 words or fewer. Remove transferred or superseded entries, preserving history in Git and reports. It is a handoff, not authority. Approvals require matching content/dependency digests. A pass requires matching artifact digests and no later implementation change after `reviewed_head`. Status alone proves neither. Reconcile/reapprove legacy unbound artifacts; never invent provenance.

Where current user feedback or preserved request evidence contradicts a narrowed artifact, reconcile the outcome through its owning skill before accepting completion. Autonomous approval does not authorize replacing requested automation or integrations with a manual fallback. A verified slice may finish while a required follow-on remains open, but keep that distinction and its blocker visible; do not report the full request delivered.

Keep one compact current delivery summary in the existing run summary or handoff, referencing canonical artifacts rather than mirroring them. State the requested outcome, verified outcome, deployed outcome only when authorized evidence exists, remaining scope/blocker, current slug/owning checkout and next action. Refresh it at meaningful delivery boundaries, not each tool call. A reused checkout or agent name does not identify the current feature. When verified source and delivery histories diverge, reconcile the actual target against its current baseline, reuse still-valid mapping evidence, and distinguish adaptation still needed from behavior already delivered; preserve archives and avoid reopening completed work merely to synchronize old counts. This creates no new artifact or gate.

While implementation or repair is pending, route an oversized plan to apply for replacement of superseded rationale through draft/reapproval; do not reopen a completed plan merely for size. Preserve operative tasks, proof, base and risks; leave completed/archived records intact. This is reconciliation, not permission to waive checks.

## Confidence and challenge

High confidence requires all four: explicit outcome/constraints; current-source support; evidence for relevant contracts and important failure modes; no unresolved material assumption or conflicting evidence. Privacy, migrations, concurrency, and irreversible behavior need stronger evidence. Agreement or a stated probability is insufficient.

Record confidence and evidence under Decision review for autonomous approval. At high confidence, skip the challenger. Otherwise send one fresh, read-only challenger the strongest unresolved assumption, check citations, resolve objections, and record residual uncertainty. Missing preference/authority needs the user. Carry valid evidence across gates; challenge only changed material uncertainty, with bounded repair follow-ups. Artifact edits still require reapproval and dependent digest reconciliation.

Keep one active implementation lane per product repo, including final review. This session implements by default; if delegated, one implementer keeps the related change. Parallel work is read-only research. Queue unrelated added requests until the current feature passes or is explicitly blocked; clarifications of its current outcome stay in scope. Do not hold an independently complete verified delivery for unrelated fixes: perform its already-authorized release first unless the user explicitly requests a batch or actual dependencies require one; an explicit user reprioritization requires a committed handoff before switching. Disjoint files do not justify overlapping migration or verification lanes. Do not start a final verifier merely to wait for unfinished code.

Final review combines source and behavior on a stable completed commit. Before allocating another review checkout, prefer retargeting an owned, clean, inactive one after retaining its prior report and required receipts and confirming no work will be discarded; a changed candidate hash alone does not justify another directory; the reviewer must still use fresh context and inspect the exact candidate. Use a review context without inherited implementation history through the host's available delegation mechanism or a separate fresh session. Confirm isolation rather than relying on default dispatch behavior; no named agent profile or particular model is required. For delegated work, establish completion/blocker conditions and use notifications or meaningful waits. A timeout is not new evidence: resume waiting without status messages, file/queue polling, replanning, handoff recaps, or speculation about future work. Reassess on a completion, blocker, changed requirement, observed failure, or agreed deadline; keep needed user updates brief and factual without waking the worker. When no useful independent work remains, prefer a host-supported suspended wait that resumes on worker completion, blocker or user input. Confirm automatic resumption before yielding; do not end an unattended run assuming someone will restart it. If unavailable, use permitted blocking waits consistent with host responsiveness/timeouts and keep intervening reasoning minimal. Do not reread context, regenerate status prose or reconsider the same queue merely because a wait elapsed. Skills cannot add a notification capability the host lacks.

## One slug

Name the slug; ask which when several are active without queue authorization. Follow `next:` and its owning skill to the next human approval gate. Session approval immediately starts the next handoff unless told to stop.

| Current state | Next action |
| --- | --- |
| only `context.md` | Resume `sdlc-explore`; no intent is ready |
| draft intent | Present it; on acceptance run `sdlc-design` |
| accepted intent, no spec or draft spec | Run `sdlc-design` |
| specified spec, no plan or draft plan | Run `sdlc-apply` plan step |
| planned plan, unticked boxes | Run `sdlc-apply` from first unticked box |
| all boxes ticked, no current report | Run independent `sdlc-verify` |
| failed report or CRITICAL finding | Run `sdlc-apply` repair, then fresh `sdlc-verify` |
| blocked report | Restore review capability or environment, then run `sdlc-verify` |
| current pass, statuses short of done | Ask to mark done in a normal run |
| current pass, all statuses done | Run `sdlc-archive` when requested |

Report progress as `N/M boxes ticked` for the current canonical plan; label historical source-pool counts as historical. A plan with zero or malformed boxes cannot advance.

## Autonomous queue

This mode begins only after the user explicitly authorizes it for existing intents. It covers local artifact approvals, implementation, local commits, marking done, and archiving. It does not authorize creating new intents, pushing, deploying, production changes, destructive operations, external commitments, or material cost/security exceptions. Explicit additional user authorization for delivery decomposition permits routing bounded linked delivery intents through `sdlc-plan`; the queue grant alone does not. Keep the original outcome and unfinished obligations open, and verify/close each bounded delivery against its own approved scope. Do not ask for per-artifact approval during the run. If a decision requires authority outside this grant, record a specific blocker for that slug and continue with independent work. A prior user restriction still applies.

1. Inventory every `intent/*/` folder except `intent/archive/`. Queue only folders with `intent.md`; leave context-only folders for exploration. Read each intent and identify contract/migration prerequisites, their owners/order, intended delivery baseline, shared validation resources, incompatible outcomes, and work that would stale another artifact. Check target-source prerequisites before coding a change promised for that target; otherwise label local work and its release prerequisites. Assess confidence in material dependency/order choices; use one fresh challenger only for unresolved uncertainty. Do not reread archived intent history without a relevant dependency. Choose a serial order from evidence, not directory order alone. Record the order and assumptions in the run summary; re-evaluate after each slug.
2. Preflight the full skill bundle (`sdlc-plan`, `sdlc-design`, `sdlc-apply`, `sdlc-verify`, `sdlc-archive`), Python 3.8 or newer for the local validator, Git ownership, and a dispatchable fresh-context verifier before implementation. Check challenger availability when confidence requires one. Keep blocked slugs incomplete. The host must preserve an active or automatically resumable run; skills cannot schedule or restart themselves.
3. For each slug, rerun the status validator and reconcile stale approvals or reports. At each draft gate, the owning skill prepares the artifact and records confidence, supporting evidence, and any needed challenge under Decision review. Reuse supported decisions across gates; challenge only new or changed material uncertainty. After an objection is resolved, avoid another review unless evidence or the governing decision changed. The orchestrator decides within the stated outcome; agent agreement does not create certainty or authority. If no defensible choice fits, leave the gate draft and record the blocker in a short `context.md` with the evidence and exact recovery action; commit only that handoff.
4. Finish or block one slug, including its independent final review, before starting another implementation. An authorized replan may checkpoint an oversized active bundle and switch to its first bounded delivery; preserve completed work/evidence and parent scope, and reconcile/reapprove changed artifacts before resuming. Do not routinely interrupt a sound delivery just to split it. Use `sdlc-apply` and one fresh `sdlc-verify` review at the stable feature boundary; interim reviews need an explicit unresolved risk, failure, or binding requirement. On fail, repair and reverify within that skill's attempt limit. On blocked verification, record the recovery needed in the blocked report or `context.md`. Never promote a malformed, stale, or unobserved report to pass.
5. On a current pass, run `validate <slug>` before setting statuses done. Set intent, spec, and plan statuses to `done` in a bookkeeping commit; these status edits do not change approved digests. Run `archive-check <slug>`, invoke `sdlc-archive`, and confirm the move. Reinspect Git and remaining intents before the next slug.
6. At the end, summarize archived slugs, blocked slugs with exact recovery actions, and checks run. Do not describe blocked work as complete. If the host nears its execution limit, commit only valid completed slices and leave a concise `context.md` handoff for the current slug where needed; a later explicit autonomous invocation resumes the queue.

At slug completion, inspect worktrees you own and remove only clean, inactive checkouts with no unfinished task/handoff, whose commits and evidence are retained and which have no live process using them. Do not force-remove, delete branches, move live checkouts, or prune globally. If ownership or safety is unclear, keep the checkout and record its path and reason in the handoff.

The queue chooses defensible options after confidence assessment and any needed challenge. It cannot infer business preferences, waive proof, or authorize external actions. Use a small reversible experiment to resolve technical uncertainty when useful.
