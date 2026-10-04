---
name: sdlc-fix
description: >-
  Fix a bounded bug or make a behavior-preserving refactor in an existing,
  readable flow. Reproduce and verify the change, with stronger independent
  review for consequential behavior. Route new capabilities or architectural
  changes through sdlc-plan. Do not push unless asked.
license: MIT
metadata:
  author: acourtiol
  version: "1.12"
---

# sdlc-fix

Repair a bounded existing flow without opening `intent/<slug>/`. The fix request normally authorizes a commit containing only this concern, subject to explicit user restrictions and the host's permission policy. It does not authorize a push or external action.

## Choose the workflow by scope and consequence

This path fits a concrete bug in an existing readable flow or a behavior-preserving refactor. Judge both the size of the change and the impact if it is wrong; a small patch can be high consequence and a large mechanical change can be low consequence.

Use `sdlc-plan` if investigation reveals a new capability, unresolved product choice, architectural decision, or work spanning multiple subsystems. Do not disguise expanded scope as a fix.

Escalate assurance for changes affecting authorization, sensitive data, irreversible operations or migrations, financial calculations, safety-critical behavior, or another consequential invariant. Before editing, establish an independent reviewer route at the stable completed-fix boundary. Use the host's available delegation mechanism without inherited implementation history, or a separate fresh session with a bounded handoff. No named agent profile or particular model is required. Confirm actual isolation; review with inherited implementation history cannot pass as independent. If the host cannot provide that capability, do not make an autonomous consequential fix; state the blocker. Use a disposable checkout and a limited test environment for the independent check when the change could damage data or depend on privileged access. No review route makes the work blocked, not verified.

## Ownership preflight

Before editing, record the repository root, branch, and `HEAD`, then inspect:

```sh
git status --short
git diff --cached
git diff
git ls-files --others --exclude-standard
```

Use the current owning checkout by default; create another only to isolate concrete overlapping work or provide a clean review candidate. For an agent-created checkout, use the agreed project workspace's `.worktrees/<purpose>` by default, anchoring its root once from the initial workspace to avoid nested worktree areas. Before creation, ensure it is excluded from Git tracking and relevant source/test discovery, applying the project's targeted exclusion convention if needed. Keep host-managed isolation when required and record its path and reason. Use persistent, non-cache storage for resumable checkouts and retained proof receipts; temporary directories are disposable scratch. Preserve all existing work. Do not reset, stash, clean, or include unrelated changes. If an existing staged or unstaged diff touches a path you need to edit, use an isolated worktree or separate the exact hunks before proceeding; `git commit --only` commits the selected path's full working-tree content. If you cannot separate ownership safely, stop before editing that path. For unrelated staged files, keep them staged and commit this fix with an explicit path-only commit (`git commit --only -- <owned-paths>`), after reviewing exactly what that command will include. Never use `git add -A`.

## Confidence and check scope

Keep one active implementation lane per product repo through its final review; implement here by default or retain one delegated owner. Parallel research is read-only. Queue other fixes/features unless explicitly reprioritized, checkpointing before a switch. A separate decision challenger is needed only when confidence is below high: the outcome/constraints, current-source support, evidence for relevant contracts and important failure modes, and absence of unresolved material assumptions must all hold for high confidence. Consequential behavior needs stronger evidence. A missing preference or authority needs the user. Challenge the strongest uncertainty with bounded inputs; reuse resolved evidence and avoid repeated agent polling. Required consequential independent verification remains in place regardless of confidence.

Before the first implementation check, inspect the configured runner/discovery rules for affected tests, including component tests and distinct file extensions. In existing Proof or the fix record, name relevant tests omitted by the normal command and their explicit runner. Run those focused tests early; a green broad receipt cannot cover files it excludes. Classify failures against the baseline without changing assertions to hide them; unavailable required coverage remains blocked.

Bound checks to the reported behavior, complete fix diff and concretely affected contracts/callers. For adjacent flows, name the changed dependency/invariant and use its smallest meaningful regression or smoke; do not recertify a whole earlier feature. Broader checks need a binding repository/user requirement, concrete integration risk or observed failure.

