"""crew#537 CP5: the first business idea goes through the research engine end to end and lands on
the ledger with its sources and a prior. The receipt is the RESEARCH-LEDGER row itself.

Graded from the data, never from prose: a row of `kind: idea` must carry at least one source URL
and a numeric prior in (0, 1). A ledger with no such row is CP5 unfinished; a row with a prior but
no source is an opinion, not research (R31/R32).

Note for crew#553's successor: `crew verify` keys checkpoint tests by CP number alone
(crew/bdd.py find_marker), not by issue, so this file is named by its issue to keep the lookup
honest until verify learns to read `--issue`.
"""
# Rejected: a JSON Schema check of science/schemas/research_ledger.json -- it validates shape, not that an idea row exists with sources and a prior
# Standard: Testing row, docs/reference/STANDARDS.md (pytest marker per checkpoint, run by `crew verify` on the qa runner)
from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "science" / "RESEARCH-LEDGER.jsonl"


def _ideas() -> list[dict]:
    rows = [json.loads(line) for line in LEDGER.read_text().splitlines() if line.strip()]
    return [r for r in rows if r.get("kind") == "idea"]


@pytest.mark.cp5
def test_an_idea_row_is_on_the_ledger():
    assert LEDGER.exists(), f"no research ledger at {LEDGER}"
    assert _ideas(), "no `kind: idea` row on science/RESEARCH-LEDGER.jsonl -- the research engine has produced no idea"


@pytest.mark.cp5
def test_the_idea_carries_its_sources_and_a_prior():
    for row in _ideas():
        sources = row.get("sources") or []
        assert sources and all(str(s).startswith("http") for s in sources), \
            f"idea {row.get('question', '')[:60]!r} carries no source URL"
        prior = row.get("forecast")
        assert isinstance(prior, (int, float)) and 0 < prior < 1, \
            f"idea {row.get('question', '')[:60]!r} carries no prior in (0, 1): {prior!r}"
        assert row.get("question") and row.get("decision_fed"), \
            "an idea names the question it answers and the decision it feeds"
