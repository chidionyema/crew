"""crew#378 (datamap WIRED_NEVER): ~/.estate/sovereign/budget.db, the sovereign worker's
per-session token budget, was written by the worker and read by nobody, and nothing joined it
to spend. The table has no time column (session_id, total, remaining, version), so it is a
snapshot source: collected every run, exempt from the crew#73 null-time growth check like
enforcement_map, joinable to spend on session_id. Rung 4, incident test, both ways."""
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "science"))
import collect  # noqa: E402


def _source():
    reg = json.loads((ROOT / "science/sources.json").read_text())
    return next(s for s in reg["sources"] if s["name"] == "sovereign_budget")


def test_the_budget_table_is_a_registered_snapshot_source_and_graded_collected():
    src = _source()
    assert src["kind"] == "sqlite" and src["path"].endswith("sovereign/budget.db")
    assert "sovereign_budget" in collect.NO_TIME_SOURCES
    ver = json.loads((ROOT / "science/verdicts.json").read_text())
    ent = next(e for e in ver["entries"] if "budget.db" in e["key"])
    assert ent["verdict"] == "COLLECTED" and "sovereign_budget" in ent["reader"]


def test_the_query_reads_the_live_schema_and_a_snapshot_never_grows_the_null_time_verdict(tmp_path):
    db = tmp_path / "budget.db"
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE budget (session_id TEXT PRIMARY KEY, total INTEGER NOT NULL, "
              "remaining INTEGER NOT NULL, version INTEGER NOT NULL)")
    c.execute("INSERT INTO budget VALUES ('sb-1', 100, 94, 1)")
    c.commit(); c.close()
    rows, bad = collect.read_rows(db, "sqlite", _source()["query"])
    assert bad == 0 and rows == [{"session_id": "sb-1", "total": 100, "remaining": 94, "version": 1}]
    assert collect.row_time(rows[0], None) is None
    wh = sqlite3.connect(":memory:")
    wh.execute("CREATE TABLE facts (source TEXT, at TEXT, payload TEXT)")
    wh.execute("CREATE TABLE IF NOT EXISTS null_time_watermark (source TEXT PRIMARY KEY, nulls INTEGER, at TEXT)")
    wh.executemany("INSERT INTO facts VALUES (?, NULL, '{}')", [("sovereign_budget",)] * 3)
    fails, _ = collect.null_time_verdict(wh)
    assert not [f for f in fails if "sovereign_budget" in f]