Use focused affected checks in the local loop. Run a full suite when repository instructions or the change's integration risk require it; give final validation one owner rather than repeat it in both implementation and review. Before expensive isolated checks, verify candidate identity and relevant dependencies, ports, fixtures/schema, and probes cheaply. Use the smallest meaningful probe of the actual launcher and child environment, rather than parent configuration alone. After a failure, retain actionable phase/cause evidence and use the narrowest feasible reproduction before another full run; explain when that requires the full check. Reconcile a changed source candidate and pinned proof inputs under the existing approval policy; a diagnostic repair is not proof of the originally pinned candidate. After two failures of the same class, reassess with a focused reproduction before retrying the full gate.

## Work

1. Read applicable repository instructions and the affected source. For a bug, establish its reported failure and cause; run the original reproduction before editing when practical. Do not claim reproduction if it could not be exercised.
2. Inspect established adapters/error parsers before changing a provider/runtime boundary; use source, version-matched documentation or authorized captured evidence for consequential response/error shapes, rather than invented mocks. Inspect related branches sharing the defect’s contract, transition or error handling and repair confirmed defects within this bounded scope. Broader scope returns to `sdlc-plan`. Make the smallest root-cause change. For a refactor, state the behavior that must remain true. Preserve applicable validation, error handling, security, and accessibility.
3. Run the original reproduction and focused checks for the affected failure family before another broad run or independent review. For stateful defects, exercise the actual route/runtime against disposable persistence and assert the committed result after relevant failure, retry or reload; a helper return value alone cannot establish durable behavior. Contract-backed fixtures establish local handling, not live provider success. Read the check output. A regression test should fail for the reported reason when a durable automated check is useful; otherwise record the concrete reproduction and why a test does not fit. If the required environment or permission is unavailable, record a blocked result rather than a pass.
4. Review the final diff and confirm no unrelated path or user change is included. Commit the complete locally checked candidate before independent review. Follow Conventional Commits 1.0.0: `type(scope): imperative summary` (scope optional; use `fix` for bugs or `refactor` for behavior-preserving changes). Add a blank line and a sentence explaining why, with the local check evidence; mark breaking changes with `!` or a `BREAKING CHANGE:` footer. Follow the ownership preflight; do not commit if the selected paths contain work whose ownership is ambiguous. Leave no fix files dirty. A candidate commit does not establish independent verification or completion.
5. For a consequential change, dispatch the fresh independent reviewer against that exact committed candidate in a clean checkout; combine source review and final validation instead of routine per-edit reviews. Reuse an owned, clean, inactive review checkout for a later candidate only after retaining its prior report and required receipts and confirming it can be prepared without discarding work; the reviewer must still use fresh context. It independently reproduces the fixed behavior and important failure paths; a separate decision challenger is conditional on confidence. Existing check receipts may supplement review when inspectable results and all relevant code/tests/configuration, command scope, transitive/runtime dependencies and environment match the reviewed snapshot; unrelated commit differences alone do not invalidate them. Producing inputs may be verified from immutable source and retained evidence without a specific pre-run manifest format; never assign current hashes to unknown earlier inputs. Rerun if uncertain. Never accept an implementation-session claim as proof. Record the reviewed commit, evidence, findings, and resolved dissent in the existing task/PR record or final response without amending the reviewed candidate. Repairs need a new locally checked commit and fresh verification; unavailable proof remains blocked. Do not claim completion or push a consequential fix before an independent pass. Do not push unless the user asks.

When the request follows an incident or escaped defect, identify how the defect passed earlier checks and add a durable prevention that fits the cause: a regression test, clearer contract, missing diagnostic, or focused repository instruction. Route broader product changes through `sdlc-plan`.

Report what passed, failed, or could not be checked, and what evidence supports the result. A green suite alone does not prove the reported behavior was fixed.

At verified completion, make a bounded knowledge check only if the project or environment already configures a knowledge bundle or maintenance workflow. Use that workflow to update a relevant existing durable note when this fix supersedes it; otherwise skip. Do not create a note just to record the session, scan the whole bundle or unrelated knowledge, or bootstrap a missing bundle. This adds no delivery gate. Keep any knowledge edit outside the reviewed candidate so it does not invalidate the fix's independent verification.

At completion, inspect worktrees you own and remove only clean, inactive checkouts with no unfinished task/handoff, whose commits and evidence are retained and which have no live process using them. Do not force-remove, delete branches, move live checkouts, or prune globally. If ownership or safety is unclear, keep the checkout and record its path and reason in the handoff.
