#!/usr/bin/env python3
"""Flag prose habits that tend to cost readers.

A linter for prose, in the spirit of a code-smell report. It reads Markdown or
plain text, ignores code, and reports phrases and patterns worth a second look:
context leaks ("as discussed"), hedge stacks, undefined acronyms, "simply" in
instructions, throat-clearing, recaps, heavy formatting, repeated phrases and
long sentences. Phrase patterns live in patterns.tsv next to this script.

Findings are prompts to reread, not errors. The script cannot tell whether the
document has the right reader, the right order, or every step it needs.

Usage:
  prose_check.py [--json] [--ignore-quoted] [--limit N] FILE [FILE ...]
  prose_check.py - < draft.md

Needs only the Python 3 standard library. Always exits 0 unless it can't read
its input.
"""

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
PATTERNS_FILE = os.path.join(HERE, "patterns.tsv")

# Order in which categories are reported: reader-facing problems first.
CATEGORY_ORDER = [
    "context-leak", "narration", "undefined-acronym", "self-reference", "minimizer",
    "hedge-stack", "throat-clearing", "signpost", "recap", "contrastive",
    "significance", "vague-link", "chat-residue", "salesmanship",
    "politeness", "ai-vocabulary", "inflated", "transition", "intensifier",
    "redundancy", "buried-verb", "structure", "repetition", "long-sentence",
    "exclamation",
]

HEDGE_RE = re.compile(
    r"\b(may|might|could(?!n't| not)|possibly|potentially|perhaps|probably|"
    r"likely|arguably|presumably|somewhat|slightly|relatively|fairly|"
    r"generally|typically|usually|often|sometimes|largely|mostly|seemingly|"
    r"apparently|hopefully|in (some|many|most|certain) cases|"
    r"to (some|a certain) extent|in general|more or less|sort of|kind of|"
    r"a bit|seems? to|appears? to|tends? to)\b",
    re.I,
)

MINIMIZER_RE = re.compile(
    r"\b(simply|just(?! (before|after|now|then|as|like|happened|finished|started|"
    r"ran|run|in time|below|above|once|one|a few|enough))|easily|quickly|obviously|clearly|merely|trivially|"
    r"straightforward(ly)?|all you (need|have) to do|"
    r"(it'?s|it is) (easy|simple|that simple|that easy|trivial))\b",
    re.I,
)

IMPERATIVES = set("""
run install open set add create click type copy paste edit configure go use
enter select choose navigate replace change update download clone start stop
restart check make move save delete remove call import export build deploy
write define pass put press drag log sign visit point upload sync mount
""".split())

INSTRUCTION_HEADING_RE = re.compile(
    r"\b(install|setup|set up|getting started|quick ?start|steps?|how to|"
    r"tutorial|usage|configure|configuration|walkthrough)\b", re.I)

# Acronyms most technical readers know; not flagged when undefined.
KNOWN_ACRONYMS = set("""
API APIs URL URLs URI HTTP HTTPS JSON HTML CSS CLI SQL PDF CPU GPU RAM ROM OS
ID IDs UI UX SSH TLS SSL DNS IP TCP UDP USB AI LLM LLMs PR PRs CI CD README
TODO FAQ OK AM PM US UK EU YAML TOML CSV XML UTF ASCII UUID MB GB KB TB MIT
GPL BSD PNG JPG JPEG SVG GIF IDE SDK SDKs REST VM VMs RPC HTML5 JS TS NPM
AWS GCP DB IO CRUD PHP XSS CSRF SSO OAuth JWT HMAC SHA MD5 RSA AES CORS SMTP
FTP SFTP LAN WAN VPN CDN NULL EOF ETA FYI NB PS IE EG II III IV
NOTE WARNING IMPORTANT TIP CAUTION DANGER INFO ERROR DEBUG WARN FATAL TRACE
GET POST PUT PATCH DELETE HEAD OPTIONS TRUE FALSE AND OR NOT
UTC GMT DBA SRE QA HR CEO CTO ISO RFC SLA SLO MVP KPI
MUST NEVER ALWAYS ONLY SHOULD SHALL REQUIRED OPTIONAL RECOMMENDED DO DONT
""".split())

