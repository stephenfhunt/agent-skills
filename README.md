# agent-skills

My collection of generally useful agent skills, kept in one repo so they can be
installed anywhere, like dotfiles. Skills use the open
[Agent Skills](https://agentskills.io/specification) `SKILL.md` format, so the
same files work in Claude Code, claude.ai, Codex, Cursor and other agents.

## Skills

| Skill | What it does |
| ----- | ------------ |
| _none yet_ | |

## Install

### Claude Code

```sh
git clone <this repo> ~/code/agent-skills
~/code/agent-skills/scripts/install.sh
```

This symlinks each `skills/<name>` into `~/.claude/skills/`, so edits in the
repo take effect immediately (in new sessions). Re-running is safe. Useful flags:

```sh
scripts/install.sh --dry-run            # show what would change
scripts/install.sh some-skill           # just one skill
scripts/install.sh --uninstall          # remove links that point into this repo
```

The script won't overwrite an existing file or a link it didn't create unless
you pass `--force`.

### Other agents

Pass `--target` (repeatable) to link into other agents' skill directories:

```sh
scripts/install.sh --target ~/.claude/skills --target ~/.agents/skills
```

- `~/.agents/skills`: the cross-agent user location, read by Codex and by
  Gemini CLI / Antigravity.
- `~/.claude/skills`: also read by Cursor, so the default install covers it.

### claude.ai and Claude Desktop

```sh
scripts/package.sh            # all skills -> dist/<name>.zip
scripts/package.sh some-skill
```

Upload the zip in Settings > Capabilities > Skills. Uploaded copies don't
update themselves; re-package and re-upload after changes.

## Working on skills

- [docs/authoring.md](docs/authoring.md): how to write a skill here.
- [docs/iteration.md](docs/iteration.md): how to test and improve one.
- `scripts/check.sh`: validates every skill's structure and frontmatter.
- `sources/<name>/`: gitignored place for reference material a skill was written
  from (books, papers). Keep it out of `skills/`, which is installed and packaged
  as a whole.
