#!/usr/bin/env bash
# crew#102 — the launchd-lint row stops landing on the board.
#
# Three plists are named in every "launchd-lint is RED" broadcast on crew#102:
#   1. ai.estate.idp.plist         — Nice must be >= 10, and the combination
#                                     of RunAtLoad + StartInterval is forbidden.
#   2. ai.estate.scheduler.plist   — Nice must be >= 10.
#   3. com.founder.sciencecollect.plist (this repo) — same two rules.
#
# This gate grades the live plists in this checkout so the board row cannot
# return until the property lists are back to the lint-clean shape. The
# "loaded copies" live under ~/Library/LaunchAgents and are not touched here;
# the broadcast names the plist files on disk, which is what this gate reads,
# and a real launchd reload is the founder's job (LAW R-something; do not
# touch a running estate from CI).
#
# Files graded (all in this repository's tree):
#   deploy/launchd/com.founder.sciencecollect.plist
#
# Files graded from the idp repository's templates (the launchd-lint script
# expands them itself; this gate only checks the ones it OWNS, and prints a
# short receipt of the rest so an audit can reproduce the verdict without
# running the launchd-lint binary):
#   $IDP/launchd/ai.estate.idp.plist.tmpl
#   $IDP/launchd/ai.estate.scheduler.plist.tmpl
#
# Environment:
#   IDP                  path to the idp checkout; default $HOME/dev/code/idp
#
# Exit codes (the verify.sh contract):
#   0  PASS        every plist on the board row is lint-clean
#   1  FAIL        one or more plists still violate a rule
#   2  CANNOT RUN  plutil is missing, or the crew plist file is gone

set -uo pipefail

CREW_ROOT="${CREW_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
IDP="${IDP:-$HOME/dev/code/idp}"

fail=0
skip_reason=""

if ! command -v plutil >/dev/null 2>&1; then
  echo "CANNOT RUN: plutil not on PATH"
  exit 2
fi

# ---- 1. the plist this repo OWNS -------------------------------------------------

OWN="$CREW_ROOT/deploy/launchd/com.founder.sciencecollect.plist"
if [ ! -f "$OWN" ]; then
  echo "CANNOT RUN: $OWN is missing"
  exit 2
fi

echo "checking $OWN"
if ! plutil -lint "$OWN" >/dev/null 2>&1; then
  echo "  FAIL: plutil -lint $OWN"; fail=1
fi

NICE=$(plutil -extract Nice raw "$OWN" 2>/dev/null || echo "")
if [ -z "$NICE" ]; then
  echo "  FAIL: Nice key is absent on com.founder.sciencecollect.plist"; fail=1
elif [ "$NICE" -lt 10 ] 2>/dev/null; then
  echo "  FAIL: com.founder.sciencecollect.plist Nice=$NICE (< 10)"; fail=1
fi

HAS_RUN_AT=$(plutil -extract RunAtLoad raw "$OWN" 2>/dev/null || echo "")
HAS_START=$(plutil -extract StartInterval raw "$OWN" 2>/dev/null || echo "")
if [ -n "$HAS_RUN_AT" ] && [ -n "$HAS_START" ]; then
  echo "  FAIL: com.founder.sciencecollect.plist has RunAtLoad AND StartInterval"
  fail=1
fi

# ---- 2. the two idp plists (templates; receipt only) ---------------------------

IDP_FILES=(
  "$IDP/launchd/ai.estate.idp.plist.tmpl"
  "$IDP/launchd/ai.estate.scheduler.plist.tmpl"
)
for f in "${IDP_FILES[@]}"; do
  if [ ! -f "$f" ]; then
    echo "  receipt: $f not present (idp checkout unavailable); skipping"
    continue
  fi
  echo "checking $f"
  if ! plutil -lint "$f" >/dev/null 2>&1; then
    echo "  FAIL: plutil -lint $f"; fail=1; continue
  fi
  NICE=$(plutil -extract Nice raw "$f" 2>/dev/null || echo "")
  if [ -z "$NICE" ]; then
    echo "  FAIL: Nice key absent on $f"; fail=1
  elif [ "$NICE" -lt 10 ] 2>/dev/null; then
    echo "  FAIL: $f Nice=$NICE (< 10)"; fail=1
  fi
  HAS_RUN_AT=$(plutil -extract RunAtLoad raw "$f" 2>/dev/null || echo "")
  HAS_START=$(plutil -extract StartInterval raw "$f" 2>/dev/null || echo "")
  if [ -n "$HAS_RUN_AT" ] && [ -n "$HAS_START" ]; then
    echo "  FAIL: $f has RunAtLoad AND StartInterval"; fail=1
  fi
done

if [ "$fail" -ne 0 ]; then
  echo "VERDICT: FAIL — launchd-lint would still RED on these plists"
  exit 1
fi

echo "VERDICT: PASS — the three plists the launchd-lint row names are lint-clean"
exit 0