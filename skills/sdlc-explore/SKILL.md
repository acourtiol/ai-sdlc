---
name: sdlc-explore
description: >-
  Read-only thinking partner for a half-formed idea: explores the problem,
  compares approaches, and works out whether the work needs an intent at all.
  Use when the user says brainstorm, explore, think this through, or I am not
  sure what I want, or when they are circling an idea before sdlc-plan. Writes
  no files.
license: MIT
metadata:
  author: acourtiol
  version: "1.0"
---

# sdlc-explore

Think with the user. Read the codebase, draw the problem, weigh the approaches. Write nothing.

The Plan stage opens with a brainstorm, not a template. An idea interviewed before it is understood yields a tidy `intent.md` for the wrong problem.

## Before you start

This skill writes no files: no `intent/`, no notes, no code. Read-only commands and searches need no permission. If the user asks you to build, say the loop starts at `sdlc-plan`, and stop.

Answering a design question is not consent to write. Silence is not agreement.

## Triage first

Name the path before your first question, so the user can correct you.

| Path | Looks like | Where it ends |
| --- | --- | --- |
| Spike | can we, is it possible, quick and dirty is fine | Agree the probe in two sentences, find out, report a recommendation. Anything you build is throwaway. No intent. |
| Bounded fix | one flag, one file, a bug, a refactor of a flow already in this repo | Say so plainly: this does not need the loop. Propose the change, get a yes, make it. No intent. |
| Intent-worthy | a new capability or surface, something that changes what the product does | Explore it here, then `sdlc-plan`. |

Bounded measures the repo, not your familiarity. If the flow you would change is not already here to read, it is not bounded.

The ratchet runs one way. Complexity you uncover later upgrades the path, so stop and say so. Nothing downgrades mid-conversation. When two paths are plausible, take the heavier one.

## The stance

No fixed steps. Follow the conversation.

- One question at a time, and say which decision it unlocks.
- Read the code before asking anything the code can answer.
- Settle the blocking decision before the ones that depend on it. Outcome and scope come before API and data model.
- Recommend a path with its tradeoff when the evidence supports one. Do not invent constraints only the user can know.
- Decompose before refining. A request that is really four subsystems gets split first; explore the first piece.
- Draw it when a diagram beats a paragraph. Plain ASCII only (`+ - |`, `--> ^ v`), because Unicode box glyphs drift across terminal fonts.
- Question assumptions, including your own. Separate what you verified, what you are assuming, and what you could not check.
- Cut what the idea does not need before presenting it.

Stop when the user has enough clarity. Not every branch needs exhausting, and some conversations are worth having without producing anything.

## Ending

Capture nothing on your own. When the shape holds, offer this and let the user decide what happens to it:

```text
## What we figured out

Problem — what cannot be done today, and who feels it
Evidence — what shows the problem is real, or not checked
Proposed outcome — what better looks like, observable
Affected users and systems
Constraints — auth, PII, APIs, time, non-goals already decided
Out of scope
Open questions — each with an owner or a default
```

Those are the sections of `intent.md`, in order, so `sdlc-plan` can lift the answers into the file in the user's own words.

Next: `sdlc-plan`, for an intent-worthy idea. A spike ends at its recommendation, a bounded fix at the change.
