#!/usr/bin/env python3
"""Grade the general-purpose research capability from its own ledger (crew#508).

Founder, 2026-08-27: "everything needs to be feeding the machine to have real intelligence,
how is our general purpose research capability". A capability that cannot say how many
questions it asked, how many of them fed a decision, and which ones went stale is not a
capability, it is a folder of notes. Every number here is counted from
science/RESEARCH-LEDGER.jsonl at generation time, and the page prints the command beside it.

    python3 science/research_grade.py           # write docs/science/RESEARCH-GRADE.md
    python3 science/research_grade.py --print   # write nothing, show the page
    python3 science/research_grade.py --check   # exit 1 when any question is stale (>7 days, no decision)

Paths are resolved from __file__ and printed repo-relative, never the checkout's absolute
path (crew#403, the pattern in science/showcase.py rel()).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import research_intake

SCIENCE = pathlib.Path(__file__).resolve().parent
CREW = SCIENCE.parent
LEDGER = SCIENCE / "RESEARCH-LEDGER.jsonl"
FORESIGHT_STATE = SCIENCE / "foresight-state.json"
FORESIGHT_BLOCKER = SCIENCE / "foresight-model.json"
PREDICTIONS = SCIENCE / "predictions.jsonl"
PAGE = CREW / "docs" / "science" / "RESEARCH-GRADE.md"
STALE_DAYS = 7


def rel(path) -> str:
    """A path as the page prints it: repo-relative, never this checkout's absolute path."""
    try:
        return str(pathlib.Path(path).resolve().relative_to(CREW))
    except ValueError:
        return str(path)


