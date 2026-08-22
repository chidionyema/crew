#!/usr/bin/env bash
# The pull request carries a screenshot. Read only.
[ -n "${CREW_PR:-}" ] || { echo "set CREW_PR=<number> to check a pull request"; exit 2; }
command -v pr-evidence >/dev/null || { echo "pr-evidence is not on PATH"; exit 2; }
echo "\$ pr-evidence check --pr $CREW_PR"
pr-evidence check --pr "$CREW_PR"
