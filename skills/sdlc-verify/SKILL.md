---
name: sdlc-verify
description: >-
  Checks a built change against intent/slug/intent.md with evidence (commands,
  browser, screenshots) and writes intent/slug/report.md: what shipped,
  deviations from the plan, and a pass or fail verdict. Use after
  implementation, before calling the work done, or when the user asks to verify,
  test, see if it works, or is this done. Do not edit application source.
license: MIT
metadata:
  author: acourtiol
  version: "1.2"
---

# sdlc-verify

Judge the change against the intent. Cite what you did and what you saw. Write the verdict down as `intent/<slug>/report.md`. Do not edit application source or tests.

Green tests are not enough. The intent's proposed outcome is the bar.

## Before you start

Do not commit unless the user asks.

Dispatch the named verifier when one exists. Same contract if you verify in this session. A fresh context window is the point: the verdict should not be colored by the assumptions that produced the code.

`report.md` is the one file this skill writes. Application source and tests stay untouched.

## Steps

1. Resolve slug. Read `intent.md`. Read `spec.md` and `plan.md` if they exist. Read the diff (`git status`, `git diff`) so the report describes what is actually there.
2. If the change is user-facing, drive the running app (`agent-browser` skill or CLI): the flows in the intent, plus an error path. Keep screenshots or DOM as evidence. Do not write `verdict: pass` unless the report cites a human-observable moment (what was driven or shown, and what a person would see). Green tests alone are not that moment.
3. If there is no UI, run the project's real verify command and read the output. That output is enough for a pass on this dimension; still list skipped checks under Not checked.
4. Check the three dimensions:
   - **Completeness** — every box in `plan.md` ticked, every `### Requirement:` in `spec.md` covered. An unticked box is a CRITICAL finding, whatever the code looks like.
   - **Correctness** — each `#### Scenario:` exercised: what you ran or drove, what you observed. Judge against the proposed outcome in `intent.md`. For a user-facing intent, a pass needs the human-observable moment from step 2. If that moment is missing, `verdict` is `fail` or pass is withheld, and Not checked names it.
   - **Coherence** — the diff follows the Design section of `spec.md` and the patterns already in this repo.
5. Report each check: what you did, what you observed, pass or fail. Tag findings CRITICAL, WARNING, or SUGGESTION and pin each to a `file:line`. When severity is unclear, pick the lower one. Do not declare success without proof.
6. Write `intent/<slug>/report.md` from `assets/report.md`, including a failing verdict. It records what you found, so it is not a gate and carries no `status`: the frontmatter `verdict` is `pass` or `fail`. Name every check you skipped and why, under Not checked. Missing `spec.md` or `plan.md` narrows what you can verify; say so rather than passing by default.
7. If it passes and the user agrees they are done, set intent (and spec/plan if present) `status: done`. The named reviewer on the diff vs spec and plan is a separate pass.

Next: `sdlc-archive` once the statuses are `done`.
