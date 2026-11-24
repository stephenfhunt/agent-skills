# Authoring skills

Conventions for writing a skill in this repo. The format follows the open
[Agent Skills specification](https://agentskills.io/specification), so a skill
written here works in Claude Code, claude.ai, Codex, Cursor and other agents
that read `SKILL.md`.

## Anatomy

```
skills/<name>/
  SKILL.md          required: frontmatter + instructions
  references/       optional: detail loaded only when needed
  scripts/          optional: code the agent can run
  assets/           optional: templates, data files
```

Start from the template (`mkdir skills/<name> && cp templates/SKILL.md
skills/<name>/`) and fill in the placeholders, or ask an agent to use the
`skill-creator` skill to draft one. Delete template sections you don't need; the References
link is a placeholder and `scripts/check.sh` will flag it until the file exists.

## Frontmatter

Use only the portable fields:

- `name`: 1–64 chars, lowercase `a-z`, `0-9` and single hyphens, no leading or
  trailing hyphen, and identical to the directory name.
- `description`: 1–1024 chars. Say what the skill does **and** when to use it.

Avoid tool-specific fields (e.g. Claude Code's `allowed-tools`, `model`) unless
the skill is only meaningful in that tool; other agents ignore or reject them.

## The description is the trigger

The description is the only part an agent sees before deciding whether to load
the skill. Write it for that decision:

- Lead with the task the skill helps with, in the words a user would use.
- List the concrete situations that should trigger it. Agents tend to
  under-trigger, so be specific and a little insistent rather than modest.
- Mention near-misses it should *not* trigger on only if confusion is likely.

## The body

- **Explain why.** Instructions that carry their reasoning generalize to cases
  you didn't anticipate; bare MUSTs and NEVERs get followed rigidly or ignored.
- **Show, don't only tell.** A good before/after example teaches more than a
  paragraph of principle.
- **Keep SKILL.md lean.** Aim well under 500 lines. Put long reference material
  in `references/*.md`, link it with a relative path, and say when to read it.
- **Stay environment-neutral.** Don't depend on a specific agent's tool names,
  slash commands or file layout. If a skill benefits from a tool, describe the
  capability and make the skill still useful without it.
- **Write for a capable reader.** Skip what any competent model already knows;
  spend the words on judgment calls, house preferences and known failure modes.

## Adding a skill: checklist

1. Create `skills/<name>/SKILL.md` and `evals/<name>/cases.md`.
2. Run `scripts/check.sh <name>`.
3. Run the eval loop in [iteration.md](iteration.md) at least once.
4. Add a row to the skills table in `README.md`.
5. `scripts/install.sh <name>` and confirm it triggers in a fresh session.
