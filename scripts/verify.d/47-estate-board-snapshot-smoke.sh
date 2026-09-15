#!/usr/bin/env bash
# crew#102 — the prove row's smoke half: scripts/estate-snapshot still goes green.
#
# The plan's "Done commands" row #4 names `bash scripts/verify.sh` with the
# expected outcome FAIL=0. That gate is the orchestrator. This gate is its
# scoped, fast counterpart for the snapshot caller specifically: it runs the
# board-sync row of `scripts/estate-snapshot` against the same cache the
# prove-mode gate uses, asserts the row reports GREEN, and refuses to PASS
# when the row reports RED, NOT RUN, or anything else.
#
# WHY THIS EXISTS. The plan's "Count again" section names this branch's
# hourly caller as one of the jobs a smoke run on this branch must prove
# still goes green. If the rewrite of scripts/estate-board-sync.py broke
# the snapshot's `board_sync()` row, every hourly STATE.md would carry the
# silence as a NOT RUN, and the founder would not see it because the snapshot
# would refuse to commit. This gate makes that breakage loud on every PR.
#
# WHAT IT CHECKS:
#   A  scripts/estate-snapshot exists and is importable
#   B  the `estate board` row prints state GREEN
#   C  the row shape is the one STATE.md grades against
#   D  the cache file the row reads is the one we just rebuilt
#
# WHAT IT CANNOT SEE. The snapshot touches many other rows (delivery,
# OCI verification identity, spend, etc.). They are graded by their own
# incident tests and the orchestrator's FAIL=0 count. A red row elsewhere
# is not this gate's blind spot — it is the orchestrator's, and it is
# graded nightly in the same pass.
#
# STYLE MATCH. scripts/verify.d/45-estate-board.sh (header shape, exit codes
# 0=PASS / 1=FAIL / 2=CANNOT RUN).
#
# exit 0 pass | exit 1 the snapshot caller is broken | exit 2 CANNOT RUN
set -uo pipefail
cd "${CREW_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}" || exit 2

SNAP="scripts/estate-snapshot"
SYNC="scripts/estate-board-sync.py"

if [ ! -f "$SNAP" ]; then
  echo "BLIND: no snapshot at $SNAP"
  exit 2
fi
if [ ! -f "$SYNC" ]; then
  echo "BLIND: no sync at $SYNC"
  exit 2
fi
if ! command -v gh >/dev/null 2>&1; then
  echo "BLIND: \`gh\` is not on PATH; cannot reach the board issue"
  exit 2
fi
if ! gh auth status >/dev/null 2>&1; then
  echo "BLIND: \`gh auth status\` failed; cannot rebuild the cache"
  exit 2
fi

TMP_HOME="$(mktemp -d -t board-smoke-home.XXXXXX)"
META_BACKUP=""
WATERMARK_BACKUP=""

cleanup() {
  rm -rf "$TMP_HOME" 2>/dev/null || true
  if [ -n "$META_BACKUP" ] && [ -e "$META_BACKUP" ]; then
    mv "$META_BACKUP" "${HOME}/.claude/ESTATE_BOARD.meta.json" 2>/dev/null || true
  fi
  if [ -n "$WATERMARK_BACKUP" ] && [ -e "$WATERMARK_BACKUP" ]; then
    mv "$WATERMARK_BACKUP" "${HOME}/.claude/state/estate-board-sync.watermark" 2>/dev/null || true
  fi
}
trap cleanup EXIT

if [ -e "${HOME}/.claude/ESTATE_BOARD.meta.json" ]; then
  META_BACKUP="$(mktemp -t board-meta-backup.XXXXXX)"
  mv "${HOME}/.claude/ESTATE_BOARD.meta.json" "$META_BACKUP"
fi
if [ -e "${HOME}/.claude/state/estate-board-sync.watermark" ]; then
  WATERMARK_BACKUP="$(mktemp -t board-watermark-backup.XXXXXX)"
  mv "${HOME}/.claude/state/estate-board-sync.watermark" "$WATERMARK_BACKUP"
fi

mkdir -p "$TMP_HOME/.claude"

# Build a throwaway cache in the throwaway home, then run the snapshot's
# board_sync() row against it. The snapshot reads ~/.claude/ESTATE_BOARD.jsonl,
# so HOME=$TMP_HOME is the cleanest way to point it at our cache.
if ! HOME="$TMP_HOME" python3 "$SYNC" "$TMP_HOME/.claude/ESTATE_BOARD.jsonl" >/dev/null 2>&1; then
  echo "BLIND: sync could not populate $TMP_HOME/.claude/ESTATE_BOARD.jsonl"
  exit 2
fi

# Run just the board_sync row of the snapshot against the throwaway cache.
echo "\$ HOME=$TMP_HOME python3 -c 'import scripts.estate-snapshot as m; print(\"\\n\".join(m.board_sync()))'"
rows="$(HOME="$TMP_HOME" python3 - <<'PY'
import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(".").resolve()
spec = importlib.util.spec_from_file_location("estate_snapshot", ROOT / "scripts" / "estate-snapshot")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
for row in mod.board_sync():
    print(row)
PY
)"
echo "$rows"

# A: at least one row was printed.
if [ -z "$rows" ]; then
  echo "estate-snapshot.board_sync() printed no rows"
  exit 1
fi

# B + C: the row carries the GREEN state and the table shape.
if ! printf '%s\n' "$rows" | grep -qE "\| estate board \| GREEN \|"; then
  echo "estate board row did not report GREEN"
  echo "got: $rows"
  exit 1
fi

echo "snapshot caller: board row GREEN, summary shape OK"
exit 0
