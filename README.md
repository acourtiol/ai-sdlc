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

Each skill owns its artifact template and can be installed separately. A full workflow needs the relevant skills together. The autonomous queue requires `sdlc-continue`, `sdlc-plan` (to accept existing draft intents), `sdlc-design`, `sdlc-apply`, `sdlc-verify`, and `sdlc-archive`, plus a host session that can dispatch a fresh final verifier and any needed decision challenger. `sdlc-continue` includes the deterministic artifact validator used by the archive gate. No scheduler or daemon is included.

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

The request authorizes local artifact decisions, implementation, commits, completion statuses, and archival for that queue. At each intent, spec, or plan gate, the orchestrator records confidence and evidence under Decision review. Confidence is high only when all four conditions hold: the outcome and constraints are explicit; current source supports the approach; relevant contracts and important failure modes have evidence; and no material assumption or conflicting evidence remains unresolved. Sensitive data, migrations, concurrency, and irreversible behavior need stronger evidence to qualify. This is an evidence threshold, not a calibrated probability.

Only below high confidence does it dispatch a fresh research challenger for the strongest unresolved assumption. It checks citations and records the resolution and residual uncertainty. Supported decisions carry forward across gates; changed uncertainty gets a focused follow-up. Agent agreement is not evidence. The orchestrator owns the decision; high confidence does not waive approval digests, required checks, or final independent verification. If a decision depends on a missing business preference, external authority, or unavailable evidence, that slug is recorded as blocked and the queue continues with independent intents.

The queue does not authorize pushing, deployment, production changes, destructive operations, external commitments, or material cost/security exceptions. It runs only while the host keeps the session active and can dispatch independent reviewers. These skills cannot schedule themselves, keep running after the host stops, or promise overnight execution. A later explicit request resumes remaining open intents.

## Efficient execution

Keep one implementation lane active per product repository through implementation and final review. The main session implements by default; delegate the whole change to one implementer only when it saves meaningful time or context. Parallel read-only research is allowed. Queue additional implementation requests until this change finishes or blocks, unless the user explicitly reprioritizes; checkpoint before switching. Different files can still share migrations, contracts, and validation resources. Delegate bounded research or targeted interim review only for justified uncertainty, explicit requests, or concrete failures. No named agent profiles or particular models are required. Prefer completion notifications and meaningful waits over repeated agent/file polling.

Plan boxes are coherent, reviewable changes with focused checks and a commit each. Dispatch one fresh final verifier only when the completed candidate is committed. It combines source review and behavioral verification at the stable feature boundary and owns one full change-appropriate gate. Use the host's available mechanism for a review context without inherited implementation history, or a separate fresh session with a bounded handoff; confirm actual isolation rather than assuming default dispatch is independent; inherited implementation history cannot yield an independent pass. Record the concrete reason for an interim review and keep follow-ups scoped to actual findings. Run full checks earlier when repository instructions or concrete integration risk require them. Consolidate overlapping gates before approval; reconcile and reapprove existing plans before changing required proof.

The verifier can reuse an inspectable check receipt only after independently establishing matching code, tests, configuration/lockfiles, dependencies, command scope, and environment. Record its producing commit and raw evidence. Uncertain or changed inputs require a rerun. Receipt reuse never replaces fresh independent diff review, targeted material-behavior checks, or the main UI/error flow; a prior verdict cannot become a new verdict.

Before implementation, inspect prerequisite contracts, commits, and migrations against the integration baseline and any intended delivery baseline. Record ownership, order, and shared validation resources in the existing Risks/Proof sections. Check the intended target source early if release compatibility is promised. For local-only work, record outstanding release prerequisites; this grants no deployment authority.

Before expensive isolated integration checks, validate cheap prerequisites such as candidate identity, dependencies, ports, fixtures/schema readiness, and probe behavior. After two failures of the same class, reassess with a focused reproduction before another full run. Missing required proof still blocks completion.

Keep optional `context.md` to current unresolved facts absent from the other artifacts, ownership/blockers, the next action, and evidence links. Aim for 500–1,000 words or fewer, allowing justified complex handoffs. Replace superseded entries instead of appending a session journal; Git and reports retain history. Checkpoint consequential handoffs and unfinished turns rather than routine tool results. Keep unfinished plans focused on operative tasks, decisions, and proof, usually 1,000–2,000 words unless current complexity justifies more. Replace superseded rationale and Decision review rather than appending journals; retain task states, base commit, requirements, constraints, ownership, required proof, and unresolved risks. Compact through draft/reapproval, refreshing dependent bindings and invalidating stale reports. Human approval remains human unless autonomous approval is authorized. Leave completed and archived plans intact. These defaults apply on future runs; they do not rewrite existing approved product artifacts automatically.

## Portability contract

