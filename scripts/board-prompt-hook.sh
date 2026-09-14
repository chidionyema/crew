#!/usr/bin/env bash
# Wire from UserPromptSubmit in the claude-guards repo; this repo only owns the wrapper.
exec python3 "$(dirname "$0")/estate-board-sync.py" --stale-only