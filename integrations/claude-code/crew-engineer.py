#!/usr/bin/env python3
"""Wire B: engineering claims a checkpoint and posts evidence, with no person typing.

    crew-engineer.py                 # the next unfinished checkpoint
    crew-engineer.py CP3             # a named one
    crew-engineer.py --dry-run       # say what it would do, touch nothing

Four steps, in order: read the board, claim the next unfinished checkpoint, run
that checkpoint's test, post what the runner said. Then stop.

It never ticks a box, and it holds no code path that could. That is not a
promise in a comment — the checkpoint test greps this file for the qa command
and fails if it is here, so the guarantee survives whoever edits it next.
Ticking is the qa role's, on a machine this one does not control.

It does not write code either. An agent does that; this runs the loop around it,
which is the part that was costing a person four commands per checkpoint. When
the test is still red it posts the failing output as evidence and exits 1, so
what to build next is on the board rather than in somebody's terminal.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CREW = "crew"


def crew(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    p = subprocess.run([CREW, *args], cwd=ROOT, capture_output=True, text=True)
    if check and p.returncode != 0:
        sys.exit(f"crew-engineer: `crew {' '.join(args)}` refused: "
                 f"{(p.stderr or p.stdout).strip()}")
    return p


def board() -> dict:
    return json.loads(crew("status", "--format", "json").stdout)


def next_open(b: dict, want: str | None) -> dict:
    todo = [c for c in b["checkpoints"] if not c["done"]]
    if want:
        for c in b["checkpoints"]:
            if c["id"].upper() == want.upper():
                if c["done"]:
                    sys.exit(f"crew-engineer: {c['id']} is already verified. Nothing to do.")
                return c
        sys.exit(f"crew-engineer: no {want} on issue #{b['issue']}")
    if not todo:
        # Every box ticked is a finished job, not a failure. Say so and exit 0.
        print(f"every checkpoint on #{b['issue']} is verified — `crew close` closes it")
        sys.exit(0)
    return todo[0]


def run_test(cp: str) -> tuple[bool, str]:
    """Run this checkpoint's own test, the same command the board records."""
    cfg = json.loads((ROOT / ".crew.json").read_text())
    cmd = cfg["bdd_command"].format(cp=cp.lower(), tag=f"@{cp.lower()}")
    p = subprocess.run(cmd, cwd=ROOT, shell=True, capture_output=True, text=True)
    return p.returncode == 0, (p.stdout + p.stderr).strip()


def main() -> int:
    ap = argparse.ArgumentParser(prog="crew-engineer.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("checkpoint", nargs="?", help="CP3, say. Default: the next unfinished one.")
    ap.add_argument("--dry-run", action="store_true", help="say what it would do, touch nothing")
    ns = ap.parse_args()

    b = board()
    cp = next_open(b, ns.checkpoint)
    cid = cp["id"]
    print(f"#{b['issue']}  {b['done']}/{b['total']} verified.  Next: {cid} — {cp['title']}")

    if ns.dry_run:
        print(f"would claim {cid}, run its test, and post the result as evidence")
        return 0

    print(crew("claim", cid).stdout.strip())

    ok, output = run_test(cid)
    tail = "\n".join(output.splitlines()[-25:])
    log = ROOT / ".crew" / f"{cid.lower()}.log"
    log.parent.mkdir(exist_ok=True)
    log.write_text(output + "\n")
    print(tail)

    summary = (f"{cid} builds and its test passes" if ok
               else f"{cid} is not built yet — its test is still red")
    print(crew("evidence", cid, "--result", "pass" if ok else "fail",
               "--summary", summary, "--log", str(log)).stdout.strip())

    if not ok:
        print(f"\ncrew-engineer: {cid} is red. The failing output is on #{b['issue']} "
              f"and in {log.relative_to(ROOT)}. Build it, then run this again.")
        return 1

    print(f"\ncrew-engineer: {cid} is green and the evidence is posted. The box is "
          f"still unticked, and stays that way until qa runs it somewhere else.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