IRREGULAR_PARTICIPLES = set("""
built done made given taken written shown known seen found sent kept left held
put read thrown chosen broken spoken driven drawn hidden begun forgotten gotten
bound sold told paid led lost meant brought bought caught taught thought felt
heard understood stolen frozen torn worn sworn shaken proven split cut hit shut
spread cast set run won hung fed bred dealt
""".split())

PASSIVE_RE = re.compile(
    r"\b(am|is|are|was|were|be|been|being)\s+(\w+ly\s+)?(\w+ed|"
    + "|".join(sorted(IRREGULAR_PARTICIPLES)) + r")\b", re.I)

# Empty verbs that take almost any nominalisation ("perform an analysis of").
LIGHT_VERB_RE = re.compile(
    r"\b(perform|performs|performed|performing|conduct|conducts|conducted|"
    r"conducting|carry out|carries out|carried out|carrying out|"
    r"undertake|undertakes|undertook|undertaking)\s+(a|an|the)\s+"
    r"(\w+(tion|sion|ment|ance|ence|ysis))\b(\s+of\b)?", re.I)

# Common verbs, flagged only with nouns that hide a verb ("make a decision").
LIGHT_PAIR_RE = re.compile(
    r"\b(make|makes|made|making|give|gives|gave|giving|provide|provides|"
    r"provided|providing|take|takes|took|taking|reach|reached|come to|came to)"
    r"\s+(a|an|the)\s+(decision|choice|recommendation|suggestion|assumption|"
    r"determination|selection|comparison|explanation|description|"
    r"introduction|indication|confirmation|clarification|justification|"
    r"demonstration|modification|adjustment|improvement|investigation|"
    r"evaluation|assessment|examination|review|analysis)\b"
    r"(\s+(of|on|about|that)\b)?", re.I)

EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF☀-➿⭐⬆↔-⇿✅❌]")

STOPWORDS = set("""
a an the and or but if then else of to in on at by for with from as is are was
were be been being it its this that these those there here i you we they he she
him her them our your their my me us do does did doing have has had having not
no so than too very can will would should could may might must shall into out
up down over under about after before again further once all any both each few
more most other some such only own same just also what which who whom when where
why how because while until through during above below between off per via
""".split())

WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")


# ---------------------------------------------------------------- patterns

def load_patterns(path):
    patterns = []
    with open(path, encoding="utf-8") as f:
        for n, raw in enumerate(f, 1):
            line = raw.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) != 3:
                sys.exit(f"{path}:{n}: expected category<TAB>regex<TAB>reason")
            cat, rx, reason = parts
            try:
                patterns.append((cat, re.compile(rx, re.I | re.M), reason))
            except re.error as e:
                sys.exit(f"{path}:{n}: bad regex: {e}")
    return patterns


# ---------------------------------------------------------------- cleaning

def blank_keep_newlines(match):
    return re.sub(r"[^\n]", " ", match.group(0))


def clean_markdown(text, ignore_quoted):
    """Return lines with code, URLs and markup removed, line count preserved."""
    # Front matter.
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            text = re.sub(r"[^\n]", " ", text[:end + 4]) + text[end + 4:]
    # HTML comments.
    text = re.sub(r"<!--.*?-->", blank_keep_newlines, text, flags=re.S)

    out = []
    in_fence = None    # fence string of the code block we are inside
    prose_fences = []  # open ```markdown fences, whose contents are prose
    for line in text.split("\n"):
        fence = re.match(r"^\s*(```+|~~~+)\s*([\w+-]*)", line)
        if in_fence:
            if fence and fence.group(1)[0] == in_fence[0] and len(fence.group(1)) >= len(in_fence) \
                    and not fence.group(2):
                in_fence = None
            out.append("")
            continue
        if fence:
            mark, lang = fence.group(1), fence.group(2).lower()
            if (prose_fences and not lang and mark[0] == prose_fences[-1][0]
                    and len(mark) >= len(prose_fences[-1])):
                prose_fences.pop()
            elif lang in ("markdown", "md"):
                prose_fences.append(mark)
            else:
                in_fence = mark
            out.append("")
            continue
        if re.match(r"^( {4,}|\t)\S", line) and not re.match(r"^\s*([-*+]|\d+[.)])\s", line):
            # Indented code block, unless it is a nested list item. Indented
            # continuation of list items is kept (heuristic).
            if out and out[-1].strip() == "":
                out.append("")
                continue
        if ignore_quoted and re.match(r"^\s*>", line):
            out.append("")
            continue
        line = re.sub(r"``.+?``|`[^`]+`", "Code", line)
        line = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", line)
        line = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", line)
        line = re.sub(r"\[([^\]]+)\]\[[^\]]*\]", r"\1", line)
        line = re.sub(r"<https?://[^>]+>|https?://\S+", "link", line)
        line = re.sub(r"</?[A-Za-z][^>]*>", "", line)
        out.append(line)
    return out


