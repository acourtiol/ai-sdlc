---
name: sdlc-verify
description: >-
  Independently verify a completed change against its intent, spec, and plan.
  Use after implementation, before marking artifacts done or archiving, or when
  asked to verify a change. A fresh verifier subagent or separate fresh session
  writes an evidence-based report; an unavailable review or check is blocked,
  never a pass. Do not edit application source or tests.
license: MIT
metadata:
  author: acourtiol
  version: "2.0"
---

# sdlc-verify

Judge the implementation against the accepted intent and approved artifacts. Cite what you inspected, what you ran or observed, and the result in `intent/<slug>/report.md`. Do not edit application source or tests. This skill is judgment-only: fixes belong to `sdlc-apply`, followed by a new independent verification.

For a report commit, follow Conventional Commits 1.0.0: `docs(scope): imperative summary` (scope optional), a blank line, and one sentence on why.

## Review route and timing

Before implementation starts, `sdlc-apply` must establish a usable independent review route and record it in the plan. The route is either a verifier subagent with fresh context or a separate fresh session that receives the handoff below. If neither can be arranged, implementation cannot enter the autonomous path; report the missing capability as blocked. Do not discover this only after implementation is complete.

The verifier gets no implementing conversation, summary, or conclusions. It receives the repository and artifact paths, the approved artifact digests, `reviewed_head` candidate, and the verification instructions. It independently reads the source and forms its judgment. Ask a research reviewer, where available, to identify the strongest case against the material decisions and what evidence could falsify them. Consider its evidence and dissent; agreement is not proof.

For consequential changes—such as authorization, sensitive data, irreversible operations or migrations, financial calculations, or safety-critical behavior—verify the exact reviewed commit in a disposable checkout. Use a disposable test environment with limited credentials; never run consequential checks against production data or services. If required isolation or test access is unavailable, return `blocked`.

### Fresh-session handoff

When the host cannot dispatch a subagent but a separate session can be started, provide that session with only:

- repository location and slug;
- paths to `intent.md`, `spec.md`, `plan.md`, this skill, and the report template;
- the three approved digests, `reviewed_head`, and the relevant plan base commit;
- the expected user outcomes and scenarios to exercise;
- this instruction: independently inspect the exact snapshot, run the verification steps, challenge material decisions with source evidence, and write the report without relying on the implementation session's claims.

The new session writes the report and returns its path and evidence. The initiating session may commit only that report after checking its provenance and validating that no reviewed input changed. Record `isolation: fresh-session`. A handoff that is merely sent back to the implementing session for self-review is not independent.

If no independent route is available, the orchestrator may write a minimal blocked handoff with the three approved digest fields, `verdict: blocked`, and `isolation: none`. Its `## Not checked` section must contain exactly two nonempty lines: `Reason: <specific blocker>` and `Recovery: <concrete next step>`. It may omit review snapshot provenance and other sections it could not establish; `Findings` may be omitted or say `None.` A dispatched reviewer blocked by its environment records its actual `subagent` or `fresh-session` isolation. Neither case permits completion. Do not claim a review occurred when it did not.

## Snapshot and artifact contract

The report frontmatter records `intent_digest`, `spec_digest`, and `plan_digest` from the corresponding artifacts' `approved_digest` fields, plus the full commit hash in `reviewed_head` when snapshot inspection occurred. All three approved artifacts are required for a pass. If one is missing, return to its owning skill; if that prevents a valid judgment, record a blocked handoff with the specific recovery step. A missing or malformed digest, a dependency mismatch, or a digest that does not match the artifact blocks a pass.

Compute each artifact digest with `python3 <this-skill-dir>/scripts/fingerprint.py <artifact-path>` and compare it with `approved_digest`. The canonical digest excludes only `status` and `approved_digest`; it includes `approved_by`, dependency digests, `base_commit`, and all other content. It normalizes task checkbox state in the plan's “Order of work.” `intent_digest`/`spec_digest` on later artifacts must match the upstream approved digest used to prepare them.

