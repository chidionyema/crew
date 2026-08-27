"""crew#72: the research ledger was a reading list outside the warehouse.

Rules: every ledger entry names the decision it fed (LAW 35), and the ledger is a
declared warehouse source so research can be joined to spend and ships.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "science" / "RESEARCH-LEDGER.jsonl"


def _rows():
    return [json.loads(l) for l in LEDGER.read_text().splitlines() if l.strip()]


def test_incident_crew72_every_entry_names_the_decision_it_fed():
    bare = [r.get("question", "?")[:60] for r in _rows() if not str(r.get("decision_fed", "")).strip()]
    assert not bare, f"entries with no decision_fed: {bare}"


def test_incident_crew72_every_entry_has_sources_and_a_date():
    bad = [r.get("question", "?")[:60] for r in _rows() if not r.get("sources") or not r.get("date")]
    assert not bad, bad


def test_incident_crew72_ledger_is_a_declared_warehouse_source():
    reg = json.loads((ROOT / "science" / "sources.json").read_text())
    src = {s["name"]: s for s in reg["sources"]}
    s = src["research_ledger"]
    assert s["path"] == "RESEARCH-LEDGER.jsonl" and s["time_field"] == "date" and s.get("receiver")
