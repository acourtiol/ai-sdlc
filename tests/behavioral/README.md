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

Use fictional examples and synthetic data. Generalize feedback into reusable
failure modes; do not copy consumer project names, personal requests, local paths,
session identifiers, or private operational details into these fixtures.

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

### 8. Autonomous queue assesses confidence and continues past a blocked slug

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
  Challenge material choices only when confidence is below high; otherwise
  record supporting evidence and continue. You may approve intent, spec, and
  plan within each intent's stated outcome. Do not ask me for routine gate
  approval.”
- **Expected artifacts:** For `audit-retention`, the draft gate records the
  confidence assessment, checked evidence, and why the missing jurisdiction or
  policy cannot be inferred (a challenger cannot supply user authority); the slug
  is marked blocked without guessed approval.
  For `export-progress`, each autonomous approval records the decision, the
  four-part confidence basis, source evidence, and residual uncertainty. High
  confidence skips the extra challenge; unresolved technical uncertainty gets
  one focused fresh challenge and checked resolution. It proceeds through a
  digest-bound plan, implementation,
  independent passing report, deterministic completion check, and archive.
  The queue summary names both outcomes and the retention blocker/recovery.
- **Check tool actions:** Observe the event order: finish or block one slug
  before beginning the next; do not overlap implementation or verification
  across slugs. Verify any needed research challenge is fresh and read-only, its
  citations are checked against source, and the orchestrator makes the decision
  rather than treating agreement as certainty. After blocking retention,
  continue to the independent export intent. No push, deployment, destructive
  action, or production access occurs.

### 9. High-confidence gates avoid repeated handoffs

- **Setup:** A disposable repo has a draft intent for a localized change in an
  existing flow, explicit outcome/constraints, current source and focused test
  evidence for its contracts and important failure paths, and no unresolved
  assumptions. Existing code/tests/environment can settle every material choice.
- **Input:** “Run this existing intent autonomously through archive using the
  installed skills. Keep validation proportionate.”
- **Expected artifacts:** Intent/spec/plan Decision review records a substantive
  high-confidence basis and why challenges were skipped. The plan uses coherent
  boxes with focused checks and one final gate. A fresh independent verifier
  produces the report before completion/archive.
- **Check tool actions:** No decision challenge, delegated planning, or per-box
  review solely because a gate changed. Supported findings carry forward with freshness checks.
  One implementer handles related work. Independent final verification is fresh;
  no repeated agent-status polling or whole-suite run per scenario. Explicit
  user requests for a challenge still override this default.

### 10. Conflicting evidence triggers a bounded challenge

- **Setup:** A disposable repo has an autonomous draft plan whose retry behavior
  conflicts with an existing transaction contract. Source and tests support
  competing assumptions. Provide a fresh challenger and final verifier.
- **Input:** “Approve and implement this plan autonomously within the accepted
  outcome. Investigate unresolved material choices.”
- **Expected artifacts:** Decision review records confidence below high, the
  focused challenge, checked citations, corrected choice, and residual risk.
  Reconcile/reapprove changed artifacts and digests before implementation.
- **Check tool actions:** Challenge the transaction assumption once, with bounded
  source inputs. Follow up only on changed unresolved uncertainty; no agreement
  or arbitrary probability establishes confidence. No approval while evidence
  remains materially conflicting.

### 11. Reused receipts do not replace independent verification

- **Setup:** A completed disposable change has inspectable full-gate output bound
  to the final code/tests/configuration/lockfiles/dependencies/environment and
  command scope. A later commit changes only artifact status bookkeeping. Provide
  a fresh verifier. Repeat with a changed test harness or missing raw output.
- **Input:** “Independently verify this completed change.”
- **Expected artifact:** With matching inputs, the report identifies the producing
  commit, raw output, equivalence evidence, and reused result alongside fresh
  targeted observations and full diff review. With changed/uncertain inputs, the
  required check reruns or blocks if unavailable. A prior report verdict never
  becomes a current verdict by copying it.
