"""Incident, 2026-08-27: the founder asked "what happened to the elite grading? needs to be a
continuous process, not just a one off ... visible to founder." The grade existed as one
rendered page nobody surfaced. Rule: STATE.md always carries an `elite grade` row with the
ELITE/GAP/BLIND counts from idp docs/SHOWCASE.md, and the row is a verdict, never blank.
Rung 4, incident test, both ways.
"""
import importlib.util
import pathlib
from importlib.machinery import SourceFileLoader

SNAPSHOT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "estate-snapshot"


def _load():
    spec = importlib.util.spec_from_file_location(
        "estate_snapshot_eg", SNAPSHOT, loader=SourceFileLoader("estate_snapshot_eg", str(SNAPSHOT)))
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PAGE = "# Estate showcase\n\n## The bar\n\n- Entities: **287 ELITE**, **31 GAP**, **49 BLIND** of 367\n"


def test_incident_crew474_counts_reach_the_row_and_absence_is_named():
    mod = _load()
    (row,) = mod.elite_grade_row(PAGE)
    assert "| elite grade | 31 GAP, 49 BLIND |" in row and "287 ELITE of 367" in row
    (green,) = mod.elite_grade_row(PAGE.replace("31 GAP", "0 GAP").replace("49 BLIND", "0 BLIND"))
    assert "| elite grade | GREEN |" in green
    (missing,) = mod.elite_grade_row(None)
    assert "| elite grade | NOT RUN |" in missing
    (blind,) = mod.elite_grade_row("# a page with no counts\n")
    assert "| elite grade | BLIND |" in blind


def test_incident_crew474_the_row_is_in_the_section_list():
    src = SNAPSHOT.read_text(encoding="utf-8")
    start = src.index("for fn in (architect")
    assert "elite_grade" in src[start:start + 400], "elite_grade is not in main()'s section tuple"
