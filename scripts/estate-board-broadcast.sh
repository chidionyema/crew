#!/usr/bin/env bash
#
# estate-board-broadcast.sh
#
# Purpose: append one row to the estate board (of record: chidionyema/crew#102)
# by posting a comment to that GitHub issue via `gh`. The local JSONL cache at
# ~/.claude/ESTATE_BOARD.jsonl is rebuilt by scripts/estate-board-sync.py on
# read; this wrapper never touches it directly.
#
# Usage:
#   scripts/estate-board-broadcast.sh "2026-01-15T12:00:00Z  builder  (incident/high): message"
#
# Exits non-zero if `gh` is not authenticated, with a clear stderr message.

set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "usage: $0 \"<row text>\"" >&2
    exit 2
fi

if ! gh auth status >/dev/null 2>&1; then
    echo "estate-board-broadcast: gh is not authenticated; run 'gh auth login' first" >&2
    exit 3
fi

gh issue comment 102 --repo chidionyema/crew --body "$1"
