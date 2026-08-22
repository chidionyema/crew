"""CP1: crew tracks its own work through crew.

The crew repo used to be the one repo the crew did not manage. Five commits went
straight to main with no issue, no checkpoint and no independent verification,
while the tool that exists to stop exactly that sat in the same directory.
"""

import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.cp1
def test_the_repo_carries_a_committed_crew_config():
    cfg = ROOT / ".crew.json"
    assert cfg.exists(), "no .crew.json — the crew cannot track a repo it is not configured for"
    tracked = subprocess.run(["git", "ls-files", "--error-unmatch", ".crew.json"],
                             cwd=ROOT, capture_output=True, text=True)
    assert tracked.returncode == 0, ".crew.json exists but is not committed, so no other agent has it"
    data = json.loads(cfg.read_text())
    assert data["repo"] == "chidionyema/crew"


@pytest.mark.cp1
def test_the_runner_is_pytest_and_crew_understands_it():
    from crew import bdd, config

    cfg = config.load(str(ROOT))
    assert bdd.runner_kind(cfg.bdd_command) == "pytest", \
        "crew must read this repo's real runner, not require Gherkin to describe python"
    assert bdd.parse_counts("14 passed in 3.78s") == (14, 0)
    assert bdd.parse_counts("no tests ran in 0.01s") == (0, 0)


@pytest.mark.cp1
def test_every_checkpoint_has_a_test_before_its_box_can_be_ticked():
    from crew import bdd, config

    cfg = config.load(str(ROOT))
    for cp in ("CP1", "CP2", "CP3", "CP4"):
        found = bdd.find_case("pytest", cfg.root, cfg.features_dir, bdd.tag_for(cp), cp)
        assert found is not None, f"{cp} has no test carrying @pytest.mark.{cp.lower()}"


@pytest.mark.cp1
def test_the_issue_for_this_build_exists_and_is_managed_by_crew():
    out = subprocess.run(
        ["gh", "issue", "list", "--repo", "chidionyema/crew", "--label", "crew",
         "--state", "all", "--json", "number,title"],
        capture_output=True, text=True, cwd=ROOT)
    assert out.returncode == 0, f"gh failed: {out.stderr}"
    issues = json.loads(out.stdout or "[]")
    assert issues, "no crew-managed issue in this repo — the work is untracked"
