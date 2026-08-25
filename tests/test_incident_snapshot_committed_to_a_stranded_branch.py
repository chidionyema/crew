"""Incident: the hourly snapshot committed the estate's state onto a feature branch.

Measured 2026-08-24. `scripts/estate-snapshot --commit` ran from the shared checkout
`~/dev/code/crew` and committed to whatever branch that checkout was standing on. A session
left it on `research-gateway-api-edge`, mid-merge, and the 08:34 UTC snapshot went there:

    $ git log --format='%h %ci %d %s' -2 -- STATE.md
    7b476e7 2026-08-24 09:37 +0100 (research-gateway-api-edge) chore(state): snapshot 08:34 UTC
    3b42adb 2026-08-24 07:29 +0100                             chore(state): snapshot 06:28 UTC

The first fix (2026-08-24) made the job refuse unless the shared checkout was on main.
Measured 2026-08-25: the shared checkout sat on `feat/mature-platform-gate` for 14 hours,
every hourly run refused, and STATE.md on main was 14 hours stale. Refusing was correct and
useless. The class is "a scheduled job whose output depends on where a human left a shared
checkout". The fix that removes the class: the job commits from its own worktree, detached
at origin/main, and the shared checkout's branch is never consulted.

Rules asserted here:

  1. `ready_to_commit` never asks the shared checkout which branch it is on. Every git
     command it runs is a fetch, a worktree add, or runs inside the snapshot worktree.
  2. It refuses, loudly and for a stated reason, when it cannot fetch main or cannot stand
     the worktree on origin/main.
  3. `commit` runs every step inside the snapshot worktree and pushes HEAD to main. A failed
     step is named and non-zero; a failed push never prints "committed".

Rung 4. The tests drive the functions through a fake `sh`.
"""
import importlib.util
import pathlib
import sys
from importlib.machinery import SourceFileLoader

import pytest

SNAPSHOT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "estate-snapshot"


def _load():
    spec = importlib.util.spec_from_file_location(
        "estate_snapshot", SNAPSHOT, loader=SourceFileLoader("estate_snapshot", str(SNAPSHOT)))
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["estate_snapshot"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def snap(tmp_path, monkeypatch):
    mod = _load()
    monkeypatch.setattr(mod, "SNAP_WT", tmp_path / "wt")
    return mod


class _Git:
    """A fake shell. Records every command; fails the ones named in `fail`."""
    def __init__(self, fail=()):
        self.fail, self.ran = set(fail), []

    def __call__(self, cmd: str, timeout: int = 30):
        self.ran.append(cmd)
        if "rev-parse --abbrev-ref HEAD" in cmd:
            raise AssertionError(f"the shared checkout's branch was consulted: {cmd}")
        for key in self.fail:
            if key in cmd:
                return 1, f"fake failure at {key}"
        if "worktree add" in cmd:
            wt = cmd.split("worktree add --detach -q '")[1].split("'")[0]
            (pathlib.Path(wt) / ".git").parent.mkdir(parents=True, exist_ok=True)
            (pathlib.Path(wt) / ".git").write_text("gitdir: fake")
        if "git log --oneline -1" in cmd:
            return 0, "deadbee chore(state): estate snapshot"
        return 0, ""


def test_incident_the_shared_checkouts_branch_is_never_consulted(snap):
    """The incident branch, and the 14-hour stall, both came from asking the shared
    checkout where it stood. With the fake raising on that question, a clean run proves
    the question is no longer asked."""
    git = _Git(); snap.sh = git
    assert snap.ready_to_commit() == ""
    inside = [c for c in git.ran if "worktree add" not in c and "git fetch" not in c]
    assert inside and all(str(snap.SNAP_WT) in c for c in inside), git.ran


def test_it_creates_the_worktree_once_and_then_reuses_it(snap):
    git = _Git(); snap.sh = git
    assert snap.ready_to_commit() == ""
    assert sum("worktree add" in c for c in git.ran) == 1
    git.ran.clear()
    assert snap.ready_to_commit() == ""
    assert not any("worktree add" in c for c in git.ran)


@pytest.mark.parametrize("step,word", [("git fetch", "fetch"), ("worktree add", "worktree"),
                                       ("checkout -q --detach", "origin/main")])
def test_it_refuses_for_a_stated_reason_when_it_cannot_stand_on_main(snap, step, word):
    snap.sh = _Git(fail=[step])
    why = snap.ready_to_commit()
    assert why and word in why, why


def test_commit_runs_in_the_worktree_and_pushes_head_to_main(snap, capsys):
    git = _Git(); snap.sh = git
    assert snap.commit("2026-08-25 18:00 UTC") == 0
    assert all(str(snap.SNAP_WT) in c for c in git.ran), git.ran
    assert any(f"git push -q origin HEAD:{snap.BRANCH}" in c for c in git.ran)
    assert "committed and pushed to main" in capsys.readouterr().out


def test_a_failed_push_is_named_and_non_zero(snap, capsys):
    """The silent success from the incident: a failed push must never print committed."""
    snap.sh = _Git(fail=["git push"])
    assert snap.commit("2026-08-25 18:00 UTC") == 1
    out = capsys.readouterr().out
    assert "SNAPSHOT NOT COMMITTED. Failed at: push" in out and "committed and pushed" not in out


def test_the_branch_it_writes_to_is_named_once(snap):
    assert snap.BRANCH == "main"
