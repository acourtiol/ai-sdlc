# ai-sdlc

Standalone skills for the Anthropic AI-native SDLC artifact loop. Product artifacts belong in `intent/<slug>/` in consumer repositories.

## Structure

- Each `SKILL.md` must stand alone: installers copy skill folders independently. Keep templates with their owner: plan → intent, design → spec, apply → plan, verify → report. Resolve resources relative to the installed skill directory.
- Keep instructions harness-neutral. Use capabilities and task responsibilities, never named agent profiles, specific models, or vendor-only delegation arguments.
- Public docs and behavioral fixtures use fictional examples and synthetic data. Generalize consumer feedback; omit private project names, personal request details, paths, session IDs, and operational identifiers.
- Requirements and design share `spec.md`; do not add `design.md`.
- Explore normally writes nothing and owns no template. Optional `context.md` holds consequential handoff information absent from other artifacts; it creates no gate. No `notes.md` or folders for spikes and bounded fixes. Keep compact triage in explore, plan, and fix so each works independently.
- Archive is an ordinary directory move to `intent/archive/YYYY-MM-DD-<slug>/`. Skip `intent/archive/` in active-intent scans. No `archived` status, capability specs tree, delta sections, or merge step.
- Deployment and maintenance automation wait for a product-repository request. Existing plans/reports may record rollout, recovery, and observations; archive does not imply release.

Do not add a CLI, Codex plugin, agent organization, `CLAUDE.md` dumps, `production-gate.sh`, evals CI, or `bands.yaml`. Install using `npx skills add`; do not copy skills into chezmoi.

## Validate and publish

List installable skills with `npx skills add . -l`. For behavior changes, run `python3 -m unittest discover -s tests` and check affected behavioral scenarios in `tests/behavioral/README.md`. Inspect the final diff and preserve unrelated work.

Commit and push `main`. Use Conventional Commits: `type(scope): imperative summary` (scope optional); `feat` for new behavior, `fix` for corrections, `docs` or `chore` otherwise. Mark breaking changes with `!` or a `BREAKING CHANGE:` footer. Consumers update with `npx skills update`.
