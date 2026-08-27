"""Incident, 2026-08-27 (crew#479): the science jobs wrote five tracked ledgers into the
shared crew checkout four times a day and nothing committed them; the checkout sat 4,079
lines dirty and the estate showcase graded it GAP. Rule: every ledger the science jobs
write is staged and pushed by the hourly snapshot commit, and a ledger missing on disk is
skipped, never a failed commit. Rung 4, incident test, both ways.
"""
import importlib.util
import pathlib
from importlib.machinery import SourceFileLoader

SNAPSHOT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "estate-snapshot"


def _load():
    spec = importlib.util.spec_from_file_location(
        "estate_snapshot_l", SNAPSHOT, loader=SourceFileLoader("estate_snapshot_l", str(SNAPSHOT)))
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_incident_crew479_ledgers_on_disk_are_published_and_missing_ones_are_skipped(tmp_path):
    mod = _load()
    (tmp_path / "science").mkdir()
    (tmp_path / "science" / "ships.jsonl").write_text("{}\n")
    (tmp_path / "science" / "census.json").write_text("{}\n")
    assert mod.published_ledgers(tmp_path) == ["science/ships.jsonl", "science/census.json"]
    assert mod.published_ledgers(tmp_path / "nowhere") == []


def test_incident_crew479_the_writers_and_the_publisher_name_the_same_files():
    src = SNAPSHOT.read_text(encoding="utf-8")
    root = SNAPSHOT.parents[1]
    writers = (root / "science" / "outcomes.py").read_text() + (root / "science" / "datamap.py").read_text()
    for rel in _load().SCIENCE_LEDGERS:
        assert rel.split("/")[-1] in writers, f"{rel} is published but no science writer names it"
    assert "published_ledgers()" in src[src.index("def commit("):]
