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


# crew#320, 2026-08-28 (09cd04a6): RED again, 11 UNEXPLAINED producers, and every one of them was
# a second copy of a registered crew ledger inside `~/.claude/state/crew-science-worktree` -- the
# detached worktree `scripts/science-collect:68` keeps so the contract check runs main's collect.py
# (crew#90). The rule above graded the directory NAME, and a name is a proxy: that worktree is
# called `crew-science-worktree`, so it walked past `.wt-` and `.worktrees` untouched.
#
# Rule: a path is a copy when git says the directory it sits in is a linked worktree -- a linked
# worktree's `.git` is a regular file, a primary checkout's `.git` is a directory -- whatever the
# directory happens to be called. The name check stays for a worktree whose `.git` was pruned.

def _worktree(root, name):
    """A linked git worktree the way git lays one out on disk: `.git` is a file, not a directory."""
    wt = root / name
    (wt / "science").mkdir(parents=True)
    (wt / ".git").write_text("gitdir: /somewhere/.git/worktrees/" + name + "\n")
    (wt / "science" / "ships.jsonl").write_text("{}\n")
    return wt


def _checkout(root, name):
    """A primary checkout: `.git` is a directory."""
    co = root / name
    (co / "science").mkdir(parents=True)
    (co / ".git").mkdir()
    (co / "science" / "ships.jsonl").write_text("{}\n")
    return co


def test_incident_crew320_a_worktree_whose_name_is_not_dot_wt_is_still_a_copy(tmp_path):
    """The 2026-08-28 instance: the name says nothing, git's on-disk shape says everything."""
    real = _checkout(tmp_path, "crew")
    copy = _worktree(tmp_path, "crew-science-worktree")
    keys = _mac(tmp_path, [
        {"kind": "ledger", "path": str(real / "science" / "ships.jsonl"), "rows": 9},
        {"kind": "ledger", "path": str(copy / "science" / "ships.jsonl"), "rows": 9},
    ])
    assert keys == [f"mac/ledger/{real}/science/ships.jsonl"], keys


def test_incident_crew320_a_worktree_with_no_dot_git_left_is_still_skipped_by_name(tmp_path):
    """A pruned worktree has no `.git` to ask, so the name check must survive this change."""
    pruned = tmp_path / ".wt-crew69" / "state"
    pruned.mkdir(parents=True)
    (pruned / "drills.jsonl").write_text("{}\n")
    assert _mac(tmp_path, [{"kind": "ledger", "path": str(pruned / "drills.jsonl"), "rows": 1}]) == []


def test_incident_crew320_the_live_science_worktree_is_read_as_a_copy():
    """The regression itself, against the machine rather than a fixture. Skips where it is absent
    (a CI runner has no such worktree); the fixture tests above still assert the rule."""
    import pytest

    sys.path.insert(0, str(ROOT))
    from science.producers import _in_worktree

    live = Path.home() / ".claude" / "state" / "crew-science-worktree"
    if not (live / ".git").exists():
        pytest.skip(f"no science worktree at {live}; the fixture cases still ran")
    assert _in_worktree(f"{live}/science/ships.jsonl")
    # the inventory writes keys with the home directory folded to `~`, and the domain prefix on
    # the front; both forms must resolve to the same answer
    assert _in_worktree("mac/ledger/~/.claude/state/crew-science-worktree/science/ships.jsonl")
    assert not _in_worktree(f"{Path.home()}/dev/code/crew/science/ships.jsonl")
