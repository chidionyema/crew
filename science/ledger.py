#!/usr/bin/env python3
"""Writer for the research ledger (crew#72 row 1).

One command an agent calls when a research pass ends. It refuses an entry that records reading
without a decision, has no source, or has no finding a reader can act on, and it appends the
entry in the shape `scripts/verify.d/80-research-ledger.sh`, `scripts/estate-snapshot` and the
warehouse source `research_ledger` already read. Nothing else writes the ledger by hand.

    python3 science/ledger.py add --question "..." --why "..." --decision-fed "..." \
        --source URL [--source URL] --finding "..." [--finding "..."] \
        --metric "..." --metric-before "..." [--metric-after "..."] [--what-this-costs "..."] \
        [--ticket URL] [--owner NAME]
    python3 science/ledger.py add --json entry.json        # the same fields as one object
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
LEDGER = ROOT / "science" / "RESEARCH-LEDGER.jsonl"
MIN_FINDING = 20


class Refused(ValueError):
    """The entry is not research the ledger accepts."""


def validate(e: dict) -> dict:
    """Return the entry the ledger accepts, or raise Refused naming the first rule broken."""
    for key in ("question", "why", "decision_fed", "metric", "metric_before"):
        if not str(e.get(key) or "").strip():
            raise Refused(f"{key} is empty: an entry with no {key} is a reading list, not research")
    sources = [s for s in (e.get("sources") or []) if str(s).strip()]
    if not sources:
        raise Refused("sources is empty: research with no trace did not happen")
    findings = [str(f).strip() for f in (e.get("findings") or [])]
    if not findings or any(len(f) < MIN_FINDING for f in findings):
        raise Refused(f"every finding is a statement of at least {MIN_FINDING} characters; a short one says nothing")
    out = dict(e)
    out["sources"], out["findings"] = sources, findings
    # crew#537 CP4: an idea row carries a forecast (probability) and, once known, an outcome (0/1);
    # docs/science/SHOWCASE.md grades the contract from these fields.
    if out.get("forecast") is not None:
        try:
            out["forecast"] = float(out["forecast"])
        except (TypeError, ValueError):
            raise Refused("forecast is not a number") from None
        if not 0 <= out["forecast"] <= 1:
            raise Refused("forecast is a probability between 0 and 1")
    if out.get("outcome") is not None:
        if str(out["outcome"]) not in ("0", "1"):
            raise Refused("outcome is 0 or 1: an idea either happened or it did not")
        if out.get("forecast") is None:
            raise Refused("an outcome without a forecast cannot be scored; record the forecast first")
        out["outcome"] = int(str(out["outcome"]))
    out.setdefault("date", dt.datetime.now(dt.UTC).strftime("%Y-%m-%d"))
    out.setdefault("owner", os.environ.get("CLAUDE_SESSION_ID", "unknown")[:16])
    out.setdefault("metric_after", None)
    out.setdefault("what_this_costs", "")
    out.setdefault("ticket", "")
    return out


def append(e: dict, ledger: pathlib.Path = LEDGER) -> dict:
    e = validate(e)
    with ledger.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(e, ensure_ascii=False) + "\n")
    return e


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add", help="append one validated entry")
    a.add_argument("--json", type=pathlib.Path, help="entry as one JSON object; flags override")
    for flag in ("question", "why", "decision-fed", "metric", "metric-before", "metric-after",
                 "what-this-costs", "ticket", "owner", "date", "kind", "forecast", "outcome"):
        a.add_argument(f"--{flag}")
    a.add_argument("--source", action="append", default=[])
    a.add_argument("--finding", action="append", default=[])
    a.add_argument("--ledger", type=pathlib.Path, default=LEDGER)
    args = ap.parse_args(argv)
    e = json.loads(args.json.read_text()) if args.json else {}
    for flag in ("question", "why", "decision_fed", "metric", "metric_before", "metric_after",
                 "what_this_costs", "ticket", "owner", "date", "kind", "forecast", "outcome"):
        v = getattr(args, flag)
        if v is not None:
            e[flag] = v
    if args.source:
        e["sources"] = list(e.get("sources") or []) + args.source
    if args.finding:
        e["findings"] = list(e.get("findings") or []) + args.finding
    try:
        out = append(e, args.ledger)
    except Refused as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    print(f"ok\tledger\t{out['date']} {out['question'][:70]} -> {out['decision_fed'][:60]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