def classify(line):
    if not line.strip():
        return "blank"
    if re.match(r"^\s*#{1,6}\s", line):
        return "heading"
    if re.match(r"^\s*\|", line):
        return "table"
    if re.match(r"^\s*([-*_]\s*){3,}$", line):
        return "rule"
    if re.match(r"^\s*>", line):
        return "quote"
    if re.match(r"^\s*\d+[.)]\s", line):
        return "numbered"
    if re.match(r"^\s*[-*+]\s", line):
        return "bullet"
    return "prose"


def strip_markers(line, kind):
    s = line
    if kind == "heading":
        s = re.sub(r"^\s*#{1,6}\s+", "", s)
    elif kind == "numbered":
        s = re.sub(r"^\s*\d+[.)]\s+", "", s)
    elif kind == "bullet":
        s = re.sub(r"^\s*[-*+]\s+", "", s)
    elif kind == "quote":
        s = re.sub(r"^\s*(>\s?)+", "", s)
    s = re.sub(r"\*\*|__", "", s)
    s = re.sub(r"(?<![\w*])[*_](?=\S)|(?<=\S)[*_](?![\w*])", "", s)
    return s.strip()


# ---------------------------------------------------------------- units

class Unit:
    """A paragraph, list item, heading or table row: text plus line mapping."""

    def __init__(self, kind, heading):
        self.kind = kind
        self.heading = heading  # nearest heading text above this unit
        self.text = ""
        self.spans = []  # (offset, line number)

    def add(self, text, lineno):
        if self.text:
            self.text += " "
        self.spans.append((len(self.text), lineno))
        self.text += text

    def line_at(self, offset):
        line = self.spans[0][1]
        for off, n in self.spans:
            if off <= offset:
                line = n
            else:
                break
        return line


def build_units(lines):
    units = []
    current = None
    heading = ""
    for i, raw in enumerate(lines, 1):
        kind = classify(raw)
        if kind in ("blank", "rule"):
            current = None
            continue
        text = strip_markers(raw, kind)
        if kind == "heading":
            heading = text
            u = Unit("heading", heading)
            u.add(text, i)
            units.append(u)
            current = None
            continue
        if kind == "table":
            if re.match(r"^\s*\|?[\s:|-]+\|?\s*$", raw):
                continue
            text = " ".join(c.strip() for c in raw.strip().strip("|").split("|"))
            u = Unit("table", heading)
            u.add(text, i)
            units.append(u)
            current = None
            continue
        if kind in ("bullet", "numbered"):
            current = Unit(kind, heading)
            current.depth = len(raw) - len(raw.lstrip())
            current.add(text, i)
            units.append(current)
            continue
        # prose or quote: continue the current paragraph or list item
        if current is not None and (current.kind == kind or
                                    current.kind in ("bullet", "numbered")):
            current.add(text, i)
        else:
            current = Unit(kind, heading)
            current.add(text, i)
            units.append(current)
    return units


SENT_SPLIT_RE = re.compile(r"(?<=[.!?])[\"')\]]*\s+(?=[\"'(\[]?[A-Z0-9])")
ABBREV_RE = re.compile(r"\b(e\.g\.|i\.e\.|etc\.|vs\.|cf\.|Dr\.|Mr\.|Ms\.|Mrs\.|No\.)", re.I)


