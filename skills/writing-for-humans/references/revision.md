# The revision pass

This is the full catalogue of habits that make prose harder to read, arranged in the order of a
revision pass. Start with the reader and the shape of the document, because a perfectly polished
sentence in the wrong place is still in the wrong place. Leave words for last.

Each entry says what the habit is, why models tend to produce it, and what to do instead. The
reason matters: if you know why a habit appears, you'll recognise forms of it that this list
doesn't name.

One warning before the lists. These patterns are symptoms. The problem is always the cost to the
reader: time wasted, a point missed, trust lost. Wikipedia's editors, who keep a long catalogue of
signs of machine writing, ask people not to treat the signs themselves as the thing to fix, and
the same applies here. A sentence with "crucial" in it can be fine. A sentence with every listed
word removed can still be empty. Fix what the reader would trip over.

## 1. The reader

**Context leaks.** References to things only you have seen: "as discussed", "as mentioned
earlier", "the approach above", "the original issue", "Option B", "the second fix", "per your
request". *Why:* in your context window these all point at something real. *Instead:* say what you
mean in full ("the timeout change in `client.py`"), or cut the reference if the reader doesn't
need it.

**Coined labels.** Names you invented while working: "the fallback path", "the shim layer", "the
v2 flow", "Phase 3". *Why:* naming things helps you reason, and after you've used a name a few
times it feels established. *Instead:* use the name the codebase or the reader already uses. If a
new name really is needed, define it the first time it appears.

**Undefined terms and acronyms.** *Why:* you've read the project's internal vocabulary, so it
feels like common knowledge. *Instead:* spell an acronym out on first use unless your readers use
it daily (API, URL and JSON are fine for developers). Explain project-specific terms in a clause:
"the reaper (the background job that deletes expired sessions)".

**Skipped steps.** *Why:* the step is obvious to you, or you did it earlier in the session. *Instead:*
list every action from a clean start: directories, environment variables, installed tools, logins.

**Mismatched level.** The document explains what a for loop is, then assumes the reader knows
how the garbage collector works. *Why:* you're writing to an average reader rather than a specific
one. *Instead:* pick one specific reader and write for them all the way through.

## 2. Shape

**Burying the point.** The conclusion arrives in paragraph four, after background and method.
*Why:* that's the order in which you worked it out. *Instead:* put the result, answer or
recommendation in the first sentence or two, then support it.

**Narrating the process.** "First I examined… Then I noticed… After exploring several
options…". *Why:* your reasoning happened in time order, and recounting it feels like showing
your work. *Instead:* report what's true now and what the evidence is. Mention a dead end only if
the reader would otherwise try it.

**Defensive completeness.** Every edge case, caveat and alternative gets equal space. *Why:*
leaving something out feels risky, and models are rewarded for covering cases. *Instead:* rank by
what the reader needs. Keep the caveats that would change what they do, and cut, move or link the
rest.

**Recaps.** A final paragraph that restates the document, "In summary" sections, or a sentence at
the end of each section repeating it. *Why:* summarising helps you check you covered everything.
*Instead:* end when the content ends. If a long document needs a summary, put a short one at the
top.

**Warm-up openings.** A first paragraph about how important or complex the topic is. *Why:* it
gives you a run-up before the real content. *Instead:* delete the first paragraph and see whether
the document starts better without it. It often does.

**Unearned endings.** A closing line that offers more help, wishes the reader well, or reaches for
significance ("This change lays the groundwork for future improvements"). *Instead:* stop after
the last useful sentence. In a report, that's usually the next action.

## 3. Formatting

**Bullet walls.** Content that has reasons, conditions or sequence, chopped into fragments. *Why:*
lists look organised and are easy to generate one item at a time. *Instead:* write a paragraph
whenever the items connect to each other. Keep lists for items that really are parallel,
sequential or meant to be compared.

**Bold-label bullets.** "- **Speed**: It's fast." repeated down the page. *Instead:* if the labels
carry information, use a table or a definition list. If they don't, write sentences.

**Header inflation.** A heading over every two paragraphs, or headings in a document short enough
to read in a minute. *Instead:* add headings only where a reader would want to jump to that part.
Use sentence case ("Set up the database"), not Title Case.

