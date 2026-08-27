"""Incident test, crew#320 (2026-08-27): science/sources.json declines `consult` at
`.claude/logs/consult.jsonl`, yet `datamap.py --check` graded `mac/ledger/~/.claude/logs/consult.jsonl`
UNEXPLAINED. The inventory ids a file by its relative path; declines were matched by id, or by
directory prefix, never by file path. Rule: a decline that names a file decides that file.
"""
import importlib.util
import pathlib
import sys

SCIENCE = pathlib.Path(__file__).resolve().parents[1] / "science"
sys.path.insert(0, str(SCIENCE))
_spec = importlib.util.spec_from_file_location("producers", SCIENCE / "producers.py")
assert _spec is not None and _spec.loader is not None
pr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pr)
import collect  # noqa: E402


def test_incident_crew320_declined_file_is_decided(tmp_path, monkeypatch):
    f = tmp_path / "logs" / "consult.jsonl"
    monkeypatch.setattr(collect, "DECLINED", {"consult": "no backend since 2026-08-23"})
    monkeypatch.setattr(collect, "DECLINED_DIRS", {"consult": f})
    row = {"id": "logs/consult.jsonl", "path": str(f)}
    d = pr._sources_decision(row)
    assert d and d["verdict"] == "DECLINED" and d["entry"] == "sources.json declined consult"
    other = {"id": "logs/other.jsonl", "path": str(tmp_path / "logs" / "other.jsonl")}
    assert pr._sources_decision(other) is None, "a sibling file is not decided by a file decline"
