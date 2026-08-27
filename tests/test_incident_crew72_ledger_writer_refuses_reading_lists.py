"""Incident crew#72 row 1: the ledger had no writer, so entries were typed by hand and 0 of 23
recorded a decision. The rule: the writer refuses an entry with no decision fed, no source or no
usable finding, and what it appends passes the ledger validator's required fields.
"""
import importlib.util
import json
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("ledger", ROOT / "science" / "ledger.py")
assert _spec is not None and _spec.loader is not None
ledger = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ledger)

GOOD = {"question": "q?", "why": "because", "decision_fed": "STANDARDS.md row", "metric": "m",
        "metric_before": "0", "sources": ["https://example.org/x"],
        "findings": ["A finding long enough to mean something."]}


@pytest.mark.parametrize("drop", ["decision_fed", "sources", "findings", "question", "metric_before"])
def test_the_writer_refuses_an_entry_missing_the_field(drop):
    e = dict(GOOD); e[drop] = "" if drop != "sources" and drop != "findings" else []
    with pytest.raises(ledger.Refused):
        ledger.validate(e)
    with pytest.raises(ledger.Refused):
        ledger.validate({**GOOD, "findings": ["too short"]})


def test_the_writer_appends_an_entry_the_validator_accepts(tmp_path):
    path = tmp_path / "L.jsonl"
    assert ledger.main(["add", "--ledger", str(path), "--question", "q?", "--why", "w", "--decision-fed", "d",
                        "--metric", "m", "--metric-before", "0", "--source", "https://example.org",
                        "--finding", "A finding long enough to mean something.", "--owner", "t"]) == 0
    e = json.loads(path.read_text().splitlines()[-1])
    required = {"date", "question", "decision_fed", "sources", "findings", "metric", "metric_before", "owner"}
    assert required <= e.keys() and e["owner"] == "t" and e["metric_after"] is None
    assert ledger.main(["add", "--ledger", str(path), "--question", "q?", "--why", "w", "--metric", "m",
                        "--metric-before", "0", "--source", "s", "--finding", "A finding long enough to mean something."]) == 2
    assert len(path.read_text().splitlines()) == 1, "a refused entry is not written"
