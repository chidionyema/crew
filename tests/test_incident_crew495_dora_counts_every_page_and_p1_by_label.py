"""Incident test, crew#495 (2026-08-27): the first DORA baseline (comment 5438270290) reported
idp deploys=200, the listing's page cap, and change failure rate 0% because P1s were searched by
title. Rule: the four keys come from every row in the window, P1s by label, and a window edge
is respected. Rung 4, both ways: rows inside the window count; rows outside do not; a P1 with
no close date is opened but not repaired.
"""
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "science"))
import dora  # noqa: E402

NOW = datetime(2026, 8, 27, 12, 0, tzinfo=timezone.utc)
SINCE = NOW - timedelta(days=7)


def _iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def test_incident_crew495_four_keys_count_the_window_and_only_the_window():
    prs = [
        {"createdAt": _iso(NOW - timedelta(hours=3)), "mergedAt": _iso(NOW - timedelta(hours=1)), "baseRefName": "main"},
        {"createdAt": _iso(NOW - timedelta(hours=6)), "mergedAt": _iso(NOW - timedelta(hours=2)), "baseRefName": "main"},
        {"createdAt": _iso(NOW - timedelta(days=9)), "mergedAt": _iso(NOW - timedelta(days=8)), "baseRefName": "main"},  # outside
        {"createdAt": _iso(NOW - timedelta(hours=3)), "mergedAt": None, "baseRefName": "main"},  # closed, not merged
        {"createdAt": _iso(NOW - timedelta(hours=3)), "mergedAt": _iso(NOW - timedelta(hours=1)), "baseRefName": "state/live-diagram"},
    ]
    p1s = [
        {"createdAt": _iso(NOW - timedelta(hours=5)), "closedAt": _iso(NOW - timedelta(hours=1))},
        {"createdAt": _iso(NOW - timedelta(hours=2)), "closedAt": None},
        {"createdAt": _iso(NOW - timedelta(days=10)), "closedAt": _iso(NOW - timedelta(days=9))},  # outside
    ]
    k = dora.four_keys(prs, p1s, SINCE, 7)
    assert k["deploys"] == 2 and k["deploys_per_day"] == 0.29
    assert k["lead_time_h_median"] == 3.0 and k["lead_time_h_p90"] == 4.0
    assert k["p1_opened"] == 2 and k["change_failure_rate_pct"] == 100.0
    assert k["p1_closed"] == 1 and k["mttr_h_median"] == 4.0


def test_incident_crew495_no_merges_is_not_a_division():
    k = dora.four_keys([], [{"createdAt": _iso(NOW), "closedAt": None}], SINCE, 7)
    assert k["deploys"] == 0 and k["change_failure_rate_pct"] is None and k["mttr_h_median"] is None
