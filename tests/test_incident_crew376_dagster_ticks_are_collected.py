"""Incident crew#376 / crew#85, 2026-08-27: 16 hours of skipped Dagster ticks went unseen.

Dagster's job_ticks table was the only record that every schedule was skipping on a
flat load ceiling, and nothing outside Dagster's UI read it. The rule: a registry source
of kind `sqlite` is read through its query, read-only, and its `at` column is the row
time; a query that does not fit the store is UNREADABLE, never a silent zero.
"""

from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from science import collect  # noqa: E402


def _ticks_db(tmp_path):
    db = tmp_path / "schedules.db"
    conn = sqlite3.connect(db)
    conn.execute("CREATE TABLE job_ticks (id INTEGER, job_origin_id TEXT, status TEXT, type TEXT, timestamp TEXT, tick_body TEXT)")
    conn.execute("INSERT INTO job_ticks VALUES (1, 'j', 'SKIPPED', 'SCHEDULE', '2026-08-27 02:00:00.000123', '{\"skip_reason\": \"j: load 10.7 > max_load 6.0\"}')")
    conn.commit()
    conn.close()
    return db


QUERY = ("SELECT id, status, timestamp||'+00:00' AS at, "
         "json_extract(tick_body,'$.skip_reason') AS skip_reason FROM job_ticks")


def test_a_skipped_tick_lands_with_its_reason_and_time(tmp_path) -> None:
    rows, bad = collect.read_rows(_ticks_db(tmp_path), "sqlite", QUERY)
    assert bad == 0 and len(rows) == 1
    assert rows[0]["skip_reason"].endswith("max_load 6.0")
    assert collect.row_time(rows[0], "at") == "2026-08-27 02:00:00.000123+00:00"


def test_a_query_that_does_not_fit_the_store_is_unreadable_not_zero(tmp_path) -> None:
    db = _ticks_db(tmp_path)
    try:
        collect.read_rows(db, "sqlite", "SELECT 1 FROM no_such_table")
    except OSError as exc:
        assert "no_such_table" in str(exc)
    else:
        raise AssertionError("a bad query returned rows instead of raising")


def test_registry_names_the_live_dagster_store_under_the_code_root() -> None:
    names = {n: k for n, (_p, k, _t) in collect.SOURCES.items()}
    assert names["dagster-ticks"] == "sqlite" and names["dagster-runs"] == "sqlite"
    assert collect.QUERIES["dagster-ticks"].lstrip().upper().startswith("SELECT")
    path = str(collect.SOURCES["dagster-ticks"][0])
    assert path.endswith("idp/run/dagster/schedules/schedules.db") and os.sep + "idp" + os.sep in path


def test_the_collector_never_opens_the_store_for_writing(tmp_path) -> None:
    db = _ticks_db(tmp_path)
    before = db.stat().st_mtime_ns
    collect.read_rows(db, "sqlite", QUERY)
    assert db.stat().st_mtime_ns == before
