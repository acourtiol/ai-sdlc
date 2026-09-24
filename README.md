# ai-sdlc

```bash
npx skills add acourtiol/ai-sdlc -g -a claude-code -a cursor -a codex -s '*' -y
```

Name the agents. Do not pass `--agent '*'`.

Cursor, Codex, and Claude Code load the same skill folders. There is no CLI. If the idea is still half-formed, brainstorm first. In the product repo the agent writes `intent/<slug>/intent.md`, then `spec.md`, then `plan.md`, then code, then `report.md`, then archives the folder. You accept or approve at each step; after a yes, the same session starts the next skill unless you tell it to stop.

This follows Anthropic's [AI-native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook). Requirements and design go in one file, `spec.md`. Do not add a `design.md`; the playbook folded those into one session. This repo is not Anthropic, and it is not a fork of other projects that use the same playbook name.

## Skills

| Skill | Writes | When |
| --- | --- | --- |
| `sdlc-explore` | nothing | the idea is still half-formed, or you are not sure it needs the loop |
| `sdlc-plan` | `intent/<slug>/intent.md` | new product feature or change; on accept, starts design |
| `sdlc-design` | `spec.md` | accepted intent, no spec yet; on approve, starts the plan |
| `sdlc-apply` | `plan.md` then code then `sdlc-verify` | approved spec; plan gate before code; verify is not optional; fail → fix → re-verify |
| `sdlc-verify` | `report.md` | judge the running change against intent; always after apply; judgment only |
| `sdlc-archive` | moves the folder | `report.md` with `verdict: pass`, no CRITICAL, and statuses `done` |
| `sdlc-continue` | next gate | resume an in-progress `intent/<slug>/` |

The playbook's audit trail is the diff and the PR review findings. When there is no PR, `report.md` and `intent/archive/YYYY-MM-DD-<slug>/` hold that record.

`sdlc-explore` is the playbook Plan stage: you brainstorm, then `intent.md` gets written. Spike / bounded / intent-worthy triage decides whether that file is needed.

## What the skills will not do

They wait for you to accept or approve, then continue into the next skill unless you tell them to stop. They commit each artifact on its own as it is written, and each finished implementation slice on its own. They do not push unless you ask. Apply always runs verify; a failing report goes back to apply to fix, not to archive. They do not archive without a passing `report.md` with no CRITICAL. They do not deploy.

## Files in a product repo

```text
intent/<slug>/intent.md
intent/<slug>/spec.md
intent/<slug>/plan.md
intent/<slug>/report.md
intent/archive/YYYY-MM-DD-<slug>/
```

Status in frontmatter: `draft` → `accepted` → `specified` → `planned` → `done`. There is no `archived` status; a folder under `intent/archive/` is archived and one under `intent/` is not.
