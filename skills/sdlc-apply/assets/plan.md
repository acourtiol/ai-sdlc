---
status: draft
slug: example-slug
spec: spec.md
base_commit: pending
spec_digest: pending
approved_by: pending
approved_digest: pending
---

# Plan: short name

## Files that change

Exact paths. New vs edit. One line each on what changes. Name the single implementation owner; parallel researchers are read-only.

## Order of work

Replace this guidance with task boxes only. Use numeric prefixes for coherent,
reviewable changes, each with a focused check and commit; do not split by individual
file, tool call, or bookkeeping. Keep one implementer on related work. Remove every
example before approval. Boxes end at implementation, implementer-owned checks
and a committed handoff. Put final independent verification/report and
completion/archive in Review route; they cannot be checkbox prerequisites. For an
affected integration or stateful flow, put the first actual route/runtime slice
early: verify the risky contract and response plus committed state before building
all adjacent surfaces. Choose applicable failure/reload/retry cases from the spec.

- [ ] 1.1 What changes — verify: command, test, or observable behavior
- [ ] 1.2 Next step in this area — verify: ...
- [ ] 2.1 First step in the next area — verify: ...

## Risks

Carry each applicable spec Gotcha here with its concrete failure case and a
matching check in Order of work or Proof. Include only relevant migration,
external-API, compatibility, security, safety, or accessibility checks. Write
`None.` if no applicable risks were identified. Include prerequisite contract/migration owners and order, implementation versus intended delivery baseline, and shared verification resources where applicable; verify target-source dependencies before implementation, without assuming release permission.

## Proof

The end-to-end evidence that the whole spec is met. Name each check's scope and
owner: focused checks per slice, one final full change-appropriate gate owned by the
fresh verifier. Retained raw receipts and provenance use persistent, non-cache
storage; temporary scratch is not their sole copy. Consolidate overlapping gates
before approval; map shared checks to requirements/scenarios. Record cheap prerequisites before expensive integration
proof and the focused reassessment after two failures of the same class. An earlier
full gate needs a repository requirement or concrete integration risk. Name an early
probe of the affected real action through the normal launcher. Ground provider/driver
response and error variants in established adapters and contract evidence; distinguish
contract-backed fixture checks from live proof. For stateful flows, assert response
and persisted state through the actual route/runtime on disposable persistence,
including relevant failure, pending reload/recovery and retry transitions. After a
defect, check related branches sharing its contract or transition with focused
regressions before another broad gate/review; do not wait for repeated failures.
For changed shared invariants, cover affected existing callers/writers and their acknowledgements.
For schema changes, check ordering against already-applied migration history and
prove upgrade/data preservation on a disposable database; fresh creation alone
is insufficient. Use authorized baseline evidence and retain missing release
prerequisites explicitly. Stop dependent setup on failure; verify the actual child
connection target before mutating proof, with no shared-default fallback.

## Review route

Name the fresh verifier subagent or separate fresh-session handoff capability
available in this host, along with the stable completed-feature boundary,
environment and access. This assigns a task, not a required agent profile. Prevent
inheritance of implementation history using the host's available mechanism or a
separate fresh session; confirm actual isolation. Combine source review
and behavioral verification; before dispatch, check artifact/task structure,
canonical approvals/dependencies and the clean committed candidate/base. Freeze
those inputs; the verifier repeats this cheap check before setup or full proof.
Dispatch when the committed candidate is ready,
not to wait for code. An autonomous run needs a dispatchable verifier before code.
State the subsequent independent report and completion/archive sequence here,
after implementation boxes are checked; no box depends on that report.
Any interim review needs an explicit unresolved risk or binding requirement.

## Decision review

For autonomous approval only: decision, confidence, evidence for explicit outcome
and constraints, current-source support, contracts and important failure modes,
and unresolved assumptions/conflicts. At high confidence, explain why a challenge
was skipped. Otherwise record the focused challenge, checked evidence, resolution,
and residual uncertainty. Reference still-valid upstream evidence without copying
it. Replace superseded rationale; keep only current decisions and unresolved risks, preserving history in Git. Aim for a 1,000–2,000-word operative plan unless current scope needs more. Compact through reapproval, retaining task states/base/proof and reconciling downstream digests. Remove this guidance before approval.
