#!/usr/bin/env bash
# run_board_selftest.sh — one-command proof the board scripts work offline.
#
# This script does NOT post to GitHub. It exercises the writer's render and
# dead-letter paths and the reader's parse path against a temp HOME, then
# prints PASS/FAIL. Use this as the "Proved" receipt for crew#102.
#
# Usage: bash board/run_board_selftest.sh
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
export HOME="$tmp"

set +e
out="$(python3 "$here/test_board.py" 2>&1)"
rc=$?
set -e

if [[ $rc -eq 0 ]]; then
    echo "$out" | tail -n 20
    echo "PASS: board selftest green (writer render, reader parse, JSONL cache, dead-letter)"
    exit 0
fi

echo "$out"
echo "FAIL: board selftest red (rc=$rc)"
exit 1
