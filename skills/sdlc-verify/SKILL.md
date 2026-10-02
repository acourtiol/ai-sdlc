---
name: sdlc-verify
description: >-
  Independently verify a completed change against its intent, spec, and plan.
  Use after implementation, before completion or archive, or when asked to
  verify. A fresh verifier writes evidence; unavailable review or checks are
  blocked, never a pass. Do not edit application source or tests.
license: MIT
metadata:
  author: acourtiol
  version: "2.6"
---

# sdlc-verify

Judge the completed implementation in a fresh subagent or separate fresh session. Write only `intent/<slug>/report.md`; fixes belong to `sdlc-apply`, then new independent verification. The implementer cannot supply a passing verdict.

## Independent route

Resolve `assets/` and `scripts/` against this skill's installed directory supplied by the host, not the product repo. Commands use `python3` as an example; choose an available Python 3.8+ interpreter and quote resolved paths. Load a required next skill through the host or its installed `SKILL.md`; if it or its resources are unavailable, hand off at that gate rather than inventing them.

Before code, apply records the stable feature review boundary, verifier route, and environment. Dispatch only once a completed committed candidate is available; setup/preflight can stay with the implementer. This review covers source coherence and behavior together, rather than a routine reviewer followed by a verifier. An unattended run requires a dispatchable verifier. Give it no implementing conversation, summary, or conclusions: only repository/slug, artifact and skill/template paths, approved digests, candidate `reviewed_head`, plan base, and expected outcomes/scenarios. Use the host's available delegation mechanism without inherited implementation history, or a separate fresh session with that bounded handoff. No named agent profile or particular model is required. Confirm actual context isolation; a role name or default dispatch behavior does not establish independence. A verifier given implementation history cannot provide an independent pass: record blocked and obtain a fresh route. It independently reads artifacts, source, and raw evidence. A separate session receives the same handoff and records `isolation: fresh-session`; returning the handoff to the implementer is not independent.

For consequential changes (authorization, sensitive data, migrations or irreversible operations, financial calculations, safety), inspect the exact commit in a disposable checkout with limited test credentials. Never run consequential checks against production. Missing isolation, access, or an independent route is `blocked`.

## Confidence and challenge

Final independent verification is mandatory. A separate decision challenger is conditional: confidence is high only when outcome/constraints are explicit, current source supports the approach, relevant contracts and important failure modes have evidence, and no material assumption or conflicting evidence remains unresolved. Consequential behavior needs stronger evidence. Agreement or a stated probability is insufficient.

At high confidence, record the evidence and why a separate challenge was skipped under Independent challenge. Otherwise request one fresh, read-only challenger (history inheritance disabled) for the strongest unresolved assumption, check its citations, and record resolution and residual uncertainty. A missing preference or authority needs the user. Reuse still-valid decision evidence; focus follow-ups on changed uncertainty. Do not add a second full reviewer just to repeat this verification. Use completion notifications or meaningful waits. On a timeout with no new evidence, resume waiting without status polling, replanning, or repeating prior reasoning; keep needed user updates brief and factual.

## Snapshot and artifact contract

Before dependency installation, environment setup, tests, builds, or browser work, independently check artifact structure, completed task entries, approvals/dependencies, and the clean candidate/base. Use available deterministic artifact/task diagnostics. On any invalid input, stop and write only a blocked report with the discrepancy and recovery; do not continue proof while awaiting reconciliation. All three approved artifacts are required for a pass. Compute their digests with `python3 <this-skill-dir>/scripts/fingerprint.py <artifact-path>` and compare `approved_digest` and downstream dependency fields. Canonical digests exclude only `status` and `approved_digest`, and normalize task checkbox state in the plan's Order of work; other content, including approver and base, is bound. Missing, malformed, stale, or mismatched bindings block a pass and route to the owning skill for reconciliation/reapproval.

At inspection start, `HEAD` must equal the full `reviewed_head` hash and `git status --porcelain` must be empty. Inspect the full `base_commit..reviewed_head` range and artifacts. If the range is unavailable or dirty/untracked/generated files could affect the result, return `blocked`. Record repository, base, head, changed paths, working tree, and untracked paths under Change inspected.

The report records `intent_digest`, `spec_digest`, `plan_digest`, `reviewed_head`, and actual isolation. Use the literal `subagent` for a fresh subagent (or `subagent-same-model` / `subagent-different-model` when known), `fresh-session` / `separate-session` for a separate session, and `none` only for a blocked handoff; do not invent labels such as `fresh-subagent`. After writing, recheck artifacts and the implementation snapshot. A report commit or allowed status-only bookkeeping can advance HEAD; source or other semantic changes invalidate the report. Continue/archive enforce the same contract.

## Validation ownership and evidence

