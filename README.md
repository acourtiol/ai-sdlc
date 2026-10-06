# ai-sdlc

Agent skills for delivering product changes fast, with evidence that the result is what you asked for. Based on the [Anthropic AI-native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook), with ideas from [OpenSpec](https://github.com/Fission-AI/OpenSpec) and [spec-kit](https://github.com/github/spec-kit).

The skills use the [Agent Skills format](https://agentskills.io/specification). They need no named agent profiles or harness-specific delegation API.

## Install

```bash
npx skills add acourtiol/ai-sdlc -g -s '*'
```

List skills from a local checkout with `npx skills add . -l`. Update with `npx skills update`. The status script needs only POSIX `sh` and `awk`.

## Three paths, chosen by consequence

| Path | For | Artifacts | Gates |
| --- | --- | --- | --- |
| Fix (`sdlc-fix`) | Bug, tweak, small behavior change in an existing flow | none, evidence in the commit | none |
| Change (`sdlc-plan`, `sdlc-apply`, `sdlc-verify`) | New capability | `intent/<slug>/intent.md` (one page), `report.md` | you accept the intent, a fresh-context review, you accept the result |
| Critical | Migrations on populated data, auth, secrets, privacy, destructive or external-send behavior, LLM prompts or gates | adds a `## Spec` section | one acceptance covers intent and Spec; a missing independent reviewer blocks |

```text
sdlc-explore -> sdlc-plan -> sdlc-apply -> sdlc-verify -> user accepts -> close (last step of sdlc-apply)
```

`sdlc-continue` shows what is in flight and the next gate. Asked to "work the queue", it becomes an orchestrator: it schedules accepted intents by overlap, runs independent ones in parallel worktrees with one worker and one fresh verifier each, uses short research workers for hard decisions, lands passing work one at a time, and stops an intent after one failed repair round. When unsure of the tier, take the heavier one.

## Working agreements

- The intent is one page: problem, outcome in your words, acceptance scenarios, steps, and a Result filled at the end. You accept the intent before building and the result before it is closed.
- The implementer proves each acceptance item against the real path (consumer, persisted state after failure, populated-database upgrade for migrations). It does not grade itself: a fresh-context reviewer does, lite for a change and strict for critical work.
- One lane by default: current checkout, one intent at a time. Independent intents may run in parallel in `.worktrees/<slug>` with their own database and ports, merged by fast-forward or rebase; no integration branches.
- Confidence-gated challenge: at high confidence go on; otherwise one fresh read-only reviewer attacks the strongest unresolved assumption.
- Evidence lives in the commit and the intent's Result, not in extra documents. No docs-only commits that merely record verification.
- No push, deploy or external action without separate authorization. Closing an intent does not claim a release.
