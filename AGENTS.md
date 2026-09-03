# ai-sdlc (this repo)

Skills for the Anthropic AI-native SDLC artifact loop. No CLI. Product-repo files live at `intent/<slug>/`, not here.

## Commands

```bash
npx skills add . -l
npx skills add acourtiol/ai-sdlc -g -a claude-code -a cursor -a codex -s '*' -y
```

## Do not add

A CLI, a Codex plugin, an agent-org, `CLAUDE.md` dumps, `production-gate.sh`, evals CI, or `bands.yaml`. Design stays in `spec.md`; do not add a `design.md`. Do not copy these skills into chezmoi. Install with `npx skills add`.

Each `SKILL.md` has to stand alone. skills.sh copies folders independently. Templates stay in the skill that owns the artifact (`sdlc-plan` → intent, `sdlc-design` → spec, `sdlc-apply` → plan, `sdlc-verify` → report).

Archive is `intent/archive/YYYY-MM-DD-<slug>/`, a plain `mv` by `sdlc-archive`. No `archived` status; the directory is the signal. `intent/archive/` is not a slug, so anything scanning `intent/*/` skips it. Archive keeps history only: no `specs/<capability>/` tree, no delta sections, no merge step.

`sdlc-explore` writes nothing and owns no template. Do not give it a `notes.md`; the crystallized idea goes into `intent.md`. Its triage is deliberately duplicated in compact form in `sdlc-plan`, because each skill stands alone. spec-kit's clarify taxonomy and BMAD's technique library were considered for it and rejected as too much ceremony before an intent exists.

Deploy and Maintain plays wait until a product repo asks for a hook.

## Edit

Change a skill, commit, push `main`. Consumers run `npx skills update`.
