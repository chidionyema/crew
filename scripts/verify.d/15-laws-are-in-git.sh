#!/usr/bin/env bash
# LAW 24: the laws themselves are in a repository.
#
# Measured 2026-08-24: `git -C ~ rev-parse --show-toplevel` returns "fatal: not a git
# repository", so ~/AGENTS.md (20,955 bytes) and ~/AGENTS-FULL.md (106,227 bytes) had
# no history, no backup and no diff anywhere. 10-laws.sh next door checks that a law
# has a body. This one checks that the body survives the laptop.
#
# It grades the bytes, with cmp, not a line count or a timestamp.
#
# It SKIPS rather than fails where no live law file exists — CI, a fresh clone, a
# container. A gate that refuses a correct machine is an outage (LAW 38).
set -u
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

if [ ! -f "$HOME/AGENTS.md" ] && [ ! -f "$HOME/AGENTS-FULL.md" ]; then
  echo "no law files on this machine — nothing to back up, skipping"
  exit 0
fi

echo "\$ bin/laws-sync --check"
"$REPO/bin/laws-sync" --check
