---
name: sdlc-plan
description: >-
  Captures a new product feature or change as intent/<slug>/intent.md (problem,
  outcome, constraints, open questions). Use when the user starts a product idea
  or feature and the repo has no open OpenSpec change. Do not use for bugfixes,
  refactors, or implementation.
license: MIT
metadata:
  author: acourtiol
  version: "1.0"
---

# sdlc-plan

Write `intent/<slug>/intent.md` from the user's idea. Stop for accept. Do not write spec, plan, or code.

## House rules

- If the repo has `openspec/` with open (non-archived) changes, stop and use OpenSpec (`openspec` binary, never `npx openspec`).
- Do not commit unless the user asks.
- Do not create `CLAUDE.md` or auto-memory. Repeated mistakes go in project `AGENTS.md` or the repo OKF bundle.
- Beads are tickets, not these artifacts. Optional: mention a bead id in the intent body.

## Steps

1. If `openspec/` exists and has open changes, stop (see above).
2. Interview until the idea is concrete: what cannot be done today, who is affected, what better looks like, constraints, out of scope. One question at a time when a missing answer would change the artifact.
3. Derive a kebab-case `slug` from the idea. If `intent/<slug>/` already exists, pick another slug or resume with `sdlc-continue`.
4. Copy `assets/intent.md` from this skill into `intent/<slug>/intent.md`. Fill every section. Frontmatter: `status: draft`, `slug: <slug>`.
5. Show the file path and a short summary. Ask the user to **accept** (→ Design) or correct it.
6. If they accept in this session, set `status: accepted`. Do not start `sdlc-design` until they ask or accept.

After accept, the next skill is `sdlc-design`.