Pass only against a committed, clean snapshot: at the start of inspection, `HEAD` must equal `reviewed_head` and `git status --porcelain` must be empty. Inspect the plan's `base_commit..reviewed_head` range and the full artifact contents. If the change range cannot be established, or any dirty, untracked, or in-scope generated file could affect the result, use `blocked` until it is committed and reviewed. In `## Change inspected`, state the base, reviewed head, changed paths, working-tree state, and untracked paths.

After writing the report, validate that the intent/spec/plan digests and reviewed implementation snapshot remain unchanged. A report commit and explicitly allowed status-only bookkeeping may advance `HEAD`; they do not excuse source, spec, plan, or other semantic changes. Any such change invalidates the report and requires a new verification. The repository's status check and archive gate must enforce the same rule.

## Steps

1. Resolve the slug and read `intent.md`, `spec.md`, and `plan.md`. Check their approval states, digests, and dependency links. Resolve the exact `reviewed_head` and plan `base_commit` before judging behavior. Missing prerequisite artifacts cannot receive a pass.
2. Inspect the full committed change range, repository conventions, working tree, and untracked files. Record the repository, base, reviewed head, changed paths, working-tree state, and untracked paths in `## Change inspected`. Do not infer that a clean tree means no implementation exists; use the committed range.
3. For a user-facing change, exercise the intent's main flow and an error path in the running app. Preserve a screenshot, DOM snapshot, or similarly inspectable evidence in the report. Name the visible state and what a person would observe. Tests alone cannot establish this evidence.
4. For a change without a user interface, run the project's actual verification command and inspect its output. Do not invent a command or report a check that did not run.
5. Judge:
   - **Completeness:** every plan task is checked and every `### Requirement:` in the spec has evidence.
   - **Correctness:** exercise every `#### Scenario:` and compare the observed result with the intent's proposed outcome.
   - **Coherence:** review the entire change range for logic, security and trust-boundary errors, regressions, error handling, and fit with the spec, plan, and existing patterns. For every applicable spec Gotcha, inspect its matching plan check and evidence.
6. Under each Verification subsection, write at least one `- PASS | action: ... | observed: ... | evidence: ...` entry (or `FAIL`/`BLOCKED`). Name every spec requirement in Completeness and every spec scenario in Correctness. Use the exact command or user action, a concise observed result, and an evidence path or output excerpt. List skipped checks and why. Pin each finding to `file:line` and label it `CRITICAL`, `WARNING`, or `SUGGESTION`. Where relevant, record rollout prerequisites, migration state, recovery, and post-release observations under Release handoff; write `None.` otherwise. Do not declare success without evidence.
7. Choose the verdict:
   - `pass`: required outcomes and checks have evidence, all plan tasks are complete, no CRITICAL finding remains, and the inspected snapshot is valid.
   - `fail`: evidence shows a required outcome is wrong, incomplete, or unsafe. Route to `sdlc-apply` for a fix and then verify again with a new reviewer.
   - `blocked`: the reviewer cannot reach a valid judgment because a required environment, capability, permission, artifact, or snapshot is unavailable. State the precise blocker and recovery action. Blocked is not a product failure and never permits completion or archive.
8. Write `intent/<slug>/report.md` from `assets/report.md` using the contract's section headings. A full report must include all three approved digests and snapshot provenance. For a blocked handoff without review provenance, include the artifact digests and the exact `Reason:`/`Recovery:` lines in `## Not checked`. The reviewer may write only this report. Keep a failing or blocked report as evidence; never edit it to turn it into a pass. The parent workflow commits only the report after checking ownership and freshness.

When `verdict: fail` or a CRITICAL finding remains, stop and hand off to `sdlc-apply`; do not fix code here. When `verdict: blocked`, stop the slug and preserve the blocker for resumption. Only a fresh `pass` with current digests, valid isolation, and no CRITICAL finding can proceed to completion. Autonomous mode may set the artifact statuses to `done` after this condition is mechanically validated; normal mode follows its approval policy. Archiving is a separate step.
