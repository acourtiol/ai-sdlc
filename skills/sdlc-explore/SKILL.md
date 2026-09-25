---
name: sdlc-explore
description: >-
  Thinking partner for a half-formed idea: explores the problem,
  compares approaches, and works out whether the work needs an intent at all.
  Use when the user says brainstorm, explore, think this through, or I am not
  sure what I want, or when they are circling an idea before sdlc-plan. May
  checkpoint consequential findings for an intent-worthy idea in context.md.
license: MIT
metadata:
  author: acourtiol
  version: "1.2"
---

# sdlc-explore

Think with the user. Read the codebase, draw the problem, weigh the approaches. Preserve consequential findings if the discussion outgrows the session.

The Plan stage opens with a brainstorm, not a template. An idea interviewed before it is understood yields a tidy `intent.md` for the wrong problem.

## Before you start

Normally this skill writes no files or code. Read-only commands and searches need no permission. The narrow `context.md` exception below applies only to an intent-worthy idea. If the user asks directly for a bounded fix, route to `sdlc-fix`; if they ask to build a new capability, route to `sdlc-plan`. Do not implement within exploration.

Answering a design question is not acceptance of an intent or consent to build. Silence is not agreement.

## Triage first

Name the path before your first question, so the user can correct you.

| Path | Looks like | Where it ends |
| --- | --- | --- |
| Spike | can we, is it possible, quick and dirty is fine | Agree the probe in two sentences, find out, report a recommendation. Anything you build is throwaway. No intent. |
| Bounded fix | a bug or behavior-preserving refactor of a flow already in this repo | Explain the bounded path. If the user requests the fix, hand off to `sdlc-fix`; exploration alone is not consent to change code. No intent. |
| Intent-worthy | a new capability or surface, something that changes what the product does | Explore it here, then `sdlc-plan`. |

Bounded measures the repo, not your familiarity or the number of files. If the flow you would change is not already here to read, it is not bounded.

The ratchet runs one way. Complexity you uncover later upgrades the path, so stop and say so. Nothing downgrades mid-conversation. When two paths are plausible, take the heavier one.

## The stance

No fixed steps. Follow the conversation.

Use subagents to parallelize work and preserve context when it matters. Independent reads and searches go out together and come back as findings, so this conversation stays on the decision. A narrow lookup stays here. If no subagent is available, research here.

- One question at a time, and say which decision it unlocks.
- Read the code before asking anything the code can answer. If you list folders, `intent/*/` is work in flight (skip `intent/archive/`); what the product already does is the code and `AGENTS.md`, not those folders.
- Settle the blocking decision before the ones that depend on it. Outcome and scope come before API and data model.
- Recommend a path with its tradeoff when the evidence supports one. Do not invent constraints only the user can know.
- Decompose before refining. A request that is really four subsystems gets split first; explore the first piece.
- Draw it when a diagram beats a paragraph. Plain ASCII only (`+ - |`, `--> ^ v`), because Unicode box glyphs drift across terminal fonts.
- Question assumptions, including your own. Separate what you verified, what you are assuming, and what you could not check.
- Cut what the idea does not need before presenting it.

Stop when the user has enough clarity. Not every branch needs exhausting, and some conversations are worth having without producing anything.

## Keep the thread across compaction

For an intent-worthy idea, write consequential findings as they emerge, before a long investigation or handoff can bury them. If `intent/<slug>/intent.md` exists, read it first; route settled corrections through its owning gate instead of editing an approved artifact during exploration. For findings not yet ready for the intent, use `intent/<slug>/context.md`. If there is no intent yet, choose a provisional slug and create that file only when there is information worth preserving. It has no status or approval meaning. Do not create it for a spike, a bounded fix, or a conversation with no consequential findings.

Keep `context.md` short and current: verified findings with source paths or commands, decisions and their reasons, assumptions labeled as such, unresolved questions, and the next decision. Record only what is absent from other files. Do not paste chat history or repeat an existing artifact. Commit each checkpoint, staging only this concern; do not push unless asked. On resuming, read it and check its claims against the repo before relying on them. Move settled content into `intent.md` through `sdlc-plan`, then remove entries that are represented there.

## Ending

Do not turn exploration into an approved intent on your own. When the shape holds, offer this and let the user decide what happens to it:

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

Next: `sdlc-plan`, for an intent-worthy idea. A spike ends at its recommendation; an authorized bounded fix routes to `sdlc-fix`.
