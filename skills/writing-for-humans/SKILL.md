---
name: writing-for-humans
description: Write prose a person can read once and understand. Use it for READMEs, documentation, tutorials, how-to guides, explanations of code or concepts, design docs, PR descriptions, release notes, commit message bodies, handoffs, status updates, and reports or summaries of completed work. Use it whenever you produce more than a few sentences that a human will read, including messages to other agents that may be passed on to a person, and whenever you are asked to edit writing to make it clearer, shorter or less "AI-sounding". It covers working out what the reader knows, leading with the point, keeping habits that help the writer (hedging, signposting, recaps, reflexive bullets and headers, inflated vocabulary) out of the finished text, and the conventions of technical and teaching documents. It includes an optional prose-checking script for the revision pass. Not needed for short conversational replies or for code itself.
---

# Writing for humans

Write so that the person reading can understand, or act, after one pass through the page, and so
that the page sounds like a knowledgeable colleague talking to them. Getting there means picturing
the reader before you draft, putting the point first, keeping the habits that help you think out of
the text you hand over, and revising by reading as the reader would.

## Why this needs saying

You and your reader start from different places. By the time you write, you have read the
files, run the commands, tried and dropped a few approaches, and named things along the way. The
reader has none of that. They have the page, a limited amount of attention, and a reason for
opening it.

Much of what you produce while working is good for working. Hedging keeps options open. Restating
the goal keeps you on track. Listing every case makes sure none is missed. Narrating each step lets
you check your reasoning. On the page, each of these becomes a cost the reader pays: they have to
find the claim under the qualifiers, skip the recap, dig the important case out of the list, and
wade through the story to reach the result. Your working notes and the finished document are
different texts, and the reader should only ever see the finished one.

There is also a pull toward safe, generic language. Words like "robust", "seamless" and
"comprehensive" fit almost any sentence, which is why they say nothing in yours. Specific facts,
names, numbers and examples are what the reader came for.

## Before you write: picture the reader

Answer these before drafting, even if only in your head:

- **Who is reading?** A maintainer reviewing a PR, someone who found the project on GitHub, a
  teammate taking over your work tomorrow, a learner who has never used the tool.
- **What do they already know?** Judge from what they have told you and where the document will
  live, not from what you know. If you can't tell, write for a smart person who is new to this
  project.
- **Why did they open it, and what will they do next?** Install something, decide whether to
  merge, fix the bug you found, understand a design.
- **How will they read it?** Skimmed top to bottom, followed step by step with a terminal open,
  searched for one fact, read on a phone between meetings.

Then check what you are about to take for granted. The reader has not seen this conversation, the
files you opened, the errors you hit or the approaches you rejected. A label you made up while
working ("the fallback path", "Option B", "the v2 approach") means nothing to them, so define it,
replace it with a plain description, or cut it. "As discussed" and "the issue above" point into a
context the reader never had. Acronyms and project-specific terms need a short explanation the
first time they appear.

Last, ask the question Orwell and Zinsser both start from: what am I trying to say? Put the answer
in one or two sentences before you begin. If you can't, the content isn't settled yet, and that
work belongs in your notes rather than in the document.

## Write the document, not the work log

Put the point first. In a report, that's the result. In a README, it's what the project does and
why someone would want it. In a tutorial, it's what the reader will have built by the end. Supporting
detail follows, in the order the reader needs it.

Tell the reader what you found rather than how you found it. "The cache key leaves out the locale,
so French users see English pages" is worth more than three paragraphs on the order in which you
opened files. Narrate the process only when the process is the content: a postmortem, a record of
what was tried so that nobody tries it again, or a tutorial where the steps are the lesson.

Aim for what Thomas and Turner call classic style. You have seen something clearly, and you are
pointing it out to an intelligent equal. That stance gets rid of most hedging and throat-clearing
on its own, because you aren't defending yourself or performing diligence. You're showing someone
something.

Commit where you know. Where you're unsure, say so once, specifically, at the point where it
matters. "I haven't tested this on Windows" helps the reader. "This may potentially help in some
cases" doesn't. Keep what you checked separate from what you inferred, and never invent a detail
(a version number, a benchmark, a user count) to make a sentence sound stronger.

