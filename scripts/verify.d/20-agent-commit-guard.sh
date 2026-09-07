#!/bin/bash
# This guard enforces that agent commits carry a specific trailer.
# It prevents agent commits from being indistinguishable from founder commits.

# Get the commit message from stdin
commit_message=$(cat)

# Define the required agent commit trailer
REQUIRED_TRAILER="Agent-ID:"

# Check if the commit message contains the required trailer
if ! echo "$commit_message" | grep -q "$REQUIRED_TRAILER"; then
  echo "Error: Agent commits must include the '$REQUIRED_TRAILER <agent-identifier>' trailer."
  echo "Please add this trailer to your commit message."
  exit 1
fi

exit 0