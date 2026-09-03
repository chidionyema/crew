"""crew#488 CP4: the founder is supposed to read the ready count and the cost line on a STATE.md
row, and STATE.md had no portability row at all (measured 2026-08-28, generated 03:03 UTC: no
line matching `portability|cost=`). `bin/idp-drills-row` said only that the drill RAN.

Rung 4, incident test. The trap this closes is the proxy trap: a workflow's `conclusion` is not a
measurement. A green run whose log holds no `ok portability` grade line must print NOT RUN, never
GREEN, because "the run passed" and "the drill measured 2/37 layers Ready" are different claims.

Grade lines are the ones idp run 33165807800 actually printed on 2026-08-28.
"""
import datetime as dt
import importlib.machinery
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NOW = dt.datetime(2026, 8, 28, 12, 0, tzinfo=dt.UTC).timestamp()

READY = "ok      portability  ready 2/37 layers on a cluster with no OCI (floor 2)"
K3S = ("ok      portability-k3s  provider=github-hosted-azure distro=k3s wall_clock=670s "
       "cost=£0.00 (public repository, GitHub-hosted ubuntu-latest)")
LOG = f"some earlier line\n{K3S}\n{READY}\nmore output\n"


def _snap():
    loader = importlib.machinery.SourceFileLoader("snap", str(ROOT / "scripts" / "estate-snapshot"))
    spec = importlib.util.spec_from_loader("snap", loader)
    assert spec is not None
    m = importlib.util.module_from_spec(spec)
    loader.exec_module(m)
    return m


def _runs(*, created="2026-08-28T11:05:06Z", conclusion="success", status="completed"):
    return json.dumps([
        {"databaseId": 33166470567, "conclusion": "", "createdAt": "2026-08-28T11:15:33Z",
         "status": "in_progress"},
        {"databaseId": 33165807800, "conclusion": conclusion, "createdAt": created,
         "status": status},
    ])


def test_the_row_carries_both_numbers_the_founder_has_to_read():
    rows = _snap().portability_row(_runs(), LOG, now=NOW)
    assert len(rows) == 2, rows
    assert "| portability | GREEN |" in rows[0], rows[0]
    assert "ready 2/37 layers on a cluster with no OCI (floor 2)" in rows[0], rows[0]
    assert "33165807800" in rows[0], rows[0]
    # The cost line is the whole point of CP2; it must survive verbatim, currency included.
    assert "cost=£0.00" in rows[1], rows[1]
    assert "wall_clock=670s" in rows[1], rows[1]
    assert "provider=github-hosted-azure" in rows[1], rows[1]


def test_a_green_run_with_no_grade_line_is_not_run_never_green():
    rows = _snap().portability_row(_runs(), "the job succeeded and printed nothing\n", now=NOW)
    assert rows == ["| portability | NOT RUN | idp run 33165807800, 0.9h ago (bar 194h) is green "
                    "but its log holds no `ok portability` grade line |"], rows


def test_an_in_progress_run_is_never_the_one_that_is_graded():
    rows = _snap().portability_row(_runs(conclusion="failure"), LOG, now=NOW)
    assert rows == ["| portability | NOT RUN | no successful run of `portability-drill.yml` "
                    "(crew#488 CP1/CP2) |"], rows


def test_a_run_older_than_the_catalogue_max_age_goes_red():
    rows = _snap().portability_row(_runs(created="2026-08-10T11:05:06Z"), LOG, now=NOW)
    assert "| portability | RED |" in rows[0], rows[0]
    assert "(bar 194h)" in rows[0], rows[0]


def test_no_runs_at_all_prints_not_run():
    assert _snap().portability_row("[]", "", now=NOW) == [
        "| portability | NOT RUN | no successful run of `portability-drill.yml` (crew#488 CP1/CP2) |"]


def test_unparseable_gh_output_prints_not_run():
    assert _snap().portability_row("not json", "", now=NOW) == [
        "| portability | NOT RUN | `gh run list -w portability-drill.yml` did not answer JSON |"]


def test_the_row_is_wired_into_the_snapshot_body():
    src = (ROOT / "scripts" / "estate-snapshot").read_text()
    body = src[src.index("def main("):]
    assert "portability," in body, "portability() is not in main()'s row tuple"
