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
import datetime as dt
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

SCIENCE = Path(__file__).resolve().parent
SHIPS = SCIENCE / "ships.jsonl"
PREDICTIONS = SCIENCE / "predictions.jsonl"
ATTENTION = SCIENCE / "attention.jsonl"
REVENUE = SCIENCE / "revenue.jsonl"

#: The only place a customer can pay this estate is the store, and its backend answers here.
#: crew#70: every efficiency number was a cost divided by nothing because no series held what
#: came in. The admin token is read from the environment (vault entry `medusa-admin`), never
#: from a file in this repo.
STORE_API = os.environ.get("ESTATE_STORE_API", "https://api.mumchimp.com")

#: Where his own words are captured. `directive-capture.py` writes one file per project on
#: UserPromptSubmit, so this directory is the estate's complete record of what he asked for.
#: Nothing had ever read it as a series.
DIRECTIVES = Path.home() / ".claude/directives"

#: The friction lexicon lives in founder_board.py and is borrowed, never copied. Two lists of
#: his own words drift apart and the one nobody edits is the one that silently stops matching.
#: `friction-relay.py` borrows it the same way, for the same reason.
FOUNDER_BOARD = Path.home() / ".claude/scripts/founder_board.py"

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
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, check=False)
        return p.returncode, p.stdout.strip()
    except Exception as exc:                                        # noqa: BLE001
        return 1, f"{type(exc).__name__}: {exc}"


