---
name: sdlc-archive
description: >-
  Moves a finished change from intent/slug/ to
  intent/archive/YYYY-MM-DD-slug/ after checking statuses, plan boxes, and
  report.md. Use when the user says archive, close out, wrap up, or this one is
  finished. Do not skip verify. Do not archive without intent/slug/report.md,
  verdict: pass with no CRITICAL, and valid isolation frontmatter. Commit the
  move in the same step. Do not wait to be asked to commit. Do not push unless
  asked. Fail or CRITICAL → apply must fix then isolated re-verify first; do
  not archive, do not ask to skip.
license: MIT
metadata:
  author: acourtiol
  version: "1.4"
---

# sdlc-archive

Move `intent/<slug>/` to `intent/archive/YYYY-MM-DD-<slug>/`. Nothing is deleted and nothing is rewritten: the folder keeps the intent, the spec, the plan, and the report exactly as they were.

An archive is decision history. Six months on, the question is why this was built this way, and the answer is the folder.

This is not in the Anthropic playbook, where the audit trail is git plus the PR and its review findings. The dated folder carries the same record when there is no PR.

## Before you start

Using this skill is the user asking you to commit the move. Do not wait for a later message that says commit. A host rule that says commit only when asked is already satisfied. Plain `mv`, not `git mv`: git recognizes the rename from content. The message is an imperative subject, a blank line, and one sentence on why, passed with a heredoc. Do not push unless the user asks. The move is not done while the old path is still present.

`intent/archive/` is the archive, not a slug. Skip it when you list changes.

## Steps

1. Resolve the slug. Say which one you picked and how to name a different one. If several are candidates, ask.
2. Read the frontmatter on the gated files that exist (`intent.md`, `spec.md`, `plan.md`). Each should be `status: done`.
3. Count `- [ ]` against `- [x]` under Order of work in `plan.md`.
4. Check `report.md` exists. Read its frontmatter `verdict` and `isolation`, its Findings, and its Not checked section.
5. **Hard stop without a passing verify.** If `report.md` is missing: stop; next is isolated `sdlc-verify`. If `verdict` is not `pass` or Findings contains a `- CRITICAL` finding entry: stop; next is `sdlc-apply` (fix) then isolated `sdlc-verify`. If `isolation` is missing or is not `subagent`, `subagent-different-model`, or `subagent-same-model`: stop; next is isolated `sdlc-verify`. If Not checked contains `verified in implementing session`: treat verify as invalid, stop; next is isolated `sdlc-verify`. If `plan.md` has zero boxes or any unticked box, stop; finish the plan and re-verify. Do not ask to skip these checks. If statuses are not `done`, say which are short and ask before archiving; this is the only gap the user may confirm.
6. Build the target name. Today's date as `YYYY-MM-DD-<slug>`, unless the slug already starts with a `YYYY-MM-DD-` prefix, in which case use it as is. Never stack a second date.
7. If `intent/archive/<target>` already exists, stop. Do not overwrite or merge. Tell the user, and let them rename the existing archive or pick another date.
8. Move it:

   ```bash
   mkdir -p intent/archive
   mv "intent/<slug>" "intent/archive/<target>"
   ```

9. Confirm the destination path and the tasks tally. Then commit the move.
