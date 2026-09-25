---
name: sdlc-fix
description: >-
  Fix a bounded bug or make a behavior-preserving refactor in an existing,
  readable flow. Reproduce and verify the change, then commit it without an
  intent folder. Use for direct fix or refactor requests; new capabilities and
  work spanning multiple subsystems go through sdlc-plan. Do not push unless
  asked.
license: MIT
metadata:
  author: acourtiol
  version: "1.0"
---

# sdlc-fix

Repair a bounded existing flow without opening `intent/<slug>/`. The request to fix or refactor authorizes the finished commit; stage only this concern and do not push unless asked.

## Scope

Read the repo's `AGENTS.md` and the affected code before changing it. This path fits a bug with a concrete existing behavior or a refactor that preserves behavior in a flow already present to inspect. A file count alone does not establish scope. If investigation reveals a new capability, an architectural decision, or work across multiple subsystems, stop expanding the patch and route the larger change to `sdlc-plan`. State what was learned; do not disguise expanded scope as a fix.

## Work

1. For a bug, establish the reported failure and its cause. Run the original reproduction before editing when practical. A regression test should fail for the reported reason when a durable automated check is useful; otherwise record the concrete reproduction and why an automated test does not fit. Do not claim reproduction if it could not be exercised.
2. Make the smallest root-cause change. For a refactor, identify the behavior that must remain true and check it before and after. Preserve validation, error handling, security, and accessibility relevant to the flow.
3. Run the original reproduction again and the relevant tests or checks. Read their output. Report what passed, what failed, and what could not be checked. A green suite alone does not establish that the reported failure was fixed.
4. Commit the verified change, staging only this concern. Use an imperative subject, a blank line, and one sentence explaining why. Leave no fix files dirty. Do not create an intent, spec, plan, report, or handoff folder for this bounded work. Do not push unless the user asks.