def collect_ships(days: int) -> list[dict]:
    """One row per repo per day: how many commits landed, and how much they changed.

    Lines changed is deliberately included and deliberately not used as the headline.
    It is the easiest number on this page to game, and it is here so that a later
    reader can see whether commit count and line count ever disagree.
    """
    since = (dt.datetime.now(dt.UTC).date() - dt.timedelta(days=days)).isoformat()
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
            rows.append({"at": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
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
            rows.append({"at": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
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


def friction_words() -> tuple:
    """Borrow the lexicon rather than keeping a second copy of his own words."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("_fb", FOUNDER_BOARD)
        if spec is None or spec.loader is None:
            raise ImportError(f"no loadable module at {FOUNDER_BOARD}")
        fb = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fb)
        words = tuple(getattr(fb, "FRICTION", ()))
        if words:
            return words
    except Exception as exc:                                        # noqa: BLE001
        print(f"friction lexicon did not load: {type(exc).__name__}: {exc}", file=sys.stderr)
    # A degraded vocabulary under-reports friction. It must never report a clean estate, so
    # the caller is told the lexicon was not the real one.
    return ()


def collect_attention() -> tuple[list[dict], int]:
    """His messages and his complaints, per day. The measurement LAW 36 asks for.

    The founder is one of the platform's two customers and the only instrument pointed at him
    was `friction-relay.py`, which holds a six hour window and is rebuilt at every session start.
    Nothing kept a series, so "is he complaining more or less than last week" could not be asked,
    let alone answered — and LAW 36 says the complaint is the measurement, not a mood.

    Derived from `~/.claude/directives`, which has captured every prompt since 2026-07-28. This
    is a read of a store that already exists, not a new ledger (LAW 30).

    A complaint is a message matching the founder_board lexicon. That is a proxy and it is a
    crude one: it counts an angry word, not an unmet need, and a calm sentence saying the same
    thing does not count. It is reported as a rate over his own volume for that reason — the
    number to watch is the trend, and a proxy that moves with the thing is worth more than a
    perfect measure nobody has.
    """
    words = friction_words()
    per: dict[str, dict] = {}
    if not DIRECTIVES.is_dir():
        return [], 0
    for f in sorted(DIRECTIVES.glob("*.jsonl")):
        for line in f.read_text(errors="ignore").split("\n"):
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            day = str(r.get("at") or r.get("ts") or "")[:10]
            if day < "2000":
                # an epoch-zero stamp is a writer defect, not a day he wrote on
                continue
            text = str(r.get("text") or r.get("prompt") or r.get("request") or "")
            if not day or not text:
                continue
            d = per.setdefault(day, {"messages": 0, "complaints": 0})
            d["messages"] += 1
            if words and any(w in text.lower() for w in words):
                d["complaints"] += 1
    now = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
    rows = [{"at": now, "day": day, "messages": d["messages"], "complaints": d["complaints"],
             "complaint_rate": round(100 * d["complaints"] / d["messages"], 1),
             "lexicon_size": len(words)}
            for day, d in sorted(per.items())]
    return rows, len(words)


def cmd_attention(args) -> int:
    rows, lex = collect_attention()
    if not rows:
        print(f"no directive rows under {DIRECTIVES}", file=sys.stderr)
        return 1
    write_rows(ATTENTION, rows)
    if not lex:
        print("WARNING: the friction lexicon did not load, so every complaint count below is 0")
        print(f"         and means 'not measured', not 'no complaints'. Check {FOUNDER_BOARD}.")
    print(f"{ATTENTION}")
    print(f"{'day':12} {'his messages':>13} {'complaints':>11} {'rate':>6}")
    print("-" * 45)
    for r in rows[-args.days:]:
        print(f"{r['day']:12} {r['messages']:>13} {r['complaints']:>11} {r['complaint_rate']:>5.0f}%")
    print("-" * 45)
    m = sum(r["messages"] for r in rows)
    c = sum(r["complaints"] for r in rows)
    print(f"{'TOTAL':12} {m:>13} {c:>11} {100*c/max(m,1):>5.0f}%")
    print(f"\n{len(rows)} days, {rows[0]['day']} to {rows[-1]['day']}, lexicon {lex} words")
    return 0


def collect_revenue(now: dt.datetime | None = None, fetch=None) -> dict:
    """One row: has this estate ever been paid, by whom, how much, when.

    Measured, never assumed. A captured payment is counted from the store backend's
    admin orders endpoint; when the backend does not answer, or no token is set, the
    row says so with `measured: false` and the snapshot prints NOT RUN. A zero is only
    written when the store answered and reported no captured payment (LAW 30).
    """
    now = now or dt.datetime.now(dt.UTC)
    at = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    token = os.environ.get("MEDUSA_ADMIN_TOKEN", "")
    url = f"{STORE_API}/admin/orders?payment_status=captured&limit=50&fields=id,email,total,currency_code,created_at"
    row = {"at": at, "source": url, "measured": False, "paid_orders": 0, "total": 0.0,
           "currency": None, "payers": [], "first_paid_at": None, "last_paid_at": None, "reason": ""}
    if not token:
        row["reason"] = "MEDUSA_ADMIN_TOKEN not set (vault entry medusa-admin)"
        return row
    fetch = fetch or _http_json
    try:
        body = fetch(url, token)
    except Exception as exc:                                    # noqa: BLE001
        row["reason"] = f"{STORE_API} did not answer: {type(exc).__name__}: {exc}"[:200]
        return row
    orders = body.get("orders") if isinstance(body, dict) else None
    if orders is None:
        row["reason"] = "backend answered without an orders list"
        return row
    row["measured"] = True
    row["paid_orders"] = int(body.get("count", len(orders)))
    row["total"] = round(sum(float(o.get("total") or 0) for o in orders), 2)
    row["currency"] = next((o.get("currency_code") for o in orders if o.get("currency_code")), None)
    row["payers"] = sorted({o.get("email") for o in orders if o.get("email")})
    whens = sorted(o.get("created_at") for o in orders if o.get("created_at"))
    row["first_paid_at"], row["last_paid_at"] = (whens[0], whens[-1]) if whens else (None, None)
    return row


def _http_json(url: str, token: str) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())


def cmd_revenue(args) -> int:
    row = collect_revenue()
    with REVENUE.open("a") as fh:
        fh.write(json.dumps(row, separators=(",", ":")) + "\n")
    print(f"{REVENUE}")
    if not row["measured"]:
        print(f"NOT RUN  revenue not measured at {row['at']}: {row['reason']}")
        return 1
    print(f"paid orders {row['paid_orders']}  total {row['total']} {row['currency'] or ''}  "
          f"payers {len(row['payers'])}  first {row['first_paid_at']}  last {row['last_paid_at']}  "
          f"measured {row['at']}")
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
    rec = {"id": pid, "at": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
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
    rec = dict(rec, scored_at=dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
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
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("ship", help="collect delivery outcomes from git and gh")
    s.add_argument("--days", type=int, default=30)
    s.set_defaults(fn=cmd_ship)

    a = sub.add_parser("attention", help="his messages and complaints, per day")
    a.add_argument("--days", type=int, default=21, help="how many days to print, not to collect")
    a.set_defaults(fn=cmd_attention)

    v = sub.add_parser("revenue", help="has this estate ever been paid: measured from the store, never assumed")
    v.set_defaults(fn=cmd_revenue)

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
