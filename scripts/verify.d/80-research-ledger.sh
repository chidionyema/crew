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
for i, line in enumerate(lines, 1):
    try:
        e = json.loads(line)
    except json.JSONDecodeError:
        print(f"FAIL: line {i} is not JSON")
        sys.exit(1)
    missing = required - e.keys()
    if missing:
        print(f"FAIL: line {i} lacks {sorted(missing)}")
        sys.exit(1)
    if not e["sources"]:
        print(f"FAIL: line {i} has no sources — research with no trace did not happen")
        sys.exit(1)
    d = date.fromisoformat(e["date"])
    newest = max(newest or d, d)
    if e.get("metric_after") is None and not e.get("abandoned") and today - d > timedelta(days=14):
        stale_unmeasured.append(f"line {i} ({e['date']}: {e['question'][:60]})")

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