## Default to prose

Write paragraphs that each develop one idea. Prose carries the connections between facts
("because", "so", "unless", "which means"), and a bullet list drops them. Those connections are
often what the reader most needs.

Use a list when the items really are parallel (options, requirements, files), sequential (steps),
or meant to be compared. Use a table when the reader will compare several items on the same few
attributes. Use headings when the document is long enough that someone will jump to one part. A
three-paragraph note doesn't need them. Bold a term where you define it, or a warning the reader
must not miss, and almost nowhere else. Avoid nested lists. If the hierarchy matters, explain it in
sentences.

A quick test for a list: if each bullet would read fine as a sentence, and the sentences would read
better joined into a paragraph, write the paragraph.

## Habits that help you and cost the reader

These habits run all through model-written prose. Each is useful while you're working and costly
on the page.

**Stacked qualifiers.** "This could potentially help to somewhat reduce latency in certain cases."
Each hedge felt prudent, and together they say nothing. Zinsser quotes a cabinet secretary who got
five hedges into a thirteen-word sentence. Say what you know, and put the one real caveat where it
applies.

**Throat-clearing and signposting.** Openings that announce instead of delivering: "It's worth
noting that", "Let's dive into", "In this section we'll explore", "Great question". Zinsser's
answer to "It is interesting to note" was to make it interesting. Start with the content.

**Restating.** Repeating the question back, closing each section with a summary of that section,
or ending with "In summary" and the same points again. A short document doesn't need a recap. A
long one may need a short summary at the top, not the bottom.

**Reflexive structure.** Bullets for things that aren't parallel, headings over two paragraphs,
bold scattered through sentences, ideas grouped in threes because three sounds complete, and "It's
not X, it's Y" where nobody suggested X. Use structure when the content has that shape.

**Inflated words.** "Leverage" or "utilize" for use, "facilitate" for help, and the all-purpose
"robust", "seamless", "comprehensive", "crucial", "delve", "a testament to". Orwell's rule: never
use a long word where a short one will do. Look for the precise verb and the concrete noun.

**Empty intensifiers.** "Very", "really", "quite", "actually", "truly", "incredibly". Dreyer
suggests going a week without them. The sentence is usually stronger without them. If it feels
weak, the fix is a stronger word or a fact.

**"Simply", "just" and "easily" in instructions.** Anyone reading your steps is someone for whom
it isn't simple yet, or they wouldn't be reading. These words tell them nothing and make them feel
slow when they get stuck.

**Salesmanship and sign-offs.** "Blazingly fast", "powerful", "I hope this helps!", "Let me know if
you have any questions!", "Happy coding!" Describe what the thing does, and stop when you're done.

**Abstraction where an example would teach.** Compare "The function handles various edge cases
gracefully" with "If the file is empty, `load()` returns an empty list instead of raising." Orwell
showed what happens when "the race is not to the swift" becomes "success or failure in competitive
activities". One concrete case teaches more than a paragraph of generalities.

**Defensive completeness.** Every caveat, edge case and alternative gets equal weight, so the one
thing the reader must know is buried among twenty they don't need. Decide what matters most and put
it first. Move the rest later, put it in another document, or cut it.

### Don't over-correct

These habits are problems only when they cost the reader. Passive voice is right when the actor
doesn't matter ("logs are rotated nightly"). Contractions suit nearly every document. A fragment
can give emphasis. Starting a sentence with "And" or "But" is good English, and Dreyer files the
rules against all of these under "nonrules". Warmth isn't a tic either. A one-line welcome in
an onboarding doc, or thanks to a reviewer, is fine when it's sincere and brief. What to cut is the
stock enthusiasm that could appear in any document. Deleting a tic and leaving the sentence around it
unchanged usually produces something stiff, so rewrite the sentence instead. And don't swap one
tic for another, such as turning every dash into a semicolon or every "crucial" into "key".

## Sentences

Orwell's six rules still cover most of it. Don't use figures of speech you're used to seeing in
print. Use the short word. Cut any word you can. Prefer active to passive. Use everyday words over
jargon. Break any of these rules sooner than write something awful.

