#!/usr/bin/env bash
# The tracked issue's boxes, and who is allowed to have ticked them.
[ -n "${CREW_ISSUE_REPO:-}" ] && [ -n "${CREW_ISSUE:-}" ] || { echo "set CREW_ISSUE_REPO=owner/name and CREW_ISSUE=<number>"; exit 2; }
echo "\$ gh issue view $CREW_ISSUE --repo $CREW_ISSUE_REPO --json number,state"
gh issue view "$CREW_ISSUE" --repo "$CREW_ISSUE_REPO" --json number,state || exit 2
body="$(gh issue view "$CREW_ISSUE" --repo "$CREW_ISSUE_REPO" --json body -q .body)" || exit 2
total=$(printf '%s' "$body" | grep -cE '^- \[[ x]\].*CP[0-9]')
done=$(printf '%s' "$body" | grep -cE '^- \[x\].*CP[0-9]')
echo "checkpoints: $done of $total ticked"
printf '%s' "$body" | grep -E '^- \[[ x]\].*CP[0-9]'
[ "$total" -gt 0 ] || { echo "no checkpoints in the issue body"; exit 1; }
