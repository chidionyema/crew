"""crew#320, 2026-08-27: `datamap.py --check` was RED with 6 UNEXPLAINED producers, all copies of
`state/drills.jsonl` inside `~/.claude/scripts/.wt-crew*/` git worktrees. A worktree is a copy of
a repository; its files are not producers, and the yaml walk already skipped them (SKIP_DIRS).

Rule: the Mac inventory walk applies the same SKIP_DIRS rule to every row's path.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _mac(tmp_path, rows):
    inv = tmp_path / "inventory.json"
    inv.write_text(json.dumps({"rows": rows}))
    code = ("import json, science.producers as p; "
            "print(json.dumps(sorted(x['key'] for x in p.mac())))")
    out = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True,
                         env={**os.environ, "ESTATE_INVENTORY": str(inv)}, check=True).stdout
    return json.loads(out)


def test_incident_crew320_a_worktree_copy_is_skipped_and_the_original_is_kept(tmp_path):
    home = str(Path.home())
    keys = _mac(tmp_path, [
        {"kind": "ledger", "path": f"{home}/.claude/scripts/state/drills.jsonl", "rows": 3},
        {"kind": "ledger", "path": f"{home}/.claude/scripts/.wt-crew69/state/drills.jsonl", "rows": 3},
        {"kind": "ledger", "path": f"{home}/dev/code/idp/.worktrees/x/state/a.jsonl", "rows": 1},
    ])
    assert keys == ["mac/ledger/~/.claude/scripts/state/drills.jsonl"], keys
