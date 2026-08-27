"""Incident test, crew#465: a store inside a linked git worktree is covered by the main checkout.

2026-08-27: five worktrees of ~/.claude/scripts each held a copy of state/drills.jsonl, and
`collect.py --check` exited 1 with "6 store(s) in neither SOURCES nor DECLINED" although the
main checkout's file was declared. The rule: a path whose worktree root carries a `.git` file
pointing at `<main>/.git/worktrees/<name>` is the same store as `<main>/<relative path>`.
Both ways in one run (LAW 45 step 3): the worktree copy is covered, a plain stray copy with no
worktree marker is still undeclared. Rung 4.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "science"))
import collect


def test_a_worktree_copy_is_covered_and_a_plain_copy_is_not(tmp_path, monkeypatch):
    main = tmp_path / "scripts"
    (main / ".git" / "worktrees" / "wt1").mkdir(parents=True)
    (main / "state").mkdir()
    (main / "state" / "drills.jsonl").write_text('{"at": "2026-08-27T00:00:00Z"}\n')
    wt = tmp_path / ".wt-crew1"
    (wt / "state").mkdir(parents=True)
    (wt / ".git").write_text(f"gitdir: {main / '.git' / 'worktrees' / 'wt1'}\n")
    (wt / "state" / "drills.jsonl").write_text('{"at": "2026-08-27T00:00:00Z"}\n')
    stray = tmp_path / "copy"
    (stray / "state").mkdir(parents=True)
    (stray / "state" / "drills.jsonl").write_text('{"at": "2026-08-27T00:00:00Z"}\n')

    assert collect._through_worktree(wt / "state" / "drills.jsonl") == main / "state" / "drills.jsonl"
    assert collect._through_worktree(stray / "state" / "drills.jsonl") is None

    inv = tmp_path / "inventory.json"
    inv.write_text(json.dumps({"rows": [
        {"id": "wt/state/drills.jsonl", "path": str(wt / "state" / "drills.jsonl"), "kind": "ledger"},
        {"id": "copy/state/drills.jsonl", "path": str(stray / "state" / "drills.jsonl"), "kind": "ledger"},
    ]}))
    monkeypatch.setattr(collect, "INVENTORY", inv)
    monkeypatch.setattr(collect, "SOURCES", {"drills": (main / "state" / "drills.jsonl", "jsonl", "at")})
    monkeypatch.setattr(collect, "DECLINED", {})
    monkeypatch.setattr(collect, "DECLINED_DIRS", {})
    undeclared, _stale, _blind, note = collect.reconcile()
    assert note == ""
    assert [u["id"] for u in undeclared] == ["copy/state/drills.jsonl"]
