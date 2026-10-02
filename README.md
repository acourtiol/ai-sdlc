# ai-sdlc

Agent skills for turning a product idea into a specified, implemented, independently verified change. Based on the [Anthropic AI-native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook), with ideas from [OpenSpec](https://github.com/Fission-AI/OpenSpec) and [spec-kit](https://github.com/github/spec-kit).

The skills use the [Agent Skills format](https://agentskills.io/specification). They require no named agent profiles or harness-specific delegation API.

## Install

Install all skills globally, then choose your target agents in the installer:

```bash
npx skills add acourtiol/ai-sdlc -g -s '*'
```

List skills from a local checkout with `npx skills add . -l`. Update installed copies with `npx skills update`. Artifact validation requires Python 3.8+ and uses only the standard library.

## Workflow

```text
sdlc-explore → sdlc-plan → sdlc-design → sdlc-apply → sdlc-verify → sdlc-archive
```

| Skill | Purpose |
| --- | --- |
| `sdlc-explore` | Shape an idea and decide whether it needs an intent. |
| `sdlc-plan` | Capture the problem, desired outcome, and constraints in `intent.md`. |
| `sdlc-design` | Write testable requirements and design together in `spec.md`. |
| `sdlc-apply` | Write `plan.md`, then implement the approved change. |
| `sdlc-verify` | Independently check behavior against the accepted outcome; write `report.md`. |
| `sdlc-archive` | Validate completion and move the change record into the archive. |
| `sdlc-continue` | Resume at the next gate, or process existing open intents when explicitly asked. |
| `sdlc-fix` | Fix a bounded bug or make a behavior-preserving refactor without an intent folder. |

Install the relevant skills together for a complete workflow. Each skill owns its instructions and artifact templates.

## Working agreements

Product-repository artifacts live at `intent/<slug>/`. Intent, spec, and plan require approval before advancing; approval digests bind downstream work to those decisions. Material changes reopen affected approvals and invalidate stale verification.

Implementation stays in one active lane through final review. A fresh reviewer checks the committed candidate, including observable product behavior. Missing required evidence blocks completion. Archive moves the record to `intent/archive/YYYY-MM-DD-<slug>/`; it does not claim a production release.

An explicit autonomous queue request allows local decisions, implementation, commits, completion, and archive for existing intents. Decision challenges happen only below high confidence: the outcome must be clear, current source and contracts must support the approach, and material uncertainties must be resolved. Final independent verification remains required. Pushing, deployment, and consequential external actions need separate authorization.
