---
name: sdlc-apply
description: >-
  Implements an approved spec: writes intent/<slug>/plan.md, waits for plan
  approval, then codes against that plan. Use when the user is ready to build a
  specified intent. Do not start code before the plan is approved.
license: MIT
metadata:
  author: acourtiol
  version: "1.0"
---

# sdlc-apply

Produce `intent/<slug>/plan.md`, wait for approve, then implement. Ceiling is Test + review — do not deploy or push unless the user asks.

## House rules

- If the repo has `openspec/` with open changes, stop and use OpenSpec (`openspec` binary, never `npx openspec`).
- Do not commit unless the user asks. Do not push. Do not deploy.
- Require `intent/<slug>/spec.md` with `status: specified` (or explicit approve in this session).
- Named **planner** is read-only: it returns the plan markdown. This session writes `plan.md` after the user approves the plan. Named **coder** implements only after `plan.md` is `planned`.
- If implementation departs from the plan, update `plan.md` in the same change (same commit if they asked to commit).
- Upgrade path (not this skill): per-repo production hook later. Do not add `production-gate.sh` or `bands.yaml` here.

## Steps

1. Resolve `<slug>`. Read `intent.md` + `spec.md`.
2. Dispatch planner (read-only): files that change, order of work, risks, proof. Draft must be implementable by someone who did not see the chat.
3. Write `intent/<slug>/plan.md` from `assets/plan.md` (`status: draft`). Ask the user to **approve the plan**.
4. On approve, set `status: planned`. Only then dispatch **coder** (or implement here) against that plan. Smallest correct change. Real tests, not placeholders.
5. After code, say `sdlc-verify` is next. Do not declare done without verification.

If the plan is already `planned` and the user says implement, skip to step 4.
