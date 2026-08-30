#!/usr/bin/env bash
# crew#668 CP1: the incident page is generated from the ledger, and a row that teaches
# nothing (no class, no guard, no receipt) is red.
set -euo pipefail
trap 'echo "88-incident-page: failed at line $LINENO" >&2' ERR
ROOT="${CREW_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
echo "\$ scripts/incident-report --check"
python3 "$ROOT/scripts/incident-report" --check
