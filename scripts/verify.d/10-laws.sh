#!/usr/bin/env bash
# LAW 22 has a section in the laws file, not just a passing mention.
#
# Which file that is stopped being a constant at 03:37 on 2026-08-24, when the 42 law
# bodies moved out of ~/AGENTS.md into ~/AGENTS-FULL.md to cut about 80 KB off every
# session's injected context. This check named one path and started failing within the
# hour, on a good change. Ask which file carries the bodies; do not assume.
set -u
CANDIDATES=("${LAWS_FILE:-$HOME/AGENTS.md}" "$HOME/AGENTS-FULL.md")
found=""
for f in "${CANDIDATES[@]}"; do
  [ -f "$f" ] || continue
  echo "\$ grep -n '^# LAW 22' $f"
  if grep -n "^# LAW 22" "$f"; then found="$f"; break; fi
done
[ -n "$found" ] || { echo "LAW 22 has no section in any of: ${CANDIDATES[*]}"; exit 1; }
echo "law bodies read from $found"
