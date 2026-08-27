"""crew#369, 2026-08-27: `act/run_duration` was graded NEVER_EMITTED ("launchd records exit codes,
no series of durations exists") after launchd had been retired to Dagster (crew#85) and Dagster's
run store had been registered as source `dagster-runs` (crew#376) with start_time and end_time
on every row. The register said a gap the warehouse had already closed.

Rule: `act/run_duration` is COLLECTED and its reader names a registered source whose query
carries both start_time and end_time. Rung 4, one incident.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _sources():
    doc = json.loads((ROOT / "science/sources.json").read_text())
    return {s["name"]: s for s in doc["sources"]}


def test_incident_crew369_run_duration_reader_is_a_source_with_start_and_end():
    entries = json.loads((ROOT / "science/verdicts.json").read_text())["entries"]
    e = next(x for x in entries if x["key"] == "act/run_duration")
    assert e["verdict"] == "COLLECTED", e
    named = [n for n in _sources() if f"source {n}" in e["reader"]]
    assert named, e["reader"]
    q = _sources()[named[0]]["query"]
    assert "start_time" in q and "end_time" in q, q


def test_incident_crew369_a_source_without_end_time_could_not_carry_the_grade():
    # the refusing half: the only other dagster source (ticks) has no end_time, so it cannot be the reader
    ticks = _sources()["dagster-ticks"]["query"]
    assert "end_time" not in ticks