A few more matter in technical writing:

- Make the actor the subject and the action the verb. "The implementation of caching was performed
  by the team" becomes "The team added caching". Nouns made from verbs ("implementation",
  "utilization", "configuration of") are where actions go to hide.
- Put familiar information early in the sentence and new information late. Readers expect the
  stress at the end, so put the important part there.
- Call one thing by one name. Varying the word is graceful in an essay. In documentation it makes
  readers wonder whether "the server", "the daemon" and "the service" are three different things.
- Read the sentence aloud, or as if aloud. Dreyer's test is whether a reader can follow it from
  beginning to end without doubling back.

## Technical and teaching documents

Most of what you write will be READMEs, tutorials, how-to guides, reference pages, explanations
and reports of work.

First, know which kind of document you're writing. The Diátaxis framework separates four kinds:

- A **tutorial** teaches a newcomer by having them do something.
- A **how-to guide** helps a competent user reach a specific goal.
- **Reference** describes the machinery for someone looking up a fact.
- An **explanation** helps someone understand why things are the way they are.

Each meets a different need, and a document that mixes them meets none of them well. A tutorial
that stops to list every option loses the learner. A reference page that tells the design history
is hard to scan. When you notice yourself switching modes, link to a different document instead.

Assume the reader knows nothing you haven't told them. Zinsser borrows this rule from journalism.
In practice it means including the step that seems too obvious to mention.

For anything a reader will follow:

- Say what they'll end up with, and what they need before they start.
- Number the steps: one action per step, in the order they're done.
- Make commands copy-pastable, with real paths and flags, no shell prompt mixed into the command,
  and placeholders that are obviously placeholders and are explained.
- After any step whose result isn't obvious, show what success looks like: the expected output,
  the page that loads, the file that appears.
- Put conditions before instructions: "If you're on macOS, run…" rather than "Run… if you're on
  macOS."

For anything that explains:

- Start concrete. Open with something the reader has seen or can run, then generalize. Zinsser
  describes it as an upside-down pyramid that starts from one narrow fact and widens.
- Introduce one new idea at a time, and give each a concrete example before moving on.
- Use realistic examples. `foo` and `bar` teach less than a plausible function name and plausible
  data.
- Say why as well as what. A reader who knows why a step exists can adapt when their situation
  differs.
- Keep an analogy to a single point. A long analogy makes the reader work out the mapping.

For reports of work (handoffs, PR descriptions, status updates, the summary at the end of a task),
lead with the conclusion. Give the evidence the reader needs to trust it, state any caveat that
would change what they do, and end with the next action. Write it for someone who wasn't there,
because almost always they weren't.

When you hand a document back in a conversation, the note around it is a report too, so keep it
short. Say what the person must do before using the document, such as filling in a placeholder or
checking an assumption, and what you couldn't verify. Don't list what you removed or changed unless
they asked. The document already shows that.

[references/doc-types.md](references/doc-types.md) has skeletons and common failures for each kind
of document. Read it when you're writing one of them and want more than the outline above.

## Revise

Writing is rewriting. Few first drafts are right, and a model's first drafts go wrong in
predictable ways. Before you hand anything over:

1. **Reread as the reader.** Set the conversation aside and read the page as the person you
   pictured would, knowing only what's on it. Notice where they would stop, frown or skip. Check
   every term you invented and every reference to something they haven't seen.
2. **Cut what isn't working.** Zinsser had his students bracket every word that wasn't doing work,
   and found that most first drafts could lose half their length. Look hardest at the first
   paragraph, which is often warm-up, the last, which is often a recap, and every hedge. When you
   cut, keep facts, decisions, caveats and next steps. Trim introductions, repetition, reassurance
   and optional background first. Clarity still matters more than brevity, so don't cut a step a
   learner needs.
3. **Check the shape.** Make sure the most important thing comes first, and that the lists and
   headings match the content rather than habit.
