"""Incident (crew#345, 2026-08-26): live cluster verification stopped five times in one night
because a laptop's OCI browser session (a 60-minute JWT) had expired.

The estate snapshot is the file every session reads first, so it carries the one number the
ticket's acceptance criterion asks for: how many scheduled verify-drill runs in the last 24 hours
succeeded with nobody logged in. GREEN only when the window is full and every run passed; RED on
any failure or an empty window; COUNTING while the window fills; NOT RUN when GitHub cannot be
asked, never GREEN by default. Rung 4; drives verification_identity() through a fake sh.
"""
from __future__ import annotations

import importlib.util
import json
from datetime import UTC, datetime, timedelta
from importlib.machinery import SourceFileLoader
from pathlib import Path

SNAP = Path(__file__).resolve().parents[1] / "scripts" / "estate-snapshot"


def _load():
    loader = SourceFileLoader("estate_snapshot_345", str(SNAP))
    spec = importlib.util.spec_from_file_location("estate_snapshot_345", SNAP, loader=loader)
    assert spec is not None, SNAP
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


def _runs(n: int, conclusions: list[str] | None = None, hours_ago_start: float = 0.5):
    now = datetime.now(UTC)
    out = []
    for i in range(n):
        out.append({
            "status": "completed",
            "conclusion": (conclusions or [])[i] if conclusions and i < len(conclusions) else "success",
            "createdAt": (now - timedelta(hours=hours_ago_start + i)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        })
    return json.dumps(out)


def _row(monkeypatch, rc, body):
    mod = _load()
    monkeypatch.setattr(mod, "sh", lambda cmd, timeout=30: (rc, body))
    return mod.verification_identity()[0]


def test_a_full_green_window_is_the_green_row() -> None:
    mod = _load()
    assert mod.VERIFY_MIN_RUNS <= mod.VERIFY_WINDOW_H


def test_twenty_four_green_scheduled_runs_read_green(monkeypatch) -> None:
    row = _row(monkeypatch, 0, _runs(24))
    assert row.startswith("| OCI verification identity | GREEN 24/24"), row
    assert "zero logins" in row


def test_one_failure_in_the_window_is_red(monkeypatch) -> None:
    row = _row(monkeypatch, 0, _runs(24, ["success"] * 10 + ["failure"]))
    assert "RED 1/24 scheduled runs failed" in row, row


def test_a_window_still_filling_is_counting_not_green(monkeypatch) -> None:
    row = _row(monkeypatch, 0, _runs(3))
    assert "COUNTING 3/" in row and "GREEN" not in row, row


def test_runs_older_than_the_window_do_not_count(monkeypatch) -> None:
    # 30 green runs, all older than 24h: the schedule is dead now, however good it was yesterday
    row = _row(monkeypatch, 0, _runs(30, hours_ago_start=25))
    assert "RED 0 scheduled runs in 24h" in row, row


def test_github_unreachable_is_not_run_never_green(monkeypatch) -> None:
    row = _row(monkeypatch, 1, "")
    assert "NOT RUN" in row and "GREEN" not in row, row


def test_garbage_from_gh_is_not_run(monkeypatch) -> None:
    row = _row(monkeypatch, 0, "not json")
    assert "NOT RUN" in row, row


def test_the_row_is_in_the_snapshot_and_never_asks_for_a_login() -> None:
    src = SNAP.read_text()
    assert "verification_identity, crew_p1" in src, "the row is not wired into main()"
    assert "oci session authenticate" not in src
