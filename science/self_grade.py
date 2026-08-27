#!/usr/bin/env python3
"""Weekly self-grade of the research loop (LAW 35, crew#72 row 4).

Once a week the loop is graded on itself: how many ledger entries landed, how many fed a decision,
how many measured their metric afterwards. The grade is written back into the ledger as an entry,
so the grading is itself research with a decision and a source, and STATE.md's research row and
the warehouse read it like any other entry. Nothing here needs a person; the workflow
.github/workflows/self-grade.yml runs it on a schedule and lands the entry through a pull request.

    python3 science/self_grade.py            # print the grade, append the entry
    python3 science/self_grade.py --dry-run  # print only
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
LEDGER = ROOT / "science" / "RESEARCH-LEDGER.jsonl"
QUESTION = "Did the research loop improve this week? (LAW 35 weekly self-grade)"
WINDOW_DAYS = 7


def _rows(path: pathlib.Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _measured(r: dict) -> bool:
    after = str(r.get("metric_after") or "").strip()
    return bool(after) and after != str(r.get("metric_before") or "").strip()


def grade(rows: list[dict], now: dt.datetime) -> dict:
    """The week's counts and a verdict. A silent week is RED; a week with no decision fed is RED."""
    since = now - dt.timedelta(days=WINDOW_DAYS)
    week = [r for r in rows if r.get("question") != QUESTION
            and dt.datetime.fromisoformat(str(r["date"])[:10]).replace(tzinfo=dt.UTC) >= since]
    n, decided, measured = len(week), sum(1 for r in week if r.get("decision_fed")), sum(1 for r in week if _measured(r))
    prior = [r for r in rows if r.get("question") == QUESTION]
    verdict = "GREEN" if n and decided == n else "RED"
    return {"entries": n, "decided": decided, "measured": measured, "verdict": verdict,
            "prior": prior[-1]["metric_after"] if prior else "no earlier self-grade"}


def entry(g: dict, now: dt.datetime, owner: str) -> dict:
    metric_after = f"{g['entries']} entries, {g['decided']} fed a decision, {g['measured']} measured after"
    action = ("keep the cadence" if g["verdict"] == "GREEN"
              else "every entry this week names decision_fed before it lands; a silent week is the finding")
    return {
        "date": now.strftime("%Y-%m-%d"),
        "owner": owner,
        "question": QUESTION,
        "why": "LAW 35: once a week the loop is graded on itself. crew#72 row 4 found nothing did this.",
        "sources": ["science/RESEARCH-LEDGER.jsonl", "science/self_grade.py"],
        "findings": [f"Last {WINDOW_DAYS} days: {metric_after}.",
                     f"Verdict {g['verdict']}: GREEN needs at least one entry and every entry with a decision fed."],
        "decision_fed": f"{g['verdict']}: {action}",
        "metric": "research entries in the week that fed a decision",
        "metric_before": g["prior"],
        "metric_after": metric_after,
        "what_this_costs": "one scheduled run a week, one pull request",
        "ticket": "https://github.com/chidionyema/crew/issues/72",
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--ledger", type=pathlib.Path, default=LEDGER)
    ap.add_argument("--owner", default="self-grade.yml")
    a = ap.parse_args(argv)
    now = dt.datetime.now(dt.UTC)
    rows = _rows(a.ledger)
    g = grade(rows, now)
    e = entry(g, now, a.owner)
    print(f"{g['verdict']}\tself-grade\t{e['metric_after']} (prior: {g['prior']})")
    if not a.dry_run:
        with a.ledger.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(e, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
