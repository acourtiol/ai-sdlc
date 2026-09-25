---
name: sdlc-plan
description: >-
  Captures a product idea as intent/slug/intent.md (problem, evidence, outcome,
  constraints, open questions). Use whenever the user describes a feature,
  product change, or something they want built, even if they never say intent
  or plan. Skip bugfixes, refactors, and implementation. Commit intent.md in
  the same step that writes it; do not wait to be asked to commit. Do not push
  unless asked. On accept in this session, read sdlc-design and execute it.
license: MIT
metadata:
  author: acourtiol
  version: "1.5"
---

# sdlc-plan

Write `intent/<slug>/intent.md` from the user's idea. Wait for them to accept. On accept, read `sdlc-design` and execute it.

The originator should see their own words in the file. A proto-spec they can correct is faster than a ticket they did not write.

## Before you start

Triage before you write. A feasibility question is a spike: answer it, do not open an intent. One flag, one file, a bug, or a refactor of a flow already in this repo is a bounded change: make it, do not open an intent. An intent is for work that changes what the product does. When two readings are plausible, take the heavier one. If the idea is still shapeless, `sdlc-explore` first. Ask what shows the problem is real, or write `not checked`, even if explore was skipped.

Use subagents to parallelize work and preserve context when it matters. The interview stays in this session. Independent codebase reads that would bury it go out and come back as findings. If no subagent is available, read here.

Using this skill is the user asking you to commit. Do not wait for a later message that says commit. A host rule that says commit only when asked is already satisfied. Stage only this concern. The message is an imperative subject, a blank line, and one sentence on why, passed with a heredoc. Do not push unless the user asks. Chat accept is still the gate into design. A step that writes or edits and leaves those paths dirty is not done.

Do not create `CLAUDE.md` or auto-memory. Repeated mistakes belong in project `AGENTS.md` or the repo OKF bundle.

Beads are tickets. These files are the change record. A bead id in the intent body is fine.

## Steps

1. Before the interview, read this repo's `AGENTS.md` and list `intent/*/` (skip `intent/archive/`); use those as constraints, do not copy them into `intent.md`. Then interview until the idea is concrete: what cannot be done today, what shows the problem is real (or `not checked`), who is affected, what better looks like, constraints, out of scope. Ask one question at a time when a missing answer would change the file.
2. Derive a kebab-case slug. If `intent/<slug>/` already exists, pick another slug or hand off to `sdlc-continue`. If `intent/archive/*-<slug>/` exists, that name shipped before: say so and pick a slug that does not collide with the history. `intent/archive/` is the archive, never a slug.
3. Copy `assets/intent.md` into `intent/<slug>/intent.md`. Fill every section, including Evidence. Frontmatter: `status: draft`, `slug: <slug>`. Do not migrate existing consumer intents that lack Evidence. Commit that file before the next step.
4. Show the path and a short summary. Ask the user to accept (that starts Design) or to correct it. If they correct the file, commit that edit before you continue.
5. If they accept in this session, set `status: accepted` and commit that edit. Then immediately read `sdlc-design` and execute it. If they accept but tell you to stop there, stop. The accept commit still happens.

Next: `sdlc-design`.
