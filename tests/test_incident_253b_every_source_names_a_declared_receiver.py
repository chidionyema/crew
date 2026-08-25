"""crew#253 follow-up, 2026-08-25 (idp#128 merged the collector skeleton): every source in
science/sources.json names the collector receiver it lands in, and the name must be a key
the collector declares. Rung 4, both ways, against a scratch registry and scratch config.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLLECT = ROOT / "science" / "collect.py"


def _run(tmp_path, receiver, collector="receivers:\n  otlp: {}\n"):
    tmp_path.mkdir(exist_ok=True)
    (tmp_path / "store").mkdir()
    (tmp_path / "store" / "new.jsonl").write_text('{"at":"2026-08-24T00:00:00+00:00"}\n')
    (tmp_path / "inventory.json").write_text(json.dumps({"rows": [
        {"kind": "ledger", "id": "newstore", "path": str(tmp_path / "store/new.jsonl"),
         "member_of": None, "rows": 1}]}))
    src = {"name": "newstore", "root": "home", "path": "store/new.jsonl", "kind": "jsonl",
           "time_field": "at"}
    if receiver is not None:
        src["receiver"] = receiver
    (tmp_path / "sources.json").write_text(json.dumps(
        {"version": 1, "roots": {"home": "~"}, "default_stale_after_hours": 100000,
         "sources": [src], "declined": []}))
    cfg = tmp_path / "otel-collector.yaml"
    if collector is not None:
        cfg.write_text(collector)
    env = dict(os.environ, SCIENCE_WAREHOUSE=str(tmp_path / "w.db"),
               SCIENCE_REGISTRY=str(tmp_path / "sources.json"),
               ESTATE_INVENTORY=str(tmp_path / "inventory.json"), ESTATE_HOME=str(tmp_path),
               OTEL_COLLECTOR_CONFIG=str(cfg))
    return subprocess.run([sys.executable, str(COLLECT), "--check"], env=env, check=False,
                          capture_output=True, text=True)


def test_incident_253b_declared_receiver_passes(tmp_path):
    r = _run(tmp_path, "otlp")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "receivers: every source lands in a declared receiver" in r.stdout


def test_incident_253b_undeclared_or_missing_receiver_is_refused(tmp_path):
    assert _run(tmp_path / "a", "carrier_pigeon").returncode == 1
    assert _run(tmp_path / "b", None).returncode == 1


def test_incident_253b_unreadable_collector_config_is_blind_not_a_verdict(tmp_path):
    r = _run(tmp_path, "otlp", collector=None)
    assert r.returncode == 0 and "receivers: BLIND" in r.stdout, r.stdout


def test_incident_253b_live_registry_names_a_receiver_on_every_source():
    reg = json.loads((ROOT / "science" / "sources.json").read_text())
    assert all((s.get("receiver") or "").strip() for s in reg["sources"])
