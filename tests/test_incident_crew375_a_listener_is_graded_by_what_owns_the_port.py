"""crew#375, 2026-08-27: `mac/listener/*` was one NEVER_EMITTED block over 32 rows that are three
different things: a `ssh:` port forward into the colima VM (crew#458), a macOS or VM-host daemon
the estate does not run, and an estate process that owns its port. The kind now says which, the
way `scheduled_job:monitored` does, and the register grades each class on its own.

Rule: forward -> NEVER_EMITTED against crew#458; system -> EXCLUDED; app -> NEVER_EMITTED, except
a port whose owner already lands in a collected source (3210, Dagster, source dagster-runs).
Rung 4, one incident, both ways in one run.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "science"))
import datamap  # noqa: E402

HOME = str(Path.home())
ROWS = [
    {"kind": "listener", "id": "port-4318", "port": 4318, "path": "ssh:", "process": "ssh"},
    {"kind": "listener", "id": "port-5000", "port": 5000, "process": "ControlCenter",
     "path": "/System/Library/CoreServices/ControlCenter.app/Contents/MacOS/ControlCenter"},
    {"kind": "listener", "id": "port-49211", "port": 49211, "process": "rapportd", "path": "/usr/libexec/rapportd"},
    {"kind": "listener", "id": "port-9900", "port": 9900, "process": "python", "path": f"{HOME}/dev/code/hermes-v2/.venv/bin/python"},
    {"kind": "listener", "id": "port-3210", "port": 3210, "process": "python", "path": "/usr/local/bin/python3.14"},
    {"kind": "listener", "id": "port-11434", "port": 11434, "process": "ollama",
     "path": "/Applications/Ollama.app/Contents/Resources/ollama"},
]


def _graded(tmp_path):
    inv = tmp_path / "inventory.json"
    inv.write_text(json.dumps({"rows": ROWS}))
    code = "import json, science.producers as p; print(json.dumps(p.mac()))"
    out = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True,
                         env={**os.environ, "ESTATE_INVENTORY": str(inv)}, check=True).stdout
    reg = json.loads((ROOT / "science/verdicts.json").read_text())
    return {g["key"]: g for g in datamap.grade(json.loads(out), reg)}


def test_incident_crew375_each_listener_class_has_its_own_verdict(tmp_path):
    g = _graded(tmp_path)
    assert g["mac/listener/port-4318"]["kind"] == "listener:forward"
    assert g["mac/listener/port-4318"]["verdict"] == "NEVER_EMITTED"
    assert g["mac/listener/port-4318"]["ticket"] == "crew#458"
    assert {g["mac/listener/port-5000"]["kind"], g["mac/listener/port-49211"]["kind"]} == {"listener:system"}
    assert g["mac/listener/port-5000"]["verdict"] == "EXCLUDED"
    assert g["mac/listener/port-9900"]["kind"] == "listener:app"
    assert g["mac/listener/port-9900"]["verdict"] == "NEVER_EMITTED"
    # crew#460 review: Ollama.app lives under /Applications but is the estate's model server, not a daemon
    assert g["mac/listener/port-11434"]["kind"] == "listener:app"
    assert g["mac/listener/port-3210"]["verdict"] == "COLLECTED"
    assert "dagster-runs" in g["mac/listener/port-3210"]["reader"]


def test_incident_crew375_the_gap_table_keeps_two_rows_with_one_key_apart(tmp_path):
    inv = tmp_path / "inventory.json"
    inv.write_text(json.dumps({"rows": ROWS}))
    out = subprocess.run([sys.executable, "science/datamap.py", "--check"], cwd=ROOT, capture_output=True, text=True,
                         env={**os.environ, "ESTATE_INVENTORY": str(inv)}, check=False).stdout
    assert "mac/listener/* [listener:forward]" in out and "crew#458" in out
    assert "mac/listener/* [listener:app]" in out
