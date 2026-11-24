# Document types

Each section covers one kind of document: who reads it and why, what goes first, a skeleton,
and the usual ways it goes wrong. A skeleton is a starting shape, not a form to fill in. Drop the
parts your document doesn't need, and never add a section just because the skeleton lists it.

The first four types follow the Diátaxis framework. To check which one you're writing, ask two
questions. Does the reader want to *do* something or to *know* something? Are they *learning* or
*working*?

| | Learning | Working |
| --- | --- | --- |
| **Doing** | tutorial | how-to guide |
| **Knowing** | explanation | reference |

## README

**Reader:** someone deciding whether this project is what they need, and then trying it. They
often arrive from a search or a link and give it a few seconds before leaving.

**First:** one or two sentences saying what the project does and for whom, in plain words. Name the
problem it solves, not the technology it uses. If a newcomer couldn't explain the project to a
colleague after reading the opening, rewrite it.

**Skeleton:**

1. Name and a one- or two-sentence description.
2. The smallest example that shows it working: install, then one command or a few lines of code,
   with the output if that makes the point.
3. Requirements and installation, if they're more than one line.
4. Usage: the common tasks, each with an example. Link to fuller docs instead of reproducing them.
5. Limits and non-goals, briefly. Readers trust a project more when it says what it doesn't do.
6. How to get help or contribute, and the license.

**Usual failures:**

- Adjectives in place of facts: "powerful", "blazingly fast", "lightweight", "modern". If speed
  matters, give a number and say what it was measured on.
- A feature list of bold labels and emoji, with no example of the thing running.
- An opening that explains the field ("In today's world, managing configuration is hard") before
  saying what the project is.
- Install instructions that skip prerequisites the author has had installed for years.
- Several screens of reference material that belong in separate docs.

## Tutorial

**Reader:** a newcomer who wants to learn by doing. They don't know what matters yet, so they'll
follow your steps exactly, and they can't recover from a step that doesn't work.

**First:** what they'll have built or done by the end, and what they need before starting (tools,
versions, accounts, rough time).

**Skeleton:**

