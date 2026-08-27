#!/usr/bin/env bash
# crew#84: the data function's day-0 standard, as a gate. Every collected source has a
# contract (science/schemas/<source>.json) naming its owner and what it is, describing its
# fields with a PII flag, and recording how many fields were accepted undescribed.
#
#   FAIL when a source has a schema file with no owner or no description,
#   FAIL when a documented field is one the data no longer has,
#   FAIL when more fields are undescribed than the recorded baseline,
#   BLIND, printed and not failed, when a source has no schema file yet
#        (science/collect.py --write-schemas <source> writes it; --check names the source).
#
# One command; the grading lives in science/collect.py --contracts so --check and this rung
# cannot disagree.
set -uo pipefail
cd "$(dirname "$0")/../.." || exit 2
python3 science/collect.py --contracts
