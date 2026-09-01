# ai-sdlc (this repo)

Skills that implement Anthropic's AI-native SDLC artifact loop for coding agents.
No CLI. Product-repo artifacts live at `intent/<slug>/`, not here.

## Commands

```bash
npx skills add . -l
npx skills add acourtiol/ai-sdlc -g -a claude-code -a cursor -a codex -s '*' -y
```

## Hard no's

- Do not add a CLI, Codex plugin, agent-org, `CLAUDE.md` dumps, `production-gate.sh`, evals CI, or `bands.yaml`.
- Do not copy these skills into chezmoi. Install path is `npx skills add`.
- Keep each `SKILL.md` self-contained. skills.sh copies folders independently.
- Templates stay inside the skill that owns the artifact (`sdlc-plan` → intent, `sdlc-design` → spec, `sdlc-apply` → plan).
- Deploy/Maintain plays are out of scope until a product repo asks for a hook.

## Edit

Change a skill, commit, push `main`. Consumers run `npx skills update`.