1. What you'll build, and prerequisites.
2. Numbered steps. Each step is one action with a visible result, and the result is shown ("You
   should see…"). Give the expected output, and mention the most likely error and its fix.
3. A short "what you did" at the end that names the concepts the learner just used, with links to
   explanations of them.
4. Where to go next.

**Principles:** Get the learner to a visible result early. Keep explanation to one sentence ("We
use HTTPS here because the API rejects plain HTTP") and link to more. Leave out options and
alternatives, because a learner can't choose between things they don't understand yet. Test every
step from a clean environment, or say plainly which steps you couldn't test.

**Usual failures:**

- "Simply", "just" and "easily", and steps that bundle three actions into one.
- Missing expected output, so the learner can't tell whether a step worked.
- Long detours into how things work, or lists of every flag.
- An unstated assumption: a tool already installed, a directory you're already in, an environment
  variable you set earlier in the conversation.
- Showing the wrong way first and revealing later that it was wrong. If you're showing a mistake on
  purpose, say so at the time.

## How-to guide

**Reader:** someone who already uses the thing and has a specific goal: "rotate the signing key",
"run the tests against Postgres". They want the shortest correct path, and they'll adapt it to
their own setup.

**First:** a title that names the goal ("How to rotate the signing key"), then any condition that
decides whether this guide applies to them.

**Skeleton:**

1. Goal, and when you'd want it.
2. Prerequisites, if any.
3. Steps. These can branch ("If you use Docker, …; otherwise, …").
4. How to check that it worked.
5. Related guides or the relevant reference.

**Principles:** Write from the reader's goal, not from the tool's features. Include judgment where
the reader needs it ("Rotate during low traffic. Tokens signed with the old key stop working
immediately."). Leave teaching to tutorials and full option lists to reference, and link to both.

**Usual failures:** a guide titled after a feature rather than a goal; a guide that tries to cover
every variation equally; missing the check at the end.

## Reference

**Reader:** someone who is in the middle of work and needs one fact: a flag, a return value, a
limit, an error code. They search or scan, and they don't read from the top.

**First:** whatever they'll look up most. For a command, the synopsis. For a function, the
signature and a one-line summary.

**Principles:** Organize it to match the structure of the thing being described (one entry per
command, endpoint or option), and give every entry the same shape. Describe neutrally and
completely: types, defaults, units, limits, errors. Add a short example for each entry. Leave out
opinion, history and instructions, and link to them instead.

**Usual failures:** inconsistent entries; missing defaults and units; prose explanations mixed into
entries so they're hard to scan; treating auto-generated API docs as the only documentation a
project needs.

## Explanation

**Reader:** someone who wants to understand: why the system is designed this way, how the parts fit
together, what the trade-offs were. They're reading away from the keyboard and will follow an
argument.

**First:** the question the explanation answers, in concrete terms. "Why does the scheduler run
jobs in a separate process?" works better than "Scheduler architecture".

**Principles:**

- Start from something concrete the reader already knows or can see, then widen.
- Introduce one idea at a time, each with an example.
- Give the reasons, the history and the constraints. Consider the alternatives and say why they
  weren't chosen. Opinion is fine here if it's labelled and argued.
- Keep analogies to one point.
- Use a realistic example, taken from the actual codebase if you can.

**Usual failures:** starting with an abstract definition; introducing five terms in one paragraph;
"what" without "why"; an analogy that takes longer to decode than the thing itself; claims with
nothing to support them ("this approach is more scalable") where the reader needed an example or a
number.

## Design doc or proposal

**Reader:** people who will decide or review. They need to understand the problem, judge the
proposal and see the trade-offs, often in a few minutes before a meeting.

**First:** the problem and the proposal, each in a sentence or two. Then the decision you need from
the reader, and by when.

**Skeleton:**

1. Summary: the problem, the proposal and the decision needed.
2. Context: what's true now and why it's a problem, with evidence (numbers, incidents, user
   reports).
3. Proposal: what changes, concretely enough that a reviewer could spot a flaw.
4. Alternatives considered, and why each was rejected. A sentence or two each is usually enough.
5. Risks, open questions, and what you'll measure.
6. Plan: steps, order and rough size.

**Usual failures:** context so long that the proposal starts on page three; alternatives that are
obviously straw men; open questions hidden in the middle of paragraphs instead of collected where
reviewers will find them.

## PR description

**Reader:** a reviewer who will read the diff with this beside it, and later someone running
`git blame` who wants to know why the code is the way it is.

**First:** what the change does and why, in one or two sentences. Link the issue if there is one,
but don't make the reader open it to understand the change.

**Skeleton:**

1. What and why.
2. How, only where the diff doesn't make it obvious: the approach, and anything surprising.
3. How it was tested, specifically ("ran the migration against a copy of production data; 4.2M
   rows, 3 minutes").
4. What the reviewer should look at closely, and any known gaps or follow-ups.

**Usual failures:** a file-by-file list of changes that repeats the diff; the story of how you got
there; "various improvements"; claims of testing with no detail; a closing "Let me know if you have
questions".

## Commit message

**Reader:** a future maintainer reading `git log` or `git blame`, often a year later, often while
debugging.

**Shape:** a subject line of about 50 characters in the imperative ("Resume uploads from last
confirmed chunk"), then a blank line, then a body that explains why the change was needed and
anything non-obvious about how. The diff already shows what changed line by line.

**Usual failures:** "Fix bug" or "Update code"; a body that lists the files changed; leaving out the
reason, which is the one thing the diff can't show.

## Release notes and changelogs

**Reader:** a user deciding whether to upgrade and what will break if they do.

**First:** anything that requires action: breaking changes, migrations, deprecations. Then new
features, then fixes.

**Principles:** Write each entry from the user's point of view: what they can now do, or what now
behaves differently. "Uploads over 2 GB no longer fail" beats "Refactored retry logic in upload
module". Link to the PR or issue for detail. Keep internal refactors out unless they change
behaviour.

**Usual failures:** a raw list of commit messages; breaking changes buried among fixes; marketing
tone ("We're thrilled to announce…").

## Work report, handoff or status update

**Reader:** someone who wasn't there: your user coming back to the session, a teammate taking over,
a manager who wants to know where things stand. Assume they haven't seen the conversation, the
files or the dead ends.

**Shape:** conclusion, evidence, caveats, next action.

1. **Conclusion.** What is true now: done, not done, broken, decided. One or two sentences.
2. **Evidence.** What makes the conclusion believable: the test that passes, the measurement, the
   log line, the file and function. Keep what you verified separate from what you inferred.
3. **Caveats.** Only those that would change what the reader does: what you didn't test, what
   might break, what you assumed.
4. **Next action.** What the reader should do, or what you'll do next, and anything you need from
   them.

Address the reader by name or as "you", and don't guess anyone's pronouns from their name.

For a handoff, add what the next person needs to pick up the work cold: where things are, how to
run them, and what you tried that didn't work. Keep that last part short. It saves them from
repeating it, and it isn't a diary.

**Usual failures:**

- Narrating the session in order ("First I looked at… then I noticed…").
- Labels from the working session: "Option B", "the second approach", "the fix from earlier".
- "As discussed" or "as you know", when the reader may not know.
- Hedges on every claim, or confidence about things that weren't checked.
- Listing every file touched when only two matter.
- A closing offer of more help instead of the next action.
