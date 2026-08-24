#!/usr/bin/env bash
# LAW 41: a buyer arrives tomorrow and reads the risks before the features.
# This check makes the register mechanical rather than a document somebody
# remembers to update.
#
#   FAIL when the register is missing or any line is not JSON,
#   FAIL when a row lacks a required field,
#   FAIL when a row claims mitigated or closed with no evidence command,
#   FAIL when a row's evidence names a program that does not exist, because an
#        unrunnable receipt is the same as no receipt,
#   FAIL when every row is still open, which means nothing has been worked.
#
# It deliberately does NOT run the evidence commands. Some of them are drills
# that take minutes and touch credentials, and a verifier that is expensive is
# a verifier that gets skipped. What it checks is that each receipt could be
# run by somebody who does not know the estate.
REG="${CREW_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}/risk/REGISTER.jsonl"
echo "\$ python3 - $REG"
python3 - "$REG" <<'PY'
import json, os, shutil, sys

path = sys.argv[1]
try:
    lines = [l for l in open(path, encoding="utf-8") if l.strip()]
except OSError:
    print(f"FAIL: no risk register at {path}")
    sys.exit(1)

required = {"id", "opened", "title", "what_goes_wrong", "likelihood", "cost",
            "mitigation", "residual", "owner", "evidence", "status"}
seen_ids = set()
worked = 0

for i, line in enumerate(lines, 1):
    try:
        r = json.loads(line)
    except json.JSONDecodeError as e:
        print(f"FAIL: line {i} is not JSON ({e})")
        sys.exit(1)

    missing = required - r.keys()
    if missing:
        print(f"FAIL: {r.get('id', f'line {i}')} lacks {sorted(missing)}")
        sys.exit(1)

    if r["id"] in seen_ids:
        print(f"FAIL: {r['id']} appears twice")
        sys.exit(1)
    seen_ids.add(r["id"])

    if r["status"] not in ("open", "mitigated", "closed", "accepted"):
        print(f"FAIL: {r['id']} has status {r['status']!r}, "
              "expected open, mitigated, closed or accepted")
        sys.exit(1)

    if r["status"] in ("mitigated", "closed") and not r["evidence"].strip():
        print(f"FAIL: {r['id']} claims {r['status']} with no evidence command")
        sys.exit(1)
    if r["status"] in ("mitigated", "closed"):
        worked += 1

    # The first token of the evidence line has to be something that exists.
    # Expand ~ because a receipt written for a person will use it.
    prog = os.path.expanduser(r["evidence"].strip().split()[0])
    if not (shutil.which(prog) or os.path.isfile(prog)):
        print(f"FAIL: {r['id']} evidence starts with {prog!r}, which is not on "
              "PATH and is not a file -- nobody can run this receipt")
        sys.exit(1)

if not lines:
    print("FAIL: the risk register is empty")
    sys.exit(1)

if worked == 0:
    print(f"FAIL: all {len(lines)} risks are still open -- a register that only "
          "grows is a list of complaints, not a register")
    sys.exit(1)

print(f"PASS: {len(lines)} risks, {worked} mitigated or closed, every receipt runnable")
PY
