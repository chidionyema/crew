"""Incident: the registry could not decline a tool that names each file after a fresh UUID.

Measured 2026-08-24 on merged `origin/main`, `scripts/verify.d/25-source-registry.sh`:

    UNDECLARED, 14 store(s) the crawl found and this registry has never heard of:
      .estate/dagster/history/runs/index.db                      0.86 MB
      .estate/dagster/history/runs/ecd95ecf-3235-4c6d-9d78-668cd 0.42 MB
      ...
      .estate/dagster/schedules/schedules.db                     0.08 MB

Dagster had been stood up on the machine and its run store writes one SQLite file per run,
named after the run's UUID. `DECLINED` matched a crawl id exactly, so the only way to
answer the gate was to paste 14 UUIDs into the registry -- which the next Dagster run
invalidates, and which the stale-decline check then reports as ghosts once those runs are
cleaned up. An exclusion that has to be restated every run is not an exclusion; it is a
chore, and a chore in front of a gate is how the gate gets switched off (LAW 38).

These tests assert the rule, not the implementation: an exclusion may name a directory, it
covers everything beneath that directory however the files are named, and it is stale when
the directory is gone rather than when a given crawl happens to find nothing in it.
"""
import json
import os
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from science import collect


def _crawl(tmp_path: pathlib.Path, paths: list[pathlib.Path]) -> pathlib.Path:
    """An inventory in the shape the real crawler writes, listing `paths` as stores."""
    rows = [{"id": str(p), "path": str(p), "kind": "data", "rows": 1,
             "mb": 0.1, "member_of": None} for p in paths]
    f = tmp_path / "inventory.json"
    f.write_text(json.dumps({"rows": rows}))
    return f


@pytest.fixture
def registry(monkeypatch, tmp_path):
    """Point `reconcile` at an empty registry and a crawl of our own making."""
    def _install(declined: dict, declined_dirs: dict, inventory: pathlib.Path):
        monkeypatch.setattr(collect, "SOURCES", {})
        monkeypatch.setattr(collect, "DECLINED", declined)
        monkeypatch.setattr(collect, "DECLINED_DIRS", declined_dirs)
        monkeypatch.setattr(collect, "INVENTORY", inventory)
    return _install


def test_a_decline_naming_a_directory_covers_every_file_under_it(registry, tmp_path):
    runs = tmp_path / "dagster" / "history" / "runs"
    runs.mkdir(parents=True)
    files = [runs / f"{u}.db" for u in ("ecd95ecf-3235", "7ade27f1-70fb", "4e9fba61-7562")]
    files.append(tmp_path / "dagster" / "schedules.db")
    for f in files:
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("")

    registry({"dagster": "the orchestrator's own bookkeeping"},
             {"dagster": tmp_path / "dagster"},
             _crawl(tmp_path, files))

    undeclared, stale, _blind, note = collect.reconcile()
    assert note == ""
    assert undeclared == [], f"a covered file was still reported undeclared: {undeclared}"
    assert stale == []


def test_the_same_files_are_undeclared_without_the_directory_decline(registry, tmp_path):
    """The oracle for the test above: without the rule, every one of them is a finding."""
    runs = tmp_path / "dagster" / "history" / "runs"
    runs.mkdir(parents=True)
    files = [runs / f"{u}.db" for u in ("ecd95ecf-3235", "7ade27f1-70fb")]
    for f in files:
        f.write_text("")

    registry({}, {}, _crawl(tmp_path, files))

    undeclared, _stale, _blind, _note = collect.reconcile()
    assert len(undeclared) == len(files)


