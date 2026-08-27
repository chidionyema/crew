"""crew#508 CP2: every lane lands facts in the warehouse. The code lane shipped stale (closes
an idle PR) and wake-blocked (reopens it when its Blocked-by lands) in crew#504 and recorded
nothing. Incident test: the collector counts a stale close and a wake reopen from the API
shape, ignores a merge and an old close, names a refused repo, and the registry admits the
ledger as a source with a receiver.
"""
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "science"))
import outcomes  # noqa: E402

NOW = dt.datetime(2026, 8, 27, 15, 0, tzinfo=dt.UTC)


def _pr(n, state, updated, closed=None, merged=None, labels=()):
    return {"number": n, "state": state, "updated_at": updated, "closed_at": closed, "merged_at": merged,
            "labels": [{"name": lb} for lb in labels]}


def fake_fetch(p: str):
    if p.startswith("users/"):
        return [{"name": "crew"}, {"name": "idp"}]
    if p.startswith("repos/chidionyema/idp/"):
        raise RuntimeError("HTTP 403: resource not accessible")
    if "/pulls?" in p:
        return [
            _pr(1, "closed", "2026-08-27T10:00:00Z", closed="2026-08-27T10:00:00Z", labels=["stale"]),
            _pr(2, "closed", "2026-08-27T11:00:00Z", closed="2026-08-27T11:00:00Z", merged="2026-08-27T11:00:00Z", labels=["stale"]),
            _pr(3, "closed", "2026-08-25T10:00:00Z", closed="2026-08-25T10:00:00Z", labels=["stale"]),
            _pr(4, "open", "2026-08-27T12:00:00Z"),
            _pr(5, "open", "2026-08-27T12:30:00Z"),
        ]
    if p.endswith("/issues/4/events?per_page=100"):
        return [{"event": "reopened", "created_at": "2026-08-27T12:00:00Z", "actor": {"login": "github-actions[bot]"}}]
    if p.endswith("/issues/5/events?per_page=100"):
        return [{"event": "reopened", "created_at": "2026-08-27T12:30:00Z", "actor": {"login": "chidionyema"}}]
    raise AssertionError(p)


def test_a_stale_close_and_a_wake_reopen_are_counted_and_nothing_else():
    rows = outcomes.collect_pr_hygiene(now=NOW, fetch=fake_fetch)
    by = {r["repo"]: r for r in rows}
    crew = by["crew"]
    assert crew["measured"] is True
    assert crew["closed_by_stale"] == 1 and crew["closed_prs"] == [1]   # not the merge, not the old close
    assert crew["reopened_by_wake"] == 1 and crew["reopened_prs"] == [4]  # not the human reopen
    assert by["idp"]["measured"] is False and "403" in by["idp"]["reason"]
    assert crew["at"] == "2026-08-27T15:00:00Z"


def test_the_ledger_is_a_registered_source_with_a_receiver():
    reg = json.loads((ROOT / "science" / "sources.json").read_text())
    src = {s["name"]: s for s in reg["sources"]}["lane.code.pr-hygiene"]
    assert src["path"] == "pr-hygiene.jsonl" and src["root"] == "science"
    assert src["time_field"] == "at" and src["receiver"]
    wf = (ROOT / ".github" / "workflows" / "ci-runs.yml").read_text()
    assert "outcomes.py pr-hygiene" in wf and "science/pr-hygiene.jsonl" in wf
