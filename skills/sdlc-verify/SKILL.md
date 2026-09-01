---
name: sdlc-verify
description: >-
  Verifies a built change against intent/<slug>/intent.md with evidence
  (commands, agent-browser, screenshots). Use after implementation, before
  calling the work done. Reports pass/fail only — does not edit source.
license: MIT
metadata:
  author: acourtiol
  version: "1.0"
---

# sdlc-verify

Judge the change against the intent. Evidence required. Do not edit application source or tests.

## House rules

- If the repo has `openspec/` with open changes and the user is verifying that OpenSpec work, use `openspec-verify-change` instead.
- Do not commit unless the user asks.
- Dispatch the named **verifier** when available. Same contract if you verify in this session.
- Pass/fail is against `intent.md` proposed outcome (and spec/plan if present), not against "tests are green" alone.

## Steps

1. Resolve `<slug>`. Read `intent.md`. Read `spec.md` / `plan.md` if they exist.
2. If the change is user-facing, drive the running app (`agent-browser` skill/CLI): the flows in the intent, plus an error path. Screenshots or DOM as evidence.
3. If there is no UI, run the project's real verify command and read the output.
4. Report each check: what you did, what you observed, pass or fail. Never declare success without proof.
5. If it passes and the user is done, set intent (and spec/plan if present) `status: done` only when they agree. Next is the named **reviewer** on the diff vs spec+plan — that is a separate pass, not this skill.
