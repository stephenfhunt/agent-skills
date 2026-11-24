# Iterating on a skill

A lightweight loop for checking that a skill actually changes agent behaviour
for the better. The goal is judgement against concrete cases, not scores.

## Eval cases

Each skill has `evals/<name>/cases.md`, committed alongside the skill. It holds
3–6 realistic prompts, each with what good output looks like and the failure
modes to watch for:

```markdown
## case: release-notes
Prompt:
> Write release notes for these changes: ...

Good output:
- ...

Watch for:
- ...
```

Keep prompts realistic: the kind of thing you would actually ask, with enough
context to produce a real answer. Add a case whenever you see the skill fail in
real use; that failure is the most valuable test you have.

## Running an eval

Run evals from a Claude Code session in this repo. For each case, start two
fresh subagents with the same prompt:

- **baseline**: the prompt alone.
- **skill**: the prompt, preceded by an instruction to read
  `skills/<name>/SKILL.md` (and any references it points to) and follow it.

Save each output verbatim to
`evals/<name>/runs/<YYYY-MM-DD>/<case>-baseline.md` and `<case>-skill.md`.
Run directories are gitignored; they are scratch space.

To evaluate a change to an existing skill, use the previous version of the
skill as the baseline instead of no skill (copy it to the run directory first,
e.g. `git show HEAD:skills/<name>/SKILL.md > evals/<name>/runs/<date>/old-SKILL.md`).

## Reviewing

Read each pair side by side against the case's checklist. Write
`evals/<name>/runs/<date>/notes.md` with, per case:

- which output is better, and why, in a sentence or two;
- any checklist item the skill version still misses;
- anything the skill made *worse* (over-correction, bloat, new tics).

The person reviewing should read the outputs themselves; an agent's summary of
which is better is a useful second opinion, not the verdict.

## Changing the skill

1. Edit the skill to address what the notes found. Prefer explaining the
   underlying principle over patching one symptom.
2. Re-run the affected cases (and one or two unaffected ones, to catch
   regressions).
3. When a failure mode is new, add it to `cases.md` as a case or "watch for".
4. Run `scripts/check.sh`, then commit the skill and cases together. Put the
   lesson in the commit message: what failed, what changed, what improved.
5. If the description changed, reinstall (`scripts/install.sh`) and check in a
   fresh session that the skill still triggers on the right prompts and not on
   unrelated ones.
