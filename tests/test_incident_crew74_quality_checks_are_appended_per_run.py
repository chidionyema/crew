"""crew#74 row 3: every collect run appends a quality row per source and names a move.

Row count, share of rows without a time and distinct payload keys, appended per run
so two runs can be compared. Rung 4, proved both ways in one run: a shrunk source and
a null-rate jump fail; a steady source and the first sighting do not.
"""
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "science"))

import collect  # noqa: E402


def _db(rows):
    conn = sqlite3.connect(":memory:")
    conn.executescript(collect.SCHEMA)
    conn.executemany("INSERT INTO facts VALUES (?, ?, 'now', ?)", rows)
    return conn


def test_first_run_records_and_a_steady_source_never_fails():
    conn = _db([("a", "2026-08-27T00:00:00Z", '{"x": 1, "y": 2}')] * 10)
    failures, note = collect.quality_checks(conn, now="t0")
    assert failures == [] and "1 source(s) recorded, 0 compared" in note
    failures, note = collect.quality_checks(conn, now="t1")
    assert failures == [] and "1 compared" in note
    rows = conn.execute("SELECT run_at, source, rows, null_at_rate, distinct_keys "
                        "FROM quality_checks ORDER BY run_at").fetchall()
    assert rows == [("t0", "a", 10, 0.0, 2), ("t1", "a", 10, 0.0, 2)]


def test_a_null_rate_jump_and_a_shrunk_source_are_named():
    conn = _db([("a", "2026-08-27T00:00:00Z", '{"x": 1}')] * 10)
    collect.quality_checks(conn, now="t0")
    # 4 rows without a time arrive: 10 -> 14 rows, null rate 0.00 -> 0.29
    conn.executemany("INSERT INTO facts VALUES ('a', NULL, 'now', '{}')", [()] * 4)
    failures, _ = collect.quality_checks(conn, now="t1")
    assert failures == ["a: share of rows without a time moved 0.00 -> 0.29 since the last run"]
    # the source is rewritten smaller: 14 -> 9 rows, null rate back to 0.00
    conn.execute("DELETE FROM facts WHERE at IS NULL")
    conn.execute("DELETE FROM facts WHERE rowid = (SELECT min(rowid) FROM facts)")
    failures, _ = collect.quality_checks(conn, now="t2")
    assert failures == ["a: row count fell 14 -> 9 since the last run",
                        "a: share of rows without a time moved 0.29 -> 0.00 since the last run"]


def test_check_wires_the_quality_row():
    src = (ROOT / "science" / "collect.py").read_text()
    assert "quality_checks(conn)" in src and "failures.extend(q_failures)" in src