def sentences(unit):
    """Yield (start offset, sentence text)."""
    protected = ABBREV_RE.sub(lambda m: m.group(0).replace(".", "\x00"), unit.text)
    start = 0
    for m in SENT_SPLIT_RE.finditer(protected):
        seg = unit.text[start:m.start()].strip()
        if seg:
            yield start, seg
        start = m.end()
    seg = unit.text[start:].strip()
    if seg:
        yield start, seg


def words(s):
    return WORD_RE.findall(s)


def syllables(word):
    w = word.lower().strip("'-")
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))


STEM_SUFFIXES = ("ibility", "ability", "ations", "ation", "ments", "ment", "ness",
                 "able", "ible", "ity", "ing", "ed", "es", "ly", "s", "e")


def stem(w):
    """Crude suffix stripping, enough to match reliable/reliability, fix/fixed."""
    w = w.lower().strip("'")
    if w.endswith("'s"):
        w = w[:-2]
    for suf in STEM_SUFFIXES:
        if w.endswith(suf) and len(w) - len(suf) >= 4 and not (suf == "s" and w.endswith("ss")):
            return w[: -len(suf)]
    return w


def content_words(s):
    return {stem(w) for w in words(s) if len(w) > 2 and w.lower() not in STOPWORDS}


# ---------------------------------------------------------------- checks

QUOTED_RE = re.compile(r"\"[^\"]*\"|“[^”]*”")


