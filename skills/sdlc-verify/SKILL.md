---
name: sdlc-verify
description: >-
  After apply, dispatch a verifier subagent with a fresh context to check a
  built change against intent/slug/intent.md with
  evidence (commands, browser, screenshots) and write intent/slug/report.md:
  what shipped, deviations from the plan, and a pass or fail verdict. Use after
  implementation, before calling the work done, or when the user asks to
  verify, test, see if it works, or is this done. Do not skip verify. Do not
  archive. Do not verify in the implementing session. Judgment only: do not
  edit application source or tests, do not fix, do not flip a fail to pass.
  Fail or CRITICAL → apply fixes then re-verify.
license: MIT
metadata:
  author: acourtiol
  version: "1.6"
---

# sdlc-verify

Judge the change against the intent. Cite what you did and what you saw. Write the verdict down as `intent/<slug>/report.md`. Do not edit application source or tests.

Green tests are not enough. The intent's proposed outcome is the bar.

Verify is the playbook's verifier: fresh context, report only. The feedback loop (fix your own mistakes) is `sdlc-apply`, which re-runs this skill after it fixes. The implementing session does not judge and does not write a valid `report.md`.

## Before you start

When `report.md` is on disk, commit only that file. The verifier subagent does not commit. One concern per commit. The message says why. Do not push unless the user asks.

The named verifier subagent is judgment-only: it does not edit application source or tests. Dispatch verifier subagent with a fresh context to run the steps under **Verifier subagent** and write `intent/<slug>/report.md` from `assets/report.md`.

Leave model selection to the host. Do not choose, prefer, or switch the verifier's model. Record `isolation: subagent`. Do not write a `model` field.

If no named verifier, forked agent, or Task/subagent can be dispatched, stop without writing `report.md`. Tell the user isolated verify could not run. Do not mark statuses `done`. Do not archive. Verify in the implementing session is not valid.

`report.md` is the one file this skill writes. Application source and tests stay untouched. Do not edit `report.md` to flip a fail to pass.

## Steps

1. Resolve slug. Confirm `intent.md` is on disk, and `spec.md` and `plan.md` when those files exist.
2. Dispatch verifier subagent (judgment-only, fresh context). Give it this skill, the slug, and paths to `intent.md`, `spec.md`, and `plan.md`. Instruct it to read the diff from disk (`git status`, `git diff`) rather than from the implementer's session memory, to run **Verifier subagent** below, and to write `report.md` with `isolation: subagent` frontmatter. Leave model selection to the host. Do not write a `model` field.
3. If the host only returns markdown, write that return to `intent/<slug>/report.md` unchanged. Do not rewrite findings or verdict.
4. If dispatch fails or there is no report: stop, tell the user isolated verify could not run, and do not write a passing or partial `report.md`.
5. If `verdict: fail` or Findings has CRITICAL: stop judging. Next is `sdlc-apply` (fix the findings, then this skill again — a new verifier subagent). Do not fix application source or tests here. Do not archive. Do not stay on verify.
6. If `verdict: pass` and no CRITICAL: ask before setting intent (and spec/plan if present) `status: done`. Do not archive. The named reviewer on the diff vs spec and plan is a separate pass.

`sdlc-apply` always hands off here after the last plan box, and again after each fix. `sdlc-archive` must not run without this file, `verdict: pass` with no CRITICAL, and valid isolation frontmatter (`subagent`, `subagent-different-model`, or `subagent-same-model`).

## Verifier subagent

The dispatched agent executes this section. It does not inherit the implementing session's chat history, tool trace, or coding assumptions.

1. Read `intent.md`. Read `spec.md` and `plan.md` if they exist. Read the diff (`git status`, `git diff`) so the report describes what is actually there.
2. If the change is user-facing, drive the running app (`agent-browser` skill or CLI): the flows in the intent, plus an error path. Keep screenshots or DOM as evidence. Do not write `verdict: pass` unless the report cites a human-observable moment (what was driven or shown, and what a person would see). Green tests alone are not that moment.
3. If there is no UI, run the project's real verify command and read the output. That output is enough for a pass on this dimension; still list skipped checks under Not checked.
4. Check the three dimensions:
   - **Completeness** — every box in `plan.md` ticked, every `### Requirement:` in `spec.md` covered. An unticked box is a CRITICAL finding, whatever the code looks like.
   - **Correctness** — each `#### Scenario:` exercised: what you ran or drove, what you observed. Judge against the proposed outcome in `intent.md`. For a user-facing intent, a pass needs the human-observable moment from step 2. If that moment is missing, `verdict` is `fail` or pass is withheld, and Not checked names it.
   - **Coherence** — the diff follows the Design section of `spec.md` and the patterns already in this repo.
5. Report each check: what you did, what you observed, pass or fail. Tag findings CRITICAL, WARNING, or SUGGESTION and pin each to a `file:line`. When severity is unclear, pick the lower one. Do not declare success without proof.
6. Write `intent/<slug>/report.md` from `assets/report.md`, including a failing verdict. It records what you found, so it is not a gate and carries no `status`: the frontmatter `verdict` is `pass` or `fail`. Frontmatter `isolation` is `subagent`. Do not write a `model` field. Name every check you skipped and why, under Not checked. Missing `spec.md` or `plan.md` narrows what you can verify; say so rather than passing by default. Do not edit this file afterwards to flip a fail to pass.
