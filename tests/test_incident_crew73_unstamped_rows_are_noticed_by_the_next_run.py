"""crew#73 row 4: a producer that stops stamping its rows makes the next collect run fail.

6,166 warehouse rows sat with ``at IS NULL`` (close_guard 2240, stuck_detector 3919) and
no check said so, because the only thing that looked at ``at`` was a human with sqlite3.
The verdict is growth: the count of unstamped rows per source, against the count the
last run recorded. Rung 4, incident test, proved both ways in one run.
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
    conn.executemany("INSERT INTO facts VALUES (?, ?, 'now', '{}')", rows)
    return conn


def test_growth_fails_and_a_fixed_producer_clears():
    conn = _db([("close_guard", None)] * 3 + [("close_guard", "2026-08-27T00:00:00Z")])
    # first run seeds, never fails
    failures, note = collect.null_time_verdict(conn, now="t0")
    assert failures == []
    assert "first watermark seeded" in note and "close_guard=3" in note
    # the producer keeps writing rows without a time -> the next run fails, naming it
    conn.execute("INSERT INTO facts VALUES ('close_guard', NULL, 'now', '{}')")
    failures, _ = collect.null_time_verdict(conn, now="t1")
    assert failures == ["close_guard: 1 new row(s) without a time since the last run "
                        "(producer stopped stamping)"]
    # the producer is fixed: only stamped rows arrive -> the run is clean again
    conn.execute("INSERT INTO facts VALUES ('close_guard', '2026-08-27T01:00:00Z', 'now', '{}')")
    failures, _ = collect.null_time_verdict(conn, now="t2")
    assert failures == []


def test_a_snapshot_source_never_fails_and_no_watermark_is_kept_for_it():
    conn = _db([("enforcement_map", None)])
    for t in ("t0", "t1"):
        conn.execute("INSERT INTO facts VALUES ('enforcement_map', NULL, 'now', '{}')")
        failures, _ = collect.null_time_verdict(conn, now=t)
        assert failures == [], t
    assert conn.execute("SELECT count(*) FROM null_time_watermark").fetchone()[0] == 0


def test_check_wires_the_verdict():
    src = (ROOT / "science" / "collect.py").read_text()
    assert "null_time_verdict(conn)" in src and "failures.extend(null_failures)" in src
