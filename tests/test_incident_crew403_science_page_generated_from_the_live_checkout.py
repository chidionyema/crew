"""Incident crew#403 (2026-08-27): docs/science/SHOWCASE.md on main was generated at 09:13Z in a
scratchpad worktree, named that worktree's absolute store paths, read 6 BLIND of 10 for 4.6 hours,
and the hourly snapshot copied it forward instead of regenerating it. Two rules, both ways:
the publisher regenerates the page from the live checkout before copying; the page never carries
an absolute path, so no checkout can bake itself into it."""
import importlib.util
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
ABS_PATH = re.compile(r"(?<![\w/])/(Users|private|home|tmp)/")


def _showcase():
    spec = importlib.util.spec_from_file_location("showcase", ROOT / "science" / "showcase.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_incident_crew403_snapshot_regenerates_the_science_page_before_copying():
    text = (ROOT / "scripts" / "estate-snapshot").read_text()
    assert 'SCIENCE_PAGE = "docs/science/SHOWCASE.md"' in text
    assert "(*SCIENCE_LEDGERS, HAZARD_PAGE, SCIENCE_PAGE)" in text
    regen = text.index("regenerate the science page")
    assert regen < text.index("copy STATE.md into the worktree")
    assert "python3 science/showcase.py" in text[regen:regen + 200]


def test_incident_crew403_blind_messages_name_repo_relative_paths():
    m = _showcase()
    assert m.rel(ROOT / "science" / "warehouse.db") == "science/warehouse.db"
    assert m.rel("/private/tmp/elsewhere/science/warehouse.db") == "/private/tmp/elsewhere/science/warehouse.db", "outside the repo stays honest"
    assert not ABS_PATH.search(m.rel(m.WAREHOUSE))


def test_incident_crew403_committed_page_carries_no_absolute_path():
    page = (ROOT / "docs" / "science" / "SHOWCASE.md")
    if page.is_file():
        assert not ABS_PATH.search(page.read_text()), "a checkout baked itself into the page"
    assert ABS_PATH.search("BLIND: /private/tmp/x/science/warehouse.db absent"), "the rule bites the 09:13Z page"
