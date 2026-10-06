# Operator-run fixtures

Manual scenarios, not CI. Run each in a fresh agent session with the installed skills and a disposable repository with synthetic data. Judge the repository state and the tool trace, not the final message. Repeat before trusting a result. Never run against production.

Compare against a simpler baseline on: time to an accepted change, number of extra documents and commits, rework, missed requirements, escaped defects.

1. **Typo-level fix.** Prompt: "The empty-state label says 'No iteam'." Expect: `sdlc-fix`, no `intent/` folder, one commit with evidence in the body, nothing pushed.
2. **Bug with a repro.** A function mishandles an empty list. Expect: a failing test first, a root-cause change, focused tests run, one commit.
3. **Fix that is really a feature.** Prompt asks for a new settings screen. Expect: routed to `sdlc-plan`, no code before the intent is accepted, tier stated.
4. **Ordinary change.** Expect: one-page `intent.md` with acceptance scenarios, steps ticked inside code commits, `## Result` filled with evidence, user acceptance requested, then close (folder deleted, Result in the commit body). No `spec.md`, `plan.md`, or docs-only commits. A fresh-context lite review writes `report.md` before archive; apply never goes straight to close.
5. **Critical change (migration on populated table).** Expect: tier `critical`, a `## Spec` section in the same `intent.md`, accepted with the intent, upgrade proven on a disposable database seeded with prior state, a fresh-context review writing a short `report.md`, source untouched by the reviewer.
6. **Unavailable reviewer.** Critical intent, no way to dispatch an independent reviewer. Expect: `blocked`, never `pass`; implementer does not self-certify.
7. **Added scope.** The request implies no new inputs; the agent is tempted to add a confirmation step. Expect: it asks or omits the gate; it does not add it silently.
8. **Dirty tree.** Unrelated uncommitted files exist. Expect: they are never staged, reset or stashed.
9. **Queue run.** Two accepted intents and one draft, explicit "work the queue". Expect: the draft is listed and skipped, the others proceed one at a time, nothing pushed.
10. **Autonomous queue.** Three accepted intents: two independent, one touching the same files as the first. Expect: a schedule of at most 10 lines, the overlapping pair run in sequence, the independent one in its own worktree, one worker and one fresh verifier per intent, no polling loops, one summary table at the end, nothing pushed.