def read_ledger(path: pathlib.Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _day(row: dict, key: str) -> dt.date | None:
    raw = row.get(key)
    if not isinstance(raw, str) or not raw.strip():
        return None
    try:
        return dt.datetime.fromisoformat(raw.replace("Z", "+00:00")).date()
    except ValueError:
        return None


def _fed(row: dict) -> bool:
    """A question fed a decision when decision_fed carries text."""
    return isinstance(row.get("decision_fed"), str) and bool(row["decision_fed"].strip())


def grade(rows: list[dict], today: dt.date) -> dict:
    """Every field is counted, never estimated. Day-granular rows are reported as such."""
    fed = [r for r in rows if _fed(r)]
    open_rows = [r for r in rows if not _fed(r)]

    # question -> decision. Rows carrying explicit timestamps are measured to the hour; the rest
    # only record a day, so a same-day decision is 0h and the page says how many rows those are.
    hours, day_only = [], 0
    for r in fed:
        asked, decided = _day(r, "asked_at"), _day(r, "decided_at")
        if asked and decided:
            hours.append((decided - asked).total_seconds() / 3600)
            continue
        asked = _day(r, "date")
        decided = _day(r, "decided") or _day(r, "decision_date")
        if asked and decided:
            hours.append((decided - asked).days * 24.0)
        elif asked:
            hours.append(0.0)
            day_only += 1

    sources = [len(r.get("sources") or []) for r in rows]
    stale = []
    for r in open_rows:
        asked = _day(r, "date")
        if asked is None:
            continue
        age = (today - asked).days
        if age > STALE_DAYS:
            stale.append({"date": r["date"], "age_days": age, "ticket": r.get("ticket") or "-",
                          "owner": r.get("owner") or "-", "question": r.get("question") or "-"})
    stale.sort(key=lambda s: -s["age_days"])

    return {"questions": len(rows), "decisions_fed": len(fed), "open": len(open_rows),
            "fed_pct": round(100 * len(fed) / len(rows)) if rows else None,
            "median_hours_to_decision": round(statistics.median(hours), 1) if hours else None,
            "day_only_rows": day_only,
            "sources_total": sum(sources),
            "sources_median": round(statistics.median(sources), 1) if sources else None,
            "sources_min": min(sources) if sources else None,
            "sources_max": max(sources) if sources else None,
            "sourceless": sum(1 for n in sources if n == 0),
            "stale": stale}


def foresight_row() -> tuple[str, str]:
    """(verdict, evidence) for the foresight model, read from what it actually wrote."""
    if FORESIGHT_STATE.exists():
        s = json.load(FORESIGHT_STATE.open())
        return (f"TRAINED on {s.get('labelled_prs')} labelled PRs; holdout accuracy "
                f"{s.get('holdout_accuracy')} vs base rate {s.get('holdout_base_rate')} "
                f"({s.get('verdict')})", rel(FORESIGHT_STATE))
    if FORESIGHT_BLOCKER.exists():
        b = json.load(FORESIGHT_BLOCKER.open())
        if b.get("status") == "TRAINED":
            return (f"TRAINED on {b.get('rows_used')} labelled PRs; holdout accuracy "
                    f"{b.get('holdout_accuracy')} vs base rate {b.get('holdout_base_rate')} "
                    f"({b.get('verdict')})", rel(FORESIGHT_BLOCKER))
        return (f"UNTRAINED: {b.get('blocker') or b.get('open_blocker') or 'no reason recorded'}",
                rel(FORESIGHT_BLOCKER))
    return (f"UNTRAINED: neither {rel(FORESIGHT_STATE)} nor {rel(FORESIGHT_BLOCKER)} on disk; "
            "run `python3 science/foresight.py train`", "-")


def inward() -> dict:
    """What the estate knows about itself: the foresight model, and predictions it has scored."""
    verdict, evidence = foresight_row()
    trained = verdict.startswith("TRAINED")
    recorded = scored = hits = 0
    if PREDICTIONS.exists():
        latest: dict = {}
        for line in PREDICTIONS.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                latest[r["id"]] = r
        mine = [r for r in latest.values() if r.get("model") == "foresight"]
        recorded = len(mine)
        done = [r for r in mine if r.get("scored_at")]
        scored, hits = len(done), sum(1 for r in done if r.get("correct"))
    return {"verdict": verdict, "evidence": evidence, "trained": trained, "recorded": recorded,
            "scored": scored, "hits": hits,
            "hit_rate": round(100 * hits / scored) if scored else None}


def intake(now: dt.datetime | None = None) -> dict:
    """The scheduled outward intake (crew#508 CP8), graded by research_intake.grade."""
    now = now or dt.datetime.now(dt.UTC)
    sources = research_intake.watched() if research_intake.SOURCES.exists() else []
    state = json.loads(research_intake.STATE.read_text()) if research_intake.STATE.exists() else None
    return research_intake.grade(research_intake.read_rows(), state, sources, now)


def grades(g: dict, inw: dict, ink: dict | None = None) -> tuple[str, str]:
    """ELITE when the block answers its own question with numbers; GAP when it answers with a
    hole it can name; BLIND when its source is not on disk at all. Outward is also GAP when
    the intake is stale (>2 days since a pull) or a candidate release sits >7 days unanswered:
    research that stopped watching the world is research that fell behind (crew#508 CP8)."""
    ink = ink or {"fresh": True, "late": []}
    if not g["questions"]:
        out_g = "BLIND"
    elif g["stale"] or g["sourceless"] or not ink["fresh"] or ink["late"]:
        out_g = "GAP"
    else:
        out_g = "ELITE"
    if not inw["trained"] and inw["evidence"] == "-":
        in_g = "BLIND"
    elif not inw["trained"] or not inw["scored"]:
        in_g = "GAP"
    else:
        in_g = "ELITE"
    return out_g, in_g


def render(g: dict, ledger: pathlib.Path, today: dt.date) -> str:
    inw = inward()
    ink = intake()
    out_g, in_g = grades(g, inw, ink)
    med = "n/a" if g["median_hours_to_decision"] is None else f"{g['median_hours_to_decision']}h"
    L = rel(ledger)
    out = ["# Research capability, graded", ""]
    blind = [name for name, grade_ in (("Outward", out_g), ("Inward", in_g)) if grade_ == "BLIND"]
    if blind:
        out += [f"**BLIND: {', '.join(blind)} cannot see its source.** "
                "A block that cannot read its store prints this line and nothing it says below is a number.", ""]
    out += [
        f"Generated {today.isoformat()} by `python3 science/research_grade.py`. Two directions, "
        "graded separately (R37): **Outward** is what the estate learned from the world, "
        "**Inward** is what it learned about itself. Every row re-runs; no number is typed by hand.",
        "",
        "| Direction | Grade | One sentence |",
        "|---|---|---|",
        f"| Outward | **{out_g}** | {g['decisions_fed']} of {g['questions']} questions fed a "
        f"decision; {len(g['stale'])} stale, {g['sourceless']} with no source; intake "
        f"{'fresh' if ink['fresh'] else 'RED'}, {ink['candidates']} candidates ({len(ink['late'])} late). |",
        f"| Inward | **{in_g}** | foresight {'trained' if inw['trained'] else 'untrained'}; "
        f"{inw['scored']} of {inw['recorded']} predictions scored. |",
        "",
        "## Outward — questions answered from the world",
        "",
        f"Source: `{L}`.",
        "",
        "| What | Value | How it is counted |",
        "|---|---|---|",
        f"| Questions asked | {g['questions']} | rows in `{L}` |",
        f"| Decisions fed | {g['decisions_fed']} ({g['fed_pct']}%) | rows whose `decision_fed` carries text |",
        f"| Questions still open | {g['open']} | rows with no `decision_fed` |",
        f"| Median question to decision | {med} | `decided_at` - `asked_at`, else day granularity |",
        f"| Sources cited | {g['sources_total']} total, median {g['sources_median']} per question "
        f"(min {g['sources_min']}, max {g['sources_max']}) | `len(row['sources'])` |",
        f"| Questions with no source | {g['sourceless']} | `sources` empty |",
        "",
    ]
    if g["day_only_rows"]:
        out += [f"{g['day_only_rows']} of {g['decisions_fed']} fed rows record only a day, not a "
                "timestamp, so they count as 0h. The median is a floor, not a measurement, until "
                "the ledger carries `asked_at` and `decided_at`.", ""]
    out += [f"### Stale questions (>{STALE_DAYS} days, no decision fed)", ""]
    if not g["stale"]:
        out += [f"None. Every open question is under {STALE_DAYS} days old.", ""]
    else:
        out += ["| Age | Asked | Ticket | Owner | Question |", "|---|---|---|---|---|"]
        out += [f"| RED {s['age_days']}d | {s['date']} | {s['ticket']} | {s['owner']} | "
                f"{s['question'][:120]} |" for s in g["stale"]]
        out += ["", f"A red row is research that cost tokens and fed nothing. {len(g['stale'])} of "
                    f"{g['questions']} questions are in this state.", ""]
    out += [research_intake.render(ink, research_intake.read_rows()), ""]
    out += [
        "## Inward — what the estate knows about itself",
        "",
        "| What | Value | Evidence |",
        "|---|---|---|",
        f"| Foresight model | {inw['verdict']} | `{inw['evidence']}` |",
        f"| Predictions recorded | {inw['recorded']} | `{rel(PREDICTIONS)}`, `model == foresight` |",
        f"| Predictions scored | {inw['scored']} | rows carrying `scored_at` |",
        f"| Hit rate | {'n/a, nothing scored' if inw['hit_rate'] is None else str(inw['hit_rate']) + '%'} "
        f"| {inw['hits']} correct of {inw['scored']} scored |",
        "",
        "## Re-run this page", "",
        "```", "python3 science/research_grade.py --print   # the page, written nowhere",
        "python3 science/research_grade.py --check   # exit 1 when a question is stale", "```", ""]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ledger", type=pathlib.Path, default=LEDGER)
    ap.add_argument("--out", type=pathlib.Path, default=PAGE)
    ap.add_argument("--print", dest="show", action="store_true", help="write nothing, print the page")
    ap.add_argument("--check", action="store_true", help="exit 1 when any question is stale")
    ap.add_argument("--today", type=dt.date.fromisoformat, default=None,
                    help="grade as of this date (tests); default: now, UTC")
    args = ap.parse_args(argv)

    rows = read_ledger(args.ledger)
    if not rows:
        print(f"BLIND: no rows in {rel(args.ledger)}", file=sys.stderr)
        return 2
    today = args.today or dt.datetime.now(dt.UTC).date()
    g = grade(rows, today)
    page = render(g, args.ledger, today)
    if args.show:
        print(page)
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(page)
        print(f"{rel(args.out)}: {g['questions']} questions, {g['decisions_fed']} fed, "
              f"{len(g['stale'])} stale")
    if args.check and g["stale"]:
        print(f"STALE: {len(g['stale'])} question(s) over {STALE_DAYS} days with no decision",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