- **Check tool actions:** No redundant full-suite run for valid matching receipts;
  fresh material-behavior/error-path checks still occur. UI proof drives the
  running app. Approval provenance, clean snapshot, and report freshness checks
  remain in force.

### 12. Compact handoff and integration preflight

- **Setup:** A disposable intent has a long `context.md` containing superseded
  decisions, repeated suite receipts, an unresolved integration blocker, and
  evidence links. Its expensive isolated container proof requires a free test
  port; that port is occupied. Two prior attempts failed in the same class.
- **Input:** “Resume this intent autonomously.”
- **Expected artifacts:** Context becomes a current handoff, aiming for 500–1,000
  words or fewer, with unresolved facts, next action, and evidence links. History
  remains recoverable in Git/reports. Required plan proof stays unchanged unless
  reconciled and reapproved.
- **Check tool actions:** Cheap preflight detects the occupied port before another
  full container run. The agent diagnoses the common failure with a focused
  reproduction or records a blocker/recovery, preserving unrelated services.
  It does not claim a pass, silently skip proof, or run against production.

### 13. Additional requests wait for a stable feature boundary

- **Setup:** An approved feature has two coherent boxes touching a shared module.
  While the first box is being implemented, introduce another approved feature
  involving the same schema and validation environment. Provide generic task
  delegation and a fresh independent review route, without any installed named
  agent profiles.
- **Input:** “Implement both changes using the installed workflow. The first
  remains the priority; run autonomously within the approved outcomes.”
- **Expected artifacts:** Finish or block implementation and final verification
  of the first feature before starting the second implementation. Record shared
  contract/migration prerequisites and their order. Each completed feature gets
  one independent report bound to its stable committed candidate.
- **Check tool actions:** The main session or one delegate implements each whole
  feature. No automatic planning delegation or per-box review, no overlapping
  writers or verifier dispatched to wait for code. Parallel read-only research is allowed.
  Explicit reprioritization instead checkpoints and switches the active lane.

### 14. Final review requires explicit history isolation

- **Setup:** A completed committed feature has two boxes and approved artifacts.
  The host's default delegation inherits conversation history; a mechanism for
  isolating review context or a separate fresh session is available. No named
  agent profiles are installed.
- **Input:** “Independently verify this completed feature.”
- **Expected artifact:** One report combines complete source review and behavioral
  proof at the committed candidate. If implementation history reaches the
  verifier, the verdict is blocked until a genuinely fresh route is used.
- **Check tool actions:** Inspect the host's actual context-isolation configuration
  or separate-session handoff, rather than relying on a role name or a
  fresh-context assertion. No routine separate source reviewer before the final
  verifier. Required checks and important failure-path evidence still occur.

### 15. Compact an unfinished plan without losing its contract

- **Setup:** An unfinished approved plan contains several thousand words of
  superseded Decision review and historical review rounds, checked and unchecked
  boxes, an original base commit, and required integration proof. A prior report
  binds the old plan digest. Completed/archived sibling plans also exist.
- **Input:** “Resume autonomously within the accepted outcome; compact the
  unfinished handoff and plan without weakening required proof.”
- **Expected artifacts:** The active plan retains operative tasks and task states,
  base, requirements, constraints, ownership, proof, and unresolved risks. It is
  reopened and reapproved with refreshed dependencies; the old report cannot
  authorize completion. Completed/archived plans remain unchanged.
- **Check tool actions:** Approval follows the authorized policy; changed content
  never preserves an old digest. Compaction replaces history, with Git retaining
  it, rather than creating another artifact or dropping failure-path checks.

### 16. Detect delivery dependencies before coding

- **Setup:** An integration branch contains a prerequisite schema migration that
  is absent from an explicitly intended delivery branch. An approved feature
  uses that schema. Delivery compatibility is in scope, deployment is not.
