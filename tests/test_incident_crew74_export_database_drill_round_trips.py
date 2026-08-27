"""crew#74 row 1: the warehouse had never been exported; LAW 19 calls an exit
never taken a hope. Rule: EXPORT DATABASE writes every table as Parquet and a
fresh IMPORT DATABASE gets every row back; a copy missing a table or a row
fails. Rung 4, incident test, proved both ways."""
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

duckdb = pytest.importorskip("duckdb")
from science import export_drill  # noqa: E402


def _warehouse(path: Path) -> None:
    con = sqlite3.connect(path)
    con.execute("CREATE TABLE facts (source TEXT, at REAL, payload TEXT)")
    con.executemany("INSERT INTO facts VALUES (?, ?, ?)", [("spend", 1.0 + i, "{}") for i in range(5)])
    con.execute("CREATE TABLE ingest_log (run INTEGER)")
    con.execute("INSERT INTO ingest_log VALUES (1)")
    con.execute("CREATE VIEW spend_daily AS SELECT source, count(*) AS n FROM facts GROUP BY source")
    con.commit()
    con.close()


def test_every_table_round_trips_and_a_lost_table_fails(tmp_path):
    wh = tmp_path / "warehouse.db"
    _warehouse(wh)
    out = tmp_path / "export"
    counts, failures = export_drill.drill(wh, out)
    assert counts == {"facts": 5, "ingest_log": 1}
    assert failures == []
    assert sorted(p.name for p in out.iterdir()) == ["facts.parquet", "ingest_log.parquet", "load.sql", "schema.sql"]
    # the other way: the copy lost rows
    con = duckdb.connect()
    con.execute("CREATE TABLE facts AS SELECT * FROM read_parquet(?) LIMIT 3", [str(out / "facts.parquet")])
    con.execute(f"COPY facts TO '{out / 'facts.parquet'}' (FORMAT PARQUET)")
    con.close()
    assert export_drill.verify(out, counts) == ["facts: exported 3 rows, warehouse has 5"]
    # and the copy lost a table's data: the import itself refuses
    (out / "ingest_log.parquet").unlink()
    assert export_drill.verify(out, counts)[0].startswith("import of ")


def test_a_missing_warehouse_is_a_failure_not_a_pass(tmp_path):
    counts, failures = export_drill.drill(tmp_path / "absent.db", tmp_path / "out")
    assert counts == {} and failures and "does not exist" in failures[0]


def test_cli_exit_follows_the_verdict(tmp_path):
    wh = tmp_path / "warehouse.db"
    _warehouse(wh)
    env = {**os.environ, "SCIENCE_WAREHOUSE": str(wh)}
    p = subprocess.run([sys.executable, str(Path(export_drill.__file__))], capture_output=True, text=True, env=env, check=False)
    assert p.returncode == 0 and p.stdout.rstrip().splitlines()[-1].startswith("PASS    export-database: 2 table(s)")
    env["SCIENCE_WAREHOUSE"] = str(tmp_path / "absent.db")
    p = subprocess.run([sys.executable, str(Path(export_drill.__file__))], capture_output=True, text=True, env=env, check=False)
    assert p.returncode == 1 and "FAIL" in p.stdout
