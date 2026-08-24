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
if [ -z "$found" ]; then
  # Two different situations were reaching the same exit code. If a laws file is here
  # and LAW 22 has no section in it, that is a real failure. If no laws file is here at
  # all, the check never saw the thing it grades: that is CANNOT RUN (exit 2), which
  # verify.sh defines as "the check needs something this machine does not have". A CI
  # runner has no ~/AGENTS.md, so this reported the laws as broken on every pull
  # request in the repo. LAW 45: a guard that loses its evidence reports BLIND, never
  # a verdict.
  present=""
  for f in "${CANDIDATES[@]}"; do [ -f "$f" ] && present="$f"; done
  if [ -z "$present" ]; then
    echo "no laws file on this machine: none of ${CANDIDATES[*]} exists"
    echo "RESIDUAL: LAW 22's section is graded only where the laws live, which is the"
    echo "          estate laptop. Set LAWS_FILE to grade it anywhere else."
    exit 2
  fi
  echo "FAIL: LAW 22 has no section in $present"
  exit 1
fi
echo "law bodies read from $found"
