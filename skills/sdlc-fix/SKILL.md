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
  version: "1.1"
---

# sdlc-fix

Repair a bounded existing flow without opening `intent/<slug>/`. The fix request normally authorizes a commit containing only this concern, subject to explicit user restrictions and the host's permission policy. It does not authorize a push or external action.

## Choose the workflow by scope and consequence

This path fits a concrete bug in an existing readable flow or a behavior-preserving refactor. Judge both the size of the change and the impact if it is wrong; a small patch can be high consequence and a large mechanical change can be low consequence.

Use `sdlc-plan` if investigation reveals a new capability, unresolved product choice, architectural decision, or work spanning multiple subsystems. Do not disguise expanded scope as a fix.

Escalate assurance for changes affecting authorization, sensitive data, irreversible operations or migrations, financial calculations, safety-critical behavior, or another consequential invariant. Before editing, establish that an independent reviewer can inspect the change in a fresh subagent or separate session. If the host cannot provide that capability, do not make an autonomous consequential fix; state the blocker. Use a disposable checkout and a limited test environment for the independent check when the change could damage data or depend on privileged access. No review route makes the work blocked, not verified.

## Ownership preflight

Before editing, record the repository root, branch, and `HEAD`, then inspect:

```sh
git status --short
git diff --cached
git diff
git ls-files --others --exclude-standard
```

Preserve all existing work. Do not reset, stash, clean, or include unrelated changes. If an existing staged or unstaged diff touches a path you need to edit, use an isolated worktree or separate the exact hunks before proceeding; `git commit --only` commits the selected path's full working-tree content. If you cannot separate ownership safely, stop before editing that path. For unrelated staged files, keep them staged and commit this fix with an explicit path-only commit (`git commit --only -- <owned-paths>`), after reviewing exactly what that command will include. Never use `git add -A`.

## Work

1. Read the repository's `AGENTS.md` and the affected source. For a bug, establish its reported failure and cause; run the original reproduction before editing when practical. Do not claim reproduction if it could not be exercised.
2. Make the smallest root-cause change. For a refactor, state the behavior that must remain true. Preserve applicable validation, error handling, security, and accessibility.
3. Run the original reproduction and relevant checks. Read their output. A regression test should fail for the reported reason when a durable automated check is useful; otherwise record the concrete reproduction and why a test does not fit. If the required environment or permission is unavailable, record a blocked result rather than a pass.
4. For a consequential change, ask the independent reviewer to find the strongest evidence-backed reason the fix could be wrong, inspect the relevant source and tests in a fresh context, and name evidence that would settle each objection. Resolve findings or stop blocked. Summarize the review and any resolved dissent in the commit body so the reasoning survives the session.
5. Review the final diff and confirm no unrelated path or user change is included. Commit only the verified fix with an imperative subject, a blank line, and a sentence explaining why. Follow the ownership preflight; do not commit if the selected paths contain work whose ownership is ambiguous. Leave no fix files dirty. Do not push unless the user asks.

When the request follows an incident or escaped defect, identify how the defect passed earlier checks and add a durable prevention that fits the cause: a regression test, clearer contract, missing diagnostic, or focused repository instruction. Route broader product changes through `sdlc-plan`.

Report what passed, failed, or could not be checked, and what evidence supports the result. A green suite alone does not prove the reported behavior was fixed.
