"""crew#583 in the crew#488 row: the board's portability verdict came off this laptop's clock.

`portability_row()` measured `age_h = time.time() - <GitHub's createdAt>` and graded it with one
bound, `RED if age_h > stale_hours else GREEN`. Both halves of that subtraction are clocks and
only one of them is GitHub's. When a MacBook's battery dies the hardware RTC comes back at its
default epoch, `time.time()` lands years before the run's stamp, every age is negative, and no
negative number is greater than 194 -- so the row printed GREEN, with a cheerful "-350000.0h
ago", off a drill that had not run since. The founder reads this row as his CP4 receipt.

Rung 4, incident test. It does not assert the message, only that the two skew directions cannot
reach GREEN and that an honest run still can -- an over-fix that painted every row NOT RUN would
pass a test that only checked for the absence of GREEN.
"""
import datetime as dt
import importlib.machinery
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

RUN_AT = "2026-08-28T11:05:06Z"
STAMP = dt.datetime(2026, 8, 28, 11, 5, 6, tzinfo=dt.UTC).timestamp()

READY = "ok      portability  ready 2/38 layers on a cluster with no OCI (floor 2)"
K3S = ("ok      portability-k3s  provider=github-hosted-azure distro=k3s wall_clock=658s "
       "cost=£0.00 (public repository, GitHub-hosted ubuntu-latest)")
LOG = f"{K3S}\n{READY}\n"


def _snap():
    loader = importlib.machinery.SourceFileLoader("snap", str(ROOT / "scripts" / "estate-snapshot"))
    spec = importlib.util.spec_from_loader("snap", loader)
    assert spec is not None
    m = importlib.util.module_from_spec(spec)
    loader.exec_module(m)
    return m


def _runs():
    return json.dumps([{"databaseId": 33193146025, "conclusion": "success",
                        "createdAt": RUN_AT, "status": "completed"}])


def _state(rows):
    return rows[0].split("|")[2].strip()


@pytest.mark.parametrize("what, now", [
    #: the RTC reset the founder described: the machine believes it is 1970
    ("clock_at_the_1970_epoch", 0.0),
    #: a battery that came back on the manufacturing date instead
    ("clock_400d_behind_the_run", STAMP - 400 * 86400),
])
def test_a_clock_behind_the_run_is_never_green(what, now):
    rows = _snap().portability_row(_runs(), LOG, now=now)
    assert not _state(rows).startswith("GREEN"), f"{what}: {rows[0]}"
    assert _state(rows) == "NOT RUN"


def test_a_clock_ahead_of_the_run_is_still_red_not_green():
    """The other direction was already graded and must stay graded: a clock far ahead makes every
    run look ancient, which is a red board and a fixable one, not a silent green."""
    rows = _snap().portability_row(_runs(), LOG, now=STAMP + 400 * 86400)
    assert _state(rows) == "RED"


def test_seconds_of_ordinary_ntp_skew_are_not_an_incident():
    """The over-fix guard. A row that refused to measure on any negative age would turn the
    board NOT RUN every time GitHub's stamp lands a second after the local read."""
    rows = _snap().portability_row(_runs(), LOG, now=STAMP - 30)
    assert _state(rows) == "GREEN"


def test_an_honest_recent_run_still_reaches_the_founder():
    rows = _snap().portability_row(_runs(), LOG, now=STAMP + 600)
    assert _state(rows) == "GREEN"
    assert "ready 2/38" in rows[0]
    assert "cost=£0.00" in rows[1]
