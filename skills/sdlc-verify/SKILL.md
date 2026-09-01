---
name: sdlc-verify
description: >-
  Checks a built change against intent/slug/intent.md with evidence (commands,
  browser, screenshots). Use after implementation, before calling the work done,
  or when the user asks to verify, test, or see if it works. Reports pass/fail
  only; do not edit source.
license: MIT
metadata:
  author: acourtiol
  version: "1.1"
---

# sdlc-verify

Judge the change against the intent. Cite what you did and what you saw. Do not edit application source or tests.

Green tests are not enough. The intent's proposed outcome is the bar.

## Before you start

If the user is verifying OpenSpec work in a repo with open `openspec/` changes, use `openspec-verify-change` instead.

Do not commit unless the user asks.

Dispatch the named verifier when one exists. Same contract if you verify in this session.

## Steps

1. Resolve slug. Read `intent.md`. Read `spec.md` and `plan.md` if they exist.
2. If the change is user-facing, drive the running app (`agent-browser` skill or CLI): the flows in the intent, plus an error path. Keep screenshots or DOM as evidence.
3. If there is no UI, run the project's real verify command and read the output.
4. Report each check: what you did, what you observed, pass or fail. Do not declare success without proof.
5. If it passes and the user agrees they are done, set intent (and spec/plan if present) `status: done`. The named reviewer on the diff vs spec and plan is a separate pass.
