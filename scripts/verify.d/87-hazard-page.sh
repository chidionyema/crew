#!/usr/bin/env bash
# crew#495 CP2: the hazard page is generated from the register. Report mode: prints the
# open-hazard and unnamed-P1 counts; FAIL only when the generator itself cannot run.
ROOT="${CREW_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
echo "\$ scripts/hazard-register"
python3 "$ROOT/scripts/hazard-register"