def check(text, patterns, ignore_quoted=False):
    lines = clean_markdown(text, ignore_quoted)
    units = build_units(lines)
    if ignore_quoted:
        # Done per unit, not per line, because quotes often span a line break.
        for u in units:
            u.text = QUOTED_RE.sub(lambda m: " " * len(m.group(0)), u.text)
    findings = []

    def add(cat, line, snippet, reason):
        findings.append({"category": cat, "line": line,
                         "text": snippet.strip()[:120], "reason": reason})

    text_units = [u for u in units if u.kind != "heading"]
    all_sents = []  # (unit, offset, sentence)
    for u in text_units:
        for off, s in sentences(u):
            all_sents.append((u, off, s))

    # Phrase patterns.
    for u in units:
        for cat, rx, reason in patterns:
            for m in rx.finditer(u.text):
                add(cat, u.line_at(m.start()), m.group(0), reason)

    # Minimizers in instructions.
    for u, off, s in all_sents:
        ws = [w.lower() for w in words(s)]
        while ws and ws[0] in ("simply", "just", "then", "now", "next", "first", "finally", "quickly", "easily"):
            ws = ws[1:]
        first = ws[0] if ws else ""
        in_steps = (u.kind == "numbered" or first in IMPERATIVES or
                    INSTRUCTION_HEADING_RE.search(u.heading or ""))
        if not in_steps:
            continue
        for m in MINIMIZER_RE.finditer(s):
            add("minimizer", u.line_at(off + m.start()), m.group(0),
                "minimizer in instructions; the reader who is stuck is the one reading")

    # Hedge stacks.
    for u, off, s in all_sents:
        hedges = sorted({m.group(0).lower() for m in HEDGE_RE.finditer(s)})
        n = len(words(s))
        if len(hedges) >= 3 or (len(hedges) >= 2 and n <= 25):
            add("hedge-stack", u.line_at(off), s,
                f"{len(hedges)} hedges ({', '.join(hedges)}); say what you know, "
                "and put one specific caveat where it applies")

    # Undefined acronyms: first use with no expansion nearby.
    full = " ".join(u.text for u in units)
    seen = set()
    for u in units:
        for m in re.finditer(r"\b([A-Z][A-Z0-9]{1,5})(s?)\b", u.text):
            acr = m.group(1)
            if re.match(r"-\d", u.text[m.end():m.end() + 2]):
                continue  # a ticket or change ID such as CHG-2291
            if u.text[m.end():m.end() + 1] == "." and re.match(r"\.[a-z]", u.text[m.end():m.end() + 3]):
                continue  # a filename such as README.md or SKILL.md
            if acr in seen or acr in KNOWN_ACRONYMS or acr.isdigit() or re.match(r"^[A-Z]\d+$", acr):
                continue
            seen.add(acr)
            defined = (re.search(r"\(\s*" + acr + r"s?\s*\)", full) or
                       re.search(r"\b" + acr + r"s?\s*\(\s*[a-z]", full, re.I) or
                       re.search(r"\b" + acr + r"s?\b,? (stands for|means|is short for|or )", full))
            if not defined:
                add("undefined-acronym", u.line_at(m.start()), acr,
                    "acronym with no expansion; spell it out on first use unless every reader knows it")

    # Light verb + nominalisation.
    for u in text_units:
        for m in list(LIGHT_VERB_RE.finditer(u.text)) + list(LIGHT_PAIR_RE.finditer(u.text)):
            add("buried-verb", u.line_at(m.start()), m.group(0),
                "action buried in a noun; use the verb")

    # Exclamation marks in prose.
    for u, off, s in all_sents:
        if s.rstrip().endswith("!"):
            add("exclamation", u.line_at(off), s,
                "exclamation mark; rarely right in technical writing")

    # Long sentences.
    lengths = [(len(words(s)), u, off, s) for u, off, s in all_sents
               if u.kind in ("prose", "bullet", "numbered", "quote")]
    for n, u, off, s in sorted(lengths, key=lambda t: -t[0])[:3]:
        if n > 40:
            add("long-sentence", u.line_at(off), s,
                f"{n} words; can the reader follow it without doubling back?")

    # Sentence openers.
    openers = Counter()
    opener_lines = defaultdict(list)
    for u, off, s in all_sents:
        w = words(s)
        if not w:
            continue
        first = w[0].lower()
        if first in ("the", "a", "an", "code", "link"):
            continue
        openers[first] += 1
        opener_lines[first].append(u.line_at(off))
    total_sents = len(all_sents)
    for word, count in openers.most_common(3):
        if total_sents >= 8 and count >= 4 and count / total_sents >= 0.2:
            add("repetition", opener_lines[word][0], word,
                f"{count} of {total_sents} sentences start with \"{word}\"; vary or merge them")

    # Repeated phrases (3- to 5-word n-grams with function words in them).
    grams = Counter()
    gram_line = {}
    for u, off, s in all_sents:
        toks = [w.lower() for w in words(s)]
        for n in (3, 4, 5):
            for i in range(len(toks) - n + 1):
                g = tuple(toks[i:i + n])
                if any(t in ("code", "link") for t in g):  # placeholders
                    continue
                stops = sum(t in STOPWORDS for t in g)
                if stops == 0 or stops == n:
                    continue
                if stops == 1 and g[0] in ("the", "a", "an"):
                    continue  # a noun phrase; using one name per thing is good

                grams[g] += 1
                gram_line.setdefault(g, u.line_at(off))
    reported = []
    for g, c in sorted(grams.items(), key=lambda kv: (-len(kv[0]), -kv[1])):
        need = 4 if len(g) == 3 else 3
        if c < need:
            continue
        phrase = " ".join(g)
        if any(phrase in r for r in reported):
            continue
        reported.append(phrase)
        add("repetition", gram_line[g], phrase,
            f"repeated {c} times; a pet phrase, or a term that is fine to repeat?")
        if len(reported) >= 5:
            break

    # Recaps: paragraphs that mostly repeat earlier ones.
    # Recaps. A paragraph that mostly repeats one earlier paragraph, or, in a
    # short document, a closing paragraph made of words already used. (In long
    # documents the vocabulary saturates, so the closing check would misfire.)
    body = [u for u in text_units if u.kind != "table"]
    paras = [u for u in body if u.kind in ("prose", "quote") and len(content_words(u.text)) >= 10]
    doc_words = sum(len(words(u.text)) for u in body)
    earlier = []
    seen_words = set()
    for u in body:
        cw = content_words(u.text)
        if u in paras and earlier:
            best = max(len(cw & prev) / len(cw) for prev in earlier)
            closing = (u is paras[-1] and len(paras) >= 3 and doc_words < 800
                       and len(cw & seen_words) / len(cw) >= 0.6)
            if best >= 0.6 or closing:
                share = max(best, len(cw & seen_words) / len(cw))
                add("recap", u.line_at(0), u.text[:80] + "…",
                    f"{share:.0%} of this paragraph's content words appeared earlier; "
                    "does it add anything new?")
        if len(cw) >= 5:
            earlier.append(cw)
        seen_words |= cw

    # Structure.
    metrics, struct = structure_metrics(lines, units, all_sents)
    for line, snippet, reason in struct:
        add("structure", line, snippet, reason)

    findings.sort(key=lambda f: (CATEGORY_ORDER.index(f["category"])
                                 if f["category"] in CATEGORY_ORDER else 99, f["line"]))
    return metrics, findings


