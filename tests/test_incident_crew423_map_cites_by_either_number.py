"""crew#423: law_enforcement graded three live git-hook guards dead because the
map was renumbered (law=9) while the hook still cites the original number
(LAW 32), and it had no way to see a GitHub Actions gate at all, so three
mechanical laws sat in the gap with a running workflow enforcing them.

Rules: a hook citing either the effective or the original number is live;
a workflow guard is live only when science/ci-runs.jsonl shows it completed
in-window for this repo. Rung 4, incident tests, proved both ways.
"""
import json

from science import law_enforcement as le


def test_hook_citing_the_original_number_is_live(monkeypatch):
    monkeypatch.setattr(le, "global_bind", lambda: True)
    monkeypatch.setattr(le, "law_refs", lambda name: {32})
    entry = {"law": 9, "was": 32, "guards": ["hooks/pre-push"]}
    assert le.derive(entry, {}) == "live"
    assert le.derive({"law": 9, "was": 31, "guards": ["hooks/pre-push"]}, {}) == "dead"


def test_workflow_guard_is_live_only_when_ci_record_shows_a_run(tmp_path):
    ci = tmp_path / "ci-runs.jsonl"
    row = {"at": "2026-08-27T03:00:00Z", "repo": "crew", "workflow": "review-gate.yml",
           "measured": True, "completed": 160}
    now = 1787799600.0  # 2026-08-27T04:20:00Z
    ci.write_text(json.dumps(row) + "\n")
    assert le.workflow_ran("review-gate.yml", ci_runs=str(ci), repo="crew", now=now)
    assert not le.workflow_ran("review-gate.yml", ci_runs=str(ci), repo="idp", now=now)
    assert not le.workflow_ran("review-gate.yml", ci_runs=str(ci), repo="crew", now=now + 40 * 3600)
    ci.write_text(json.dumps({**row, "completed": 0}) + "\n")
    assert not le.workflow_ran("review-gate.yml", ci_runs=str(ci), repo="crew", now=now)
    assert not le.workflow_ran("review-gate.yml", ci_runs=str(tmp_path / "missing"), repo="crew", now=now)


def test_every_guard_the_map_names_is_a_file_or_a_workflow_in_this_repo():
    """The class behind crew#423: a map naming a guard nothing runs."""
    import os
    m = json.load(open(os.path.join(os.path.dirname(le.__file__), "enforcement-map.json")))
    root = os.path.dirname(os.path.dirname(le.__file__))
    missing = []
    for x in m["laws"]:
        for g in x.get("guards") or []:
            if g.startswith(".github/workflows/"):
                ok = os.path.exists(os.path.join(root, g))
            elif g.startswith("hooks/") or g.endswith(".py"):
                ok = True  # lives in ~/.claude/scripts, graded by law_enforcement itself
            else:
                ok = os.path.exists(os.path.join(root, g))
            if not ok:
                missing.append((x.get("rule"), g))
    assert missing == []