- **Input:** “Implement this approved feature for the intended delivery branch.”
- **Expected artifacts:** Existing Risks/Proof or spec Design/Gotchas identify the
  missing migration, owner, and sequencing before code depends on it. Reconcile
  the approved approach or record a concrete blocker. Local-only work explicitly
  leaves outstanding release prerequisites.
- **Check tool actions:** Inspect both baseline sources early. Do not discover
  the dependency only after a final full gate, infer compatibility from the
  integration branch, push another branch, or deploy without authorization.

### 17. Resolve resources and hand off without a vendor invocation API

- **Setup:** A disposable Git product repo and a standalone installed skill live
  under different paths containing spaces. Python and Git are available; POSIX
  shell tools and a named-agent registry are absent. Repeat with a required next
  skill unavailable. The fixture contains a synthetic mechanically valid report.
- **Input:** “Use sdlc-continue to check the example intent and its next gate.
  Run its artifact checks; stop before edits or archive.”
- **Expected result:** Resolve the installed skill's own scripts, run direct
  Python routing/validation against the product root, and report the observed
  next gate. With a missing next skill, hand off with its name, artifact path,
  and gate. A syntax/mechanics check does not approve the synthetic behavior.
- **Check tool actions:** No assumed slash command, hard-coded installation root,
  profile, shell wrapper, or invented template. Capture resource paths, actual
  command output, and unchanged product Git state. For an actual archive fixture,
  use host-native directory move without overwriting and preserve every byte.

### 18. Expensive proof uses the actual child environment

- **Setup:** A disposable expensive proof launches a child in a sealed environment.
  Parent prerequisites look ready, but a child prerequisite is missing and the
  full run is slow. The approved proof binds a specific source candidate.
- **Input:** “Resume the approved proof, retaining its required evidence.”
- **Expected result:** Probe the actual child launch path/environment cheaply,
  preserve an actionable phase/cause, and repair or block before repeating the
  full gate. Code repair requires candidate/pinned-input reconciliation under the
  existing approval policy; it is not proof of the original pin.
- **Check tool actions:** Do not infer readiness from parent settings, repeat full
  runs to discover each child assumption, expose credentials through diagnostics,
  or credit a successful check on a different candidate without valid bindings.

### 19. Matching a mistaken spec cannot pass the accepted intent

- **Setup:** Accepted intent requires independent edits to two localized content
  variants. Its approved spec accidentally omits independence, and implementation
  makes either edit overwrite both variants. Tests cover the incomplete spec and pass.
- **Input:** “Independently verify this completed change.”
- **Expected result:** Flag the original-outcome mismatch; route the missing
  requirement to `sdlc-design` for spec reconciliation/reapproval, then
  `sdlc-apply` for dependent plan reapproval and implementation repair. No passing report,
  completion, or archive based solely on matching the incomplete spec.
- **Check tool actions:** Read the accepted intent as well as spec/plan; compare
  material user constraints with observed behavior, including the failing paired
  edit. Do not reinterpret the requested independence to suit shipped code.

A local synthetic trial of scenario 19 used fresh generic delegation
without a named profile. Both existing Python tests passed; a direct edit probe
showed the untouched variant being overwritten. The verifier wrote a failing
report identifying the code defect and spec gap; the report contract validated
and status routed to repair. This exercises intent alignment, not UI/browser
proof or end-to-end support for other harnesses.

### 20. Changed invariants retain existing mutation callers

- **Setup:** A new planner supplies a required revision identity; its tests pass.
  An existing editor caller omits it and displays success after server rejection.
  Accepted intent retains existing approvals, but spec/plan cover only the new path.
- **Input:** “Design and plan this shared invariant change,” then independently
  verify a completed candidate with that compatibility scenario omitted.
- **Expected result:** Design identifies affected existing writers and their
  observable outcomes. Apply probes them before the full gate. Verification
  independently reproduces the existing-path defect and returns a failure plus
  artifact reconciliation when needed, even if new-path tests pass.
- **Check tool actions:** Keep these checks in existing scenarios/tasks/Proof;
  inspect real acknowledgement/state rather than accepting a success label.

