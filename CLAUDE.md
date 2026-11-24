# agent-skills

Personal library of agent skills in the open `SKILL.md` format, kept like a
dotfiles repo and installed into Claude Code, claude.ai and other agents.
(`AGENTS.md` is a symlink to this file.)

## Layout

- `skills/<name>/`: one directory per skill. Only skill content goes here;
  everything in it is installed and packaged.
- `evals/<name>/cases.md`: eval prompts and checklists. `evals/<name>/runs/` is
  gitignored scratch space for eval outputs.
- `templates/SKILL.md`: starting point for a new skill.
- `docs/authoring.md`: conventions for writing skills. Follow it.
- `docs/iteration.md`: the eval loop. Follow it when creating or changing a skill.
- `scripts/`: `check.sh` (validate), `install.sh` (symlink into agent dirs),
  `package.sh` (zip for claude.ai into `dist/`).

## Rules

- Run `scripts/check.sh` before committing any change under `skills/`.
- Never put eval cases, run outputs or notes inside `skills/`.
- When adding or renaming a skill, update the skills table in `README.md`.
- Keep skills environment-neutral: no dependence on Claude Code-only tools or
  frontmatter fields unless the skill is explicitly Claude Code-specific.
- Commit a skill change together with any `cases.md` changes it motivated, and
  record what failed and what changed in the commit message.
- Scripts are plain bash with no dependencies beyond coreutils (packaging uses
  `zip`, falling back to `python3`); keep them that way and run `shellcheck` if
  available.
