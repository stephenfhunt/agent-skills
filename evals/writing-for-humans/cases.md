# Eval cases: writing-for-humans

Five prompts, each with enough realistic material to tempt the habits the skill targets. Give
each prompt to the agent exactly as written, between the fences. The checker
(`skills/writing-for-humans/scripts/prose_check.py --json`) adds counts to the notes, but the
verdict comes from reading the outputs against the checklists.

## case: readme

Prompt:

````text
Write a README.md for this little tool. It's going on GitHub this week.

```python
#!/usr/bin/env python3
"""logslice: print the lines of a log file that fall inside a time window."""
import argparse, re, sys
from datetime import datetime, timedelta

TS = re.compile(r"^(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})")

def parse_when(s, now):
    m = re.fullmatch(r"(\d+)([smhd])", s)
    if m:
        n, unit = int(m.group(1)), m.group(2)
        return now - timedelta(**{{"s": "seconds", "m": "minutes", "h": "hours", "d": "days"}[unit]: n})
    return datetime.fromisoformat(s)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?", default="-")
    ap.add_argument("--since", help="ISO time or relative like 15m, 2h, 1d")
    ap.add_argument("--until", help="ISO time or relative")
    ap.add_argument("--keep-untimed", action="store_true",
                    help="keep lines without a timestamp (e.g. stack traces) if the previous timed line was kept")
    a = ap.parse_args()
    now = datetime.now()
    lo = parse_when(a.since, now) if a.since else datetime.min
    hi = parse_when(a.until, now) if a.until else datetime.max
    f = sys.stdin if a.file == "-" else open(a.file, errors="replace")
    keeping = False
    for line in f:
        m = TS.match(line)
        if m:
            t = datetime.fromisoformat(m.group(1).replace(" ", "T"))
            keeping = lo <= t <= hi
            if t > hi:
                break  # logs are in order; nothing later can match
        elif not a.keep_untimed:
            keeping = False
        if keeping:
            sys.stdout.write(line)

if __name__ == "__main__":
    main()
```

It's a single file, no dependencies, Python 3.9+. Installed with `pipx install logslice`.
MIT license.
````

Good output:

- The opening says what the tool does in plain words (print the log lines between two times),
  without "powerful" or "blazingly fast".
- A minimal example with real flags (`logslice app.log --since 15m`) comes early, ideally with a
  few lines of output.
- It explains `--keep-untimed` in terms of the problem it solves (stack traces have no
  timestamps).
- It states the assumptions the code makes: timestamps at the start of the line in ISO format,
  and a log in time order, since the tool stops at the first line past `--until`.
- It stays short and prose-led. Any table or list is for flags.

Watch for:

- An emoji heading, a bold-label feature list, a "Features" section that restates the flags.
- Marketing adjectives, "seamlessly", "effortlessly".
- Claims the code doesn't support (time zones, compressed files, speed figures).
- A "Contributing" section, badges, or a roadmap that nobody asked for.

## case: tutorial

Prompt:

````text
Using the same logslice tool (source below), write a short getting-started tutorial for
someone on our support team. They're comfortable opening a terminal but have never used
logslice and rarely use the command line otherwise. Goal: by the end they can pull out the
log lines from the 10 minutes around a customer-reported error.

Facts: install is `pipx install logslice` (pipx is already on support laptops). Our app logs
live in /var/log/acme/app.log on the support jump host, and lines look like:
2026-11-24 14:03:11 ERROR payment failed order=8812 code=card_declined
Stack traces follow ERROR lines and have no timestamp.

[same logslice source as the readme case]
````

(When running, paste the source from the readme case where the bracketed line is.)

Good output:

- Says up front what they'll be able to do and what they need.
- Numbered steps, one action each, with commands they can copy and the output they should see.
- A worked example with real-looking times: the customer saw an error at 14:03, so slice from
  13:58 to 14:08 using ISO times, with `--keep-untimed` so stack traces come along.
- Explains in a sentence why `--keep-untimed` matters for this case, and nothing more about the
  internals.
- Tells them what it looks like when it goes wrong (no output, because the time format or the
  date is wrong) and how to recover.

Watch for:

- "Simply", "just", "easily", "it's that simple".
- Steps that bundle several actions, or that assume knowledge (pipes, `less`, redirecting to a
  file) without showing it.
- A list of every flag, or digressions into how the tool works.
- No expected output anywhere.

## case: explain

Prompt:

````text
A new teammate, Sam, joined this week and will be on call next week. Explain how our HTTP client
retries failed requests, so they understand what they'll see in the logs when a downstream
service is struggling. Sam is a solid backend developer but hasn't seen this code.

```python
RETRYABLE = {429, 502, 503, 504}

def request_with_retry(session, method, url, *, max_attempts=5, base=0.2, cap=10.0, **kw):
    attempt = 0
    while True:
        attempt += 1
        try:
            resp = session.request(method, url, timeout=(3.05, 30), **kw)
        except (ConnectionError, Timeout) as e:
            if attempt >= max_attempts or method not in ("GET", "HEAD", "PUT", "DELETE"):
                raise
            log.warning("retry", extra={"url": url, "attempt": attempt, "reason": type(e).__name__})
        else:
            if resp.status_code not in RETRYABLE or attempt >= max_attempts:
                return resp
            log.warning("retry", extra={"url": url, "attempt": attempt, "reason": resp.status_code})
            ra = resp.headers.get("Retry-After")
            if ra and ra.isdigit():
                time.sleep(min(float(ra), cap))
                continue
        time.sleep(random.uniform(0, min(cap, base * 2 ** attempt)))
```
````

Good output:

- Starts concrete: what Sam will see in the logs when a service is struggling (a run of `retry`
  warnings with rising attempt numbers), then explains why.
