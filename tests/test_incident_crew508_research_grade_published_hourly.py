"""crew#508 CP6: the research grade (Outward/Inward, R37) is regenerated and published by the
hourly snapshot, the same way the science page is (crew#507). A page only a session regenerates
by hand is the class crew#403 CP6 closed; this test keeps the research grade out of it."""

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "scripts" / "estate-snapshot"


def test_the_research_grade_is_in_the_published_set():
    text = SNAPSHOT.read_text()
    assert 'RESEARCH_PAGE = "docs/science/RESEARCH-GRADE.md"' in text
    assert "(*SCIENCE_LEDGERS, HAZARD_PAGE, SCIENCE_PAGE, RESEARCH_PAGE)" in text


def test_the_research_grade_is_regenerated_after_the_science_page_and_before_the_copies():
    text = SNAPSHOT.read_text()
    science = text.index('"regenerate the science page"')
    research = text.index('"regenerate the research grade"')
    assert science < research, "the research grade step follows the science page step"
    assert "python3 science/research_grade.py" in text[research : research + 200]


def test_the_committed_research_grade_carries_no_absolute_path():
    import re

    page = (ROOT / "docs" / "science" / "RESEARCH-GRADE.md").read_text()
    assert not re.search(r"(?<![\w/])/(Users|private|home|tmp)/", page)
