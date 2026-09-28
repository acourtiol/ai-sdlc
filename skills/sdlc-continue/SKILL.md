---
name: sdlc-continue
description: >-
  Resume an existing intent at its next gate, or process all open intents
  sequentially when the user explicitly requests an autonomous run.
license: MIT
metadata:
  author: acourtiol
  version: "2.0"
---

# sdlc-continue

Read the current artifacts and run the next gate. `intent/archive/` is history, never an active slug. This skill does not create an intent. An explicit request such as “run all open intents autonomously” authorizes the optional queue mode below; ordinary continue remains a single-slug, human-gated workflow.

## Preflight

Run `sh <this-skill-dir>/scripts/status.sh` from the product repo root. Its deterministic `next:` advice is a safety check, not proof that the agent's claims are true. On malformed or stale artifacts, repair or reapprove them before advancing. The same validator is available as `python3 <this-skill-dir>/scripts/validator.py validate <slug>` and `archive-check <slug>`; archive-check adds the done-status requirement to the common contract. If this skill is installed alone, stop at a gate whose owning skill is unavailable and name the missing skill. Do not improvise another skill's template or verification.

Before modifying anything, record repository, branch, HEAD, staged paths, working-tree paths, and untracked paths. Preserve pre-existing work. If ownership overlaps or the index contains unrelated staged work, use a clean isolated worktree when feasible; otherwise leave that slug blocked. Never reset, stash, or commit someone else's changes. Check repository state again between slugs.

Read any `context.md`, then verify its claims against current source, artifacts, and Git. It is a handoff, not authority. An accepted artifact is valid only when its `approved_digest` matches its current content and its upstream digest matches the approved upstream artifact. A passing report is current only when its artifact digests match and no implementation change followed its `reviewed_head`. Status words alone never establish approval or completion. Legacy artifacts without these bindings must be reconciled and reapproved; do not silently invent provenance.

## One slug

When several active slugs exist and the user did not request the queue, ask which one. Name the chosen slug. Follow `next:` and the owning skill. The normal run stops at the next human approval gate. After the user accepts or approves in this session, execute the owning skill's next handoff unless told to stop.

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

Report progress as `N/M boxes ticked` when a plan exists. A plan with zero or malformed boxes cannot advance.

## Autonomous queue

This mode begins only after the user explicitly authorizes it for existing intents. It covers local artifact approvals, implementation, local commits, marking done, and archiving. It does not authorize creating new intents, pushing, deploying, production changes, destructive operations, external commitments, or material cost/security exceptions. Do not ask for per-artifact approval during the run. If a decision requires authority outside this grant, record a specific blocker for that slug and continue with independent work. A prior user restriction still applies.

1. Inventory every `intent/*/` folder except `intent/archive/`. Queue only folders with `intent.md`; leave context-only folders for exploration. Read each intent and identify dependencies, shared files, incompatible outcomes, and work that would make another intent's approved artifacts stale. Use a fresh research subagent to challenge the proposed order when the interaction is material. Choose a serial order from evidence, not directory order alone. Record the order and assumptions in the run summary; re-evaluate after each slug.
2. Preflight the full skill bundle (`sdlc-plan`, `sdlc-design`, `sdlc-apply`, `sdlc-verify`, `sdlc-archive`), Python 3.8 or newer for the local validator, Git ownership, and dispatchable fresh-context research challenger and verifier before implementation. The queue may continue past a blocked slug but cannot manufacture an in-session challenge or pass. A host session must remain active for the queue; these skills do not schedule or restart themselves after the host stops.
3. For each slug, rerun the status validator and reconcile stale approvals or reports. At each draft intent, spec, or plan gate, the owning skill prepares the artifact and dispatches a fresh, read-only research challenger before autonomous approval. Give the challenger the proposed choice, user outcome, relevant artifacts, and source paths. Ask it to find the strongest counterargument, alternative, failure mode, and evidence that would falsify the choice. Check its evidence directly. Record the decision, objections, dissent, and residual risk in that artifact's Decision review. The orchestrator decides within the user's stated outcome; subagent agreement does not create certainty or authority. If no defensible choice fits, leave the gate draft and record the blocker in a short `context.md` with the evidence and exact recovery action; commit only that handoff.
4. Implement through `sdlc-apply` and obtain an independent `sdlc-verify` report. On fail, repair and reverify within that skill's attempt limit. On blocked verification, record the recovery needed in the blocked report or `context.md`. Never promote a malformed, stale, or unobserved report to pass.
5. On a current pass, run `validate <slug>` before setting statuses done. Set intent, spec, and plan statuses to `done` in a bookkeeping commit; these status edits do not change approved digests. Run `archive-check <slug>`, invoke `sdlc-archive`, and confirm the move. Reinspect Git and remaining intents before the next slug.
6. At the end, summarize archived slugs, blocked slugs with exact recovery actions, and checks run. Do not describe blocked work as complete. If the host nears its execution limit, commit only valid completed slices and leave a concise `context.md` handoff for the current slug where needed; a later explicit autonomous invocation resumes the queue.

The queue can choose among technically defensible options after adversarial review. It cannot infer missing business preferences, waive required evidence, or substitute its own permission for an external action. When a choice remains uncertain, a small reversible experiment is preferable to unsupported confidence.