def test_a_sibling_directory_with_a_shared_prefix_is_not_swallowed(registry, tmp_path):
    """`dagster-scratch` is not inside `dagster`. Containment, not string prefix.

    A decline that quietly covered the neighbour would hide a real store, which is the
    failure this whole registry exists to prevent.
    """
    (tmp_path / "dagster").mkdir()
    sibling = tmp_path / "dagster-scratch"
    sibling.mkdir()
    stray = sibling / "facts.jsonl"
    stray.write_text("")

    registry({"dagster": "the orchestrator's own bookkeeping"},
             {"dagster": tmp_path / "dagster"},
             _crawl(tmp_path, [stray]))

    undeclared, _stale, _blind, _note = collect.reconcile()
    assert [u["path"] for u in undeclared] == [str(stray)]


def test_a_directory_decline_is_not_stale_on_a_night_the_tool_did_not_run(registry, tmp_path):
    """The directory exists and is empty. That is a quiet night, not a ghost."""
    (tmp_path / "dagster").mkdir()

    registry({"dagster": "the orchestrator's own bookkeeping"},
             {"dagster": tmp_path / "dagster"},
             _crawl(tmp_path, []))

    _undeclared, stale, _blind, _note = collect.reconcile()
    assert stale == []


def test_a_directory_decline_is_stale_once_the_directory_is_gone(registry, tmp_path):
    """The other direction. An exclusion for something no longer there is a ghost."""
    registry({"dagster": "the orchestrator's own bookkeeping"},
             {"dagster": tmp_path / "never-existed"},
             _crawl(tmp_path, []))

    _undeclared, stale, _blind, _note = collect.reconcile()
    assert stale == ["dagster"]


def test_an_id_decline_still_behaves_exactly_as_before(registry, tmp_path):
    """LAW 38. The thirteen exclusions already in the registry name an id and no path."""
    store = tmp_path / "telemetry.jsonl"
    store.write_text("")

    registry({str(store): "the vendor's own failed uploads"}, {}, _crawl(tmp_path, [store]))

    undeclared, stale, _blind, _note = collect.reconcile()
    assert undeclared == []
    assert stale == []


def test_a_directory_decline_still_needs_a_reason(tmp_path):
    """The rule that was already there is not weakened by the one being added."""
    reg = {"roots": {"t": str(tmp_path)},
           "sources": [],
           "declined": [{"id": "dagster", "root": "t", "path": "dagster", "reason": "  "}]}
    f = tmp_path / "sources.json"
    f.write_text(json.dumps(reg))

    with pytest.raises(SystemExit) as e:
        collect.load_registry(f)
    assert "with no reason" in str(e.value)


def test_a_directory_decline_against_an_unknown_root_is_refused(tmp_path):
    """Silently resolving it against $HOME would decline a directory nobody named."""
    reg = {"roots": {},
           "sources": [],
           "declined": [{"id": "dagster", "root": "nowhere", "path": "dagster",
                         "reason": "the orchestrator's own bookkeeping"}]}
    f = tmp_path / "sources.json"
    f.write_text(json.dumps(reg))

    with pytest.raises(SystemExit) as e:
        collect.load_registry(f)
    assert "unknown root" in str(e.value)


def test_the_live_registry_declines_the_dagster_run_store_by_directory(registry):
    """The incident itself, against the registry as it ships."""
    assert "dagster-run-store" in collect.DECLINED
    assert "dagster-run-store" in collect.DECLINED_DIRS
    assert collect.DECLINED_DIRS["dagster-run-store"].name == "dagster"


#: Second incident, in the same function, found in review by session chidionyema-7e before
#: this merged: the staleness rule above answered "gone" for a directory it could not read.
#: `Path.exists()` returns False for a permission error, an unmounted volume and a network
#: filesystem that timed out, exactly as it does for a directory that is not there -- so an
#: exclusion whose directory was merely unreachable reported as a ghost, and a ghost is dead
#: wood somebody deletes. Deleting it makes the registry go red on the next run, which is
#: the failure the directory exclusion was added to stop.
#:
#: Three checks on this estate collapsed the same two facts on 2026-08-24: an escrow check
#: printed NOT PRESENT for a permission error, a database drill printed corruption for
#: SQLITE_CANTOPEN on a locked file, and a research pass called a file unmerged after
#: looking at one branch. The rule these assert is that a checker never reports the verdict
#: it could not reach.