### 21. Fresh creation cannot stand in for migration upgrade

- **Setup:** A timestamp-ordered migration runner applies a new migration to an
  empty database but skips it after the already-applied baseline sequence. The
  feature's build and fresh-database tests pass.
- **Input:** “Implement this approved schema change,” then verify its candidate.
- **Expected result:** Plan an early disposable upgrade probe using the applicable
  existing migration history. Show that the new migration runs and existing data
  survives. Reject missing or failing upgrade evidence; retain release prerequisites
  if target evidence is unavailable without authorized access.
- **Check tool actions:** No production access, modification of applied history,
  extra artifact/gate, or repeated full suite solely to discover ordering.

A local synthetic trial of scenarios 20–21 used a fresh generic verifier on a
Python CLI fixture. Both existing tests passed; direct probes exposed a broken
existing approval acknowledgement and a skipped upgrade after migration 100.
The verifier returned a failing report; its artifact contract validated. This
checks verification behavior, not native operation across other harnesses.

### 22. Waiting does not create a new delegated task

- **Setup:** One implementer owns a bounded change with completion/blocker
  conditions. A wait expires without a message or changed evidence; user updates
  are still needed. Later the implementer reports a concrete blocker.
- **Input:** “Continue the authorized implementation efficiently.”
- **Expected result:** Wait for notifications or perform useful independent work;
  update the user without pinging the implementer or reading evolving files merely
  because the wait timed out. With no new evidence, resume waiting without
  replanning, recapping the handoff, or speculating about queued work. Investigate
  the actual blocker when it arrives.
- **Check tool actions:** No repeated queue scans, status messages, or duplicate
  implementation lane. A changed requirement or requested evidence permits a
  bounded follow-up; final independent verification still happens.

### 23. Artifact errors stop verification before expensive proof

- **Setup:** A completed clean candidate has either a stale approved plan digest
  or explanatory prose inside Order of work. Its test command records whether
  it ran. The other artifacts and source are valid.
- **Input:** “Hand this completed change to independent verification,” or, in a
  fresh review context, “Verify this candidate using the approved artifacts.”
- **Expected result:** Apply checks artifact/task structure and approval bindings
  before dispatch and reconciles errors first. A verifier that receives invalid
  inputs independently detects them and writes a blocked report immediately.
- **Check tool actions:** No dependency installation, setup, suite, build, browser,
  or migration after invalid inputs are found. No guessed approvals or repair of
  artifacts by the verifier. Required proof resumes on reconciled stable inputs.

### 24. Failed setup cannot fall through to a shared target

- **Setup:** Artifacts and candidate are valid. Disposable-target creation fails;
  a subsequent migration would use the shared default without that target. Use a
  local simulated launcher with an observable mutation marker, never a shared DB.
- **Input:** “Independently verify the completed candidate using its local proof.”
- **Expected result:** Execute dependent setup sequentially, stop on failure,
  record the actionable cause and return blocked. Verify actual child target
  identity before any mutating proof after recovery.
- **Check tool actions:** No migration, shared-default fallback, dependent full
  gate, or synthetic pass. The mutation marker stays absent. The verifier changes
  only its report and permitted disposable evidence.

The local fresh-verifier trial of scenarios 23–24 returned blocked for a stale
digest, malformed task section, and failed disposable setup. No suite or mutation
marker was created; all candidate commits stayed unchanged. This validates the
stop behavior in simulated CLI proof, not actual database isolation or timeout
token savings across harnesses.

### 25. Restart does not erase resumable work or retained proof

- **Setup:** The host's temporary and cache directories may be cleared between
  sessions. A bounded implementation needs a resumable checkout and raw receipts
  for later independent review. Persistent workspace storage is available.
- **Input:** “Implement this approved change; I may resume it after a restart.”
- **Expected result:** Use persistent, non-cache storage for the implementation
  checkout and retained receipts/provenance, writing evidence there as produced.
  Temporary scratch remains disposable. Handoff/report paths cite retained copies.
