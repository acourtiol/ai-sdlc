---
name: sdlc-design
description: >-
  Turns an accepted intent/<slug>/intent.md into intent/<slug>/spec.md
  (requirements, design, gotchas). Use after the user accepts an intent, or when
  they ask for a spec / design for an existing intent. Planning only — do not
  implement.
license: MIT
metadata:
  author: acourtiol
  version: "1.0"
---

# sdlc-design

Write `intent/<slug>/spec.md` from an accepted intent. Stop for approve. Do not write plan or code.

## House rules

- If the repo has `openspec/` with open changes, stop and use OpenSpec (`openspec` binary, never `npx openspec`).
- Do not commit unless the user asks.
- Require `intent/<slug>/intent.md` with `status: accepted` (or the user explicitly accepting in this session). If it is still `draft`, run `sdlc-plan` / ask them to accept first.
- The named **planner** subagent is read-only. Dispatch it to research the codebase and return spec markdown; this session writes the file after the user approves. If no subagent is available, research here, still present the draft, still wait.

## Steps

1. Resolve `<slug>` (user names it, or the only `intent/*/intent.md` that is `accepted` without a spec).
2. Read `intent.md`. Dispatch planner (read-only) with: intent path, ask for requirements + design that fit this repo, flag policy/gotchas.
3. Copy `assets/spec.md` into `intent/<slug>/spec.md` as `status: draft` only after you have a complete draft. Prefer showing the draft first; write the file when the content is ready, still `draft` until they approve.
4. Ask the user to **approve** the spec (→ Build) or correct it.
5. On approve, set spec `status: specified`. Do not start `sdlc-apply` until they ask.

Next skill: `sdlc-apply`.
