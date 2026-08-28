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


def test_crew558_a_worktree_named_nothing_like_the_pattern_is_still_skipped(tmp_path):
    """2026-08-28: the gate went RED with 11 UNEXPLAINED producers, every one of them a ledger
    inside `~/.claude/state/crew-science-worktree` -- a git worktree `scripts/science-collect`
    creates on every run, and a name the `.wt-`/`.worktrees` list never matched. The name was a
    proxy for the thing. Git marks a worktree by writing `.git` as a FILE; that is the test now.
    """
    wt = tmp_path / "state" / "some-checkout"
    wt.mkdir(parents=True)
    (wt / ".git").write_text("gitdir: /Users/x/dev/code/crew/.git/worktrees/some-checkout\n")
    real = tmp_path / "dev" / "crew"
    (real / ".git").mkdir(parents=True)          # a normal checkout: .git is a directory
    keys = _mac(tmp_path, [
        {"kind": "ledger", "path": str(wt / "science" / "ships.jsonl"), "rows": 3},
        {"kind": "ledger", "path": str(real / "science" / "ships.jsonl"), "rows": 3},
    ])
    assert len(keys) == 1 and keys[0].endswith("dev/crew/science/ships.jsonl"), keys
