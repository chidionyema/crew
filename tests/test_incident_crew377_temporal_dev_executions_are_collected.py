"""crew#377 (datamap WIRED_NEVER): ~/.estate/temporal/dev.db, the Temporal dev server's store,
held every workflow execution's start, close, status and duration in executions_visibility and
nothing read it. The history tables are encoded blobs; the visibility table is the readable row.
Rung 4, incident test, both ways: the query over the live schema yields a stamped row, and a
row whose start_time is not a time is filed as unstamped rather than mis-dated."""
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "science"))
import collect  # noqa: E402

DDL = ("CREATE TABLE executions_visibility (namespace_id CHAR(64) NOT NULL, run_id CHAR(64) NOT NULL, "
       "_version BIGINT NOT NULL DEFAULT 0, start_time TIMESTAMP NOT NULL, execution_time TIMESTAMP NOT NULL, "
       "workflow_id VARCHAR(255) NOT NULL, workflow_type_name VARCHAR(255) NOT NULL, status INT NOT NULL, "
       "close_time TIMESTAMP NULL, history_length BIGINT NULL, history_size_bytes BIGINT NULL, "
       "execution_duration BIGINT NULL, state_transition_count BIGINT NULL, memo BLOB NULL, "
       "encoding VARCHAR(64) NOT NULL, task_queue VARCHAR(255) NOT NULL DEFAULT '')")


def _source():
    reg = json.loads((ROOT / "science/sources.json").read_text())
    return next(s for s in reg["sources"] if s["name"] == "temporal_dev_executions")


def _db(tmp_path, start):
    db = tmp_path / "dev.db"
    c = sqlite3.connect(db)
    c.execute(DDL)
    c.execute("INSERT INTO executions_visibility (namespace_id, run_id, start_time, execution_time, workflow_id, "
              "workflow_type_name, status, close_time, execution_duration, encoding, task_queue) VALUES "
              "('ns', 'run-1', ?, ?, 'wf-1', 'KiniFinish', 2, '2026-08-26 03:58:01.000000+00:00', 9600000000, 'json', 'kini')",
              (start, start))
    c.commit(); c.close()
    return db


def test_registered_graded_collected_and_a_live_shaped_row_carries_its_start_time(tmp_path):
    src = _source()
    assert src["kind"] == "sqlite" and src["path"].endswith("temporal/dev.db") and src["time_field"] == "at"
    ver = json.loads((ROOT / "science/verdicts.json").read_text())
    ent = next(e for e in ver["entries"] if "temporal/dev.db" in e["key"])
    assert ent["verdict"] == "COLLECTED" and "temporal_dev_executions" in ent["reader"]
    rows, bad = collect.read_rows(_db(tmp_path, "2026-08-26 03:57:51.383855+00:00"), "sqlite", src["query"])
    assert bad == 0 and rows[0]["workflow_type_name"] == "KiniFinish" and rows[0]["status"] == 2
    assert "execution_time" in rows[0]  # 09cd04a6 on crew#447: execution_duration = close_time - execution_time
    assert collect.row_time(rows[0], "at") is not None


def test_a_start_time_that_is_not_a_time_is_unstamped_not_misdated(tmp_path):
    rows, _ = collect.read_rows(_db(tmp_path, "not a time"), "sqlite", _source()["query"])
    assert collect.row_time(rows[0], "at") is None