**Scattered bold.** Bold on phrases throughout a paragraph. *Instead:* bold a term where you define
it, or a warning that must not be missed.

**Emoji in headings and lists.** *Instead:* leave them out of technical documents unless the
project's existing docs use them.

**Punctuation tics.** Many em dashes, and "The result? A faster build." style colon or
question-mark reveals. Newer models have been tuned away from em dashes, and some now overcorrect
into strings of short, choppy sentences, which is just as recognisable. *Instead:* vary sentence
length according to the content, and use whichever punctuation a careful human writer would.

## 4. Sentences

**Hedge stacks.** "This might potentially help to somewhat reduce latency in some cases." *Why:*
each qualifier protects against being wrong. *Instead:* decide what you actually know. State it
plainly and add one specific caveat where it applies: "This cut p95 latency from 840 ms to 310 ms
on the staging load test. I haven't measured production."

**Throat-clearing.** "It's worth noting that", "It's important to remember", "Interestingly,",
"Importantly,", "Needless to say", "Please note". *Instead:* delete the phrase and start the
sentence at its real subject.

**Signposting.** "Let's dive in", "Let's break this down", "In this section, we'll explore",
"Here's a breakdown". *Instead:* deliver the content. Headings already tell the reader where they
are.

**Unprompted contrast.** "It's not just a cache, it's a consistency layer." "This isn't about
speed. It's about reliability." "X, not Y" where nobody suggested Y. *Why:* it creates a feeling
of insight with no new information. *Instead:* state the positive claim. Keep a contrast only when
the reader really holds the mistaken view, and then name it as a misconception.

**Triads.** "Fast, reliable, and scalable." "Clarity, consistency, and confidence." *Why:* three
items sound complete. *Instead:* list as many items as are true, and support each one.

**Avoiding "is".** "Serves as", "stands as", "functions as", "acts as", "represents". *Instead:*
use "is" when you mean "is".

**Inflated significance.** "Plays a crucial role in", "is a testament to", "underscores the
importance of", "marks a pivotal shift", "in the ever-evolving landscape of". *Why:* models drift
toward language that sounds important in any context. *Instead:* say what the thing does and let
the reader judge how much it matters.

**Participle tails.** Sentences ending in an "-ing" clause that adds commentary: "…, highlighting
the need for better tests", "…, ensuring a seamless experience". *Instead:* cut the tail, or make
it a separate claim with support.

**Vague connection.** "X is closely connected to Y", "associated with", "in connection with". *Why:*
it feels like a claim while committing to nothing. *Instead:* name the relationship: X calls Y, X
replaced Y, X depends on Y.

**Buried verbs.** "Perform an installation of", "make a decision", "provide an explanation of",
"the implementation of caching was carried out". *Instead:* use the verb: install, decide,
explain, "we added caching".

**Elegant variation.** Calling one thing "the server", then "the backend", then "the service".
*Instead:* in technical writing, one thing has one name.

**Unanchored claims.** "This approach is more maintainable." *Instead:* show the evidence (an
example, a number, a comparison) or drop the claim.

## 5. Words

These lists are prompts to look again, not a ban list. One hit is often fine. A cluster of them in
a few paragraphs is a sign that the prose has gone generic.

**Long word → short word.** (Orwell and Zinsser)

| Instead of | Try |
| --- | --- |
| utilize, leverage, make use of | use |
| facilitate | help, let, make easier |
| commence, initiate | start |
| endeavor, attempt | try |
| numerous, a large number of | many |
| sufficient | enough |
| assistance | help |
| additional(ly) | more, also |
| approximately | about |
| demonstrate | show |
| prior to | before |
| subsequent(ly) | later, after |
| in order to | to |
| due to the fact that | because |
| at this point in time, currently | now (or nothing) |
| in the event that | if |
| for the purpose of | to, for |
| with regard to, with respect to | about, on |
| the vast majority of | most |
| is able to, has the ability to | can |
| methodology | method |
| individuals | people |