def structure_metrics(lines, units, all_sents):
    out = []
    kinds = [classify(l) for l in lines]
    content = [k for k in kinds if k not in ("blank", "rule")]
    n_bullets = sum(k in ("bullet", "numbered") for k in content)
    headings = [u for u in units if u.kind == "heading"]
    prose_words = sum(len(words(u.text)) for u in units if u.kind != "heading")
    raw = "\n".join(lines)
    bold = len(re.findall(r"\*\*[^*\n]+\*\*|__[^_\n]+__", raw))
    dashes = raw.count("—") + len(re.findall(r"\s--\s", raw))
    n_sents = len(all_sents)
    sent_lens = [len(words(s)) for _, _, s in all_sents if words(s)]
    total_words = sum(sent_lens)
    syl = sum(syllables(w) for _, _, s in all_sents for w in words(s))
    grade = (0.39 * (total_words / max(1, len(sent_lens))) +
             11.8 * (syl / max(1, total_words)) - 15.59) if total_words else 0.0
    passive = sum(1 for _, _, s in all_sents if PASSIVE_RE.search(s))

    per100 = lambda x: 100.0 * x / max(1, prose_words)
    metrics = {
        "words": prose_words,
        "sentences": n_sents,
        "mean_sentence_words": round(total_words / max(1, len(sent_lens)), 1),
        "max_sentence_words": max(sent_lens) if sent_lens else 0,
        "reading_grade": round(grade, 1),
        "list_line_share": round(n_bullets / max(1, len(content)), 2),
        "headings": len(headings),
        "bold_spans": bold,
        "em_dashes_per_1000_words": round(1000.0 * dashes / max(1, prose_words), 1),
        "passive_sentence_share": round(passive / max(1, n_sents), 2),
    }

    if prose_words >= 150 and metrics["list_line_share"] > 0.5:
        out.append((1, f"{metrics['list_line_share']:.0%} of lines are list items",
                    "reads like a briefing; would some of these lists be clearer as paragraphs?"))
    if prose_words >= 100 and per100(len(headings)) > 1.5:
        out.append((1, f"{len(headings)} headings for {prose_words} words",
                    "many headings for the length; add one only where a reader would jump"))
    if prose_words >= 100 and per100(bold) > 2:
        out.append((1, f"{bold} bold spans for {prose_words} words",
                    "heavy bold; keep it for definitions and warnings"))
    if prose_words >= 200 and metrics["em_dashes_per_1000_words"] > 8:
        out.append((1, f"{metrics['em_dashes_per_1000_words']} em dashes per 1000 words",
                    "many dashes; a weak signal on its own, but check whether commas, "
                    "parentheses or full stops would read better"))
    if n_sents >= 10 and metrics["passive_sentence_share"] > 0.3:
        out.append((1, f"{metrics['passive_sentence_share']:.0%} of sentences look passive",
                    "lots of passive voice; fine where the actor doesn't matter, but "
                    "check who does what is clear"))

    # Short sections, emoji and title case in headings, nested lists, bold-label bullets.
    heading_lines = [(i + 1, l) for i, l in enumerate(lines) if classify(l) == "heading"]
    level = lambda l: len(re.match(r"^\s*(#+)", l).group(1))
    if len(heading_lines) >= 3:
        for idx, (ln, l) in enumerate(heading_lines):
            if level(l) == 1:
                continue
            nxt = heading_lines[idx + 1][0] if idx + 1 < len(heading_lines) else len(lines) + 1
            body = [lines[j - 1] for j in range(ln + 1, nxt)]
            n = sum(len(words(strip_markers(b, classify(b)))) for b in body
                    if classify(b) not in ("blank", "rule", "heading"))
            if 0 < n < 40 and nxt <= len(lines):
                out.append((ln, l.strip(), f"section of {n} words; does it need its own heading?"))
    for ln, l in heading_lines:
        if EMOJI_RE.search(l):
            out.append((ln, l.strip(), "emoji in heading"))
        text = strip_markers(l, "heading")
        ws = [w for w in words(text) if w.lower() not in STOPWORDS]
        if (len(ws) >= 3 and all(w[0].isupper() for w in ws) and not text.isupper()
                and level(l) > 1):
            out.append((ln, l.strip(), "Title Case heading; sentence case reads more naturally"))
    for i, l in enumerate(lines, 1):
        k = classify(l)
        if k in ("bullet", "numbered"):
            if EMOJI_RE.search(l[:12]):
                out.append((i, l.strip(), "emoji at start of list item"))
            if len(l) - len(l.lstrip()) >= 2 and re.match(r"^\s+([-*+]|\d+[.)])\s", l):
                out.append((i, l.strip(), "nested list; would sentences show the hierarchy better?"))
    label_bullets = [i for i, l in enumerate(lines, 1)
                     if re.match(r"^\s*([-*+]|\d+[.)])\s+(\*\*|__)[^*_]+(\*\*|__)\s*[:—–-]", l)]
    if len(label_bullets) >= 4:
        out.append((label_bullets[0], f"{len(label_bullets)} bold-label bullets",
                    "\"- **Label**: text\" pattern; a table or plain sentences may read better"))
    return metrics, out


