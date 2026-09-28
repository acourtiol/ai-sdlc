# ai-sdlc

```bash
npx skills add acourtiol/ai-sdlc -g -a claude-code -a cursor -a codex -a opencode -s '*' -y
```

Name each target agent; do not pass `--agent '*'`. For one-shot installation from this checkout, use `npx skills add . -l` to list skills, then install the selected folders with the CLI. Consumers run `npx skills update` to update installed copies.

These are independently installable skills, not a CLI or orchestration framework. In a product repo the artifacts live at `intent/<slug>/`. The normal workflow is:

```text
sdlc-explore → sdlc-plan → sdlc-design → sdlc-apply → sdlc-verify → sdlc-archive
```

Explore helps shape an idea. Plan writes the intent, design writes requirements and design together in `spec.md`, apply writes the plan and implements it, verify judges the change, and archive closes the change record. A bounded bug or behavior-preserving refactor can use `sdlc-fix` without an intent folder.

## Skills

| Skill | Writes | When |
| --- | --- | --- |
| `sdlc-explore` | optional `intent/<slug>/context.md` | the idea is half-formed or it is unclear whether it needs the loop |
| `sdlc-fix` | code and tests, no intent folder | a bounded bug or behavior-preserving refactor in an existing flow |
| `sdlc-plan` | `intent/<slug>/intent.md` | a product change after exploration; intent acceptance starts design |
| `sdlc-design` | `spec.md` | an accepted intent; spec approval starts planning |
| `sdlc-apply` | `plan.md`, implementation, then verification handoff | a specified change; plan approval precedes implementation |
| `sdlc-verify` | `report.md` | independent judgment of a completed implementation |
| `sdlc-archive` | moves the folder | validated passing report and completed artifacts |
| `sdlc-continue` | resumes one intent or runs the authorized open-intent queue | an in-progress change, or an explicit autonomous queue request |

Each skill owns its artifact template and can be installed separately. A full workflow needs the relevant skills together. The autonomous queue requires `sdlc-continue`, `sdlc-plan` (to accept existing draft intents), `sdlc-design`, `sdlc-apply`, `sdlc-verify`, and `sdlc-archive`, plus a host session that can dispatch fresh reviewers. `sdlc-continue` includes the deterministic artifact validator used by the archive gate. No scheduler or daemon is included.

The validator and fingerprint scripts require Python 3.8 or newer and use only the standard library. The autonomous queue checks for the complete skill bundle and a working Python interpreter before processing intents.

## Artifact states and integrity

Statuses belong to individual artifacts:

| Artifact | Status progression | Meaning |
| --- | --- | --- |
| `intent.md` | `draft` → `accepted` → `done` | the problem and desired outcome are accepted |
| `spec.md` | `draft` → `specified` → `done` | requirements and design are approved against the accepted intent |
| `plan.md` | `draft` → `planned` → `done` | implementation work and checks are approved against the spec |
| `report.md` | no status; `verdict: pass`, `fail`, or `blocked` | independent evidence about one reviewed implementation snapshot |
| intent folder | active path → `intent/archive/YYYY-MM-DD-<slug>/` | archive location closes the change record; there is no `archived` status |

Accepted intent, spec, and plan content carries an `approved_digest` and `approved_by`; downstream artifacts record the digest they depend on. A material upstream change reopens dependent decisions. The report records all three approved digests and `reviewed_head`. The continue and archive checks validate the artifact grammar, dependencies, evidence shape, and report freshness. A passing report is invalidated by later semantic artifact or implementation changes; report/status bookkeeping is handled explicitly by the validator.

Verification uses an independent subagent or a separate fresh session with an explicit handoff. Missing review capability or required test access produces `blocked`, which never permits completion or archive. A `fail` means evidence showed incorrect or incomplete behavior and goes back through repair and fresh review. User-facing changes need observable evidence from the running product, not only green tests.

## Autonomous queue

After creating and exploring one or more `intent.md` files, explicitly ask `sdlc-continue` to run all open intents autonomously. This is an opt-in workflow for existing intents; it does not create new ones. It inventories active intent folders, skips `intent/archive/` and context-only folders, then processes independent changes serially, rechecking the repo between them. A valid passing report allows the workflow to mark the artifact statuses done and archive the folder.

The request authorizes local artifact decisions, implementation, commits, completion statuses, and archival for that queue. Before each material intent, spec, or plan decision, the orchestrator asks a fresh research subagent to find the strongest counterargument, alternative, failure mode, and evidence that could disprove the proposed choice. It checks the evidence and records its rationale, dissent, and remaining risk in the artifact. The research agent advises; the orchestrator makes and owns the decision. Agreement between agents is not proof. If a decision depends on a missing business preference, external authority, or unavailable evidence, that slug is recorded as blocked and the queue continues with independent intents.

The queue does not authorize pushing, deployment, production changes, destructive operations, external commitments, or material cost/security exceptions. It runs only while the host keeps the session active and can dispatch independent reviewers. These skills cannot schedule themselves, keep running after the host stops, or promise overnight execution. A later explicit request resumes remaining open intents.

## Verification and harness capability

Installation support does not establish end-to-end workflow support. We have not run an acceptance session for all harnesses, so no complete harness is claimed as tested. Use this matrix to record exercised capabilities; update a cell only after a reproducible check in that harness.

| Harness | Skill discovery | Template/resource resolution | Fresh reviewer dispatch | Browser verification |
| --- | --- | --- | --- | --- |
| Claude Code | Not verified in this repo | Not verified in this repo | Not verified in this repo | Not verified in this repo |
| Cursor | Not verified in this repo | Not verified in this repo | Not verified in this repo | Not verified in this repo |
| Codex | Not verified in this repo | Not verified in this repo | Not verified in this repo | Not verified in this repo |
| OpenCode | Not verified in this repo | Not verified in this repo | Not verified in this repo | Not verified in this repo |

The OpenCode install target uses `-a opencode`, as shown in the [skills CLI documentation](https://github.com/vercel-labs/skills). This repo has not yet validated discovery, sibling resource lookup, isolated reviewer dispatch, or browser tooling in an OpenCode session. The same capability checks remain open for the other harnesses.

## Release and maintenance

Archiving closes the change record; it does not mean production deployment succeeded. Where relevant, the plan and report should name rollout prerequisites, migrations, recovery or rollback steps, and post-release observations. Deployment remains a separate product-repository activity.

After release, record whether the expected behavior occurred. Feed incidents and escaped defects back through `sdlc-fix` or `sdlc-plan`, and identify the durable prevention—such as a regression check, clearer contract, missing diagnostic, or focused repository instruction. Archive history is not the current product reference; put lasting system knowledge in current documentation, tests, or focused `AGENTS.md` guidance.

## Project constraints

- Requirements and design stay in `spec.md`; do not add `design.md`.
- Do not add a CLI, Codex plugin, agent organization, `CLAUDE.md` dumps, `production-gate.sh`, evals CI, or `bands.yaml`.
- Archive is a plain move to `intent/archive/YYYY-MM-DD-<slug>/`; it is history, not a specs tree or merge step.
- Explore normally writes nothing and owns no template. For an intent-worthy idea that needs a durable handoff first, it may write consequential findings to `context.md`; this file is not an approval or status.
- Deploy and maintain activities may be manual until a product repository needs an automation hook.

Install with `npx skills add`; do not copy these skill folders into chezmoi.
