#!/usr/bin/env bash
# The documentation standard, enforced. Founder, 2026-08-24: "we need better dos
# nanagent, our docunentaion standards are very poor", then "tine to establish
# standards", then "this is what i nean things get lost".
#
# Measured the same day, across the seven repositories this estate owns:
#
#   documents        190
#   persisted        186 / 190     4 exist only on this laptop
#   owned              0 / 190     not one document names who maintains it
#   dated             99 / 190
#   substantial      187 / 190
#   passing all        0 / 190
#
# Four rules, and each one exists because its absence has already cost something:
#
#   persisted    tracked by git. LAW 24. An untracked document is one disk failure
#                from gone and no diff will ever show who changed it. This is the
#                literal mechanism of "things get lost".
#   owned        names a maintainer. A document nobody owns rots, and a rotted
#                document is worse than a missing one because it reads as current.
#   dated        carries a machine-readable date, so a reader can tell whether they
#                are holding something written before or after the thing it describes.
#   substantial  over 200 characters of prose once headings and fences are stripped.
#                Same floor LAW 32 already sets for demo and onboarding pages: a
#                heading with nothing under it satisfies a gate, not a reader.
#
# THE RATCHET. Turning this on against 190 failing documents would make every run red
# for weeks, and a permanently red gate is one everybody learns to skip -- LAW 38 calls
# that an outage, not a strict standard. So today's failures are recorded in
# science/DOCS-BASELINE.json as tolerated, and this gate refuses exactly two things:
#
#   1. a document that is not in the baseline and fails any rule  (new work is clean)
#   2. a document in the baseline that fails MORE rules than it did (nothing rots further)
#
# The backlog burns down by deleting lines from the baseline. It may never grow.
#
# In CI only the crew repository is checked out, so only crew's documents are graded
# there. Locally all seven are. The baseline is keyed by repo AND path, so a repo that
# is absent simply contributes nothing rather than reading as deleted.
set -uo pipefail
ROOT="${CREW_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
cd "$ROOT" || exit 2

echo "\$ python3 science/docsmap.py --json | compare against science/DOCS-BASELINE.json"
python3 - "$ROOT" <<'PY'
import json, pathlib, subprocess, sys

root = pathlib.Path(sys.argv[1])
base_path = root / "science" / "DOCS-BASELINE.json"

if not base_path.exists():
    print(f"FAIL: no baseline at {base_path}. Write one with "
          "`python3 science/docsmap.py --write-baseline science/DOCS-BASELINE.json` "
          "and commit it. Without a starting line this gate cannot tell a pre-existing "
          "failure from one introduced today, so it would refuse everything.")
    sys.exit(1)

baseline = json.loads(base_path.read_text())["tolerated"]

proc = subprocess.run([sys.executable, str(root / "science" / "docsmap.py"), "--json"],
                      capture_output=True, text=True)
if proc.returncode != 0:
    print(f"FAIL: docsmap.py exited {proc.returncode}\n{proc.stderr[-800:]}")
    sys.exit(1)
docs = json.loads(proc.stdout)

# Only grade repositories that are actually present. In CI six of the seven are not
# checked out, and a missing repo must read as "not graded here", never as "fixed".
present = {d["repo"] for d in docs}
graded = {k: v for k, v in baseline.items() if k.split("::", 1)[0] in present}

new_failures, regressions = [], []
for d in docs:
    key = f"{d['repo']}::{d['path']}"
    now = set(d["failures"])
    if not now:
        continue
    was = set(graded.get(key, []))
    if key not in graded:
        new_failures.append((key, sorted(now)))
    elif now - was:
        regressions.append((key, sorted(was), sorted(now)))

if new_failures:
    print(f"FAIL: {len(new_failures)} document(s) introduced that do not meet the standard.")
    for key, f in new_failures[:12]:
        print(f"  {key}")
        print(f"      missing: {', '.join(f)}")
    print()
    print("  persisted    -> git add the file. A document only this laptop holds is lost.")
    print("  owned        -> add a line `Owner: <name or role>` near the top.")
    print("  dated        -> add a YYYY-MM-DD date saying when this was last true.")
    print("  substantial  -> write more than 200 characters of actual prose, or delete it.")
    print()
    print("  This gate is a ratchet, not a wall: it never refuses a document that was")
    print("  already failing. It refused these because they are new work, and new work")
    print("  is held to the standard from the day it is written.")
    sys.exit(1)

if regressions:
    print(f"FAIL: {len(regressions)} document(s) got worse than the baseline allows.")
    for key, was, now in regressions[:12]:
        print(f"  {key}\n      was: {', '.join(was) or 'clean'}\n      now: {', '.join(now)}")
    sys.exit(1)

still = sum(1 for d in docs if d["failures"])
clean = len(docs) - still
print(f"PASS: {len(docs)} documents graded, {clean} meet the standard, "
      f"{still} on the baseline backlog, 0 new failures, 0 regressions")
PY
