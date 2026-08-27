"""crew#373, 2026-08-27: datamap graded 39 scheduled jobs "unmonitored" because their plists lack
hc-wrap, while Dagster ran every one of them from schedule.yml and wrote exit status and duration
per run (dagster-runs, crew#376). Rule: a label in schedule.yml is monitored; a label in neither
schedule.yml nor an hc-wrap plist is not. Rung 4, both ways."""
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "science"))
import producers  # noqa: E402


def test_a_dagster_job_is_monitored_and_a_bare_launchd_job_is_not(tmp_path, monkeypatch):
    pytest.importorskip("yaml")
    sched = tmp_path / "schedule.yml"
    sched.write_text("jobs:\n  ai.estate.example:\n    command: [/usr/bin/true]\n    cron: '* * * * *'\n")
    monkeypatch.setattr(producers, "SCHEDULE_YML", sched)
    assert producers._monitored(None, "ai.estate.example") is True
    assert producers._monitored(None, "ai.estate.other") is False
    assert producers._monitored(str(tmp_path / "missing.plist"), "ai.estate.other") is False
