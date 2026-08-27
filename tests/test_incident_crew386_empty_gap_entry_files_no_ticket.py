"""Incident test, crew#386 (2026-08-27): `datamap.py --file-tickets` filed crew#386 for the register
entry `cluster/UNPARSEABLE/*` with **Members this run:** 0. A gap entry nothing matched is a rule
waiting for a member, not a producer nobody reads. Rule: file a ticket only for an entry with members.
"""
import importlib.util
import pathlib
import subprocess

_p = pathlib.Path(__file__).resolve().parents[1] / "science" / "datamap.py"
_spec = importlib.util.spec_from_file_location("datamap", _p)
assert _spec is not None and _spec.loader is not None
dm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dm)


def _gh_ok(*a, **k):
    return subprocess.CompletedProcess(a, 0, stdout="https://github.com/x/crew/issues/999\n", stderr="")


def test_incident_crew386_empty_gap_entry_files_no_ticket(monkeypatch, tmp_path):
    calls = []
    monkeypatch.setattr(dm, "REGISTER", tmp_path / "verdicts.json")
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: (calls.append(a), _gh_ok())[1])
    reg = {"entries": [
        {"key": "cluster/UNPARSEABLE/*", "verdict": "WIRED_NEVER", "why": "unparseable"},
        {"key": "mac/data/x.db", "verdict": "WIRED_NEVER", "why": "no reader"},
    ]}
    graded = [{"key": "mac/data/x.db", "kind": "data", "verdict": "WIRED_NEVER",
               "entry": "mac/data/x.db", "measures": ["exists"]}]
    filed = dm.file_tickets(graded, reg, "x/crew")
    assert filed == 1 and len(calls) == 1, "the entry with a member is ticketed"
    assert reg["entries"][1]["ticket"] == "crew#999"
    assert "ticket" not in reg["entries"][0], "the empty entry is not ticketed"
