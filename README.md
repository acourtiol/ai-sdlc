# ai-sdlc

```bash
npx skills add acourtiol/ai-sdlc -g -a claude-code -a cursor -a codex -s '*' -y
```

Name the agents. Do not pass `--agent '*'`.

Cursor, Codex, and Claude Code load the same skill folders. There is no CLI. In the product repo the agent writes `intent/<slug>/intent.md`, then `spec.md`, then `plan.md`, then code. You accept or approve at each step.

This follows Anthropic's [AI-native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook). The Design stage is one file, `spec.md`, covering requirements and design together. There is no `design.md`. That name comes from OpenSpec.

This repo is not Anthropic. It is also not a fork of other projects that use the same playbook name.

## Skills

| Skill | Writes | When |
| --- | --- | --- |
| `sdlc-plan` | `intent/<slug>/intent.md` | new product feature or change |
| `sdlc-design` | `spec.md` | accepted intent, no spec yet |
| `sdlc-apply` | `plan.md` then code | approved spec; plan gate before code |
| `sdlc-verify` | evidence only | judge the running change against intent |
| `sdlc-continue` | next gate | resume an in-progress `intent/<slug>/` |

## If the repo still has OpenSpec

If `openspec/` has open changes, use the `openspec` binary (never `npx openspec`). Use these skills for new work after that tree is archived, or in repos that never had one.

## What the skills will not do

They wait for you to accept or approve. They do not commit unless you ask. They do not write `CLAUDE.md` memory dumps. They stop at test and review; they do not deploy.

## Files in a product repo

```text
intent/<slug>/intent.md
intent/<slug>/spec.md
intent/<slug>/plan.md
```

Status in frontmatter: `draft` → `accepted` → `specified` → `planned` → `done`.
