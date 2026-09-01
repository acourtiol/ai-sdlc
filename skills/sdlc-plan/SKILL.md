---
name: sdlc-plan
description: >-
  Captures a product idea as intent/slug/intent.md (problem, outcome,
  constraints, open questions). Use whenever the user describes a feature,
  product change, or something they want built, even if they never say intent
  or plan. Skip bugfixes, refactors, and implementation. If the repo has open
  OpenSpec changes, use OpenSpec instead.
license: MIT
metadata:
  author: acourtiol
  version: "1.1"
---

# sdlc-plan

Write `intent/<slug>/intent.md` from the user's idea. Stop so they can accept. Leave spec, plan, and code for later skills.

The originator should see their own words in the file. A proto-spec they can correct is faster than a ticket they did not write.

## Before you start

If `openspec/` has open (non-archived) changes, stop and use OpenSpec (`openspec` binary, never `npx openspec`). Mixing both trees in one change splits the audit trail.

Do not commit unless the user asks. Chat accept is the gate; git is optional.

Do not create `CLAUDE.md` or auto-memory. Repeated mistakes belong in project `AGENTS.md` or the repo OKF bundle.

Beads are tickets. These files are the change record. A bead id in the intent body is fine.

## Steps

1. Confirm there is no open OpenSpec change.
2. Interview until the idea is concrete: what cannot be done today, who is affected, what better looks like, constraints, out of scope. Ask one question at a time when a missing answer would change the file.
3. Derive a kebab-case slug. If `intent/<slug>/` already exists, pick another slug or hand off to `sdlc-continue`.
4. Copy `assets/intent.md` into `intent/<slug>/intent.md`. Fill every section. Frontmatter: `status: draft`, `slug: <slug>`.
5. Show the path and a short summary. Ask the user to accept (that starts Design) or to correct it.
6. If they accept in this session, set `status: accepted`. Do not start `sdlc-design` unless they ask to keep going.

Next: `sdlc-design`.