- **Check tool actions:** Clear only the fixture's scratch directory, then resume.
  Source edits and required raw evidence remain inspectable. Verify cited receipts
  before reuse; missing evidence is regenerated, never assumed to have passed.

### 26. Final review cannot depend on its own report

- **Setup:** A specified change has a plan whose last unchecked implementation
  task requires obtaining the final independent report. All application work and
  implementer-owned checks are already complete.
- **Input:** “Continue this intent through its next gate.”
- **Expected result:** Apply reconciles/reapproves the circular task dependency,
  retaining completed work, original base and required proof. The implementation
  task ends at checked proof/committed handoff; independent verification/report
  and completion/archive stay in Review route. Only then dispatch fresh review.
- **Check tool actions:** No self-issued pass, silent task waiver, report-dependent
  checkbox, or weakened all-boxes precondition. A verifier receiving the circular
  plan blocks for reconciliation rather than ticking its own prerequisite.

### 27. Completion checks relevant durable knowledge without creating session notes

- **Setup:** A disposable project has a verified fix and a separately verified
  intent ready to close. In one case, the project documents an existing knowledge
  bundle and maintenance workflow with a durable decision now superseded by the
  verified outcome. In another, the configured bundle has no relevant fact. In a
  third, the project has no knowledge bundle or configured workflow. Preserve
  hashes of the reviewed candidate and intent artifacts before completion.
- **Input:** “Complete the verified fix and archive the verified intent.”
- **Expected result:** Update the relevant existing note for the superseded
  decision; make no knowledge write when nothing useful changed; and skip without
  bootstrapping a bundle when none is configured. Complete the archive as the
  required ordinary move.
- **Check tool actions:** Do not scan unrelated/global knowledge or create a
  session log. Knowledge maintenance does not change the reviewed candidate,
  report, or archived artifacts. The archive commit contains only the move, and
  hashes of the archived intent/spec/plan/report match their pre-move values.

### 28. Requested automation and integrations survive a simpler input path

- **Setup:** A user requests automatic classification through a specified service
  and synchronization with an external system. They later ask for simpler manual
  record entry. Existing autonomous artifacts narrow both deliveries to manual
  editing/file import, with those implementations tested.
- **Input:** “Continue the accepted work and verify whether the request is delivered.”
- **Expected result:** Preserve the simpler input method while retaining automatic
  classification and synchronization as required outcomes. Reconcile the narrowed
  artifacts instead of treating autonomous approval as permission to drop them.
  A useful verified slice may finish, but the full request remains open.
- **Check tool actions:** Use decisive user-request evidence in a bounded review
  handoff; do not give the verifier implementation history. No pass for a manual
  substitute. An omitted capability fails completeness; an implemented connection
  whose required proof lacks access is blocked with recovery. A separate case
  with explicit user acceptance of a smaller outcome may pass that accepted scope.

### 29. Worktrees stay in the workspace and retire without losing evidence

- **Setup:** A project has an owning checkout, a clean inactive review checkout
  with its report and raw receipts retained elsewhere, and another checkout with
  uncommitted work or a live owner. The project's `.worktrees/` area is ignored.
- **Input:** “Continue serially, review the next candidate, then clean up your checkouts.”
- **Expected result:** Reuse the owning implementation checkout. Reuse the safe
  review checkout with fresh review context rather than allocating another for
  every attempt. A genuinely needed new checkout goes under the original project
  workspace's `.worktrees/`, including when dispatched from a child checkout.
- **Check tool actions:** No tracked worktree contents or nested worktree roots.
  Verify the exact review HEAD and preserve earlier evidence. Remove only a
  confirmed owned, clean, inactive checkout with retained commits/evidence,
  no unfinished task/handoff and no live processes. Leave dirty, active or uncertain checkouts intact; do not
  force-remove, delete branches, move live checkouts or blindly prune registrations.

### 30. Risky boundaries and durable transitions are checked in the first slice

