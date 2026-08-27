"""crew#371, 2026-08-28: act/model_routing was NEVER_EMITTED because the spend history row
dropped the per-model split that estate_spend.scan() already computed. The row now carries
by_model and reqs_by_model (claude-guards crew#371) and the warehouse exposes them as the
view spend_by_model.

Both ways: a spend row with by_model yields one view row per model with usd and requests;
a row from before the change (no by_model) yields nothing, never a zero row; an epoch-day
row is dropped like spend_daily drops it.
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
    conn.executescript(c.SCHEMA if hasattr(c, "SCHEMA") else "")
    conn.execute("CREATE TABLE IF NOT EXISTS facts (source TEXT NOT NULL, at TEXT, "
                 "ingested_at TEXT NOT NULL, payload TEXT NOT NULL)")
    for r in rows:
        conn.execute("INSERT INTO facts VALUES ('spend', ?, '2026-08-28T00:00:00', ?)",
                     (r.get("at"), json.dumps(r)))
    conn.executescript(c.SPEND_VIEW)
    return conn


def test_row_with_by_model_yields_usd_and_requests_per_model():
    conn = _db([{"at": "2026-08-28T00:10:00", "day": "2026-08-28", "total": 3.0, "requests": 5,
                 "by_owner": {}, "reqs_by_owner": {},
                 "by_model": {"fable-5": 2.5, "haiku-4-5": 0.5},
                 "reqs_by_model": {"fable-5": 3, "haiku-4-5": 2}}])
    got = conn.execute("SELECT day, model, usd, requests FROM spend_by_model").fetchall()
    assert got == [("2026-08-28", "fable-5", 2.5, 3), ("2026-08-28", "haiku-4-5", 0.5, 2)]


def test_row_before_the_change_yields_nothing_not_zero():
    conn = _db([{"at": "2026-08-27T00:10:00", "day": "2026-08-27", "total": 3.0, "requests": 5,
                 "by_owner": {"x": 3.0}, "reqs_by_owner": {"x": 5}}])
    assert conn.execute("SELECT count(*) FROM spend_by_model").fetchone()[0] == 0


def test_epoch_day_row_is_dropped():
    conn = _db([{"at": "1970-01-01T00:00:00", "day": "1970-01-01", "total": 1.0, "requests": 1,
                 "by_model": {"fable-5": 1.0}, "reqs_by_model": {"fable-5": 1}}])
    assert conn.execute("SELECT count(*) FROM spend_by_model").fetchone()[0] == 0
