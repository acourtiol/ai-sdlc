# ai-sdlc (this repo)

Skills for the Anthropic AI-native SDLC artifact loop. No CLI. Product-repo files live at `intent/<slug>/`, not here.

## Commands

```bash
npx skills add . -l
npx skills add acourtiol/ai-sdlc -g -a claude-code -a cursor -a codex -s '*' -y
```

## Do not add

A CLI, a Codex plugin, an agent-org, `CLAUDE.md` dumps, `production-gate.sh`, evals CI, or `bands.yaml`. Design stays in `spec.md`; do not add a `design.md`. Do not copy these skills into chezmoi. Install with `npx skills add`.

Each `SKILL.md` has to stand alone. skills.sh copies folders independently. Templates stay in the skill that owns the artifact (`sdlc-plan` → intent, `sdlc-design` → spec, `sdlc-apply` → plan).

Deploy and Maintain plays wait until a product repo asks for a hook.

## Edit

Change a skill, commit, push `main`. Consumers run `npx skills update`.