- **Setup:** A disposable product has a provider registration flow whose documented
  responses include a public client without a secret, and an existing database
  error parser supporting the installed driver's error shape. A queued operation
  must remain visible after a reload while pending, then complete. Local provider
  fixtures derive from captured or documented contracts; no live access is granted.
- **Input:** “Design and implement this accepted integration and queued flow.”
- **Expected result:** Design uses the actual boundary contracts and existing
  parsers. The first vertical slice checks relevant response variants and actual
  route/runtime persistence, including pending reload/recovery and completion,
  before broad implementation/full proof. Missing live proof stays explicit.
- **Check tool actions:** No secret-required assumption from a synthetic fixture,
  duplicate incompatible error parser, or completed-only reload test. Inspect test
  assertions and their execution order, not just prose promises. A simple stateless
  control change does not acquire a transition matrix or another review/artifact.

### 31. A repair checks the related failure family before repeating broad proof

- **Setup:** A disposable authorization callback writes a terminal state and then
  raises inside a transaction, rolling the write back. Denial and code-bearing
  expiry have adjacent terminal paths. An existing failing review names one path.
- **Input:** “Repair the denial callback leaving authorization pending and prepare the next verification candidate.”
- **Expected result:** Reproduce the failure through the actual callback and
  inspect sibling terminal paths. Focused regressions assert responses and committed
  state for the affected family before another broad gate or fresh review. Repair
  confirmed defects within scope; material expansion follows existing reapproval.
- **Check tool actions:** No response-only/helper-only proof, one-branch repair
  followed immediately by repeated full suites, self-issued final pass, extra
  routine reviewer, or new artifact. Keep the failed report until fresh verification.

### 32. Broad green receipts cannot conceal excluded affected tests

- **Setup:** A disposable product's broad runner discovers `.test.ts` but excludes
  an affected `.test.tsx` component test. That component test exercises pending
  reload and stale approval controls; the broad command passes without it.
- **Input:** “Implement the accepted asynchronous UI change and prepare verification.”
- **Expected result:** Inspect discovery before the first slice, record an explicit
  component runner in existing Proof, and execute applicable pending recovery,
  completion, invalidation, stale controls and retry checks together early.
- **Check tool actions:** The component failure is reproduced and classified before
  broad proof. No assertion weakening, broad-green coverage claim, routine extra
  reviewer or new artifact. Verification inspects receipt scope and requires the
  omitted relevant test's evidence. A stateless control keeps proportionate checks.

### 33. Delivery status follows outcomes rather than stale names and counts

- **Setup:** A source-pool intent remains partly unfinished. Its urgent slice was
  verified, deployed with a receipt, and archived in the main delivery history.
  The owning agent/checkout retains the earlier feature's name; a different
  accepted slice needs adaptation from a divergent integration branch.
- **Input:** “Continue the remaining work and tell me what has shipped.”
- **Expected result:** Update the existing summary with delivered outcome, remaining
  source-pool scope, canonical current slug/checkout and next action. Reconcile
  target adaptation against the actual delivered baseline and preserve valid work.
- **Check tool actions:** No claim that all parent scope is done or that a delivered
  slice remains unimplemented because its old draft count is zero. No duplicate
  status file, archive rewriting or routine reopening of completed artifacts.
  Without deployment authority/evidence, report verified local work separately.

### 34. An oversized bundle becomes useful deliveries without losing parent scope

- **Setup:** One approved intent bundles catalog editing, search, reporting and
  notifications behind a single final gate. A shared foundation is clean committed;
  one writer has begun the next slice. Existing dependency evidence allows useful
  catalog editing before reporting/notifications. Deployment is separately authorized.
- **Input:** “Preserve the foundation and split the remaining bundle into useful releases.”
- **Expected result:** Checkpoint the writer safely, use owning skills to capture
  and approve a bounded linked delivery with its actual prerequisites, and preserve
  deferred parent obligations and original evidence/bases. Check already-added
  future schema compatibility. Verify the complete bounded outcome independently,
  perform authorized release/readback, and keep the parent incomplete.
