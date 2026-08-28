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
    """The in-flight entry is NEWER than the completed one and carries `conclusion: success`.

    crew#569 review (78caaa17): the first version gave it `conclusion: ""`, so the conclusion
    half of the filter already excluded it and the `status == "completed"` half never decided
    anything -- deleting that half left all 7 tests green. A fixture that cannot fail is the
    proxy trap, inside the file whose docstring is about the proxy trap. With this shape,
    dropping the status check selects run 33166470567 and the assertions below go red.
    """
    return json.dumps([
        {"databaseId": 33166470567, "conclusion": "success", "createdAt": "2026-08-28T11:15:33Z",
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
    """A run still in flight has no complete log to quote, so it must not be the graded one
    even when the API already reports `conclusion: success` for it."""
    rows = _snap().portability_row(_runs(), LOG, now=NOW)
    assert "33165807800" in rows[0], rows[0]
    assert "33166470567" not in rows[0], "the in-flight run was graded"


def test_a_failed_last_run_is_not_graded_as_the_successful_one():
    rows = _snap().portability_row(_runs(conclusion="failure"), LOG, now=NOW)
    assert "33166470567" not in rows[0], "the in-flight run was graded"
    assert rows == ["| portability | NOT RUN | no successful run of `portability-drill.yml` "
                    "(crew#488 CP1/CP2) |"], rows


def test_a_log_we_could_not_read_says_so_instead_of_blaming_the_drill():
    """LAW 29. `sh()` returns (124, 'TIMED OUT after 60s') or (1, '<ExcType>: ...'), both
    non-empty strings with no grade line, so without the rc the row would report the drill as
    silent when the truth is that the fetch failed."""
    rows = _snap().portability_row(_runs(), "TIMED OUT after 60s", now=NOW, log_rc=124)
    assert rows == ["| portability | NOT RUN | could not read the log of idp run 33165807800, "
                    "0.9h ago (bar 194h) (`gh run view --log` exited 124) |"], rows


def test_one_definition_of_the_last_successful_run():
    """The gatherer and the row must agree, or the row cites one run's id and quotes another's
    log. They agree by calling the same function, not by two copies staying identical."""
    snap = _snap()
    src = (ROOT / "scripts" / "estate-snapshot").read_text()
    assert src.count('r.get("conclusion") == "success"') == 1, "the selection is written twice"
    rows = json.loads(_runs())
    assert snap.last_success(rows)["databaseId"] == 33165807800
    assert snap.last_success([]) is None


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
