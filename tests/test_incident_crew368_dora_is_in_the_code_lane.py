"""crew#368 follow-up: SHOWCASE.md listed `dora` under `unmapped` after crew#547 declared the
source without naming its lane (2026-08-28 01:2xZ, science hook on session 09cd04a6). A source
the collector owns and the snapshot commits is not a discovery; it belongs to a lane the day it
is declared, or the lane grade lies (crew#508: a lane is graded on what it emits).

Standard: Observability row, docs/reference/STANDARDS.md
Rejected: mapping every unmapped name by hand in one sweep -- hindsight_recall is owned by
~/.claude/settings.json and its lane is that owner's call (LAW 29).
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "science"))
import showcase  # noqa: E402


def _lane_of(name: str) -> str | None:
    return next((lane for lane, names in showcase.LANE_SOURCES.items() if name in names), None)


def test_dora_is_graded_in_the_code_lane():
    assert _lane_of("dora") == "code"


def test_every_source_the_collector_owns_has_a_lane():
    sources = json.loads((ROOT / "science" / "sources.json").read_text())
    rows = sources["sources"] if isinstance(sources, dict) else sources
    mine = [s["name"] for s in rows if s.get("owner") == "scripts/science-collect"]
    assert mine, "science-collect owns at least one source"
    unmapped = [n for n in mine if _lane_of(n) is None]
    assert not unmapped, f"sources science-collect owns but no lane grades: {unmapped}"
