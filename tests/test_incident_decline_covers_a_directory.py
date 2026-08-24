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

    undeclared, stale, note = collect.reconcile()
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

    undeclared, _stale, _note = collect.reconcile()
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

    undeclared, _stale, _note = collect.reconcile()
    assert [u["path"] for u in undeclared] == [str(stray)]


def test_a_directory_decline_is_not_stale_on_a_night_the_tool_did_not_run(registry, tmp_path):
    """The directory exists and is empty. That is a quiet night, not a ghost."""
    (tmp_path / "dagster").mkdir()

    registry({"dagster": "the orchestrator's own bookkeeping"},
             {"dagster": tmp_path / "dagster"},
             _crawl(tmp_path, []))

    _undeclared, stale, _note = collect.reconcile()
    assert stale == []


def test_a_directory_decline_is_stale_once_the_directory_is_gone(registry, tmp_path):
    """The other direction. An exclusion for something no longer there is a ghost."""
    registry({"dagster": "the orchestrator's own bookkeeping"},
             {"dagster": tmp_path / "never-existed"},
             _crawl(tmp_path, []))

    _undeclared, stale, _note = collect.reconcile()
    assert stale == ["dagster"]


def test_an_id_decline_still_behaves_exactly_as_before(registry, tmp_path):
    """LAW 38. The thirteen exclusions already in the registry name an id and no path."""
    store = tmp_path / "telemetry.jsonl"
    store.write_text("")

    registry({str(store): "the vendor's own failed uploads"}, {}, _crawl(tmp_path, [store]))

    undeclared, stale, _note = collect.reconcile()
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
