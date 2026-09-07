#!/bin/bash
# This script lists commits that are considered founder decisions.
# It filters out commits that contain the 'Agent-ID:' trailer.

# Use git log to get all commit messages and filter out those with the Agent-ID trailer
git log --pretty=format:"%h %an: %s" --no-merges | grep -v "Agent-ID:"

exit 0