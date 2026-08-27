#!/usr/bin/env python3
"""Velocity per lane, measured from the board, never felt (crew#527 CP1).

    python3 science/velocity.py                  # one line per lane, and one row per lane per day appended
    python3 science/velocity.py --check          # exit 1 when a lane is red; the line names it
    python3 science/velocity.py --days 7 --json

A lane is a `lane:*` label on chidionyema/crew (crew#527). For each lane over the window:
opened, closed, open now, half-done (some checklist boxes ticked, some open), boxes ticked
now, median age of the open issues in days. A lane is red when three daily rows in a row
show the open count not falling and the ticked count not rising: work arriving, nothing
finishing. Rows land in science/velocity.jsonl once per lane per UTC day (a rerun is a no-op),
which is what the crew#508 science page charts. Issues without a lane label are counted as
`lane:unsorted` so the total is the board's total.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from itertools import pairwise
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dora import _gh, _ts  # the one GitHub reader, pages followed to the end

REPO = os.environ.get("BOARD_REPO", "chidionyema/crew")
OUT = Path(os.environ.get("VELOCITY_JSONL") or Path(__file__).resolve().parent / "velocity.jsonl")
BOARD = Path(os.environ.get("VELOCITY_BOARD_MD") or OUT.parent / "BOARD.md")
# the one picker (claude-guards estate_board.py); the path is the scripts dir, never a machine
ESTATE_BOARD = Path(os.environ.get("ESTATE_BOARD") or Path.home() / ".claude" / "scripts" / "estate_board.py")
BOARD_TOP = 60
UNSORTED = "lane:unsorted"
RED_DAYS = 3


def lane_of(issue: dict) -> str:
    names = [lab if isinstance(lab, str) else lab.get("name", "") for lab in issue.get("labels", [])]
    return next((n for n in names if n.startswith("lane:")), UNSORTED)


def boxes(body: str | None) -> tuple[int, int]:
    b = body or ""
    return len(re.findall(r"- \[x\]", b, re.I)), len(re.findall(r"- \[ \]", b))


def lane_velocity(issues: list[dict], now: datetime, days: int) -> dict[str, dict]:
    """Per-lane counts from issue rows {labels, createdAt, closedAt, state, body}. Pure."""
    since = now - timedelta(days=days)
    out: dict[str, dict] = {}
    ages: dict[str, list[float]] = {}
    for i in issues:
        lane = lane_of(i)
        r = out.setdefault(lane, {"opened": 0, "closed": 0, "open": 0, "half_done": 0, "ticked": 0, "no_checklist": 0})
        ages.setdefault(lane, [])
        if _ts(i["createdAt"]) >= since:
            r["opened"] += 1
        if i.get("closedAt") and _ts(i["closedAt"]) >= since:
            r["closed"] += 1
        if i.get("state", "open").lower() == "open":
            r["open"] += 1
            ages[lane].append((now - _ts(i["createdAt"])).total_seconds() / 86400)
            t, u = boxes(i.get("body"))
            r["ticked"] += t
            if t and u:
                r["half_done"] += 1
            if not t and not u:
                r["no_checklist"] += 1
    for lane, r in out.items():
        r["median_age_d"] = round(statistics.median(ages[lane]), 1) if ages[lane] else 0.0
    return dict(sorted(out.items()))


def red_lanes(rows: list[dict], red_days: int = RED_DAYS) -> list[str]:
    """Lanes whose last `red_days` daily rows show open not falling and ticked not rising."""
    by: dict[str, list[dict]] = {}
    for r in sorted(rows, key=lambda r: r["day"]):
        by.setdefault(r["lane"], []).append(r)
    red = []
    for lane, hist in by.items():
        h = hist[-red_days:]
        if len(h) < red_days:
            continue
        stuck = all(b["open"] >= a["open"] and b["ticked"] <= a["ticked"] for a, b in pairwise(h))
        if stuck and h[-1]["open"]:
            red.append(lane)
    return red


def read_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def append_rows(path: Path, day: str, per_lane: dict[str, dict], at: str) -> int:
    """One row per lane per day; a lane already written for `day` is skipped."""
    have = {(r["day"], r["lane"]) for r in read_rows(path)}
    n = 0
    with path.open("a") as f:
        for lane, r in per_lane.items():
            if (day, lane) in have:
                continue
            f.write(json.dumps({"at": at, "day": day, "lane": lane, **r}, sort_keys=True) + "\n")
            n += 1
    return n


def write_board(path: Path, picker: Path, at: str, top: int = BOARD_TOP) -> bool:
    """Regenerate science/BOARD.md from the one picker's finish-first rank (crew#527 CP2).

    Returns False, and writes a BLIND page, when the picker is missing or cannot read the board;
    the page is never left stale-but-green."""
    head = ["# Board rank, finish-first", "",
            f"Regenerated {at} by science/velocity.py from `estate_board.py rank --top {top}`.",
            "Order: fraction of checklist boxes ticked, then P0 before P1, then founder-request, then age;",
            "an issue whose `Blocked-on: #N` names an open issue ranks below every unblocked one.",
            "The top row is what a session with nothing assigned works on next.", ""]
    if not picker.is_file():
        path.write_text("\n".join([*head, f"BLIND: picker {picker} is missing", ""]))
        return False
    r = subprocess.run([sys.executable, str(picker), "rank", "--top", str(top)], capture_output=True, text=True, check=False)
    if r.returncode != 0 or not r.stdout.strip():
        path.write_text("\n".join([*head, f"BLIND: `{picker.name} rank` exit {r.returncode}: {(r.stderr or r.stdout).strip()[:300]}", ""]))
        return False
    path.write_text("\n".join([*head, "```", r.stdout.rstrip(), "```", ""]))
    return True


def fetch(repo: str, since: datetime) -> list[dict]:
    rows = []
    for i in _gh(f"repos/{repo}/issues", state="all", since=since.strftime("%Y-%m-%dT%H:%M:%SZ"), per_page="100"):
        if "pull_request" in i:
            continue
        rows.append({"number": i["number"], "labels": [lab["name"] for lab in i["labels"]], "createdAt": i["created_at"],
                     "closedAt": i.get("closed_at"), "state": i["state"], "body": i.get("body")})
    # `since` filters by update time, so untouched open issues would be missed: add every open one
    seen = {r["number"] for r in rows}
    for i in _gh(f"repos/{repo}/issues", state="open", per_page="100"):
        if "pull_request" in i or i["number"] in seen:
            continue
        rows.append({"number": i["number"], "labels": [lab["name"] for lab in i["labels"]], "createdAt": i["created_at"],
                     "closedAt": None, "state": "open", "body": i.get("body")})
    return rows


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="velocity per lane from the board")
    ap.add_argument("--repo", default=REPO)
    ap.add_argument("--days", type=int, default=1, help="window for opened/closed (default: the last day)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--check", action="store_true", help="exit 1 when a lane is red")
    ap.add_argument("--no-write", action="store_true")
    a = ap.parse_args(argv)
    now = datetime.now(UTC)
    per_lane = lane_velocity(fetch(a.repo, now - timedelta(days=a.days)), now, a.days)
    day = now.strftime("%Y-%m-%d")
    written = 0 if a.no_write else append_rows(OUT, day, per_lane, now.strftime("%Y-%m-%dT%H:%M:%SZ"))
    red = red_lanes(read_rows(OUT)) if not a.no_write else []
    board_ok = write_board(BOARD, ESTATE_BOARD, now.strftime("%Y-%m-%dT%H:%M:%SZ")) if not a.no_write else None
    if a.json:
        print(json.dumps({"measured_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "days": a.days, "lanes": per_lane, "red": red}, indent=1))
    else:
        print(f"velocity, last {a.days} day(s) to {now:%Y-%m-%dT%H:%MZ}, {a.repo}; {written} row(s) appended to {OUT.name}; {BOARD.name} {'regenerated' if board_ok else ('BLIND' if board_ok is False else 'skipped')}")
        for lane, r in per_lane.items():
            flag = " RED" if lane in red else ""
            print(f"  {lane:<20} open={r['open']:<3} opened={r['opened']:<3} closed={r['closed']:<3} half-done={r['half_done']:<3} "
                  f"ticked={r['ticked']:<4} no-checklist={r['no_checklist']:<3} median-age={r['median_age_d']}d{flag}")
    if a.check and red:
        print(f"RED: {', '.join(red)}: {RED_DAYS} days with the open count not falling and no box ticked")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
