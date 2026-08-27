"""Incident, 2026-08-25 (crew#253): science/datamap.py kept its own list of why a store
is uncollected and never read science/sources.json, so the snapshot said 28 UNEXPLAINED
while the gate (collect.py --reconcile) said 11. Rung 4. The rule: a store the registry
declines is never UNEXPLAINED, and a store nobody decided about still is.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "science"))

import collect  # noqa: E402
import datamap  # noqa: E402
import producers  # noqa: E402


def _rows(tmp_path, monkeypatch, rows):
    """Verdict per store path after the register (crew#320) grades a mac inventory."""
    inv = tmp_path / "inventory.json"
    inv.write_text(json.dumps({"rows": rows}))
    monkeypatch.setattr(producers, "INVENTORY", inv)
    graded = datamap.grade(producers.mac(), datamap.register())
    paths = {r["path"] for r in rows}
    return {g["evidence"]: g["verdict"] for g in graded if g["evidence"] in paths}


def test_incident_253_registry_decline_is_not_unexplained(tmp_path, monkeypatch):
    ddir = next(iter(collect.DECLINED_DIRS.values()))
    by_id = next(i for i in collect.DECLINED if i not in collect.DECLINED_DIRS)
    out = _rows(tmp_path, monkeypatch, [
        {"id": by_id, "path": str(Path.home() / by_id), "kind": "data", "collected": False},
        {"id": "x.jsonl", "path": str(ddir / "x.jsonl"), "kind": "data", "collected": False},
    ])
    assert set(out.values()) == {"DECLINED"}, out


def test_incident_253_undecided_store_stays_unexplained(tmp_path, monkeypatch):
    out = _rows(tmp_path, monkeypatch, [
        {"id": "nobody/decided.jsonl", "path": str(tmp_path / "nobody/decided.jsonl"),
         "kind": "data", "collected": False},
    ])
    assert out == {str(tmp_path / "nobody/decided.jsonl"): "UNEXPLAINED"}
