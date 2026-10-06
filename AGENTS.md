# ai-sdlc

Standalone skills for a fast, evidence-backed change workflow. Product artifacts belong in `intent/<slug>/` in consumer repositories.

## Structure

- Each `SKILL.md` must stand alone: installers copy skill folders independently. Resolve resources relative to the installed skill directory.
- Keep instructions harness-neutral: capabilities and task responsibilities, never named agent profiles, specific models, or vendor-only delegation arguments.
- Public docs and fixtures use fictional examples and synthetic data. Omit private project names, personal details, paths and session IDs.
- Requirements live in the intent's Acceptance list; critical intents add a `## Spec` section in the same file. No `spec.md`, `design.md`, `plan.md`, digests, validators or fingerprint scripts.
- A finished intent is deleted in a `chore(<slug>): close intent` commit whose body carries the Result; git is the archive. An intent is open while its folder exists.
- Deployment and maintenance automation wait for a product-repository request.

## Keep it small

The workflow's value is delivering what the user expected, fast. Before adding a rule, ask what failure it prevents, whether that failure was observed, and whether a one-line rule or a check in the product repo would do instead. Do not add a rule per incident. A skill over about 60 lines, or total skill text over about 25 KB, is a smell: delete or merge before growing. Do not add a CLI, plugin, agent organization, evals CI, or retained-receipt and digest-binding machinery.

## Validate and publish

List installable skills with `npx skills add . -l`. For changes to `status.sh`, run `python3 -m unittest discover -s tests`. Inspect the final diff and preserve unrelated work. Commit with Conventional Commits (`type(scope): imperative summary`); mark breaking changes with `!` or a `BREAKING CHANGE:` footer. Push `main` only when asked; consumers update with `npx skills update`.
