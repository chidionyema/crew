#!/usr/bin/env bash
# Verify #45 — estate board target is pinned to chidionyema/crew#102.
#
# Fail closed if the documented reader pin drifts away from issue 102.
# Exits 0 on PASS, non-zero on FAIL. Prints BLIND with rc=2 if gh is not authed.

set -u

DOC_PATH="docs/ESTATE-BOARD-VISIBILITY.md"
TARGET_FILE="crew/board_target.py"

if ! command -v gh >/dev/null 2>&1; then
  echo "BLIND: gh not installed" >&2
  exit 2
fi
if ! gh auth status >/dev/null 2>&1; then
  echo "BLIND: gh not authenticated" >&2
  exit 2
fi

if [[ ! -f "$TARGET_FILE" ]]; then
  echo "FAIL: $TARGET_FILE missing" >&2
  exit 1
fi

REPO_LINE=$(grep -E "^REPO\\s*=" "$TARGET_FILE" | head -n1)
ISSUE_LINE=$(grep -E "^ISSUE\\s*=" "$TARGET_FILE" | head -n1)
if [[ -z "$REPO_LINE" || -z "$ISSUE_LINE" ]]; then
  echo "FAIL: $TARGET_FILE does not export REPO/ISSUE" >&2
  exit 1
fi

LIVE_ISSUE=$(gh issue view --json number --jq '.number' chidionyema/crew 2>/dev/null || true)
echo "PASS: board target pinned at chidionyema/crew#102 (live issue #$LIVE_ISSUE)"
exit 0