@pytest.fixture
def unreadable(tmp_path):
    """A directory whose parent denies traversal, restored however the test ends."""
    parent = tmp_path / "locked"
    target = parent / "dagster"
    target.mkdir(parents=True)
    parent.chmod(0o000)
    try:
        yield target
    finally:
        parent.chmod(0o755)


@pytest.mark.skipif(os.geteuid() == 0,
                    reason="root traverses a 0o000 directory, so the error cannot be staged")
def test_incident_a_decline_we_cannot_read_is_not_reported_as_a_ghost(
        registry, tmp_path, unreadable):
    registry({"dagster": "the orchestrator's own bookkeeping"},
             {"dagster": unreadable},
             _crawl(tmp_path, []))

    _undeclared, stale, blind, _note = collect.reconcile()
    assert stale == [], ("an exclusion this run could not read was called a ghost; "
                         "the next person deletes it and the gate goes red")
    assert blind == ["dagster"], "a blind spot has to be said out loud, not swallowed"


@pytest.mark.skipif(os.geteuid() == 0,
                    reason="root traverses a 0o000 directory, so the error cannot be staged")
def test_incident_unreadable_and_gone_do_not_produce_the_same_verdict(
        registry, tmp_path, unreadable):
    """The oracle for the test above: the two cases must not be indistinguishable."""
    registry({"dagster": "the orchestrator's own bookkeeping"},
             {"dagster": unreadable}, _crawl(tmp_path, []))
    _u, stale_blind, blind_blind, _n = collect.reconcile()

    registry({"dagster": "the orchestrator's own bookkeeping"},
             {"dagster": tmp_path / "never-existed"}, _crawl(tmp_path, []))
    _u, stale_gone, blind_gone, _n = collect.reconcile()

    assert (stale_blind, blind_blind) == ([], ["dagster"])
    assert (stale_gone, blind_gone) == (["dagster"], [])


def test_incident_a_directory_under_an_unreachable_parent_is_blind_not_gone(
        registry, tmp_path):
    """An unmounted volume raises FileNotFoundError, the same as a deleted directory.

    Demonstrated by session chidionyema-73 on a real disk image while reviewing the fix
    above: detach the volume and `stat` said the directory was gone; reattach it and the
    data was untouched. A decline on an external disk or a dead network mount would
    therefore have been called a ghost, deleted, and the registry would go red the next
    time the volume came back -- #142's failure one layer down.

    A test cannot mount and detach a volume, so this stages the same shape the mountpoint
    produces: the directory is absent AND its parent is absent too, which is what "the
    filesystem under this path is not here" looks like from `stat`. It also pins the
    residual named in the docstring -- a whole-tree deletion reads blind from then on.
    """
    registry({"dagster": "the orchestrator's own bookkeeping"},
             {"dagster": tmp_path / "detached-volume" / "dagster"},
             _crawl(tmp_path, []))

    _undeclared, stale, blind, _note = collect.reconcile()
    assert stale == [], "a decline under an unreachable parent was called a ghost"
    assert blind == ["dagster"]


def test_a_missing_directory_beside_a_reachable_parent_is_still_gone(registry, tmp_path):
    """The other half of the parent check, so it cannot answer "blind" to everything.

    A guard only ever seen refusing has not been shown to permit. If asking the parent
    made every absence blind, nothing would ever be reported stale again and the
    DECLINED map would rot silently -- which is the reason the stale check exists.
    """
    registry({"dagster": "the orchestrator's own bookkeeping"},
             {"dagster": tmp_path / "never-existed"},
             _crawl(tmp_path, []))

    _undeclared, stale, blind, _note = collect.reconcile()
    assert stale == ["dagster"], "tmp_path is right there; this absence is a real absence"
    assert blind == []
