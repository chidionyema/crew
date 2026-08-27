"""crew#72: the research ledger was a reading list outside the warehouse.

Rules: every ledger entry names the decision it fed (LAW 35), and the ledger is a
declared warehouse source so research can be joined to spend and ships.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "science" / "RESEARCH-LEDGER.jsonl"


def _rows():
    return [json.loads(line) for line in LEDGER.read_text().splitlines() if line.strip()]


def records_a_decision(row: dict) -> bool:
    """crew#72 row 2: sources and findings with no decision is a reading list, not research."""
    return bool(str(row.get("decision_fed", "")).strip())


def test_incident_crew72_every_entry_names_the_decision_it_fed():
    bare = [r.get("question", "?")[:60] for r in _rows() if not records_a_decision(r)]
    assert not bare, f"entries with no decision_fed: {bare}"


def test_incident_crew72_the_rule_refuses_a_reading_list_entry_and_permits_a_decision():
    reading_list = {"question": "q", "sources": ["s"], "findings": "f", "decision_fed": "  "}
    decided = {"question": "q", "sources": ["s"], "findings": "f", "decision_fed": "crew#72 row 2"}
    assert not records_a_decision(reading_list)
    assert records_a_decision(decided)


def test_incident_crew72_every_entry_has_sources_and_a_date():
    bad = [r.get("question", "?")[:60] for r in _rows() if not r.get("sources") or not r.get("date")]
    assert not bad, bad


def test_incident_crew72_ledger_is_a_declared_warehouse_source():
    reg = json.loads((ROOT / "science" / "sources.json").read_text())
    src = {s["name"]: s for s in reg["sources"]}
    s = src["research_ledger"]
    assert s["path"] == "RESEARCH-LEDGER.jsonl" and s["time_field"] == "date" and s.get("receiver")


def _snap():
    import importlib.machinery
    import importlib.util
    loader = importlib.machinery.SourceFileLoader("snap", str(ROOT / "scripts" / "estate-snapshot"))
    spec = importlib.util.spec_from_loader("snap", loader)
    assert spec is not None
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


def test_state_md_carries_a_research_row_that_is_never_green_for_a_silent_week(tmp_path):
    # crew#72 row 5: a reader that reaches him. NOT RUN without a ledger, RED for a silent week,
    # GREEN only when an entry landed inside the window.
    import datetime as dt
    snap = _snap()
    now = dt.datetime(2026, 8, 27, 2, 0, tzinfo=dt.UTC)
    missing = tmp_path / "RESEARCH-LEDGER.jsonl"
    assert "NOT RUN" in snap.research_row(missing, now)[0]
    missing.write_text(json.dumps({"date": "2026-08-10", "question": "q"}) + "\n")
    assert snap.research_row(missing, now)[0].startswith("| research | RED |")
    missing.write_text(json.dumps({"date": "2026-08-25", "question": "q", "decision_fed": "crew#72"}) + "\n")
    row = snap.research_row(missing, now)[0]
    assert row.startswith("| research | GREEN |") and "1 with a decision fed" in row, row
    live = snap.research_row(LEDGER, now)[0]
    assert live.startswith("| research | ") and "NOT RUN" not in live, live