**Vocabulary that has drifted to generic.** delve, tapestry, testament, multifaceted, intricate,
meticulous, pivotal, showcase, underscore (as a verb), bolster, garner, foster, boast (meaning
"has"), vibrant, seamless, robust, holistic, synergy, paradigm, landscape (meaning a field),
realm, journey (for a process), empower, elevate, streamline, embark, unlock (potential),
cutting-edge, game-changer, crucial, comprehensive, nuanced. Wikipedia's editors note that the
list changes from one model generation to the next. Words like "delve" faded once people mocked
them, and newer models lean on "practical", "clearer", "steady", "quietly", "matters" and
"multifaceted". So don't swap one word for its near synonym. Ask whether the sentence says
something specific.

**Empty intensifiers.** (Dreyer) very, really, quite, rather, actually, truly, incredibly,
extremely, literally, basically, essentially, definitely, pretty (as in "pretty good"), surely,
of course.

**Minimisers in instructions.** simply, just, easily, quickly, obviously, clearly, merely,
straightforward, "all you need to do is", "it's easy". (Google's developer style guide makes the
same rule.)

**Redundant pairs.** (Dreyer's "trimmables") end result, final outcome, future plans, past
history, advance planning, added bonus, free gift, close proximity, each and every, first and
foremost, basic fundamentals, combine together, join together, repeat again, revert back, return
back, continue on, still remains, exact same, general consensus, new innovation, unexpected
surprise, true fact, PIN number, ATM machine, may possibly.

**Transitions as filler.** Additionally, Furthermore, Moreover, Ultimately, That said, At the end
of the day. Usually the sentence connects fine without them. If it doesn't, the fix is to reorder
the ideas, not to add a connector.

## 6. Tone

**Salesmanship.** powerful, blazing(ly) fast, lightning-fast, effortless, world-class,
best-in-class, next-generation, revolutionary, supercharge, "has you covered", "look no further",
"take it to the next level", "Whether you're a beginner or an expert…". *Instead:* describe what
it does, and give numbers where speed or scale matters.

**Chat residue.** "Certainly!", "Great question", "You're absolutely right", "I hope this helps",
"Let me know if you have any questions", "Feel free to reach out", "Happy coding!", "Would you like
me to…". *Why:* these come from conversational training and leak into documents. *Instead:* leave
them out of documents entirely. In a conversation, offer a specific next step only if there is one.

**Over-politeness in instructions.** "Please click Save." *Instead:* "Click **Save**."

**Exclamation marks.** Rarely right in technical writing. Let the content carry the energy.

**Self-reference.** "As an AI…", "Based on my training data…", "I don't have access to…" in a
document meant for someone else. *Instead:* state the limit concretely if it matters to the reader
("I couldn't check the production logs"), and otherwise leave it out.

## 7. Check you didn't over-correct

After a pass like this, reread for damage.

- **Stiffness.** A sentence with its tic removed but its structure unchanged. Rewrite the whole
  sentence.
- **Lost information.** A cut that took a fact, a condition or a caveat the reader needed.
- **Choppiness.** Every sentence short, every connector gone. Ideas that depend on each other
  belong in one sentence or one paragraph.
- **Swapped tics.** Semicolons wherever the dashes were, "key" wherever "crucial" was, a colon
  reveal where the contrast used to be.
- **Rules that aren't rules.** Passive voice, contractions, fragments, a sentence that starts with
  "And" or "But", and a preposition at the end of a sentence are all fine when they serve the
  reader.

## Before and after

A paragraph from a handoff note:

> I've made significant progress on the authentication issue. After a thorough investigation, it
> appears that the problem might be related to token expiration. As discussed, I explored a few
> different approaches—Option A seemed promising but had some drawbacks. Ultimately, I implemented
> a robust solution that should seamlessly handle the edge cases. It's worth noting that further
> testing may be needed. Let me know if you have any questions!

Revised:

> Users were being logged out after an hour because the refresh job used the access token's
> expiry (60 minutes) instead of the refresh token's (30 days). I changed it to read
> `refresh_expires_at` (`auth/refresh.py`, line 42) and added a test that fast-forwards the clock
> past 60 minutes. I haven't tested it with SSO accounts, which issue their own tokens.

The revision drops the narration, the reference to "Option A", the hedges and the sign-off. It
adds what the first version never said: the cause, the change, the evidence and the one gap that
remains.