# ---------------------------------------------------------------- output

def report_text(name, metrics, findings, limit):
    m = metrics
    print(f"{name}: {m['words']} words, {m['sentences']} sentences, "
          f"mean {m['mean_sentence_words']} words/sentence (max {m['max_sentence_words']}), "
          f"reading grade {m['reading_grade']}")
    print(f"  list lines {m['list_line_share']:.0%}, headings {m['headings']}, "
          f"bold {m['bold_spans']}, em dashes {m['em_dashes_per_1000_words']}/1000 words, "
          f"passive {m['passive_sentence_share']:.0%} of sentences")
    if not findings:
        print("  no findings")
        return
    by_cat = defaultdict(list)
    for f in findings:
        by_cat[f["category"]].append(f)
    for cat in sorted(by_cat, key=lambda c: CATEGORY_ORDER.index(c) if c in CATEGORY_ORDER else 99):
        items = by_cat[cat]
        print(f"\n{cat} ({len(items)})")
        for f in items[:limit]:
            print(f"  {f['line']}: {f['text']!r} - {f['reason']}")
        if len(items) > limit:
            print(f"  ... and {len(items) - limit} more")
    print()


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Flag prose habits that tend to cost readers. "
                    "Findings are prompts to reread, not errors.")
    ap.add_argument("files", nargs="+", help="Markdown or text files; - for stdin")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--ignore-quoted", action="store_true",
                    help="skip blockquotes and \"double-quoted\" text, e.g. when the "
                         "document quotes bad examples on purpose")
    ap.add_argument("--limit", type=int, default=12,
                    help="findings shown per category in text output (default 12)")
    ap.add_argument("--patterns", default=PATTERNS_FILE, help="pattern file to use")
    args = ap.parse_args(argv)

    patterns = load_patterns(args.patterns)
    results = []
    for path in args.files:
        try:
            text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
        except OSError as e:
            sys.exit(f"{path}: {e}")
        metrics, findings = check(text, patterns, args.ignore_quoted)
        results.append({"file": path, "metrics": metrics, "findings": findings})

    if args.json:
        json.dump(results if len(results) > 1 else results[0], sys.stdout, indent=2)
        print()
    else:
        for r in results:
            report_text(r["file"], r["metrics"], r["findings"], args.limit)


if __name__ == "__main__":
    main()
