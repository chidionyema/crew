"""Incident test, crew#320 (2026-08-27): `science/datamap.py --check` in a detached worktree died with
`sqlite3.OperationalError: no such table: facts` because science/warehouse.db existed as a 0-byte
file collect.py had never filled. Rule: a warehouse without a facts table reads as no warehouse.
"""
import importlib.util
import pathlib
import sqlite3

_p = pathlib.Path(__file__).resolve().parents[1] / "science" / "datamap.py"
_spec = importlib.util.spec_from_file_location("datamap", _p)
dm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dm)


def test_incident_crew320_empty_warehouse_reads_as_no_warehouse(tmp_path, monkeypatch):
    empty = tmp_path / "warehouse.db"
    empty.write_bytes(b"")
    monkeypatch.setattr(dm, "WAREHOUSE", empty)
    assert dm.collected() == {}
    filled = tmp_path / "filled.db"
    db = sqlite3.connect(filled)
    db.execute("CREATE TABLE facts (source TEXT, payload TEXT)")
    db.execute("INSERT INTO facts VALUES ('probe', '{\"a\": 1}')")
    db.commit()
    db.close()
    monkeypatch.setattr(dm, "WAREHOUSE", filled)
    assert dm.collected()["probe"]["rows"] == 1, "a real warehouse still reads"
