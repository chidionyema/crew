#!/usr/bin/env bash
# scripts/estate-board-broadcast.sh
#
# Posts one broadcast row to the estate board issue (chidionyema/crew#102).
# The JSONL at ~/.claude/ESTATE_BOARD.jsonl remains only the offline cache the
# prompt hooks read. A row that fails to land here is dead-lettered to
# ~/.claude/state/board-deadletter.jsonl and warned loudly — never dropped silently.
#
# Comment format on the board: `ts` **from** (kind/priority): message
#
# Usage:
#   scripts/estate-board-broadcast.sh "<comment-body>"
#
# Required environment:
#   GH_TOKEN          GitHub token with repo scope (issue: write)
#   ESTATE_BOARD_REPO  default: chidionyema/crew
#   ESTATE_BOARD_ISSUE default: 102
set -euo pipefail

BOARD_REPO="${ESTATE_BOARD_REPO:-chidionyema/crew}"
BOARD_ISSUE="${ESTATE_BOARD_ISSUE:-102}"
CACHE="${ESTATE_BOARD_JSONL:-$HOME/.claude/ESTATE_BOARD.jsonl}"
DEADLETTER="${ESTATE_BOARD_DEADLETTER:-$HOME/.claude/state/board-deadletter.jsonl}"

body="${1:-}"
if [[ -z "$body" ]]; then
  echo "usage: $0 <comment-body>" >&2
  exit 64
fi

# 1. Append to the offline cache first; the cache is the recovery surface.
mkdir -p "$(dirname "$CACHE")" "$(dirname "$DEADLETTER")"
printf '%s\n' "$body" >> "$CACHE"

# 2. Post to the GitHub issue. On any failure, dead-letter and warn.
if command -v gh >/dev/null 2>&1 && [[ -n "${GH_TOKEN:-}" ]]; then
  if gh issue comment "$BOARD_ISSUE" --repo "$BOARD_REPO" --body "$body" >/dev/null 2>&1; then
    exit 0
  fi
fi

# 3. Fallback: dead-letter so the row is never dropped silently.
ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
printf '{"at":"%s","repo":"%s","issue":%s,"body":%s}\n' \
  "$ts" "$BOARD_REPO" "$BOARD_ISSUE" "$(printf '%s' "$body" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')" \
  >> "$DEADLETTER"

echo "WARN: estate board post failed; row dead-lettered to $DEADLETTER" >&2
exit 75
