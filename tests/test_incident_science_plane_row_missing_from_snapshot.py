"""Incident, 2026-08-25: the founder asked "we have data pipeline set up or not?" and no
row in STATE.md could answer it; a session measured the estate by hand instead. His words:
"the fact that you need to check means our process is broken." LAW 39.

Rule: the estate snapshot always carries the science-plane rows (warehouse, scheduler,
experiment tracker, forecast ledger), and each row is a verdict, never blank.
Rung 4, incident test.
"""
import importlib.util
import pathlib
from importlib.machinery import SourceFileLoader

SNAPSHOT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "estate-snapshot"


def _load():
    spec = importlib.util.spec_from_file_location(
        "estate_snapshot_sp", SNAPSHOT, loader=SourceFileLoader("estate_snapshot_sp", str(SNAPSHOT)))
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_incident_science_plane_rows_answer_the_pipeline_question():
    rows = _load().science_plane()
    names = {r.split("|")[1].strip() for r in rows}
    for needed in ("science plane: warehouse", "science plane: scheduler",
                   "science plane: experiment tracker", "science plane: forecast ledger"):
        assert needed in names, f"{needed} row missing: {rows}"
    for r in rows:
        state = r.split("|")[2].strip()
        assert state, f"blank verdict: {r}"
        assert state not in {"PASS"}, "a row never says PASS (snapshot rule)"
