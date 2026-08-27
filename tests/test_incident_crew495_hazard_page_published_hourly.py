"""Incident crew#495 CP2: docs/HAZARDS.md on main was a day stale while risk/REGISTER.jsonl and the
P1 list moved. The snapshot regenerates and publishes the page every hour with STATE.md.
Rung 4 (incident test); the rule is that the page is in the published set and regenerated first."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_incident_crew495_snapshot_publishes_the_hazard_page():
    text = (ROOT / "scripts" / "estate-snapshot").read_text()
    assert 'HAZARD_PAGE = "docs/HAZARDS.md"' in text
    assert "(*SCIENCE_LEDGERS, HAZARD_PAGE, SCIENCE_PAGE, RESEARCH_PAGE)" in text, "the page ships with the science ledgers"
    regen = text.index("regenerate the hazard page")
    copy = text.index("copy STATE.md into the worktree")
    assert regen < copy, "the page is regenerated before anything is copied"
    assert "python3 scripts/hazard-register" in text[regen:copy]


def test_incident_crew495_register_rows_r14_to_r17_exist():
    rows = (ROOT / "risk" / "REGISTER.jsonl").read_text()
    for rid in ("R14", "R15", "R16", "R17"):
        assert f'"id": "{rid}"' in rows, rid
