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
        {"kind": "ledger", "path": f"{home}/dev/code/idp/state/a.jsonl", "rows": 1},
        {"kind": "ledger", "path": f"{home}/dev/code/idp/.worktrees/x/state/a.jsonl", "rows": 1},
    ])
    assert keys == ["mac/ledger/~/.claude/scripts/state/drills.jsonl",
                    "mac/ledger/~/dev/code/idp/state/a.jsonl"], keys


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
    """A pruned worktree has no `.git` to ask, so the name check must survive this change.

    crew#556 review: it is skipped because the file is covered elsewhere, not because it sits in a
    directory called `.wt-`. Both halves are asserted here, because dropping the second one is what
    blinded the register to eleven ledgers.
    """
    pruned = tmp_path / ".wt-crew69" / "state"
    pruned.mkdir(parents=True)
    (pruned / "drills.jsonl").write_text("{}\n")
    copy = {"kind": "ledger", "path": str(pruned / "drills.jsonl"), "rows": 1}
    real = {"kind": "ledger", "path": str(tmp_path / "state" / "drills.jsonl"), "rows": 1}

    assert _mac(tmp_path, [real, copy]) == [f"mac/ledger/{tmp_path}/state/drills.jsonl"]
    # and alone, it is the only record of that file: keeping it beats going blind
    assert _mac(tmp_path, [copy]) == [f"mac/ledger/{pruned}/drills.jsonl"]


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


# crew#556 review (d5ae1960, 2026-08-28): the rule above was right about what a copy IS and wrong
# about what to do with one. Measured on the live inventory: 36 rows read as copies, and 23 of them
# were the ONLY row for their file, because the Mac inventory reaches ~/dev/code/crew through the
# science and snapshot worktrees and almost nowhere else (2 of its 319 rows are under that checkout,
# both `.db`). Dropping them made the register blind to eleven science ledgers -- the failure this
# module's docstring exists to make impossible. The copies were also stale: science/ships.jsonl read
# 57 rows in both worktrees and 150 in the real ledger.
#
# Rule: dropping a copy must never drop the last row for a file. A copy resolves onto its primary
# (git answers where that is) and is restated from the file that is actually there; a copy git
# cannot place is dropped only when another row already covers the same repo-relative file.

def _git_worktree(tmp_path, name):
    """A real linked worktree, made by git, so `rev-parse --git-common-dir` can place it."""
    primary = tmp_path / "repo"
    (primary / "science").mkdir(parents=True)
    (primary / "science" / "ships.jsonl").write_text("{}\n" * 150)
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t", "HOME": str(tmp_path)}
    run = lambda *a: subprocess.run(["git", "-C", str(primary), *a], check=True,
                                    capture_output=True, env=env)
    run("init", "-q", "-b", "main")
    run("add", "-A")
    run("commit", "-qm", "x")
    wt = tmp_path / name
    run("worktree", "add", "-q", "--detach", str(wt))
    return primary, wt


def test_incident_crew556_a_copy_resolves_onto_its_primary_with_the_primary_size(tmp_path):
    """The copy says 57 rows and the real ledger holds 150: the row that survives says 150."""
    primary, wt = _git_worktree(tmp_path, "crew-science-worktree")
    (wt / "science" / "ships.jsonl").write_text("{}\n" * 57)  # a stale checkout, as on the Mac

    sys.path.insert(0, str(ROOT))
    from science.producers import _dedupe_copies

    kept = _dedupe_copies([{"kind": "ledger", "path": str(wt / "science" / "ships.jsonl"),
                            "rows": 57}])
    assert len(kept) == 1, kept
    assert kept[0]["path"] == str(primary / "science" / "ships.jsonl"), kept
    assert kept[0]["rows"] == 150, kept[0]


def test_incident_crew556_two_copies_of_one_file_collapse_to_one_row(tmp_path):
    """Deduplication still holds: crew#320's whole point, and the reason `continue` was there."""
    primary, wt1 = _git_worktree(tmp_path, "crew-science-worktree")
    subprocess.run(["git", "-C", str(primary), "worktree", "add", "-q", "--detach",
                    str(tmp_path / "crew-snapshot-worktree")], check=True, capture_output=True)
    wt2 = tmp_path / "crew-snapshot-worktree"

    sys.path.insert(0, str(ROOT))
    from science.producers import _dedupe_copies

    kept = _dedupe_copies([{"kind": "ledger", "path": str(w / "science" / "ships.jsonl"), "rows": 57}
                           for w in (wt1, wt2)])
    assert [r["path"] for r in kept] == [str(primary / "science" / "ships.jsonl")], kept


def test_incident_crew556_no_dropped_row_takes_the_last_row_for_its_file(tmp_path):
    """The property, over the machine's own inventory: for every row the walk drops, some surviving
    producer covers the same repo-relative file. This is the assertion the review asked for; it
    fails on the code that shipped in crew#556's first push (23 files lost their only row)."""
    import pytest

    sys.path.insert(0, str(ROOT))
    from science.producers import (INVENTORY, _abs, _dedupe_copies, _in_worktree, _primary_path,
                                   _worktree_root)

    if not INVENTORY.exists():
        pytest.skip(f"no inventory at {INVENTORY}; the fixture cases above still ran")
    rows = json.loads(INVENTORY.read_text()).get("rows", [])
    where = lambda r: str(r.get("path") or r.get("plist") or r.get("id") or r.get("name") or "")
    kept = _dedupe_copies(rows)
    kept_paths = {str(_abs(where(r))) for r in kept if where(r)}
    kept_where = {where(r) for r in kept}

    def covered(path):
        """Some surviving producer holds this repo-relative file: the primary git named, or any
        kept row ending in the same repo-relative tail (the only comparison available when git
        cannot place the worktree)."""
        if (primary := _primary_path(path)) and primary in kept_paths:
            return True
        wt = _worktree_root(path)
        if wt is None:
            return False
        tail = str(_abs(path).relative_to(wt))
        return any(k == tail or k.endswith("/" + tail) for k in kept_paths)

    orphans = [p for r in rows if (p := where(r)) and p not in kept_where and _in_worktree(p)
               and not covered(p)]
    assert orphans == [], f"{len(orphans)} dropped row(s) were the last one for their file: {orphans[:5]}"
