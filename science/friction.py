#!/usr/bin/env python3
"""What the founder has had to say twice, measured over every transcript on this machine.

WHY THIS EXISTS. Founder, 2026-08-24: "in tired of repearting instructino that are
fucking autibantabkle and enforcable yet dday by fucjig day you all hav the transrcpi
fron alsession i hate repeatig bnyself". That is a falsifiable claim about a dataset that
has been sitting on this disk the whole time -- 75,138 transcript files, 4.5 GB -- and
nobody has ever counted it. Counting it is the first thing a data science function owes
the person paying for it.

WHAT WAS ALREADY THERE, AND WHAT WAS MISSING. founder_board.collect_founder_friction()
already reads transcripts and separates the founder's own words from machinery wearing
his role, and friction-relay.py already carries the last six hours of them into every new
session. Both are good and neither is re-implemented here; this imports their parsers.
What neither does is COUNT. The relay makes today's complaint visible to six sessions.
It cannot tell anyone that the same complaint was made on four previous days, because
its window is six hours wide and it keeps no history.

So the gap is not detection and it is not delivery. It is that nothing has ever measured
whether a complaint STOPS. An instruction he has repeated on five separate days is not a
mood, it is a missing guard, and the repeat count is how you find which guard to write.

REPORT MODE ONLY. This reads and prints. It writes no ledger of his words -- the
transcripts are the source and a second copy of them would be exactly the thing LAW 30
forbids.

    python3 science/friction.py                 # every day held on disk
    python3 science/friction.py --days 14       # a window
    python3 science/friction.py --json          # for a reader that is not a person

WHAT IT WILL GET WRONG, SAID HERE RATHER THAN DISCOVERED LATER. Repeats are found by
matching phrases, and he types fast and does not correct typos: "instructino",
"autibantabkle", "fucjig" all appear in one message. A phrase spelled two ways counts as
two phrases, so every number below UNDER-reports the repetition. That is the safe
direction for a number that accuses, and it means the real figure is worse than the one
printed.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone

#: The parsers live with the board, and they stay there. Importing them costs one path
#: entry and buys the one thing that actually matters: when the founder's message format
#: changes, it changes in one place and both readers follow it.
SCRIPTS = os.path.expanduser("~/.claude/scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)
try:
    from founder_board import FRICTION, _founder_messages, _walk_transcripts
except ImportError as exc:                                   # pragma: no cover
    sys.exit(f"cannot import the founder-message parsers from {SCRIPTS}/founder_board.py: {exc}\n"
             f"This deliberately has no fallback copy of them. A second parser would drift.")

#: Words that carry no topic. Kept short on purpose: an aggressive stop list is a way of
#: deciding the answer before measuring it.
STOP = set("""a an and are as at be been but by can cant do does doesnt dont for from get
have has had i if in is it its just like me my no not of on or our so than that the their
them then there these they this to too us was we were what when why will with you your
im ive ill youre thats dont wont ok okay now here need needs will would should could""".split())

WORD = re.compile(r"[a-z']+")


def normalise(text: str) -> list[str]:
    """A complaint reduced to its content words, lowercased, punctuation gone."""
    return [w for w in WORD.findall(text.lower()) if w not in STOP and len(w) > 2]


def phrases(words: list[str], lo: int = 2, hi: int = 5) -> set[str]:
    """Every contiguous run of `lo`..`hi` content words, as a set.

    A set, not a list: a phrase said three times inside one long message is one person
    making one point, and counting it three times would manufacture the finding.
    """
    out = set()
    for n in range(lo, hi + 1):
        for i in range(len(words) - n + 1):
            out.add(" ".join(words[i:i + n]))
    return out


def day_of(epoch: float) -> str:
    return datetime.fromtimestamp(epoch, timezone.utc).strftime("%Y-%m-%d")


def collect(max_age_s: float) -> list[dict]:
    """Every message the founder typed inside the window that reads as friction.

    The whole corpus, not the newest 80 files. That bound is right for a page that has to
    render in a second and wrong for a question about whether something recurs.
    """
    now = time.time()
    out, scanned = [], 0
    for path, mtime in _walk_transcripts():
        if now - mtime > max_age_s:
            continue
        scanned += 1
        session = os.path.basename(os.path.dirname(path))[-12:]
        for ts, text in _founder_messages(path):
            if not ts or now - ts > max_age_s:
                continue
            low = text.lower()
            if any(w in low for w in FRICTION):
                out.append({"at": ts, "day": day_of(ts), "session": session,
                            "text": " ".join(text.split())})
    out.sort(key=lambda r: r["at"])
    #: The same message can be read out of two transcript files when a session is resumed
    #: or forked. Deduplicate on the exact words and the second, or every fork inflates
    #: the repeat count and the whole report becomes a story about file copies.
    seen, deduped = set(), []
    for r in out:
        key = (round(r["at"]), r["text"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(r)
    return deduped, scanned


def recurring(rows: list[dict], min_days: int = 2, min_hits: int = 3) -> list[dict]:
    """Phrases he has used on more than one day, ranked by how many days they span.

    Days, not hits, is the ranking. Ten complaints in one bad afternoon is one bad
    afternoon. The same words on five separate days is something the estate is doing to
    him repeatedly, and only the second kind is a missing guard.
    """
    days_of: dict[str, set[str]] = defaultdict(set)
    hits: Counter[str] = Counter()
    first: dict[str, float] = {}
    last: dict[str, float] = {}
    for r in rows:
        for p in phrases(normalise(r["text"])):
            days_of[p].add(r["day"])
            hits[p] += 1
            first.setdefault(p, r["at"])
            last[p] = r["at"]

    kept = [{"phrase": p, "days": len(d), "hits": hits[p],
             "first": day_of(first[p]), "last": day_of(last[p])}
            for p, d in days_of.items() if len(d) >= min_days and hits[p] >= min_hits]

    #: A phrase whose every occurrence sits inside a longer kept phrase says nothing the
    #: longer one does not, and printing both is how a report of 40 findings becomes a
    #: report of 4,000 that nobody reads.
    kept.sort(key=lambda k: (-len(k["phrase"]), -k["days"]))
    survivors: list[dict] = []
    for k in kept:
        if any(k["phrase"] in s["phrase"] and k["hits"] <= s["hits"] for s in survivors):
            continue
        survivors.append(k)
    survivors.sort(key=lambda k: (-k["days"], -k["hits"]))
    return survivors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=float, default=3650,
                    help="window in days; the default is everything on disk")
    ap.add_argument("--json", action="store_true", help="machine output")
    ap.add_argument("--min-days", type=int, default=2,
                    help="a phrase must appear on at least this many separate days")
    args = ap.parse_args()

    started = time.time()
    rows, scanned = collect(args.days * 86400)
    rep = recurring(rows, min_days=args.min_days)
    days = sorted({r["day"] for r in rows})

    if args.json:
        print(json.dumps({"scanned_transcripts": scanned, "complaints": len(rows),
                          "days_with_a_complaint": len(days),
                          "first_day": days[0] if days else None,
                          "last_day": days[-1] if days else None,
                          "recurring": rep, "took_s": round(time.time() - started, 1)},
                         indent=2))
        return 0

    print(f"transcripts scanned      : {scanned}")
    print(f"complaints found         : {len(rows)}")
    if not rows:
        print("nothing in his own words reads as friction in this window.")
        return 0
    print(f"days with a complaint    : {len(days)}  ({days[0]} to {days[-1]})")
    print(f"complaints per such day  : {len(rows) / len(days):.1f}")
    print(f"took                     : {time.time() - started:.1f}s")

    per_day = Counter(r["day"] for r in rows)
    print("\nby day, most recent last")
    for d in days[-14:]:
        print(f"  {d}  {per_day[d]:>3}  {'#' * min(per_day[d], 60)}")

    print(f"\nsaid on more than one day, ranked by how many days he had to say it")
    if not rep:
        print("  nothing recurs across days in this window.")
    for k in rep[:25]:
        print(f"  {k['days']:>2} days, {k['hits']:>3}x  {k['first']}..{k['last']}  \"{k['phrase']}\"")
    return 0


if __name__ == "__main__":
    sys.exit(main())
