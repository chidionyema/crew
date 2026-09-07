#!/usr/bin/env bash
# This script lists commits attributed to the founder by filtering out agent commits.
# Agent commits are identified by the 'Co-authored-by: Agent Workforce <agent-workforce@example.com>' trailer.
#
# Usage: scripts/founder-decisions.sh [git log options]

set -euo pipefail

AGENT_TRAILER_REGEX="Co-authored-by: Agent Workforce <agent-workforce@example.com>"

# Use git log to show commits, filtering out those with the agent trailer
# --invert-grep: Show all lines that do not match the grep pattern
# -i: Ignore case when matching
# -E: Use extended regex
# --grep: Match commit messages that contain the pattern

git log --invert-grep -i -E --grep="$AGENT_TRAILER_REGEX" "$@"
