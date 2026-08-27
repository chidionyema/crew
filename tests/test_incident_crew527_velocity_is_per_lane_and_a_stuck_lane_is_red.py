"""crew#527 CP1 (founder 2026-08-27: "187 is huge ... apply science to our board ... help us with
velocity"). Velocity is measured per lane from the board, one row per lane per day, and a lane
where work arrives and nothing finishes for three days is red. Both ways: an open issue counts
once, in its lane, with its checklist state; a closed one counts as closed only inside the
window; a rerun on the same day writes nothing; a lane whose open count falls, or whose ticked
count rises, is not red.
"""
import json
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "science"))
import velocity

NOW = datetime(2026, 8, 27, 18, 0, tzinfo=UTC)


def _iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


ISSUES = [
    {"labels": ["lane:platform", "P1"], "createdAt": _iso(NOW - timedelta(days=4)), "closedAt": None, "state": "open", "body": "- [x] a\n- [ ] b"},
    {"labels": ["lane:platform"], "createdAt": _iso(NOW - timedelta(hours=2)), "closedAt": None, "state": "open", "body": "no boxes"},
    {"labels": ["lane:platform"], "createdAt": _iso(NOW - timedelta(days=3)), "closedAt": _iso(NOW - timedelta(hours=1)), "state": "closed", "body": ""},
    {"labels": ["lane:platform"], "createdAt": _iso(NOW - timedelta(days=9)), "closedAt": _iso(NOW - timedelta(days=5)), "state": "closed", "body": ""},  # outside window
    {"labels": [], "createdAt": _iso(NOW - timedelta(days=1)), "closedAt": None, "state": "open", "body": "- [ ] x"},
]


def test_incident_crew527_counts_are_per_lane_and_inside_the_window():
    v = velocity.lane_velocity(ISSUES, NOW, days=1)
    p = v["lane:platform"]
    assert (p["open"], p["opened"], p["closed"], p["half_done"], p["ticked"], p["no_checklist"]) == (2, 1, 1, 1, 1, 1)
    assert p["median_age_d"] == 2.0
    assert v["lane:unsorted"] == {"opened": 1, "closed": 0, "open": 1, "half_done": 0, "ticked": 0, "no_checklist": 0, "median_age_d": 1.0}


def test_incident_crew527_a_day_is_written_once(tmp_path):
    out = tmp_path / "velocity.jsonl"
    v = velocity.lane_velocity(ISSUES, NOW, 1)
    assert velocity.append_rows(out, "2026-08-27", v, _iso(NOW)) == 2
    assert velocity.append_rows(out, "2026-08-27", v, _iso(NOW)) == 0
    assert velocity.append_rows(out, "2026-08-28", v, _iso(NOW)) == 2
    rows = [json.loads(line) for line in out.read_text().splitlines()]
    assert len(rows) == 4 and rows[0]["lane"] == "lane:platform" and rows[0]["day"] == "2026-08-27"


def _hist(lane, opens, ticks):
    return [{"day": f"2026-08-2{i}", "lane": lane, "open": o, "ticked": t} for i, (o, t) in enumerate(zip(opens, ticks, strict=True), start=1)]


def test_incident_crew527_a_stuck_lane_is_red_and_a_moving_one_is_not():
    stuck = _hist("lane:process", [10, 11, 11], [4, 4, 4])
    falling = _hist("lane:platform", [10, 9, 9], [4, 4, 4])
    ticking = _hist("lane:agents", [10, 10, 12], [4, 4, 6])
    short = _hist("lane:money", [10, 10], [4, 4])
    empty = _hist("lane:science", [1, 0, 0], [0, 0, 0])
    assert velocity.red_lanes(stuck + falling + ticking + short + empty) == ["lane:process"]
