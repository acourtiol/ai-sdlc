---
name: sdlc-archive
description: >-
  Archive an implemented intent after deterministic approval, completion, and
  verification checks. Use when the user closes a finished change.
license: MIT
metadata:
  author: acourtiol
  version: "2.1"
---

# sdlc-archive

Move `intent/<slug>/` to `intent/archive/YYYY-MM-DD-<slug>/`. Nothing is deleted and nothing is rewritten: the folder keeps the intent, the spec, the plan, and the report exactly as they were.

An archive is decision history. Six months on, the question is why this was built this way, and the answer is the folder.

## Before you start

Invoking this workflow normally authorizes the archive commit, subject to explicit user restrictions and host policy. Before moving anything, record repository, branch, HEAD, staged paths, and working-tree/untracked paths. Preserve unrelated work; if the index contains someone else's staged changes or ownership overlaps, use a clean isolated worktree when feasible or stop the commit. Never reset, stash, or absorb those changes. Plain `mv`, not `git mv`: Git recognizes the rename from content. Stage only the move. Follow Conventional Commits 1.0.0: `chore(scope): imperative summary` (scope optional), a blank line, and one sentence on why. Do not push unless asked.

`intent/archive/` is the archive, not a slug. Skip it when you list changes.

## Steps

1. Resolve the slug. In an ordinary run, say which one you picked; if several are candidates, ask. In an explicitly authorized autonomous queue, use its selected slug without another approval request.
2. Run `python3 <this-skill-dir>/scripts/validator.py archive-check <slug>` from the product repo root. This local copy uses the same contract as `sdlc-continue`. It checks grammar, all done statuses, plan boxes, approval digests and upstream bindings, substantive report evidence, valid independent isolation, reviewed HEAD freshness, and dirty/untracked paths. Read its reason on failure and follow the owning skill; never waive a failed check. A blocked verification needs recovery, while a failed verification needs repair and a fresh review.
3. Read the report and compare its claimed observations with the cited evidence. Mechanical validity cannot prove that the verifier actually exercised a flow. If a cited required observation is absent or contradicted, withhold archive and request fresh independent verification.
4. Build the target name. Today's date as `YYYY-MM-DD-<slug>`, unless the slug already starts with a `YYYY-MM-DD-` prefix, in which case use it as is. Never stack a second date.
5. If `intent/archive/<target>` already exists, stop. Do not overwrite or merge. Tell the user, and let them rename the existing archive or pick another date.
6. Move it:

   ```bash
   mkdir -p intent/archive
   mv "intent/<slug>" "intent/archive/<target>"
   ```

7. Confirm the destination path and tasks tally. Then commit the move. Archive closes the implementation record; it does not assert deployment or production success.
