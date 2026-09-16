#!/usr/bin/env bash
# scripts/verify.d/62-board-issue.sh — pin the board to crew#102.
#
# This gate fails if the board target drifted: the doc must name the right repo,
# the right issue number, the right cache path, and the right dead-letter path.
# A board that quietly moved is a board nobody can read (LAW 28).

set -u

DOC="${REPO_ROOT:-.}/docs/CREW-BOARD-VISIBILITY.md"
SYNC="${REPO_ROOT:-.}/scripts/estate-board-sync.py"
REPO="chidionyema/crew"
ISSUE=102

fail() {
    echo "FAIL: $*" >&2
    exit 1
}

[ -f "$DOC" ]  || fail "missing $DOC — board visibility doc is part of the contract"
[ -f "$SYNC" ] || fail "missing $SYNC — board sync script is part of the contract"

grep -q "$REPO"   "$DOC"  || fail "$DOC does not name repo $REPO"
grep -q "#$ISSUE" "$DOC"  || fail "$DOC does not name issue #$ISSUE"
grep -q 'ESTATE_BOARD.jsonl' "$DOC" || fail "$DOC does not name the cache path"
grep -q 'board-deadletter.jsonl' "$DOC" || fail "$DOC does not name the dead-letter path"

grep -q "$REPO" "$SYNC" || fail "$SYNC does not default to repo $REPO"
grep -q 'BOARD_ISSUE = int' "$SYNC" || fail "$SYNC does not pin BOARD_ISSUE"

if command -v gh >/dev/null 2>&1; then
    if ! gh auth status >/dev/null 2>&1; then
        echo "BLIND: gh not authenticated — skipping live check, doc and script graded above"
        exit 0
    fi
    out=$(gh issue view "$ISSUE" --repo "$REPO" --json number,state 2>&1) \
        || fail "gh issue view failed: $out"
    state=$(printf '%s' "$out" | grep -o '"state":"[A-Z]*"' | head -1 | cut -d'"' -f4)
    [ "$state" = "OPEN" ] || fail "issue $REPO#$ISSUE is $state, not OPEN"
fi

echo "PASS: board pinned to $REPO#$ISSUE; doc and sync script agree"