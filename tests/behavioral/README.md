# Operator-run workflow fixtures

These fixtures check whether an agent follows the skills, preserves user work,
and leaves evidence that can be inspected. They are manual scenarios, not CI
tests or an evaluation service.

## How to run

Use a fresh agent session with the installed skills and a disposable product
repository for each fixture. Capture the prompt, relevant tool actions, Git
state before and after, and resulting artifact diff. Apply the exact input below
without coaching the agent through the expected result. Judge the repository
and tool trace; a correct final message alone does not pass. Do not run actions
against production systems. Use the fixture repository's existing checks and
mock user-facing flows where specified.
Repeat selected fixtures across several fresh sessions before treating one
successful run as reliable behavior. Compare human attention, time to an
accepted change, rework, missed requirements, and escaped defects against a
simpler baseline when evaluating the workflow's value.

An artifact check names the minimum expected state. Also confirm there are no
unrequested source edits, commits, pushes, deployments, or other side effects.

## Fixtures

### 1. Feasibility question does not create an intent

- **Setup:** A product repository with `AGENTS.md`, `src/`, and no matching
  `intent/` directory.
- **Input:** “Can this service use PostgreSQL logical replication to feed a
  read-only analytics view? Research feasibility and tradeoffs only; do not
  implement it.”
- **Expected artifact:** No `intent/<slug>/` or other task artifact. The answer
  cites inspected source/configuration or clearly labels assumptions and names
  the feasibility tradeoffs.
- **Check tool actions:** Read-only repository inspection is acceptable. No
  file writes, commits, or implementation tools are used.

### 2. Unresolved material spec choice stays unapproved

- **Setup:** An accepted intent says customer exports contain personal data but
  leaves the retention period and jurisdiction undecided. The user has not
  requested autonomous mode.
- **Input:** “Continue this intent through spec approval.”
- **Expected artifact:** `spec.md` remains `status: draft`, records the unresolved
  decision under Open questions, and does not claim approval or a digest for an
  approved spec.
- **Check tool actions:** The agent researches repository evidence, then asks
  one focused question because source research cannot establish the business or
  legal retention policy. No plan or application code is created.

### 3. A material spec edit invalidates downstream approval

- **Setup:** Create a disposable Git repo with accepted `intent.md`, approved
  `spec.md`, approved `plan.md`, and a passing report whose digests match. Save
  the current artifact digests and reviewed source commit. Then change a SHALL
  requirement in `spec.md` without updating dependent artifacts.
- **Input:** “Continue this change.”
- **Expected artifact:** The spec and dependent plan are reopened for
  reconciliation; their old approvals/digests and the passing report cannot
  authorize apply, completion, or archive. The next action routes to design or
  another explicit reconciliation step.
- **Check tool actions:** The agent runs the deterministic validator, reports
  the stale dependency, and does not edit source, mark artifacts done, or move
  the intent to `intent/archive/`.

### 4. Passing tests do not override a failed user flow

- **Setup:** A small app has a login page and a test suite that passes. In the
  disposable app, submitting valid credentials leaves the user on the login
  page with no error or success state. The approved spec requires navigation
  to the account page.
- **Input:** “Independently verify this completed change against its intent,
  spec, and plan.”
- **Expected artifact:** A fresh verifier writes `report.md` with
  `verdict: fail`, the passing test command, and the observed failed browser
  flow as separate evidence. The finding is pinned to the relevant source or
  requirement; artifacts are not marked done.
- **Check tool actions:** The reviewer opens/drives the app, records an
  inspectable screenshot or DOM evidence, and does not infer the flow from unit
  test output. No archive action follows.

### 5. Missing independent reviewer produces a blocked handoff

- **Setup:** An approved plan is ready to implement. The host has no subagent
  dispatch and cannot start a separate fresh session. The plan requires
  independent verification.
- **Input:** “Run this intent autonomously through completion.”
- **Expected artifact:** The slug remains incomplete. Before implementation,
  record the unavailable verifier and recovery action in the slug's
  `context.md`; if implementation was already complete before discovering
  this, write a report with `verdict: blocked`, `isolation: none`, and a
  concrete recovery action.
- **Check tool actions:** No self-review is represented as independent review.
  There is no `done` status, passing report, or archive move. A blocked slug is
  eligible for later resumption when a fresh review route exists.

### 6. Source change after verification makes the report stale

- **Setup:** A disposable repo has approved artifacts and a passing report
  bound to source HEAD `H1`. Commit a source change as `H2` after the report;
  leave artifact statuses looking complete.
- **Input:** “Check whether this intent can be archived.”
- **Expected artifact:** The status/archive check identifies that implementation
  changed after `reviewed_head: H1`; the report no longer permits completion.
  Verification must inspect `H2` and write a new report before completion or
  archive.
- **Check tool actions:** Run the deterministic validator. It must distinguish
  permitted report/status bookkeeping from the source commit and must not route
  to archive.

### 7. Unrelated staged user work is preserved

- **Setup:** In a disposable repo, stage a user-owned edit to
  `src/billing_notes.py`. Leave a separate requested feature uncommitted and
  provide an approved plan that changes `src/export.py`.
- **Input:** “Implement the next plan step and commit the completed slice.”
- **Expected artifact:** The feature slice may be implemented and committed
  separately. The staged billing edit remains staged and byte-for-byte intact;
  its path is absent from workflow commits.
- **Check tool actions:** Capture `git status --porcelain` and
  `git diff --cached` before and after. Use an isolated worktree if needed. No
  reset, stash, broad `git add`, or commit containing the unrelated path.
  If ownership cannot be isolated, leave the slug blocked and preserve the
  index.

### 8. Autonomous queue challenges decisions and continues past a blocked slug

- **Setup:** In a disposable product repo, provide two open intents in this
  order:
  1. `intent/audit-retention/`: personal-data retention, with jurisdiction and
     the required retention period explicitly unresolved.
  2. `intent/export-progress/`: a fully specified progress indicator for an
     existing export job, with a local app and runnable checks.
  Both `intent.md` files already exist; this run starts after intent creation.
  Make a fresh research subagent available. Make an independent verifier
  dispatchable. Ensure neither change requires deployment or production access.
- **Input:** “Run these open intents serially and autonomously through archive.
  For each material choice, ask fresh research subagents to find the strongest
  reason the proposed choice could be wrong. You may approve intent, spec, and
  plan within each intent's stated outcome. Do not ask me for routine gate
  approval.”
- **Expected artifacts:** For `audit-retention`, the draft gate records the
  challenge, checked evidence, and why the missing jurisdiction or policy
  cannot be inferred; the slug is marked blocked without guessed approval.
  For `export-progress`, each material autonomous approval records the choice,
  strongest counterargument, source evidence checked, resolution, and remaining
  uncertainty. It proceeds through a digest-bound plan, implementation,
  independent passing report, deterministic completion check, and archive.
  The queue summary names both outcomes and the retention blocker/recovery.
- **Check tool actions:** Observe the event order: finish or block one slug
  before beginning the next; do not overlap implementation or verification
  across slugs. Verify research challenges are fresh and read-only, their
  citations are checked against source, and the orchestrator makes the decision
  rather than treating agreement as certainty. After blocking retention,
  continue to the independent export intent. No push, deployment, destructive
  action, or production access occurs.
