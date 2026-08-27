"""Incident: the hourly snapshot committed the estate's state onto a feature branch.

Measured 2026-08-24. `scripts/estate-snapshot --commit` runs hourly from the shared
checkout `~/dev/code/crew` and committed to whatever branch that checkout was standing
on. A session left it on `research-gateway-api-edge`, mid-merge and conflicted, so this
is where the 08:34 UTC snapshot went:

    $ git log --format='%h %ci %d %s' -2 -- STATE.md
    7b476e7 2026-08-24 09:37 +0100 (research-gateway-api-edge) chore(state): snapshot 08:34 UTC
    3b42adb 2026-08-24 07:29 +0100                             chore(state): snapshot 06:28 UTC

STATE.md on main was two and a half hours stale. It is the file every session is told to
read before measuring anything or asking the founder anything -- it exists so that six
sessions which cannot see each other stop re-measuring the same estate. While it was
stale, every session reading it was reading a stale estate and none of them could tell.

The job reported nothing wrong. It committed, exited 0, and printed "committed:" -- from
a separate `git log -1` that runs whatever the commit chain did, so a failed push and a
successful one printed the same line. It never asked where it was.

Two rules, asserted here rather than described:

  1. It refuses to commit unless the checkout is on main with no merge in progress. A
     snapshot not written is visible in the timestamp; a snapshot written somewhere else
     looks exactly like success.
  2. A refusal is loud and non-zero. The failure that hid for two and a half hours was a
     silent success, so silence is the thing being removed.

Rung 4. The tests drive `ready_to_commit()` through a fake `sh`, because the real one
answers about whichever checkout the suite happens to run in -- which is the bug.
"""
import importlib.util
import pathlib
import sys
from importlib.machinery import SourceFileLoader

import pytest

SNAPSHOT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "estate-snapshot"


def _load():
    """Import the script by path. It has no .py extension, so it needs an explicit loader.

    That missing extension is not incidental: it is why `scripts/verify.d/15-code-standard.sh`
    could not see this file at all, which is tracked separately.
    """
    spec = importlib.util.spec_from_file_location(
        "estate_snapshot", SNAPSHOT, loader=SourceFileLoader("estate_snapshot", str(SNAPSHOT)))
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["estate_snapshot"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def snap():
    return _load()


def _fake_sh(branch: str, merging: bool = False, status: str = ""):
    """Answer the three questions `ready_to_commit` asks, and fail loudly on any other."""
    def sh(cmd: str, timeout: int = 30):
        if "rev-parse --abbrev-ref HEAD" in cmd:
            return 0, branch
        if "MERGE_HEAD" in cmd:
            return (0, "abc123") if merging else (1, "")
        if "status --porcelain" in cmd:
            return 0, status
        raise AssertionError(f"ready_to_commit ran an unexpected command: {cmd}")
    return sh


def test_incident_it_refuses_to_commit_the_snapshot_to_a_feature_branch(snap, monkeypatch):
    monkeypatch.setattr(snap, "sh", _fake_sh("research-gateway-api-edge"))
    why = snap.ready_to_commit()
    assert why, "the exact branch from the incident was accepted"
    assert "research-gateway-api-edge" in why, "a refusal that does not name the branch"
    assert "main" in why


def test_incident_it_refuses_while_a_merge_is_in_progress(snap, monkeypatch):
    """The checkout was also mid-merge. A snapshot inside someone's half-finished merge
    is worse than a stale one: it is a stale one that also has to be untangled."""
    monkeypatch.setattr(snap, "sh", _fake_sh("main", merging=True))
    assert "merge" in snap.ready_to_commit()


def test_on_main_with_no_merge_it_permits(snap, monkeypatch):
    """The control. A guard only ever seen refusing has not been shown to permit, and a
    guard that refuses correct work is an outage (LAW 38) -- this is the case where the
    hourly job must go through."""
    monkeypatch.setattr(snap, "sh", _fake_sh("main"))
    assert snap.ready_to_commit() == ""


def test_it_refuses_when_it_cannot_read_the_branch_at_all(snap, monkeypatch):
    """Not-on-main and cannot-tell must both refuse, and for stated reasons.

    The same collapse as science/collect.py's Path.exists(): a checker that cannot reach
    a verdict must not report the convenient one. Here the convenient one is "carry on".
    """
    def sh(cmd: str, timeout: int = 30):
        return 128, "fatal: not a git repository"
    monkeypatch.setattr(snap, "sh", sh)
    why = snap.ready_to_commit()
    assert why and "cannot read" in why


def test_the_branch_it_writes_to_is_named_once(snap):
    """Three commands in `commit()` name the branch. If they ever disagree the job pushes
    somewhere other than where it fast-forwarded from, which is this incident again."""
    assert snap.BRANCH == "main"
