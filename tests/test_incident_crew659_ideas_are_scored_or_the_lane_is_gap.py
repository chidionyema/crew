"""crew#659 CP2 and CP3: the research lane graded ELITE with one idea on the ledger, because the
scoreboard counted questions fed and had no row for ideas. Founder, 2026-08-30: "if no progress
then I have to run the lane myself"; progress is a scored idea per day. These tests pin:

- the grade is GAP when no scored idea landed inside the window, whatever the questions say;
- the worker writes an idea only with an Inspect score, and refuses a non-frontier lane;
- the ledger row it writes is one science/ledger.py accepts and research_grade.py counts.
"""

from __future__ import annotations

import datetime as dt
import json
import pathlib
import sys

import pytest

SCIENCE = pathlib.Path(__file__).resolve().parents[1] / "science"
sys.path.insert(0, str(SCIENCE))
import research_grade  # noqa: E402
import research_worker  # noqa: E402

TODAY = dt.date(2026, 8, 30)
FRESH_INTAKE = {"fresh": True, "late": [], "candidates": 0}
INWARD = {"trained": True, "scored": 1, "evidence": "x"}


def _question(day: str) -> dict:
    return {
        "date": day,
        "question": "q",
        "why": "w",
        "decision_fed": "yes",
        "sources": ["https://a"],
        "findings": ["a finding long enough to count"],
        "metric": "m",
        "metric_before": "0",
    }


def _idea(decided_at: str, score: float | None = 1.0) -> dict:
    row = _question(decided_at[:10]) | {"kind": "idea", "title": "t", "decided_at": decided_at}
    if score is not None:
        row["score"] = score
    return row


def test_perfect_questions_and_no_fresh_idea_is_gap_not_elite():
    rows = [_question("2026-08-29")] * 30 + [_idea("2026-08-27T10:00:00+00:00")]
    g = research_grade.grade(rows, TODAY)
    assert g["ideas"] == 1 and g["ideas_scored"] == 1 and g["ideas_fresh"] == 0
    assert research_grade.grades(g, INWARD, FRESH_INTAKE)[0] == "GAP"


def test_a_scored_idea_inside_the_window_lets_the_lane_grade_elite():
    rows = [_question("2026-08-29"), _idea("2026-08-30T01:00:00+00:00", 0.5)]
    g = research_grade.grade(rows, TODAY)
    assert g["ideas_fresh"] == 1 and g["ideas_mean_score"] == 0.5
    assert research_grade.grades(g, INWARD, FRESH_INTAKE)[0] == "ELITE"


def test_an_idea_without_a_score_does_not_count_as_progress():
    rows = [_question("2026-08-29"), _idea("2026-08-30T01:00:00+00:00", score=None)]
    g = research_grade.grade(rows, TODAY)
    assert g["ideas"] == 1 and g["ideas_scored"] == 0 and g["ideas_fresh"] == 0
    assert research_grade.grades(g, INWARD, FRESH_INTAKE)[0] == "GAP"


def test_the_page_carries_the_ideas_table(tmp_path, monkeypatch):
    monkeypatch.setattr(research_grade, "intake", lambda: FRESH_INTAKE | {"rows": []})
    monkeypatch.setattr(research_grade.research_intake, "render", lambda *_: "")
    monkeypatch.setattr(
        research_grade,
        "inward",
        lambda: INWARD | {"verdict": "TRAINED", "recorded": 1, "hits": 1, "hit_rate": 100},
    )
    ledger = tmp_path / "l.jsonl"
    ledger.write_text(json.dumps(_idea("2026-08-30T01:00:00+00:00")) + "\n")
    page = research_grade.render(
        research_grade.grade(research_grade.read_ledger(ledger), TODAY), ledger, TODAY
    )
    assert "## Outward — ideas for the store front" in page
    assert "| Ideas with a score | 1 |" in page
    assert "| Scored in the last 1d | 1 |" in page


# --- the worker, with no network ----------------------------------------------------------------
REPORT = {
    "report": "# Market\n\nAgencies pay for tooling.",
    "sources": ["https://s1", "https://s2"],
    "costs_usd": 0.12,
}


def _researcher(brief, deep):
    return REPORT


def _extractor(report, brief, n, lane, market):
    return [
        {
            "title": "Retainer pricing tool",
            "claim": "Agencies with under 10 staff will pay for it",
            "price_hypothesis": "29 GBP per month",
            "sources": ["https://s1"],
        }
    ]


def _grader(ideas, report, grader, run_id):
    for i in ideas:
        i.update(grade="P", score=0.5, grader=grader, inspect_log="science/inspect-logs/x.eval")
    return ideas


def _no_grade(ideas, report, grader, run_id):
    return ideas


def test_the_worker_writes_a_scored_idea_the_ledger_accepts_and_the_grade_counts(tmp_path):
    ledger = tmp_path / "l.jsonl"
    out = research_worker.run(
        "tooling agencies pay for",
        "UK SME",
        1,
        "claude",
        "gemini",
        False,
        ledger,
        tmp_path / "reports",
        _researcher,
        _extractor,
        _grader,
    )
    assert out["ideas"] == 1 and out["mean_score"] == 0.5
    rows = research_grade.read_ledger(ledger)
    assert (
        rows[0]["kind"] == "idea"
        and rows[0]["score"] == 0.5
        and rows[0]["sources"] == ["https://s1"]
    )
    assert (tmp_path / "reports" / f"{out['run_id']}.md").exists()
    g = research_grade.grade(rows, dt.datetime.now(dt.UTC).date())
    assert g["ideas_fresh"] == 1


def test_an_unscored_idea_never_reaches_the_ledger(tmp_path):
    ledger = tmp_path / "l.jsonl"
    with pytest.raises(research_worker.Refused, match="no score"):
        research_worker.run(
            "b",
            "",
            1,
            "claude",
            "gemini",
            False,
            ledger,
            tmp_path / "reports",
            _researcher,
            _extractor,
            _no_grade,
        )
    assert not ledger.exists()


@pytest.mark.parametrize(
    "worker,grader", [("minimax", "gemini"), ("claude", "groq"), ("deepseek", "deepseek")]
)
def test_a_non_frontier_lane_is_refused_before_any_call(tmp_path, worker, grader):
    with pytest.raises(research_worker.Refused, match="not a frontier lane"):
        research_worker.run(
            "b",
            "",
            1,
            worker,
            grader,
            False,
            tmp_path / "l.jsonl",
            tmp_path,
            _researcher,
            _extractor,
            _grader,
        )


def test_configure_points_every_model_at_the_router_and_never_prints_the_key(monkeypatch, tmp_path):
    key = tmp_path / "key"
    key.write_text("router-virtual-key\n")
    monkeypatch.setenv("ROUTER_URL", "https://router.example")
    monkeypatch.setenv("ROUTER_KEY_FILE", str(key))
    monkeypatch.setattr(research_worker, "probe_lane", lambda lane, role, ask=None: lane)
    shown = research_worker.configure("claude", "gemini")
    assert shown["OPENAI_BASE_URL"] == "https://router.example/v1"
    assert shown["OPENAI_API_KEY"] == "<redacted>" and "router-virtual-key" not in json.dumps(shown)
    assert shown["SMART_LLM"] == "openai:claude" and shown["EMBEDDING"] == "openai:embed"


def test_parse_ideas_refuses_an_idea_missing_a_field():
    with pytest.raises(research_worker.Refused, match="has no price_hypothesis"):
        research_worker.parse_ideas('[{"title": "t", "claim": "c", "sources": ["u"]}]')
