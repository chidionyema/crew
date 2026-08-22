#!/usr/bin/env bash
# LAW 22 has a section in the laws file, not just a passing mention.
LAWS="${LAWS_FILE:-$HOME/AGENTS.md}"
echo "\$ grep -n '^# LAW 22' $LAWS"
[ -f "$LAWS" ] || { echo "no laws file at $LAWS"; exit 2; }
grep -n "^# LAW 22" "$LAWS" || exit 1
