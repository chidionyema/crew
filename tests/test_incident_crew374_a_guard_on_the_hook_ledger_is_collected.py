"""crew#374, 2026-08-27: the register graded `mac/guard/*` NEVER_EMITTED as one block while 19 of
its 46 members were settings hooks that `hook-run.py` already records in the hook-outcomes ledger
(source `hook_outcomes`, crew#391). A measurement the ledger holds outranks a blanket in the
register, the way a sources.json decision outranks it for a store.

Rule: a guard row whose id has rows in the ledger is COLLECTED with the ledger as reader; a guard
the ledger has never seen keeps whatever the register says. Rung 4, one incident.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _decided(tmp_path, rows, ledger_lines):
    inv = tmp_path / "inventory.json"
    inv.write_text(json.dumps({"rows": rows}))
    led = tmp_path / "hook-outcomes.jsonl"
    led.write_text("".join(json.dumps(x) + "\n" for x in ledger_lines))
    code = ("import json, science.producers as p; "
            "print(json.dumps({x['key']: x.get('decided') for x in p.mac()}))")
    out = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True,
                         env={**os.environ, "ESTATE_INVENTORY": str(inv), "HOOK_OUTCOMES": str(led)},
                         check=True).stdout
    return json.loads(out)


def test_incident_crew374_ledger_rows_decide_collected_and_an_unseen_guard_is_left_to_the_register(tmp_path):
    home = str(Path.home())
    rows = [
        {"kind": "guard", "id": "goal-guard.py", "path": f"{home}/.claude/scripts/goal-guard.py"},
        {"kind": "guard", "id": "_router", "path": f"{home}/.estate/guards/hooks/_router"},
    ]
    ledger = [{"at": "2026-08-27T07:00:00Z", "event": "PreToolUse", "hook": "goal-guard.py", "exit": 0},
              "not json", {"at": "x"}]
    got = _decided(tmp_path, rows, ledger)
    assert got["mac/guard/goal-guard.py"]["verdict"] == "COLLECTED"
    assert "hook_outcomes" in got["mac/guard/goal-guard.py"]["reader"]
    assert got["mac/guard/_router"] is None, got


def test_incident_crew374_a_missing_ledger_decides_nothing(tmp_path):
    home = str(Path.home())
    inv = tmp_path / "inventory.json"
    inv.write_text(json.dumps({"rows": [
        {"kind": "guard", "id": "goal-guard.py", "path": f"{home}/.claude/scripts/goal-guard.py"}]}))
    code = "import json, science.producers as p; print(json.dumps([x.get('decided') for x in p.mac()]))"
    out = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True,
                         env={**os.environ, "ESTATE_INVENTORY": str(inv),
                              "HOOK_OUTCOMES": str(tmp_path / "absent.jsonl")}, check=True).stdout
    assert json.loads(out) == [None]
