#!/usr/bin/env bash
# deadman-check.sh -- is the Mac still alive?
#
# Every monitor this estate had ran ON the Mac it was monitoring. When the Mac stops, the
# jobs stop, and so does the thing that would have said so. The local Healthchecks receiver
# is the clearest case: it answers HTTP 000 while 12 of 40 wrapped jobs ping it into
# nothing, and on 2026-08-24 it exited 137 and stayed down for hours with no one told.
#
# This check runs on GitHub Actions instead, which is outside that failure domain, costs
# nothing, and needs no account the estate does not already have.
#
# What it watches is one heartbeat, not 46 jobs. com.founder.estatesnapshot has
# StartInterval 3600 and commits STATE.md to main every hour. If those commits stop, the
# Mac is gone -- and knowing that is what has to arrive first. Per-job monitoring stays
# with the local receiver, which is the right place for it, because per-job detail from
# inside a dead machine is not worth having.
#
# The threshold is deliberately loose. Measured over the 30 hours to 2026-08-24 12:45, the
# hourly snapshot missed four runs, with gaps of 96, 100, 144 and 170 minutes. A dead-man
# set tight enough to catch those would fire on a healthy-but-flaky estate several times a
# day and be muted within a week, which is the failure mode this is supposed to avoid
# (LAW 38: a guard that refuses correct work is an outage). So the gate fires only on
# sustained silence, and the missed-run count is reported on every run without gating.
#
# Overrides, both for testing:
#   DEADMAN_MAX_MINUTES   silence past this is a failure. Default 180.
#   DEADMAN_AGE_MINUTES   pretend the heartbeat is this old, instead of reading git.
#
# Exit 0 alive, exit 1 silent. Nothing else exits non-zero: a check that cannot tell
# whether it looked says BLIND and passes, because failing on its own breakage trains
# people to ignore it.
set -u

HEARTBEAT_PATH="${DEADMAN_PATH:-STATE.md}"
MAX="${DEADMAN_MAX_MINUTES:-180}"
REPORT_WINDOW_HOURS=30
EXPECTED_INTERVAL_MINUTES=60

age=""
if [ -n "${DEADMAN_AGE_MINUTES:-}" ]; then
  age="$DEADMAN_AGE_MINUTES"
  echo "heartbeat age: ${age}m (forced by DEADMAN_AGE_MINUTES, not measured)"
else
  last=$(git log -1 --format=%at -- "$HEARTBEAT_PATH" 2>/dev/null || true)
  if [ -z "$last" ]; then
    echo "BLIND: no commit touching $HEARTBEAT_PATH is reachable from this checkout."
    echo "       A shallow clone does this. Fetch depth 0 and run again."
    exit 0
  fi
  now=$(date +%s)
  age=$(( (now - last) / 60 ))
  echo "heartbeat: $HEARTBEAT_PATH last changed $(date -u -r "$last" '+%Y-%m-%d %H:%M UTC' 2>/dev/null || echo "at epoch $last")"
  echo "heartbeat age: ${age}m"
fi

echo "threshold: ${MAX}m of silence"
echo

# Reported on every run, gating nothing. A snapshot that lands late is a real defect and a
# number nobody prints is a number nobody fixes (LAW 28), but it is not the Mac being dead.
if [ -z "${DEADMAN_AGE_MINUTES:-}" ]; then
  stamps=$(git log --since="$REPORT_WINDOW_HOURS hours ago" --format=%at -- "$HEARTBEAT_PATH" 2>/dev/null | sort -n)
  if [ -n "$stamps" ]; then
    misses=$(printf '%s\n' "$stamps" | awk -v iv="$EXPECTED_INTERVAL_MINUTES" '
      NR > 1 { gap = ($1 - prev) / 60; if (gap + 0 > iv * 1.5) { n++; worst = (gap + 0 > worst + 0) ? gap : worst } }
      { prev = $1 }
      END { printf "%d %d", n + 0, worst + 0 }')
    n=${misses% *}
    worst=${misses#* }
    total=$(printf '%s\n' "$stamps" | grep -c .)
    echo "last ${REPORT_WINDOW_HOURS}h: $total heartbeats, $n gap(s) over $((EXPECTED_INTERVAL_MINUTES * 3 / 2))m, worst ${worst}m   (reported, not gating)"
  fi
  echo
fi

if [ "$age" -gt "$MAX" ]; then
  echo "DEAD: the Mac has been silent for ${age}m, past the ${MAX}m threshold."
  echo "      Every job on it is unmonitored right now, including the monitors."
  exit 1
fi

echo "ALIVE: last heartbeat ${age}m ago, inside the ${MAX}m threshold."
exit 0
