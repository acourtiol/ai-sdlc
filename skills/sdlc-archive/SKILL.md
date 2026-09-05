---
name: sdlc-archive
description: >-
  Moves a finished change from intent/slug/ to
  intent/archive/YYYY-MM-DD-slug/ after checking statuses, plan boxes, and
  report.md. Use when the user says archive, close out, wrap up, or this one is
  finished. Do not archive work that has not been verified without saying so.
license: MIT
metadata:
  author: acourtiol
  version: "1.0"
---

# sdlc-archive

Move `intent/<slug>/` to `intent/archive/YYYY-MM-DD-<slug>/`. Nothing is deleted and nothing is rewritten: the folder keeps the intent, the spec, the plan, and the report exactly as they were.

An archive is decision history. Six months on, the question is why this was built this way, and the answer is the folder.

This is not in the Anthropic playbook, where the audit trail is git plus the PR and its review findings. The dated folder carries the same record when there is no PR.

## Before you start

Do not commit unless the user asks. Plain `mv`, not `git mv`: git recognizes the rename from content when the user diffs or commits, so history survives without touching their index.

`intent/archive/` is the archive, not a slug. Skip it when you list changes.

## Steps

1. Resolve the slug. Say which one you picked and how to name a different one. If several are candidates, ask.
2. Read the frontmatter on the gated files that exist (`intent.md`, `spec.md`, `plan.md`). Each should be `status: done`.
3. Count `- [ ]` against `- [x]` under Order of work in `plan.md`.
4. Check `report.md` exists. Read its frontmatter `verdict`, its Findings, and its Not checked section.
5. Report anything short: statuses that are not `done`, unticked boxes as `N/M`, a missing `report.md`, `verdict: fail`, or a CRITICAL finding. Each one is a warning that needs the user's confirmation, not a block. Say what is short, ask, and archive if they confirm. A missing `report.md` is worth offering `sdlc-verify` first.
6. Build the target name. Today's date as `YYYY-MM-DD-<slug>`, unless the slug already starts with a `YYYY-MM-DD-` prefix, in which case use it as is. Never stack a second date.
7. If `intent/archive/<target>` already exists, stop. Do not overwrite or merge. Tell the user, and let them rename the existing archive or pick another date.
8. Move it:

   ```bash
   mkdir -p intent/archive
   mv "intent/<slug>" "intent/archive/<target>"
   ```

9. Confirm the destination path, the tasks tally, and any warning it was archived in spite of.
