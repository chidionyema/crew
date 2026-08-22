#!/usr/bin/env bash
# A negative control: strip the evidence off the pull request, prove the gate
# says no, then put the body back. A gate nobody has watched refuse is a gate
# nobody has tested. This EDITS a real pull request, so it is opt-in.
[ "${VERIFY_ALLOW_MUTATION:-0}" = "1" ] || { echo "set VERIFY_ALLOW_MUTATION=1 to run the negative control (it edits a real PR body and restores it)"; exit 2; }
[ -n "${CREW_PR:-}" ] || { echo "set CREW_PR=<number>"; exit 2; }
command -v pr-evidence >/dev/null || { echo "pr-evidence is not on PATH"; exit 2; }

orig="$(gh pr view "$CREW_PR" --json body -q .body)" || exit 2
restore() { printf '%s' "$orig" | gh pr edit "$CREW_PR" --body-file - >/dev/null; }
trap restore EXIT

printf '%s' "$orig" \
  | python3 -c 'import sys,re;print(re.sub(r"<!-- pr-evidence -->.*?<!-- /pr-evidence -->","",sys.stdin.read(),flags=re.S).rstrip())' \
  | gh pr edit "$CREW_PR" --body-file - >/dev/null
echo "\$ pr-evidence check --pr $CREW_PR   # evidence block temporarily removed"
pr-evidence check --pr "$CREW_PR"; rc=$?
echo "rc=$rc"
[ $rc -eq 1 ] || { echo "the gate did NOT refuse an empty pull request"; exit 1; }
echo "the gate refused, and the body is restored on exit"
