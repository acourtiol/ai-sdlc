---
name: sdlc-plan
description: >-
  Captures a product idea as intent/slug/intent.md (problem, evidence, outcome,
  constraints, open questions). Use whenever the user describes a feature,
  product change, or something they want built, even if they never say intent
  or plan. Skip bugfixes, refactors, and implementation.
license: MIT
metadata:
  author: acourtiol
  version: "1.3"
---

# sdlc-plan

Write `intent/<slug>/intent.md` from the user's idea. Stop so they can accept. Leave spec, plan, and code for later skills.

The originator should see their own words in the file. A proto-spec they can correct is faster than a ticket they did not write.

## Before you start

Triage before you write. A feasibility question is a spike: answer it, do not open an intent. One flag, one file, a bug, or a refactor of a flow already in this repo is a bounded change: make it, do not open an intent. An intent is for work that changes what the product does. When two readings are plausible, take the heavier one. If the idea is still shapeless, `sdlc-explore` first. Ask what shows the problem is real, or write `not checked`, even if explore was skipped.

Do not commit unless the user asks. Chat accept is the gate; git is optional.

Do not create `CLAUDE.md` or auto-memory. Repeated mistakes belong in project `AGENTS.md` or the repo OKF bundle.

Beads are tickets. These files are the change record. A bead id in the intent body is fine.

## Steps

1. Interview until the idea is concrete: what cannot be done today, what shows the problem is real (or `not checked`), who is affected, what better looks like, constraints, out of scope. Ask one question at a time when a missing answer would change the file.
2. Derive a kebab-case slug. If `intent/<slug>/` already exists, pick another slug or hand off to `sdlc-continue`. If `intent/archive/*-<slug>/` exists, that name shipped before: say so and pick a slug that does not collide with the history. `intent/archive/` is the archive, never a slug.
3. Copy `assets/intent.md` into `intent/<slug>/intent.md`. Fill every section, including Evidence. Frontmatter: `status: draft`, `slug: <slug>`. Do not migrate existing consumer intents that lack Evidence.
4. Show the path and a short summary. Ask the user to accept (that starts Design) or to correct it.
5. If they accept in this session, set `status: accepted`. Do not start `sdlc-design` unless they ask to keep going.

Next: `sdlc-design`.
