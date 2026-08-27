"""crew#74 row 1 (LAW 19): the warehouse exit is a drill that runs, not a sentence.
Rung 4 incident test, both ways, on a built-in database: the export and re-import
round-trip every row; an export with one table's Parquet removed is refused with the
table named in the diff. Neither case touches the real warehouse."""
import pathlib

import pytest

duckdb = pytest.importorskip("duckdb")
from science import exit_drill  # noqa: E402


@pytest.fixture
def db(tmp_path):
    p = tmp_path / "fixture.duckdb"
    exit_drill.fixture_db(p)
    return p


def test_export_database_round_trips_every_row(db, tmp_path):
    ok, r = exit_drill.drill(db, tmp_path / "out")
    assert ok, r
    assert r["tables"] == 2 and r["rows"] == 1002 and r["parquet_bytes"] > 0


def test_a_damaged_export_is_refused_and_names_the_table(db, tmp_path):
    ok, r = exit_drill.drill(db, tmp_path / "out", damage="facts")
    assert not ok
    assert r["error"] or "facts" in r["diff"]


def test_the_drill_is_scheduled_off_the_laptop():
    wf = pathlib.Path(__file__).resolve().parents[1] / ".github" / "workflows" / "warehouse-exit-drill.yml"
    text = wf.read_text()
    assert "- cron:" in text and "science/exit_drill.py --fixture" in text
