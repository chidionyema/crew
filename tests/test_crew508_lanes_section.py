"""crew#508 (founder, 2026-08-27): "science covers everything ... I need to see progress across
all lanes simultaneously, everything needs to be feeding the machine."

The Lanes section grades every lane on facts it emitted in the last 24h. A lane that emitted
nothing is BLIND and sorts first: unobserved is not the same as healthy. These tests build a
throwaway warehouse with two sources and assert the grades the page would print.
"""
import datetime as dt
import importlib.util
import pathlib
import sqlite3

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _showcase():
    spec = importlib.util.spec_from_file_location("showcase_crew508", ROOT / "science" / "showcase.py")
    assert spec is not None and spec.loader is not None
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


@pytest.fixture
def warehouse(tmp_path, monkeypatch):
    """A facts table with one fresh row per lane under test, plus one older than the window."""
    m = _showcase()
    now = dt.datetime(2026, 8, 27, 12, 0, 0)
    db_path = tmp_path / "warehouse.db"
    db = sqlite3.connect(db_path)
    db.execute("create table facts (source text, ingested_at text, at text, payload text)")
    fresh = (now - dt.timedelta(hours=2)).isoformat(sep=" ")
    stale = (now - dt.timedelta(hours=48)).isoformat(sep=" ")
    rows = ([("ships", fresh)] * 3 + [("board", fresh)] * 5
            + [("ships", stale)] * 99                      # outside the 24h window
            + [("a_source_no_lane_claims", fresh)] * 2)
    db.executemany("insert into facts (source, ingested_at) values (?, ?)", rows)
    db.commit()
    db.close()
    monkeypatch.setattr(m, "WAREHOUSE", db_path)
    monkeypatch.setattr(m, "CHECKPOINT_LEDGERS", ())     # no ledger: checkpoints are 0 with a reason
    return m, now


def test_two_sources_land_in_their_two_lanes_with_the_window_respected(warehouse):
    m, now = warehouse
    rows = {r["lane"]: r for r in m.lanes(now)["rows"]}
    assert rows["code"]["facts"] == 3, "ships is the code lane; the 48h-old rows are out of window"
    assert rows["crew"]["facts"] == 5, "board is the crew lane"


def test_a_lane_no_source_fed_is_blind(warehouse):
    m, now = warehouse
    rows = {r["lane"]: r for r in m.lanes(now)["rows"]}
    assert rows["hermes-v2"]["facts"] == 0
    assert rows["hermes-v2"]["grade"] == "BLIND"
    for lane in ("portal", "science", "data-ml"):
        assert rows[lane]["grade"] == "BLIND", lane


def test_a_fed_lane_with_no_checkpoint_is_gap_not_elite(warehouse):
    m, now = warehouse
    rows = {r["lane"]: r for r in m.lanes(now)["rows"]}
    assert rows["code"]["checkpoints"] == 0
    assert rows["code"]["grade"] == "GAP"
    assert rows["crew"]["grade"] == "GAP"


def test_facts_plus_a_ticked_checkpoint_is_elite(warehouse, tmp_path):
    m, now = warehouse
    ledger = tmp_path / "ledger.md"
    ledger.write_text("- [x] code lane: gate green\n- [ ] crew: not yet\n- [x] CODE again\n")
    m.CHECKPOINT_LEDGERS = (ledger,)
    rows = {r["lane"]: r for r in m.lanes(now)["rows"]}
    assert rows["code"]["checkpoints"] == 2, "case-insensitive, unticked boxes ignored"
    assert rows["code"]["grade"] == "ELITE"
    assert rows["crew"]["grade"] == "GAP", "an unticked box is not a checkpoint"


def test_an_unmapped_source_is_listed_not_absorbed(warehouse):
    m, now = warehouse
    d = m.lanes(now)
    assert d["unmapped"] == {"a_source_no_lane_claims": 2}
    unmapped = [r for r in d["rows"] if r["lane"] == m.UNMAPPED]
    assert len(unmapped) == 1 and unmapped[0]["facts"] == 2
    assert sum(r["facts"] for r in d["rows"] if r["lane"] in m.LANE_SOURCES) == 8, "no double count"


def test_blind_lanes_are_printed_first(warehouse):
    m, now = warehouse
    grades = [r["grade"] for r in m.lanes(now)["rows"]]
    assert grades[0] == "BLIND"
    assert grades == sorted(grades, key=lambda g: {"BLIND": 0, "GAP": 1, "ELITE": 2}[g])


def test_the_rendered_table_carries_every_lane_and_no_absolute_path(warehouse):
    m, now = warehouse
    blind = {t: "not under test" for t, _, _ in m.SECTIONS if t != "Lanes"}
    page = m.render(now, {"Lanes": m.lanes(now)}, blind, {})
    assert "## Lanes" in page
    for lane in m.LANE_SOURCES:
        assert f"| {lane} |" in page, lane
    assert "| Lane | Facts, 24h | Checkpoints, 24h | Grade | Sources counted |" in page
    assert str(ROOT) not in page and "/private/" not in page


def test_a_missing_warehouse_is_blind_never_a_row_of_zeroes(tmp_path, monkeypatch):
    m = _showcase()
    monkeypatch.setattr(m, "WAREHOUSE", tmp_path / "gone.db")
    with pytest.raises(m.Blind):
        m.lanes(dt.datetime(2026, 8, 27, 12, 0, 0))


def test_an_empty_file_where_the_warehouse_should_be_is_blind(tmp_path, monkeypatch):
    """The live worktree's warehouse.db is a 0-byte file; sqlite opens it and has no facts table."""
    m = _showcase()
    empty = tmp_path / "warehouse.db"
    empty.touch()
    monkeypatch.setattr(m, "WAREHOUSE", empty)
    with pytest.raises(m.Blind, match="no readable facts table"):
        m.lanes(dt.datetime(2026, 8, 27, 12, 0, 0))