- Covers what is retried and what isn't: 429, 502, 503 and 504 responses; connection errors and
  timeouts only for idempotent methods, so a POST that times out is never retried. It explains
  why that matters (no double charges).
- Explains the backoff with numbers (full jitter: a random wait up to 0.4 s, 0.8 s, 1.6 s… capped
  at 10 s), and that a numeric `Retry-After` overrides it.
- Says what happens after the fifth attempt: the last response is returned, or the exception is
  raised.
- Pitched to a competent developer: no explanation of what HTTP status codes are.

Watch for:

- Opening with an abstract definition of exponential backoff.
- Jargon ("full jitter", "idempotent") with no explanation.
- Line-by-line narration of the code instead of behaviour.
- Bullet-point fragments where the connections ("so", "because") matter.
- Missing the POST and idempotency point, which is the thing most likely to bite on call.
- Guessing Sam's pronouns from the name. The baseline wrote "I've written it to him directly".

## case: handoff

Prompt:

````text
I'm out tomorrow and Priya is picking this up. She wasn't in any of this. Write her a handoff
note. Here's my running log from today:

09:40 nightly export job (export-orders) failed again, 3rd night. error: "psycopg.errors.
QueryCanceled: canceling statement due to statement timeout"
09:55 thought it was the new index from Tues (ord_created_idx). dropped it on staging, reran
export on staging - still times out. so not the index. (call this theory A, dead)
10:30 theory B: table bloat. checked pg_stat_user_tables, orders n_dead_tup ~41M vs 60M live.
autovacuum last ran 9 days ago on orders?! vacuum blocked by something?
11:10 found it: a long-running txn from the analytics replica slot... no wait, that's logical
replication slot "bi_sync" — inactive since 11/15 when BI team paused their connector. Slot
holds xmin back so vacuum can't clean orders. that's the real root cause
11:25 confirmed w/ pg_replication_slots: bi_sync active=false, xmin age huge
11:40 pinged Marco (BI) in #data-platform — he says connector is paused until they migrate,
maybe 2 weeks, ok to drop slot as long as they get a heads up, they'll do a full resync
13:00 dropped slot on STAGING ONLY. ran VACUUM (VERBOSE) orders on staging, took 22 min, dead
tuples down to ~200k. export on staging now finishes in 6 min (was timing out at 30)
14:15 wrote change request CHG-2291 to drop the slot on prod + manual vacuum. needs approval
from Dana (DBA on call) - not approved yet. Marco said he'd post in #bi-announce before we drop
it, haven't seen it yet
15:00 also bumped statement_timeout for export role to 45min on prod as a stopgap (the
"timeout hack"), so tonight's run might pass anyway. should revert once vacuum is done
15:30 TODO: add alert on replication slot inactivity / xmin age so this doesn't happen again.
haven't started. also index from tues is still dropped on staging, need to recreate it
````

Good output:

- Opens with where things stand: the cause is known (an inactive replication slot, `bi_sync`,
  is stopping vacuum on `orders`), the fix is proven on staging, and production is waiting on
  CHG-2291.
- Gives the evidence briefly: the dead tuple counts, and the export going from timing out at
  30 minutes to finishing in 6 on staging.
- Lists what Priya needs to do, in order: get Dana's approval, confirm that Marco's notice is
  posted, drop the slot and vacuum on production, revert the 45-minute timeout, recreate
  `ord_created_idx` on staging, and add the alert.
- Explains the timeout stopgap in plain words and says it's temporary. Says tonight's run may
  pass because of it, so a passing run doesn't mean the problem is fixed.
- Names people by role as well as name (Dana, the on-call DBA; Marco on the BI team), and gives
  the channel names.

Watch for:

- "Theory A" or "theory B", "the timeout hack", or "as discussed" left in.
- A chronological replay of the day.
- Burying the open approval or the timeout revert.
- Hedges on things the log shows were confirmed, or confidence about tonight's run.
- Undefined jargon that Priya might not know, such as xmin. A short gloss is fine.
- A closing "Let me know if you have any questions" when the writer will be out.

## case: revise

Prompt:

````text
Can you tighten up this paragraph from our onboarding doc? Keep all the actual information.

"Welcome to the team! In today's fast-paced engineering environment, it's important to note
that our deployment process plays a crucial role in ensuring the reliability of our services.
Let's dive into how it works. Essentially, when you merge a pull request into main, our robust
CI pipeline will automatically run the full test suite, which typically takes approximately 12
minutes. If all tests pass, the changes are then seamlessly deployed to staging, where they
can be verified. It's worth mentioning that production deploys are not automatic — they
require a manual approval from a member of the on-call rotation, which can be requested in the
#deploys channel. Additionally, please note that deploys are frozen on Fridays after 2pm. In
summary, the process is designed to balance speed and safety, empowering engineers to ship
with confidence!"
````

Good output:

- Keeps every fact: merging to main triggers CI; the full test suite takes about 12 minutes;
  passing changes deploy to staging automatically for verification; production needs manual
  approval from someone on call; you ask in `#deploys`; no deploys on Fridays after 2pm.
- Comes out at roughly half the length or less, as plain sentences in a friendly, direct voice.
- Uses "you" and active voice where it helps ("Ask in #deploys for approval").

Watch for:

- Lost information, especially the Friday freeze or where to ask for approval.
- Over-correction: telegraphic fragments, a bullet list where the paragraph worked, or a stiff
  tone with all the warmth removed. Some welcome is fine in onboarding.
- New tics introduced in place of the old ones.
- A long covering note that lists every phrase removed, or a bullet list of judgment calls. One
  or two sentences on anything the user must decide is enough. (The first skill run did this.)
- Dropping the welcome. Over-correction treats warmth as a tic. (The first skill run did this.)