4. **Run the checker, if you can.** This skill includes `scripts/prose_check.py`, which needs only
   Python 3. Run `python3 <this skill's directory>/scripts/prose_check.py FILE`. It flags the
   habits above: filler phrases, hedge stacks, context leaks such as "as discussed", undefined
   acronyms, "simply" in steps, heavy formatting, recaps and repeated phrases. Treat each finding
   as a prompt to reread that sentence, not as an error. If the sentence still reads well, leave
   it. Never rewrite just to make a count go down. The checker can't tell whether you chose the
   right reader or left out a step, so a clean report doesn't mean the document is good.
5. **Try a cold read, if you can.** If you can give the document to a helper with fresh context,
   such as a subagent or a separate session, give it only the document and a description of the
   reader. Ask it to say in a few sentences what the document tells it to do or believe, and to
   list anything it couldn't follow. Where its answer differs from what you meant, the reader will
   struggle too. If you can't do this, do the same exercise yourself in step 1.

[references/revision.md](references/revision.md) has the full catalogue of habits, with
before-and-after examples and word lists. Read it while revising, especially when you're editing
someone else's draft or have been asked to make writing sound less machine-made.

## Examples

### A README opening

Before:

> # 🚀 SyncWave
>
> SyncWave is a powerful, blazingly fast, and robust tool that seamlessly synchronizes your files
> across multiple environments. Whether you're a developer, a data scientist, or a hobbyist,
> SyncWave has you covered!
>
> ## ✨ Features
>
> - ⚡ **Lightning fast**: Built for performance
> - 🔒 **Secure**: Your data stays safe
> - 🧩 **Extensible**: Plugin architecture

After:

> # syncwave
>
> syncwave copies a directory to one or more machines over SSH and keeps the copies in sync as
> files change. It sends only the changed blocks of each file, so after a small edit to a large
> repository a sync takes about a second.
>
> ```sh
> pip install syncwave
> syncwave ./project user@devbox:~/project
> ```
>
> It needs Python 3.10 or later and SSH access to each machine. Sync is one-way: changes made on
> a remote copy are overwritten.

The second version says what the tool does, what makes it different, how to try it, and its main
limit, in fewer words than the first spends on adjectives. In a real README each of those facts
comes from the code. If you can't check the "about a second", leave it out.

### A work report

Before:

> I've completed a thorough investigation of the issue. First, I looked at the logs, which showed
> some errors. Then I examined the retry logic and noticed that it might potentially not be
> handling certain edge cases correctly. After exploring several approaches, including Option A
> (increasing the timeout) and Option B, I implemented the fix we discussed. It's worth noting
> that this should hopefully resolve the problem in most cases. Let me know if you have any
> questions!

After:

> Uploads over 2 GB were failing because the retry loop restarted each upload from byte zero, so a
> large file never finished inside the 10-minute job limit. Retries now resume from the last
> confirmed chunk (`resume_from_offset` in `upload.py`). A 5 GB test upload that failed on three
> attempts out of three before the change now finishes in about four minutes.
>
> I haven't tested against the S3-compatible store in staging, which reports offsets differently.
> Someone should try one large upload there before we release.

The first version narrates the work, names an option the reader never saw, and hedges every claim.
The second gives the cause, the change, the evidence, the remaining risk and the next step.

### A tutorial step

Before:

> Next, simply configure your environment. Just set the necessary variables and you're good to go!

After:

> 3. Set your API key so the client can authenticate. Replace `sk-...` with the key from the
>    **API keys** page of your account:
>
>    ```sh
>    export ACME_API_KEY="sk-..."
>    ```
>
>    Check that it worked:
>
>    ```sh
>    acme whoami
>    ```
>
>    You should see your account's email address. If you see `401 Unauthorized`, the key was
>    probably copied incompletely, so copy it again.

## References

- [references/doc-types.md](references/doc-types.md): skeletons and common failures for READMEs,
  tutorials, how-to guides, reference, explanations, design docs, PR descriptions, commit messages,
  release notes and work reports.
- [references/revision.md](references/revision.md): the full catalogue of habits and the word lists
  for the revision pass.
- [references/sources.md](references/sources.md): the books and guides this skill draws on, for
  anyone who wants to read further.
