---
slug: example-slug
intent_digest: pending
spec_digest: pending
plan_digest: pending
reviewed_head: pending
verdict: blocked
isolation: none
---

# Report: short name

## Change inspected

- Isolation: use `subagent`, `subagent-same-model`, `subagent-different-model`, `fresh-session`, or `separate-session`; `none` is only for a blocked handoff. Record the same literal in frontmatter; do not invent `fresh-subagent`.
- Repository and branch:
- Plan base commit:
- Reviewed HEAD (must match frontmatter):
- Changed paths in the reviewed range:
- Working tree: `git status --porcelain` result at review start:
- Untracked paths:
- Artifact digests: list the exact approved digests recorded above and confirm dependency links.

## What shipped

What the change actually does now, the affected surfaces, and the requirements it satisfies. Use the reviewed diff and approved artifacts, not implementation-session claims.

## Deviations from plan

TBD: where the implementation departed from the plan and why, with evidence, or write `None.`

## Verification

For each check, use `- PASS | action: <exact command or user action> | observed: <result> | evidence: <path or output excerpt>` (or `FAIL`/`BLOCKED`). Include each requirement name verbatim in a Completeness `action:` and each scenario name verbatim in a Correctness `action:`; reference shared check entries instead of repeating commands. For reused receipts, identify producing commit, matching code/tests/configuration/dependencies/environment and command scope, raw output and result. Record fresh targeted observations by this verifier as well.

### Completeness

Name every spec requirement and its check entry. Confirm every plan box is ticked.
Compare the delivered result with the original accepted intent and constraints;
a spec that missed the wanted outcome cannot justify a pass. Report a material
spec gap for `sdlc-design` draft/reapproval, followed by dependent plan
reconciliation/reapproval in `sdlc-apply`; do not edit those artifacts here.

### Correctness

Name every spec scenario and its check entry. For user-facing changes, include the main flow, an error path, and a human-observable state with screenshot/DOM evidence.

### Coherence

Give check entries for the full diff's logic, trust boundaries, regressions, error handling, and fit with the spec, plan, and existing patterns. For each applicable spec Gotcha, identify its plan check and observed evidence.

## Independent challenge

TBD: record confidence with evidence for explicit outcome/constraints, current-source support, contracts and important failure modes, and absence of unresolved material assumptions/conflicts. Explain why a separate challenge was skipped at high confidence, or summarize the focused challenge, evidence checked, resolution, and residual uncertainty. Final fresh verification remains mandatory. Remove this guidance before writing the report.

## Findings

Write `None.` or list each finding as `- CRITICAL`, `- WARNING`, or `- SUGGESTION`, pinned to `file:line`. State what evidence would settle uncertain impact.

## Not checked

Which checks you skipped and why. Write `None.` if every applicable check ran. For a blocked handoff, replace this prompt with exactly two nonempty lines: `Reason: <specific blocker>` and `Recovery: <concrete next step>`.

## Release handoff

Where relevant, list rollout prerequisites, migration state, recovery or rollback,
and post-release observations with an owner. Write `None.` if this change has no
release handoff. Archive alone does not claim deployment succeeded.

## Verdict

Write `pass`, `fail`, or `blocked`, matching frontmatter. A pass requires evidence for every required outcome, a complete plan, a clean committed reviewed snapshot, matching approved digests, and no CRITICAL findings. A blocked handoff may omit snapshot provenance; it never permits completion or archive. Any work that still needs a separate change belongs in a new intent.
