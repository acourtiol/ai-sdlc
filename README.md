# ai-sdlc

Skills for Anthropic's [AI-native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook): Plan → Design → Build → Test, with a human gate at every handoff.

No CLI. Agents write `intent/<slug>/intent.md`, `spec.md`, and `plan.md` in the product repo, then implement. Cursor, Codex, and Claude Code install the same folders.

Based on the playbook. Not a fork of third-party "AI-native SDLC" repos. Not Anthropic.

## Install

```bash
npx skills add acourtiol/ai-sdlc -g -a claude-code -a cursor -a codex -s '*' -y
```

Never `--agent '*'`.

| Skill | Writes | When |
| --- | --- | --- |
| `sdlc-plan` | `intent/<slug>/intent.md` | new product feature or change |
| `sdlc-design` | `spec.md` | accepted intent, no spec yet |
| `sdlc-apply` | `plan.md` then code | approved spec; plan gate before code |
| `sdlc-verify` | evidence only | judge the running change against intent |
| `sdlc-continue` | next gate | resume an in-progress `intent/<slug>/` |

## Coexist with OpenSpec

If the product repo has `openspec/` with open changes, use OpenSpec (`openspec` binary, never `npx openspec`). These skills are for new work in repos without that tree, or after those changes are archived.

## Hard rules the skills enforce

- Gates are real: do not skip accept/approve.
- Do not commit unless the user asks (chat approval is the gate; git is optional).
- Do not dump `CLAUDE.md` or auto-memory. Repeated mistakes go in the project's `AGENTS.md` or its OKF bundle.
- Ceiling is Test + review. No production deploy from these skills.

## Layout in a product repo

```text
intent/<slug>/intent.md
intent/<slug>/spec.md
intent/<slug>/plan.md
```

Status in frontmatter: `draft` → `accepted` → `specified` → `planned` → `done`.
