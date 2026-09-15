#!/usr/bin/env bash
# crew#102 — the prove-mode half is proved, not just present (PROVE arm).
#
# 45-estate-board.sh is the hermetic parser-and-rebuild gate; this gate is
# its live counterpart for the plan's proof row. It runs the sync against
# a throwaway cache in $TMPDIR, asserts the pinned summary line shape, and
# confirms the second invocation logs "fetch: cache-hit" and
# "write: skipped (hash unchanged)" on stdout — the two strings the plan's
# "Idempotent on a re-run (the memoised path is the proof)" step names.
#
# WHAT IT CHECKS (paired arms, LAW 38: a guard seen refusing is a guard seen
# permitting):
#   A  `python3 scripts/estate-board-sync.py <cache>` exits 0
#   B  the printed summary line matches the orchestrator-pinned regex
#   C  the cache file holds > 0 JSON-valid rows
#   D  a second invocation exits 0 AND logs "fetch: cache-hit"
#   E  a second invocation logs "write: skipped (hash unchanged)"
#   F  the cache file is not rewritten between invocations (mtime preserved)
#
# WHAT IT CANNOT SEE (residual, stated because a guard that hides its blind spot
# lies). It grades the prove path against the live issue. A GitHub outage, a
# rate limit, or a moved issue number is invisible here by design and is
# graded hourly by the `estate board` row of scripts/estate-snapshot.
#
# STYLE MATCH. scripts/verify.d/45-estate-board.sh (header shape, exit codes
# 0=PASS / 1=FAIL / 2=CANNOT RUN).
#
# exit 0 pass | exit 1 the prove path is broken | exit 2 CANNOT RUN
set -uo pipefail

REPO="${ESTATE_BOARD_REPO:-chidionyema/crew}"
ISSUE="${ESTATE_BOARD_ISSUE:-102}"
SCRIPT="scripts/estate-board-sync.py"
CACHE="$(mktemp -t board-prove.XXXXXX.jsonl)"
META_BACKUP=""
WATERMARK_BACKUP=""

cleanup() {
  rm -f "$CACHE" 2>/dev/null || true
  if [ -n "$META_BACKUP" ] && [ -e "$META_BACKUP" ]; then
    mv "$META_BACKUP" "${HOME}/.claude/ESTATE_BOARD.meta.json" 2>/dev/null || true
  fi
  if [ -n "$WATERMARK_BACKUP" ] && [ -e "$WATERMARK_BACKUP" ]; then
    mv "$WATERMARK_BACKUP" "${HOME}/.claude/state/estate-board-sync.watermark" 2>/dev/null || true
  fi
}
trap cleanup EXIT

HYPHEN_SCRIPT="${ROOT:-$(pwd)}/${SCRIPT}"
if [ ! -f "$HYPHEN_SCRIPT" ]; then
  cd "${CREW_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}" || exit 2
  HYPHEN_SCRIPT="$SCRIPT"
fi
[ -f "$HYPHEN_SCRIPT" ] || { echo "no read side at $SCRIPT"; exit 2; }

if ! command -v gh >/dev/null 2>&1; then
  echo "BLIND: \`gh\` is not on PATH; cannot reach the board issue $REPO#$ISSUE"
  exit 2
fi
if ! gh auth status >/dev/null 2>&1; then
  echo "BLIND: \`gh auth status\` failed; cannot rebuild $REPO#$ISSUE"
  exit 2
fi

# Stash any pre-existing meta.json / watermark files so the prove run can
# operate on a clean slate (the first invocation is the full fetch; the
# second is the cache-hit). Restore on exit.
if [ -e "${HOME}/.claude/ESTATE_BOARD.meta.json" ]; then
  META_BACKUP="$(mktemp -t board-meta-backup.XXXXXX)"
  mv "${HOME}/.claude/ESTATE_BOARD.meta.json" "$META_BACKUP"
fi
if [ -e "${HOME}/.claude/state/estate-board-sync.watermark" ]; then
  WATERMARK_BACKUP="$(mktemp -t board-watermark-backup.XXXXXX)"
  mv "${HOME}/.claude/state/estate-board-sync.watermark" "$WATERMARK_BACKUP"
fi

# A: first invocation exits 0
echo "\$ python3 $SCRIPT $CACHE"
out1="$(python3 "$HYPHEN_SCRIPT" "$CACHE" 2>&1)"; rc1=$?
echo "$out1"
if [ "$rc1" -ne 0 ]; then
  echo "estate-board-sync first run exited $rc1; cannot grade the prove path"
  exit 1
fi

# B: pinned summary line
summary_re="^estate-board-sync: ([0-9]+) row\(s\) from ${REPO}#${ISSUE} -> ${CACHE}\$"
summary="$(printf '%s\n' "$out1" | grep -E "$summary_re" || true)"
if [ -z "$summary" ]; then
  echo "first run: expected summary line matching: $summary_re"
  echo "got: $out1"
  exit 1
fi
echo "first run: summary line OK"

# C: cache holds > 0 JSON-valid rows
lines="$(wc -l <"$CACHE" | tr -d ' ')"
if [ "${lines:-0}" -lt 1 ]; then
  echo "BLIND: first run wrote 0 rows to $CACHE"
  exit 2
fi
python3 -c "
import json, pathlib
p = pathlib.Path('${CACHE}')
ok = 0
for ln in p.read_text().splitlines():
    if not ln.strip():
        continue
    try:
        json.loads(ln)
        ok += 1
    except Exception as exc:
        print(f'invalid JSONL row: {exc}')
        raise SystemExit(2)
print(f'{ok} valid row(s)')
" || { echo "cache holds invalid JSONL"; exit 1; }

# Snapshot mtime so F can compare after the second run.
mtime_before="$(stat -f %m "$CACHE" 2>/dev/null || stat -c %Y "$CACHE" 2>/dev/null || echo 0)"

# Second invocation: must hit the memoised path. The meta.json (or, if absent,
# the watermark) was written by the first run; the second run must short-circuit.
echo "\$ python3 $SCRIPT $CACHE   # second run, must be a cache hit"
out2="$(python3 "$HYPHEN_SCRIPT" "$CACHE" 2>&1)"; rc2=$?
echo "$out2"
if [ "$rc2" -ne 0 ]; then
  echo "estate-board-sync second run exited $rc2; memoised path is broken"
  exit 1
fi

# D: "fetch: cache-hit" was logged.
if ! printf '%s\n' "$out2" | grep -q "fetch: cache-hit"; then
  echo "second run did not log 'fetch: cache-hit'; expected the memoised path"
  echo "got: $out2"
  exit 1
fi

# E: "write: skipped (hash unchanged)" was logged.
if ! printf '%s\n' "$out2" | grep -q "write: skipped (hash unchanged)"; then
  echo "second run did not log 'write: skipped (hash unchanged)'"
  echo "got: $out2"
  exit 1
fi

# F: cache file was not rewritten (mtime preserved) — the BATCHED optimisation
# in its strongest form. A no-op rename that moved mtime would still be a lie
# to a downstream reader that grades by mtime.
mtime_after="$(stat -f %m "$CACHE" 2>/dev/null || stat -c %Y "$CACHE" 2>/dev/null || echo 0)"
if [ "$mtime_after" != "$mtime_before" ]; then
  echo "second run rewrote the cache (mtime $mtime_before -> $mtime_after); the hash-equal path must not touch the file"
  exit 1
fi

echo "prove path: cache-hit on second run, cache untouched, plan-named strings present"
exit 0
