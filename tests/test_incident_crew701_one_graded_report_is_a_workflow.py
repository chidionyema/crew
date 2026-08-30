"""crew#701 CP1: the research loop is a workflow on a runner, graded by Inspect, kept by MLflow."""

from __future__ import annotations

import pathlib
import sys

import pytest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "science"))
import research_run  # noqa: E402
import research_worker as rw  # noqa: E402

WF = yaml.safe_load((ROOT / ".github/workflows/science-research.yml").read_text())


def test_the_workflow_is_dispatchable_reads_the_router_secret_and_keeps_the_artefact():
    assert "workflow_dispatch" in WF[True] or "workflow_dispatch" in WF.get("on", {})
    steps = WF["jobs"]["research"]["steps"]
    run = next(s for s in steps if s.get("name") == "one graded report")
    assert run["env"]["ROUTER_KEY"] == "${{ secrets.SCIENCE_ROUTER_KEY }}"
    assert "science/research_run.py" in run["run"]
    art = next(s for s in steps if "upload-artifact" in s.get("uses", ""))
    assert art["if"] == "always()" and art["with"]["path"] == "research-run/"


def test_an_intake_row_becomes_a_question_that_names_the_release(tmp_path):
    q = research_run.question_for(research_run.intake_row(0))
    assert "fluxcd/flux2" in q and "v2.9.4" in q and "release notes" in q
    with pytest.raises(rw.Refused, match="does not exist"):
        research_run.intake_row(10_000)


def test_a_failed_grade_drops_the_report(tmp_path, monkeypatch):
    monkeypatch.setattr(rw, "configure", lambda w, g: {})
    monkeypatch.setattr(
        research_run,
        "research",
        lambda q, r: {"report": "r", "sources": ["https://a"], "costs_usd": 0},
    )
    monkeypatch.setattr(research_run, "grade", lambda *a, **k: 0.0)
    monkeypatch.setattr(research_run, "record", lambda *a, **k: "ml1")
    out = tmp_path / "o"
    rc = research_run.main(["--question", "q", "--out", str(out)])
    assert rc == 1 and not (out / "report.md").exists()
    monkeypatch.setattr(research_run, "grade", lambda *a, **k: 1.0)
    rc = research_run.main(["--question", "q", "--out", str(out)])
    assert rc == 0 and (out / "report.md").read_text().startswith("# q")


def test_the_default_lanes_are_on_a_key_that_also_carries_embed(monkeypatch):
    """Run 33304930630: worker minimax on a key with no embed row -> GPT Researcher's context
    compression 403s and the report is hollow. The defaults are the frontier lanes the science
    router key carries beside embed (idp vault-seed.yml, science entry); the workflow says the same."""
    monkeypatch.delenv("RESEARCH_WORKER_LANE", raising=False)
    monkeypatch.delenv("RESEARCH_GRADER_LANE", raising=False)
    wf = yaml.safe_load((ROOT / ".github" / "workflows" / "science-research.yml").read_text())
    inputs = wf[True]["workflow_dispatch"]["inputs"]
    src = (ROOT / "science" / "research_run.py").read_text()
    assert inputs["worker"]["default"] == "claude" and '"RESEARCH_WORKER_LANE", "claude"' in src
    assert inputs["grader"]["default"] == "claude-fast" and '"RESEARCH_GRADER_LANE", "claude-fast"' in src
    req = (ROOT / "requirements-research.txt").read_text()
    assert "openai>=3.1" in req, "Inspect's openai provider refuses openai<3.1 (run 33304930630)"
    assert "litellm>=1.84" in req, "pip-audit: litellm 1.83.0 carries 11 known vulnerabilities (run 33305374523)"
