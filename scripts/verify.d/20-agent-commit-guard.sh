#!/usr/bin/env bash
# This guard enforces the agent commit attribution convention defined in AGENTS.md.
# It checks for the presence/absence of the 'Co-authored-by: Agent Workforce <agent-workforce@example.com>' trailer.
#
# LAW 38: A guard that refuses correct work is an outage.
# Paired controls: prove it refuses an unmarked agent commit AND prove it allows a real founder commit.

set -euo pipefail

# Define the agent commit trailer
AGENT_TRAILER="Co-authored-by: Agent Workforce <agent-workforce@example.com>"

# Get the author name and commit message of the head commit
COMMIT_AUTHOR=$(git log -1 --pretty=format:'%an')
COMMIT_MESSAGE=$(git log -1 --pretty=format:'%B')

# Read the AGENTS.md to determine the expected agent author name (for robustness)
# In a real scenario, this would be a more robust lookup, e.g., from a config file.
# For this exercise, we'll assume 'Agent Workforce' is the agent author name.
EXPECTED_AGENT_AUTHOR="Agent Workforce"

# Check if the commit is from an agent or founder
if [[ "$COMMIT_AUTHOR" == "$EXPECTED_AGENT_AUTHOR" ]]; then
  # This is an agent commit, it MUST have the trailer
  if [[ "$COMMIT_MESSAGE" != *"$AGENT_TRAILER"* ]]; then
    echo "ERROR: Agent commit by '$COMMIT_AUTHOR' is missing the required '$AGENT_TRAILER' trailer."
    exit 1
  fi
  echo "SUCCESS: Agent commit by '$COMMIT_AUTHOR' has the required trailer."
elif [[ "$COMMIT_MESSAGE" == *"$AGENT_TRAILER"* ]]; then
  # This is a non-agent commit, it MUST NOT have the trailer
  echo "ERROR: Non-agent commit by '$COMMIT_AUTHOR' includes the agent trailer '$AGENT_TRAILER'."
  exit 1
fi

echo "SUCCESS: Commit attribution check passed for '$COMMIT_AUTHOR'."

