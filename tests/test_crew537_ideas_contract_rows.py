"""crew#537 CP4: the contract between the research capability and prospector is three graded rows
on docs/science/SHOWCASE.md — ideas generated per week, ideas graded (forecast with source), ideas
resolved with Brier — red until the ledger holds the data, never absent. Both directions here:
an idea-free ledger grades every row FAIL; one graded and resolved idea grades them ok with the
Brier score computed, and the writer refuses a forecast that is not a probability.
"""
import datetime as dt
import json
import pathlib
import sys

SCIENCE = pathlib.Path(__file__).resolve().parents[1] / "science"
sys.path.insert(0, str(SCIENCE))
import ledger  # noqa: E402
import showcase  # noqa: E402

NOW = dt.datetime(2026, 8, 28, 0, 0, tzinfo=dt.timezone.utc)
TITLE = "Ideas: the prospector contract (crew#537)"


def _entry(**extra):
    e = {"question": "Is idea X worth a week?", "why": "founder asked", "decision_fed": "run it",
         "metric": "revenue", "metric_before": "0", "sources": ["https://example.invalid/src"],
         "findings": ["a finding long enough to count as a statement"], "date": "2026-08-27"}
    e.update(extra)
    return e


def test_a_ledger_with_no_idea_rows_grades_every_row_red(monkeypatch, tmp_path):
    led = tmp_path / "RESEARCH-LEDGER.jsonl"
    led.write_text(json.dumps(_entry()) + "\n")   # research, not an idea
    monkeypatch.setattr(showcase, "LEDGER", led)
    data, blind = showcase.build(NOW)
    assert TITLE not in blind, "an empty contract is a red row, never an absent section"
    d = data[TITLE]
    assert d["ideas"] == 0 and [g for _, _, g in d["rows"]] == [False, False, False]
    page = showcase.render(NOW, data, blind, {})
    section = page.split(f"## {TITLE}")[1].split("\n## ")[0]
    assert section.count("| FAIL (no data) |") == 3
    for name in ("ideas generated per week", "ideas graded (forecast with source)", "ideas resolved with Brier"):
        assert f"| {name} |" in section


def test_one_graded_and_resolved_idea_turns_the_rows_ok_with_a_brier(monkeypatch, tmp_path):
    led = tmp_path / "RESEARCH-LEDGER.jsonl"
    ledger.append(_entry(kind="idea", forecast="0.8", outcome="1"), led)
    ledger.append(_entry(kind="idea", forecast=0.3), led)            # graded, not yet resolved
    monkeypatch.setattr(showcase, "LEDGER", led)
    data, blind = showcase.build(NOW)
    d = data[TITLE]
    assert (d["ideas"], d["this_week"], d["graded"], d["resolved"], d["brier"]) == (2, 2, 2, 1, 0.04)
    assert [g for _, _, g in d["rows"]] == [True, True, True]
    section = showcase.render(NOW, data, blind, {}).split(f"## {TITLE}")[1].split("\n## ")[0]
    assert "| ideas resolved with Brier | 1, Brier 0.04 | ok |" in section
    assert showcase.numbers(data)["ideas Brier"] == 0.04


def test_the_writer_refuses_a_forecast_that_is_not_a_probability(tmp_path):
    led = tmp_path / "RESEARCH-LEDGER.jsonl"
    for bad in ({"forecast": "1.5"}, {"forecast": "high"}, {"outcome": "2", "forecast": 0.5}, {"outcome": "1"}):
        try:
            ledger.append(_entry(kind="idea", **bad), led)
        except ledger.Refused:
            continue
        raise AssertionError(f"accepted {bad}")
    assert not led.exists()


def test_the_page_lists_the_section_between_predictions_and_foresight():
    titles = [t for t, _, _ in showcase.SECTIONS]
    assert titles.index("Predictions") < titles.index(TITLE) < titles.index("Foresight: will this PR go red?")
