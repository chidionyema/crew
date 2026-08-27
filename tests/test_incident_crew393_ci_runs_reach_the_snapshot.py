"""crew#393 (crew#320 register): 33 workflows across the estate produced runs with durations,
queue waits and pass rates in the Actions API, and nothing pulled them; the register said
NEVER_EMITTED for every one. Rung 4, incident test: the collector turns the API shape into one
row per (repo, workflow), the snapshot row reads those rows, and both the empty and the stale
case print NOT RUN, never a number.
"""
import datetime as dt
import importlib.machinery
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "science"))
import outcomes  # noqa: E402

NOW = dt.datetime(2026, 8, 27, 4, 0, tzinfo=dt.UTC)


def _snap():
    loader = importlib.machinery.SourceFileLoader("snap", str(ROOT / "scripts" / "estate-snapshot"))
    spec = importlib.util.spec_from_loader("snap", loader)
    assert spec is not None
    m = importlib.util.module_from_spec(spec)
    loader.exec_module(m)
    return m


def _run(path, created, started, updated, conclusion="success", status="completed"):
    return {"path": f".github/workflows/{path}", "created_at": created, "run_started_at": started,
            "updated_at": updated, "status": status, "conclusion": conclusion}


def fake_fetch(p: str):
    if p.startswith("users/"):
        return [{"name": "crew"}, {"name": "idp"}]
    if p.startswith("repos/chidionyema/idp/"):
        raise RuntimeError("HTTP 403: resource not accessible")
    return {"workflow_runs": [
        _run("crew-qa.yml", "2026-08-27T03:00:00Z", "2026-08-27T03:00:30Z", "2026-08-27T03:05:30Z"),
        _run("crew-qa.yml", "2026-08-27T02:00:00Z", "2026-08-27T02:01:00Z", "2026-08-27T02:04:00Z", "failure"),
        _run("crew-qa.yml", "2026-08-27T03:50:00Z", "2026-08-27T03:50:10Z", "2026-08-27T03:50:10Z", None, "in_progress"),
        _run("review-gate.yml", "2026-08-27T03:00:00Z", "2026-08-27T03:00:05Z", "2026-08-27T03:00:25Z"),
    ]}


def test_collector_shapes_one_row_per_workflow_and_names_a_refused_repo():
    rows = outcomes.collect_ci(now=NOW, fetch=fake_fetch)
    by = {(r["repo"], r["workflow"]): r for r in rows}
    qa = by[("crew", "crew-qa.yml")]
    assert (qa["runs"], qa["completed"], qa["passed"], qa["pass_rate"]) == (3, 2, 1, 0.5)
    assert qa["median_duration_s"] == 300.0 and qa["median_queue_wait_s"] == 60.0
    assert by[("crew", "review-gate.yml")]["median_duration_s"] == 20.0
    refused = by[("idp", None)]
    assert refused["measured"] is False and "403" in refused["reason"]


def test_snapshot_row_is_green_from_rows_and_not_run_when_stale_or_missing(tmp_path):
    snap = _snap()
    path = tmp_path / "ci-runs.jsonl"
    assert "NOT RUN" in snap.ci_row(path)[0]
    rows = outcomes.collect_ci(now=NOW, fetch=fake_fetch)
    path.write_text("".join(json.dumps(r) + "\n" for r in rows))
    fresh = snap.ci_row(path, now=NOW.timestamp() + 3600)[0]
    assert "| ci runs | GREEN |" in fresh and "2 workflows, 4 runs/24h, 2/3 passed" in fresh
    assert "slowest median 300.0s (crew/crew-qa.yml)" in fresh and "1 repo(s) refused" in fresh
    stale = snap.ci_row(path, now=NOW.timestamp() + 40 * 3600)[0]
    assert "NOT RUN" in stale and "40h old" in stale


def test_register_names_this_reader_and_the_workflow_runs_it():
    v = json.load((ROOT / "science" / "verdicts.json").open())
    entry = next(e for e in v["entries"] if e["key"] == "github/workflow/*")
    assert entry["verdict"] == "COLLECTED" and "estate-snapshot ci()" in entry["reader"]
    assert any(s["name"] == "ci_runs" for s in json.load((ROOT / "science" / "sources.json").open())["sources"])
    assert "python3 science/outcomes.py ci" in (ROOT / ".github" / "workflows" / "ci-runs.yml").read_text()


def test_pages_merge_so_a_repo_with_more_than_100_runs_a_day_is_counted():
    # first live run: gh api --paginate without --slurp made crew, idp and prospector JSONDecodeError
    pages = [{"total_count": 3, "workflow_runs": [1, 2]}, {"total_count": 3, "workflow_runs": [3]}]
    assert outcomes._merge_pages(pages) == {"total_count": 3, "workflow_runs": [1, 2, 3]}
    assert outcomes._merge_pages([[{"name": "a"}], [{"name": "b"}]]) == [{"name": "a"}, {"name": "b"}]
    assert outcomes._merge_pages({"workflow_runs": []}) == {"workflow_runs": []}