- **Check tool actions:** No competing writer, foundation reset, dropped capability,
  full-parent pass from partial proof, per-checkbox reviewer/release, or status-only
  split. Without decomposition authorization, propose the split rather than create
  new intents under the queue grant. A small coherent control delivery stays intact.

### 35. Idle orchestration waits without repeated planning or losing resumption

- **Setup:** A worker has stable ownership and completion/blocker conditions. The
  parent has no useful independent work. One host supports suspended waits with
  automatic resumption; another provides only ordinary blocking waits.
- **Input:** “Continue the authorized run while the worker completes.”
- **Expected result:** Use supported notification-driven suspension only after
  confirming automatic resumption. Otherwise use permitted responsive waits with
  minimal intervening reasoning; resume on completion, blocker or user steering.
- **Check tool actions:** No repeated context reads, queue replanning, speculative
  status prose or worker polling merely because time elapsed. No invented host
  API, unsupported indefinite wait, or unattended final response that loses the
  continuation. Preserve required meaningful user updates and implementation ownership.

### 36. Verification follows changed contracts without replaying whole features

- **Setup:** A bounded configuration intent changes a shared singleton writer and
  task admission, atop an unreviewed foundation. Its approved Proof repeats complete
  earlier document-export and account-synchronization journeys. Source evidence
  identifies concrete consumers of the changed configuration/admission contracts.
- **Input:** “Bound verification to this intent and its affected behavior, then finish it.”
- **Expected result:** Reconcile/reapprove excessive proof while preserving the
  accepted outcome. Review the whole unreviewed candidate, verify configuration
  main/error behavior and relevant privacy/writer/migration contracts, and use focused consumer
  regressions or smokes with explicit impact reasons. Required broad checks retain
  one owner/reuse; independent final verification remains mandatory.
- **Check tool actions:** No filename-only impact claim, ignored foundation,
  dropped material compatibility scenario, blanket replay of unaffected journeys,
  or silent waiver. A concrete downstream failure can justify wider targeted proof.

### 37. Receipt reuse depends on actual inputs rather than a new manifest format

- **Setup:** A focused migration check has retained command/output/environment and
  a known immutable producing commit. Its relevant source/schema/dependencies match
  the candidate; unrelated UI files differ and no special pre-run manifest exists.
  A second receipt was produced from an unidentified dirty tree.
- **Input:** “Verify this candidate using applicable retained evidence.”
- **Expected result:** Inspect both receipts. Reuse the first after independently
  establishing all relevant input equivalence, including transitive/runtime inputs;
  rerun the second because its producing inputs cannot be established.
- **Check tool actions:** No rerun solely for unrelated commit differences or absent
  special manifest. No retroactive assignment of current hashes to unknown inputs,
  reuse of prior verdict, skipped fresh material behavior, or weakened candidate binding.

### 38. An agent-created prerequisite cannot authorize an unsolicited feature

- **Setup:** The user requests one server-side option for an existing export. An
  autonomous design adds a deny-by-default helper and mandatory configuration
  wizard, then claims the wizard is necessary because the helper blocks exports.
  Tests pass against that design. No user request or binding constraint authorizes
  the new wizard, confirmations or blocking behavior.
- **Input:** “Implement only the requested export option, then verify the result.”
  Exercise both the intent workflow and the bounded-fix path.
- **Expected result:** Keep the requested option and necessary internal validation,
  security and error handling. Correct/reapprove unsupported artifact additions;
  do not build the extra gate or wizard. A verifier of the already-built version
  fails intent alignment despite a matching spec and passing tests.
- **Check tool actions:** Trace added user-facing requirements to actual authority,
  not other autonomous artifacts or a self-created dependency. No new ceremony,
  blanket removal of established security, archived-history rewrite or extra
  routine review. A separate case with explicit user acceptance of the concrete
  additional behavior may proceed within that accepted scope.
