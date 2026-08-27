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
present=""
for f in "${CANDIDATES[@]}"; do
  [ -f "$f" ] || continue
  present="yes"
  echo "\$ grep -n '^# LAW 22' $f"
  if grep -n "^# LAW 22" "$f"; then found="$f"; break; fi
done
# A guard that loses its evidence reports BLIND, never a verdict. On a CI runner no laws
# file exists at all, and that is not the same finding as "the file is here and LAW 22 is
# not in it". Exit 2 is the harness's CANNOT RUN, the same as gates 30/35/60/86.
[ -n "$present" ] || { echo "BLIND: no laws file on this host (${CANDIDATES[*]}); the laptop grades this check"; exit 2; }
[ -n "$found" ] || { echo "LAW 22 has no section in any of: ${CANDIDATES[*]}"; exit 1; }
echo "law bodies read from $found"
