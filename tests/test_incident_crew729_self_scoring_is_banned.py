"""crew#729: self scoring is banned forever (founder, 2026-08-31, verbatim).

The incident: docs/science/RESEARCH-GRADE.md printed Outward ELITE — "30 of 30 questions
fed a decision" — and every one of those rows was written by the research lane about
itself, while the founder did the shelf-scanning the lane exists for. Founder: "the
research ledger should never score itself SELF SCORING IS BANNED FOREVER ... And evidence
says research should score lowest". And: "NO FOUNDER CALIBRATE ... Because the estate
reports to founder" — the external evidence is a machine-checkable pointer (a merged PR
URL or repo@sha in `used_in`), never a word a person has to type.

The guard this test watches fail: a ledger of perfect self-authored rows must never grade
ELITE. On the pre-fix grader (origin/main before this PR) the first test prints ELITE and
fails; the transcript rides the PR body.
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "science"))

import research_grade as rg

PERFECT_SELF_LEDGER = {"questions": 5, "stale": [], "sourceless": 0, "ideas_fresh": 1}
PERFECT_INWARD = {"trained": True, "evidence": "science/foresight-state.json", "scored": 4}


def test_a_perfect_self_authored_ledger_never_grades_elite():
    out_g, in_g = rg.grades(PERFECT_SELF_LEDGER, PERFECT_INWARD)
    assert out_g != "ELITE", "self-authored rows raised the grade: self scoring is banned"
    assert in_g != "ELITE"
    assert (out_g, in_g) == ("GAP", "GAP")


def test_one_external_receipt_lifts_the_cap_and_only_then():
    assert rg.grades(PERFECT_SELF_LEDGER, PERFECT_INWARD, delivered_n=1) == ("ELITE", "ELITE")
    # blind stays blind whatever the receipts say
    blind = rg.grades(
        {"questions": 0, "stale": [], "sourceless": 0},
        {"trained": False, "evidence": "-", "scored": 0},
        delivered_n=3,
    )
    assert blind == ("BLIND", "BLIND")


def test_a_receipt_without_a_verifiable_pointer_does_not_count(tmp_path):
    p = tmp_path / "DELIVERY-RECEIPTS.jsonl"
    rows = [
        {"date": "2026-08-31", "what": "prose claim, no pointer"},  # no used_in
        {
            "date": "2026-08-31",
            "what": "prose pointer",
            "used_in": "we used it a lot",
        },  # not a URL/sha
        {
            "date": "2026-08-31",
            "what": "flux interval research",
            "used_in": "https://github.com/chidionyema/idp/pull/1057",
        },  # counts
        {"date": "2026-08-31", "what": "pinned checkout", "used_in": "idp@1467fc1e"},  # counts
    ]
    p.write_text("".join(json.dumps(r) + "\n" for r in rows))
    assert len(rg.delivered(p)) == 2


def test_the_page_states_the_ban_and_floors_with_no_receipts(tmp_path, monkeypatch):
    monkeypatch.setattr(rg, "RECEIPTS", tmp_path / "none.jsonl")
    import datetime as dt

    ledger = tmp_path / "L.jsonl"
    ledger.write_text(
        json.dumps(
            {"date": "2026-08-30", "question": "q", "decision_fed": "d", "sources": ["https://x"]}
        )
        + "\n"
    )
    g = rg.grade(rg.read_ledger(ledger), dt.date(2026, 8, 31))
    page = rg.render(g, ledger, dt.date(2026, 8, 31))
    assert "SELF SCORING IS BANNED FOREVER" in page
    assert "| Outward | **ELITE**" not in page
    assert "grade floors at GAP" in page


def test_the_weekly_self_grade_machine_is_gone_and_stays_gone():
    """Founder, 2026-09-01: "no self grading in this estate ... BANNED ... get rid of that
    shit" — said over the weekly self-grade pull request title. The machine was
    .github/workflows/self-grade.yml calling science/self_grade.py on a Monday cron. This
    guard sweeps the class: no workflow file may mention a self-grade, and the grader
    module may not exist under any name."""
    root = pathlib.Path(__file__).resolve().parents[1]
    workflows = root / ".github" / "workflows"
    offenders = [
        p.name
        for p in workflows.glob("*.yml")
        if "self-grade" in p.read_text() or "self_grade" in p.read_text()
    ]
    assert offenders == [], f"a workflow still runs a self-grade: {offenders}"
    graders = [str(p.relative_to(root)) for p in (root / "science").glob("*self*grade*")]
    assert graders == [], f"a self-grade module came back: {graders}"