Own one full change-appropriate final gate on the stable completed feature snapshot. No other writer may change that reviewed checkout or artifact inputs during review; subsequent changes require fresh verification. Parallel research may inspect other work, but another implementation lane waits until review finishes or is blocked. Follow repository instructions and the approved Proof; do not add a universal suite. Focused implementation checks need not become repeated full gates. Do not silently omit duplicate checks required by an existing approved plan: reconcile/reapprove its proof before verification.

Reuse an earlier check receipt only if you independently inspect raw output and provenance and establish that code, tests, configuration/lockfiles, dependencies, command scope, and environment match this snapshot. Record the producing commit, identity of those inputs, command, result, and evidence path. A report/status-only commit need not rerun the suite when those inputs are unchanged. A claim, stale/missing output, changed input, or uncertain equivalence requires a rerun. Never reuse a prior verdict as the current verdict.

Even with valid receipts, independently inspect the full diff and gather fresh targeted evidence for material behavior and important failure paths. For UI changes, drive the main flow and an error path in the running app and preserve screenshot/DOM evidence; tests alone do not prove that flow. For non-UI changes, run the actual project verification command unless its required results are covered by a valid receipt. Cover every spec scenario, mapping shared checks to their named scenarios rather than rerunning a suite for each one.

Before expensive integration proof, cheaply check candidate identity, dependencies, ports, fixtures/schema readiness, isolation, and relevant probe behavior. Use the smallest meaningful probe of the actual launcher and child environment, rather than parent configuration alone. Run dependent setup steps sequentially and stop on failure. Before migrations or other mutating proof, verify the actual child connection resolves to the intended disposable database/schema or equivalent target; never fall back to a shared default. Missing or mismatched isolation is blocked. After a failure, retain actionable phase/cause evidence and use the narrowest feasible reproduction before another full run; explain when that requires the full check. Reconcile a changed source candidate and pinned proof inputs under the existing approval policy; a diagnostic repair is not proof of the originally pinned candidate. After two failures of the same class, stop repeating the full gate and return a precise blocker/recovery or evidence-backed failure for a focused reassessment. Do not waive proof or run against production.

For a changed shared invariant or command, independently identify affected existing callers/writers and exercise their important retained behavior and success/error acknowledgements. Check this against intent and source even if the plan covers only the new path. A missing material compatibility scenario is a design/plan gap to reconcile, not grounds for a pass. For schema changes, inspect migration identity/order and require evidence that upgrade over the applicable existing migration history actually applies the change and preserves data. A fresh-database pass or successful build is not equivalent. Existing matched receipts may cover these checks under the reuse rule above; do not add a duplicate full gate.

## Report and verdict

Use `assets/report.md` and retain its headings. Before judging spec compliance, check that its requirements and the delivered behavior still satisfy the accepted intent and material constraints. Flag a spec that missed or changed the user's outcome rather than passing an implementation merely because it matches that spec. A material spec gap returns to `sdlc-design` for draft/reapproval, then `sdlc-apply` for dependent plan reconciliation/reapproval before implementation resumes; the verifier writes only its report. Under each Verification subsection write at least one `- PASS | action: ... | observed: ... | evidence: ...` entry (or `FAIL`/`BLOCKED`). Include each requirement name verbatim in the `action:` of a Completeness entry and each scenario name verbatim in the `action:` of a Correctness entry; entries may reference shared receipts/checks. Coherence covers the entire change, trust boundaries, regressions, error handling, existing patterns, and each applicable spec Gotcha's plan check. All plan boxes must be ticked. Cite exact commands/actions and inspectable output, record skipped checks, and pin CRITICAL/WARNING/SUGGESTION findings to `file:line`. Record relevant rollout, migration, recovery, and observation under Release handoff; otherwise `None.`

- `pass`: all required outcomes/checks have evidence, the plan is complete, snapshot and bindings are valid, and no CRITICAL finding remains.
- `fail`: evidence shows an outcome is wrong, incomplete, or unsafe. Hand off to apply for repair and fresh verification; never flip the report to pass yourself.
- `blocked`: judgment is prevented by missing environment, capability, permission, artifact, or snapshot. Record the reason and recovery; it never permits completion/archive.

If no independent review occurred, the orchestrator may write only a blocked handoff with the three approved digest fields, `verdict: blocked`, `isolation: none`, and exactly two nonempty lines under Not checked: `Reason: <blocker>` and `Recovery: <next step>`. It may omit unavailable provenance/sections; Findings may be absent or `None.` A dispatched reviewer records its actual isolation even when blocked.

The parent checks report content and returns any format/evidence gaps to this verifier before committing the report exactly once, separately, after `reviewed_head`. An uncommitted report is not yet a valid pass; the available deterministic validator must pass after that commit. Repair an already committed report only by replacing its owned, unshared report-only tip; otherwise use fresh verification on a new clean candidate. Never amend the reviewed implementation or append another report commit to the same verdict. Use Conventional Commits (`docs(scope): imperative summary`, scope optional), a blank line, and one sentence on why. Only a current independent pass permits completion under the calling workflow's approval policy. Archive is separate.
