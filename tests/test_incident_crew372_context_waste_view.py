"""crew#372, 2026-08-28: act/context_waste was NEVER_EMITTED. The spend scan read every
call's cache_read_input_tokens and kept only the dollars. The history row now carries
tokens by driver and reread_pct (claude-guards crew#372) and the warehouse exposes them
as the view context_waste.

Both ways: a spend row with tokens yields tokens_sent, tokens_reread and the pct; a row
from before the change (no tokens) yields nothing, never a zero row; an epoch-day row is
dropped like spend_daily drops it.
"""
import importlib.util
import json
import pathlib
import sqlite3
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _collect():
    spec = importlib.util.spec_from_file_location("collect", ROOT / "science" / "collect.py")
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules["collect"] = mod
    spec.loader.exec_module(mod)
    return mod


def _db(rows):
    c = _collect()
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE IF NOT EXISTS facts (source TEXT NOT NULL, at TEXT, "
                 "ingested_at TEXT NOT NULL, payload TEXT NOT NULL)")
    for r in rows:
        conn.execute("INSERT INTO facts VALUES ('spend', ?, '2026-08-28T00:00:00', ?)",
                     (r.get("at"), json.dumps(r)))
    conn.executescript(c.SPEND_VIEW)
    return conn


def _row(day, tokens, pct, at=None):
    return {"at": at or f"{day}T00:10:00", "day": day, "total": 3.0, "requests": 5,
            "by_owner": {}, "reqs_by_owner": {}, "tokens": tokens, "reread_pct": pct}


def test_row_with_tokens_yields_sent_reread_and_pct():
    conn = _db([_row("2026-08-28", {"raw_input": 100, "cache_read": 1800, "cache_write": 100,
                                    "output": 40}, 90.0)])
    got = conn.execute("SELECT day, tokens_sent, tokens_reread, tokens_reread_pct, tokens_output "
                       "FROM context_waste").fetchall()
    assert got == [("2026-08-28", 2000, 1800, 90.0, 40)]


def test_two_rows_one_day_keep_the_later_larger_count():
    conn = _db([_row("2026-08-28", {"raw_input": 1, "cache_read": 10, "cache_write": 1,
                                    "output": 1}, 83.3, at="2026-08-28T01:00:00"),
                _row("2026-08-28", {"raw_input": 2, "cache_read": 30, "cache_write": 2,
                                    "output": 2}, 88.2, at="2026-08-28T23:00:00")])
    assert conn.execute("SELECT tokens_reread FROM context_waste").fetchall() == [(30,)]


def test_row_before_the_change_yields_nothing_not_zero():
    conn = _db([{"at": "2026-08-27T00:10:00", "day": "2026-08-27", "total": 3.0, "requests": 5,
                 "by_owner": {"x": 3.0}, "reqs_by_owner": {"x": 5}}])
    assert conn.execute("SELECT count(*) FROM context_waste").fetchone()[0] == 0


def test_epoch_day_row_is_dropped():
    conn = _db([_row("1970-01-01", {"raw_input": 1, "cache_read": 1, "cache_write": 0,
                                    "output": 0}, 50.0, at="1970-01-01T00:00:00")])
    assert conn.execute("SELECT count(*) FROM context_waste").fetchone()[0] == 0


def test_spend_schema_names_the_new_fields():
    sc = json.loads((ROOT / "science" / "schemas" / "spend.json").read_text())
    for k in ("tokens", "reread_pct", "by_model", "reqs_by_model"):
        assert k in sc["fields"] and k in sc["field_docs"], k
