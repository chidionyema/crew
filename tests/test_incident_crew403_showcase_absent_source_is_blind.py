"""Incident test, crew#403: the science showcase never renders an empty section.

A section whose store is missing says BLIND with the path it looked for; a section
whose store is present renders its numbers. Both directions in one run (LAW 45 step 3),
and the progress section diffs the previous run's numbers rather than re-describing them.
"""
import datetime as dt
import json
import pathlib
import sys

SCIENCE = pathlib.Path(__file__).resolve().parents[1] / "science"
sys.path.insert(0, str(SCIENCE))
import showcase  # noqa: E402

NOW = dt.datetime(2026, 8, 27, 0, 0, tzinfo=dt.UTC).replace(tzinfo=None)  # naive UTC, as showcase.main() builds it


def test_absent_ledger_renders_blind_with_its_path(monkeypatch, tmp_path):
    monkeypatch.setattr(showcase, "LEDGER", tmp_path / "RESEARCH-LEDGER.jsonl")
    data, blind = showcase.build(NOW)
    assert "Research ledger" in blind and "RESEARCH-LEDGER.jsonl absent" in blind["Research ledger"]
    page = showcase.render(NOW, data, blind, {})
    assert "## Research ledger" in page and "BLIND:" in page.split("## Research ledger")[1].split("##")[0]


def test_present_ledger_renders_its_count(monkeypatch, tmp_path):
    led = tmp_path / "RESEARCH-LEDGER.jsonl"
    led.write_text(json.dumps({"date": "2026-08-20", "question": "q?", "decision_fed": "d"}) + "\n")
    monkeypatch.setattr(showcase, "LEDGER", led)
    data, blind = showcase.build(NOW)
    assert "Research ledger" not in blind
    assert data["Research ledger"] == {"entries": 1, "with_decision": 1, "first": "2026-08-20", "last_date": "2026-08-20",
                                       "last": [{"date": "2026-08-20", "question": "q?", "decision": "d", "metric": ""}]}
    assert "- 1 entries, 2026-08-20 to 2026-08-20; 1 record the decision they fed" in showcase.render(NOW, data, blind, {})


def test_progress_is_a_diff_against_the_previous_run(monkeypatch, tmp_path):
    led = tmp_path / "RESEARCH-LEDGER.jsonl"
    led.write_text(json.dumps({"date": "2026-08-20", "question": "q?"}) + "\n")
    monkeypatch.setattr(showcase, "LEDGER", led)
    data, blind = showcase.build(NOW)
    prev = {"generated": "2026-08-26T00:00Z", "numbers": {"research entries": 0, "research entries with a decision": 0}}
    page = showcase.render(NOW, data, blind, prev)
    assert "- research entries: 0 -> 1" in page
    assert "research entries with a decision" not in page.split("## Capabilities")[0]   # unchanged: not listed
