"""Incident crew#72 row 4: LAW 35 says the loop is graded on itself once a week, and nothing did.
The rule: the self-grade is RED for a silent week and for a week whose entries fed no decision,
GREEN only when every entry of a non-empty week fed one; the grade lands as a ledger entry the
existing validator accepts, and never counts itself as research.
"""
import datetime as dt
import importlib.util
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("self_grade", ROOT / "science" / "self_grade.py")
assert _spec is not None and _spec.loader is not None
sg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sg)

NOW = dt.datetime(2026, 8, 27, tzinfo=dt.UTC)


def _row(days_ago: int, decision: str = "x", after: str = "") -> dict:
    return {"date": (NOW - dt.timedelta(days=days_ago)).strftime("%Y-%m-%d"), "question": "q",
            "decision_fed": decision, "metric_before": "0", "metric_after": after}


def test_a_silent_week_is_red_and_a_decided_week_is_green():
    assert sg.grade([_row(20)], NOW)["verdict"] == "RED"
    assert sg.grade([_row(2, decision="")], NOW)["verdict"] == "RED"
    g = sg.grade([_row(2), _row(5, after="1")], NOW)
    assert (g["verdict"], g["entries"], g["decided"], g["measured"]) == ("GREEN", 2, 2, 1)


def test_the_grade_never_counts_itself_and_the_entry_passes_the_ledger_validator(tmp_path):
    prior = sg.entry(sg.grade([_row(3)], NOW - dt.timedelta(days=7)), NOW - dt.timedelta(days=7), "t")
    g = sg.grade([_row(3), prior], NOW)
    assert g["entries"] == 1 and g["prior"] == prior["metric_after"]
    ledger = tmp_path / "L.jsonl"
    ledger.write_text(json.dumps(_row(3)) + "\n")
    assert sg.main(["--ledger", str(ledger), "--owner", "t"]) == 0
    rows = [json.loads(line) for line in ledger.read_text().splitlines()]
    e = rows[-1]
    required = {"date", "question", "decision_fed", "sources", "findings", "metric", "metric_before", "owner"}
    assert required <= e.keys() and e["sources"] and all(len(f) >= 20 for f in e["findings"])
    assert e["decision_fed"].startswith("GREEN:")
