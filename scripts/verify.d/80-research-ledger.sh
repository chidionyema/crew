#!/usr/bin/env bash
# LAW 35: the estate researches the world, records where it looked, and closes
# each loop with a metric. This check makes all three mechanical.
#
#   FAIL when the ledger is missing or malformed,
#   FAIL when no research entry has landed in 7 days (the ethos has stalled),
#   FAIL when an entry older than 14 days still has metric_after: null and no
#        abandoned marker (an improvement claimed and never measured).
LEDGER="${CREW_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}/science/RESEARCH-LEDGER.jsonl"
echo "\$ python3 - $LEDGER"
python3 - "$LEDGER" <<'PY'
import json, sys
from datetime import date, timedelta

path = sys.argv[1]
try:
    lines = [l for l in open(path, encoding="utf-8") if l.strip()]
except OSError:
    print(f"FAIL: no ledger at {path}")
    sys.exit(1)

required = {"date", "question", "decision_fed", "sources", "findings", "metric", "metric_before", "owner"}
today = date.today()
newest = None
stale_unmeasured = []

# Every per-line problem is collected and reported together. This check used to
# exit on the first bad line, so a ledger with four malformed rows cost four
# pushes and four CI runs to clean, each one revealing the next fault. A gate
# that shows one fault at a time turns a five-minute fix into an afternoon
# (LAW 14: the cheaper way, once measured, is the way).
problems = []
for i, line in enumerate(lines, 1):
    try:
        e = json.loads(line)
    except json.JSONDecodeError:
        problems.append(f"line {i} is not JSON")
        continue
    missing = required - e.keys()
    if missing:
        problems.append(f"line {i} lacks {sorted(missing)}")
        continue
    if not e["sources"]:
        problems.append(f"line {i} has no sources — research with no trace did not happen")

    # findings must be a list of statements, never one string. Both shapes used to
    # pass here, and a string is the dangerous one because iterating it succeeds:
    # a consumer that loops over findings gets one character per finding and never
    # raises. That is how it was read on 2026-08-24 and briefly reported as data
    # corruption. Pick one shape and make the gate hold it (LAW 30: the ledger has
    # to be queryable, which means a consumer can trust the type).
    f = e["findings"]
    if not isinstance(f, list) or not f:
        problems.append(
            f"line {i} findings is {type(f).__name__}, expected a non-empty "
            "list of statements. A string iterates into characters, so a consumer "
            "reading it gets silent nonsense instead of an error.")
    elif any(not isinstance(x, str) or len(x) < 20 for x in f):
        problems.append(
            f"line {i} has a finding under 20 characters. That is the "
            "signature of a string that was split into characters somewhere "
            "upstream, and of a finding that says nothing.")
    try:
        d = date.fromisoformat(e["date"])
    except (TypeError, ValueError):
        problems.append(f"line {i} date {e['date']!r} is not an ISO date")
        continue
    newest = max(newest or d, d)
    if e.get("metric_after") is None and not e.get("abandoned") and today - d > timedelta(days=14):
        stale_unmeasured.append(f"line {i} ({e['date']}: {e['question'][:60]})")

if problems:
    print(f"FAIL: {len(problems)} malformed entr{'y' if len(problems) == 1 else 'ies'}:")
    for p in problems:
        print(f"  {p}")
    sys.exit(1)
if newest is None:
    print("FAIL: ledger is empty")
    sys.exit(1)
if today - newest > timedelta(days=7):
    print(f"FAIL: newest entry is {newest}, over 7 days old — the research ethos has stalled")
    sys.exit(1)
if stale_unmeasured:
    print("FAIL: claimed improvements never measured (metric_after still null after 14 days):")
    for s in stale_unmeasured:
        print(f"  {s}")
    sys.exit(1)
print(f"PASS: {len(lines)} entries, newest {newest}, every entry carries sources, none unmeasured past 14 days")
PY