The skills use the [Agent Skills format](https://agentskills.io/specification).
Their artifact and evidence rules are independent of a model, named agent
profile, slash-command syntax, or delegation API. A capable host needs repository
file access, Git, an available Python 3.8+ interpreter, and the project's required
validation tools. The examples use `python3`; select the installed interpreter
and quote paths. `validator.py route` is the portable status entrypoint;
`status.sh` is an optional POSIX convenience. Archive uses an ordinary filesystem
folder move with an absent destination, preserving the artifact bytes.

Resolve each skill's resources against its installed directory. At a handoff,
load the required skill through the host or read its installed `SKILL.md` and
needed resources. A missing skill produces a precise handoff at that gate.
Independent review requires demonstrably separate context without inherited
implementation history: host delegation or a separately started fresh session
with the bounded artifact handoff. If neither is available, verification remains
blocked. An unattended queue additionally needs that route dispatchable during
the run; an interactive workflow can hand off to a separate session.

Native skill support is documented for [Codex](https://learn.chatgpt.com/docs/build-skills),
[Claude Code](https://code.claude.com/docs/en/skills),
[Cursor](https://cursor.com/docs/skills), and
[OpenCode](https://opencode.ai/docs/skills/). Installation and invocation vary by
host. Local/global skill installation does not establish availability in a remote
or cloud execution environment; confirm resources and tools there. This contract
supports capable harnesses, not an unconditional promise about every agent host.

## Verification and harness capability

Installation support does not establish end-to-end workflow support. We have not run an acceptance session for all harnesses, so no complete harness is claimed as tested. Use this matrix to record exercised capabilities; update a cell only after a reproducible check in that harness.

| Harness | Skill discovery | Template/resource resolution | Fresh reviewer dispatch | Browser verification |
| --- | --- | --- | --- | --- |
| Claude Code | Native smoke blocked by expired OAuth (2026-10-02) | Not exercised by native smoke | Not verified in this repo | Not verified in this repo |
| Cursor | Native smoke blocked by workspace trust (2026-10-02) | Not exercised by native smoke | Not verified in this repo | Not verified in this repo |
| Codex (local app sessions) | Catalog and skill loading observed (2026-10-02) | Local resources exercised | Two-step trial and fresh generic intent-mismatch review (2026-10-02) | Not verified in these fixtures |
| OpenCode | Not verified in this repo | Not verified in this repo | Not verified in this repo | Not verified in this repo |

The 2026-10-02 local checks ran under Python 3.14.7, Codex CLI 0.160.0,
Claude Code 2.1.287, and Cursor 3.22.12; no OpenCode binary was installed.
Version/help inspection establishes no workflow capability. Native probes use
the disposable fixture in behavioral scenario 17; authentication/trust failures
are blocked, never passes. The tests also exercise direct routing and archive
validation with separate installed-resource and product paths containing spaces
and non-ASCII characters. This Linux run does not establish Windows execution.

The OpenCode install target uses `-a opencode`, as shown in the [skills CLI documentation](https://github.com/vercel-labs/skills). This repo has not yet validated discovery, sibling resource lookup, isolated reviewer dispatch, or browser tooling in an OpenCode session. The same capability checks remain open for the other harnesses.

## Release and maintenance

Archiving closes the change record; it does not mean production deployment succeeded. Where relevant, the plan and report should name rollout prerequisites, migrations, recovery or rollback steps, and post-release observations. Deployment remains a separate product-repository activity.

After release, record whether the expected behavior occurred. Feed incidents and escaped defects back through `sdlc-fix` or `sdlc-plan`, and identify the durable prevention—such as a regression check, clearer contract, missing diagnostic, or focused repository instruction. Archive history is not the current product reference; put lasting system knowledge in current documentation, tests, or focused `AGENTS.md` guidance.

## Design basis and feedback

The [Anthropic AI-native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook)
provides the artifact loop and human accountability. Its stages are modular;
these skills adapt the local intent, design, implementation, and verification
loop rather than reproduce Claude-specific infrastructure. Deployment and
maintenance remain product-owned until an integration is requested.

[OpenSpec](https://github.com/Fission-AI/OpenSpec/blob/main/docs/workflows.md)
informs iterative refinement and completeness/correctness/coherence review;
[spec-kit](https://github.com/github/spec-kit) informs testable requirements,
clarification, and distinct paths for features, fixes, and assessment. We retain
one design file, digest-bound decisions, required independent verification, and
plain historical archive rather than import their whole artifact/CLI systems.

Public experience is input, not proof of an improvement. Examples include
[spec-kit's token-budget extension](https://github.com/tinesoft/spec-kit-token-budget),
[OpenSpec's unavailable-workflow report](https://github.com/Fission-AI/OpenSpec/issues/1734),
and its [verification-of-removed-behavior bug](https://github.com/Fission-AI/OpenSpec/issues/1959).
They motivate compact current artifacts, capability checks, and verification
against the actual accepted outcome. Their anecdotes and reported savings do not
establish this workflow's performance.

Evaluate representative product changes through their existing plans/reports
and session telemetry: time from approval to independently verified delivery,
failed checks and repair cycles, repeated product corrections, and missed
requirements or escaped defects. Separate environment/setup failures from
workflow handoffs. Distinguish new input, cached/repeated input, and output where
telemetry provides them; do not sum cumulative counters or equate processed input
with fresh context or spend. Compare similar scopes across several runs, retaining
required proof and human outcome acceptance. Do not add artifacts or a reporting
gate solely to collect these measures. A skill change earns its place through
observed improvement without worse correctness or intent alignment.

## Project constraints

- Requirements and design stay in `spec.md`; do not add `design.md`.
- Do not add a CLI, Codex plugin, agent organization, `CLAUDE.md` dumps, `production-gate.sh`, evals CI, or `bands.yaml`.
- Archive is a plain move to `intent/archive/YYYY-MM-DD-<slug>/`; it is history, not a specs tree or merge step.
- Explore normally writes nothing and owns no template. For an intent-worthy idea that needs a durable handoff first, it may write consequential findings to `context.md`; this file is not an approval or status.
- Deploy and maintain activities may be manual until a product repository needs an automation hook.

Install with `npx skills add`; do not copy these skill folders into chezmoi.
