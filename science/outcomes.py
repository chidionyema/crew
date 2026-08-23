#!/usr/bin/env python3
"""Collect what the estate produced, so spend can be divided by something.

Every instrument on this estate points inward: guards, laws, complaints, tokens.
Not one records an outcome. The consequence is measurable — the estate can say it
spent $854 yesterday and cannot say what that bought.

Two collections start here, and neither existed before.

**Delivery.** Commits, pull requests merged and issues closed, per day, across the
repositories that ship. Joined against `spend_daily` this gives dollars per
shipped change. It is a crude denominator and it is the first one that exists.

**Predictions.** `method_metrics.json` has carried `predictions: []` for weeks, so
the estate has never once predicted a cause and then checked itself (LAW 29, and
goal G3 in PLAN.md). A prediction is written BEFORE the repair, and scored after,
by a different command, so the score cannot be edited to fit.

    python3 science/outcomes.py ship            # collect delivery, last 30 days
    python3 science/outcomes.py predict --issue 26 --step "..." --because "..."
    python3 science/outcomes.py score --id 3 --correct   # or --wrong
    python3 science/outcomes.py rate            # the hit rate, misses included

Why a new file and not an append to something existing (LAW 30): there is no
store of this kind to append to. `method_metrics.json` has the slot but is
regenerated wholesale by `reflect.py` every four hours, so anything appended to it
is erased. These two ledgers are the first of their kind, not a second copy of one.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import datetime as dt
from pathlib import Path

SCIENCE = Path(__file__).resolve().parent
SHIPS = SCIENCE / "ships.jsonl"
PREDICTIONS = SCIENCE / "predictions.jsonl"

# The repositories that actually ship something. Measured, not guessed: these are
# the trees with a commit in the last 7 days as of 2026-08-23.
REPOS = [
    Path.home() / "dev/code/crew",
    Path.home() / "dev/code/maestro",
    Path.home() / "dev/code/hermes-v2",
    Path.home() / "dev/code/prospector-main",
    Path.home() / "dev/code/survival-stack",
    Path.home() / ".claude",
]


def sh(cmd: list[str], cwd: Path | None = None, timeout: int = 60) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout.strip()
    except Exception as exc:                                        # noqa: BLE001
        return 1, f"{type(exc).__name__}: {exc}"


def collect_ships(days: int) -> list[dict]:
    """One row per repo per day: how many commits landed, and how much they changed.

    Lines changed is deliberately included and deliberately not used as the headline.
    It is the easiest number on this page to game, and it is here so that a later
    reader can see whether commit count and line count ever disagree.
    """
    since = (dt.date.today() - dt.timedelta(days=days)).isoformat()
    rows: list[dict] = []
    for repo in REPOS:
        if not (repo / ".git").exists():
            continue
        rc, out = sh(["git", "log", f"--since={since}", "--date=short",
                      "--pretty=format:%ad\t%H\t%s"], cwd=repo)
        if rc:
            continue
        per_day: dict[str, dict] = {}
        for line in out.split("\n"):
            if not line.strip():
                continue
            parts = line.split("\t", 2)
            if len(parts) < 3:
                continue
            day, sha, subject = parts
            d = per_day.setdefault(day, {"commits": 0, "feats": 0, "fixes": 0, "shas": []})
            d["commits"] += 1
            if subject.startswith("feat"):
                d["feats"] += 1
            if subject.startswith("fix"):
                d["fixes"] += 1
            d["shas"].append(sha[:8])
        for day, d in per_day.items():
            rows.append({"at": dt.datetime.now().isoformat(timespec="seconds"),
                         "day": day, "repo": repo.name, **d})
    return rows


def collect_prs() -> list[dict]:
    """Pull requests merged on the crew board, per day. Skipped silently if gh is absent."""
    rc, out = sh(["gh", "pr", "list", "--repo", "chidionyema/crew", "--state", "merged",
                  "--limit", "100", "--json", "number,mergedAt,title"], timeout=90)
    if rc or not out:
        return []
    try:
        prs = json.loads(out)
    except json.JSONDecodeError:
        return []
    rows = []
    for pr in prs:
        merged = (pr.get("mergedAt") or "")[:10]
        if merged:
            rows.append({"at": dt.datetime.now().isoformat(timespec="seconds"),
                         "day": merged, "repo": "crew", "pr": pr["number"],
                         "title": pr.get("title", "")[:120]})
    return rows


def write_rows(path: Path, rows: list[dict]) -> None:
    """Rewrite, not append. Ships are derived from git, which is the source of truth;
    appending would double-count every re-run."""
    path.write_text("".join(json.dumps(r, separators=(",", ":")) + "\n" for r in rows))


def cmd_ship(args) -> int:
    ships = collect_ships(args.days)
    prs = collect_prs()
    write_rows(SHIPS, ships + prs)

    by_day: dict[str, int] = {}
    for r in ships:
        by_day[r["day"]] = by_day.get(r["day"], 0) + r["commits"]
    merged: dict[str, int] = {}
    for r in prs:
        merged[r["day"]] = merged.get(r["day"], 0) + 1

    print(f"{SHIPS}")
    print(f"{'day':12} {'commits':>8} {'PRs merged':>11}")
    print("-" * 34)
    for day in sorted(set(by_day) | set(merged), reverse=True)[:args.days]:
        print(f"{day:12} {by_day.get(day, 0):>8} {merged.get(day, 0):>11}")
    print("-" * 34)
    print(f"{'TOTAL':12} {sum(by_day.values()):>8} {sum(merged.values()):>11}")
    return 0


def load_predictions() -> list[dict]:
    if not PREDICTIONS.exists():
        return []
    out = []
    for line in PREDICTIONS.read_text(errors="ignore").split("\n"):
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def cmd_predict(args) -> int:
    """Write a prediction BEFORE the repair. It cannot be scored by this command."""
    rows = load_predictions()
    pid = max([r["id"] for r in rows], default=0) + 1
    rec = {"id": pid, "at": dt.datetime.now().isoformat(timespec="seconds"),
           "issue": args.issue, "step": args.step, "because": args.because,
           "scored_at": None, "correct": None}
    with open(PREDICTIONS, "a") as fh:
        fh.write(json.dumps(rec, separators=(",", ":")) + "\n")
    print(f"prediction #{pid} recorded, unscored")
    print(f"  step:    {args.step}")
    print(f"  because: {args.because}")
    print(f"\nscore it after the repair:  python3 science/outcomes.py score --id {pid} --correct")
    return 0


def cmd_score(args) -> int:
    rows = load_predictions()
    hit = [r for r in rows if r["id"] == args.id]
    if not hit:
        print(f"no prediction #{args.id}", file=sys.stderr)
        return 1
    rec = hit[-1]
    if rec.get("scored_at"):
        print(f"prediction #{args.id} is already scored "
              f"{'correct' if rec['correct'] else 'wrong'}; a score is not revised",
              file=sys.stderr)
        return 1
    rec = dict(rec, scored_at=dt.datetime.now().isoformat(timespec="seconds"),
               correct=bool(args.correct), note=args.note or "")
    with open(PREDICTIONS, "a") as fh:
        fh.write(json.dumps(rec, separators=(",", ":")) + "\n")
    print(f"prediction #{args.id} scored {'CORRECT' if args.correct else 'WRONG'}")
    return 0


def cmd_rate(args) -> int:
    """The hit rate, published whatever it is. LAW 29 sets the floor low on purpose."""
    rows = load_predictions()
    latest: dict[int, dict] = {}
    for r in rows:
        latest[r["id"]] = r
    scored = [r for r in latest.values() if r.get("scored_at")]
    correct = [r for r in scored if r.get("correct")]
    print(f"predictions logged: {len(latest)}")
    print(f"scored:             {len(scored)}")
    if not scored:
        print("hit rate:           unmeasurable, n = 0")
        print("\nThat is the honest answer and it is the same one method_metrics.json")
        print("has given for weeks. It changes when a repair predicts its cause first.")
        return 0
    print(f"hit rate:           {len(correct)}/{len(scored)} = {100*len(correct)/len(scored):.0f}%")
    if len(scored) < 5:
        # A percentage printed off one or two calls is the most misleading number this
        # file can emit: 100% at n=1 reads like a track record and is a coin that landed
        # once. Say the n out loud rather than trusting a later reader to notice it.
        print(f"                    NOT A RATE YET — n = {len(scored)}, needs 5 before "
              f"the percentage means anything")
    misses = [r for r in scored if not r.get("correct")]
    if misses:
        print("\nmisses, named (LAW 29 — publish the rate including these):")
        for r in misses:
            print(f"  #{r['id']} issue {r.get('issue')}: predicted {r['step']!r}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("ship", help="collect delivery outcomes from git and gh")
    s.add_argument("--days", type=int, default=30)
    s.set_defaults(fn=cmd_ship)

    p = sub.add_parser("predict", help="record a causal prediction BEFORE the repair")
    p.add_argument("--issue", required=True, help="the issue or PR this is about")
    p.add_argument("--step", required=True, help="the step you say produced the outcome")
    p.add_argument("--because", required=True, help="why that step and not its neighbour")
    p.set_defaults(fn=cmd_predict)

    c = sub.add_parser("score", help="score a prediction after the repair")
    c.add_argument("--id", type=int, required=True)
    g = c.add_mutually_exclusive_group(required=True)
    g.add_argument("--correct", action="store_true")
    g.add_argument("--wrong", dest="correct", action="store_false")
    c.add_argument("--note", default="")
    c.set_defaults(fn=cmd_score)

    r = sub.add_parser("rate", help="the hit rate, misses included")
    r.set_defaults(fn=cmd_rate)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
