"""Incident tests. Each one is a way a green tick could be a lie.

Named for the failure, asserting the rule, not the implementation.
"""

from pathlib import Path

import pytest

from crew import bdd, board as B
from crew.thread import Entry, latest, marker, parse_comments

BEHAVE_NOTHING_MATCHED = """\
0 features passed, 0 failed, 0 skipped
0 scenarios passed, 0 failed, 0 skipped
0 steps passed, 0 failed, 0 skipped, 0 undefined
"""

BEHAVE_GREEN = """\
1 feature passed, 0 failed, 0 skipped
3 scenarios passed, 0 failed, 0 skipped
9 steps passed, 0 failed, 0 skipped, 0 undefined
"""

BEHAVE_RED = """\
0 features passed, 1 failed, 0 skipped
2 scenarios passed, 1 failed, 0 skipped
7 steps passed, 1 failed, 2 skipped, 0 undefined
"""


def result(output, code):
    p, f = bdd.parse_counts(output)
    return bdd.Result(cp="CP1", tag="@cp1", command="behave", exit_code=code,
                      output=output, scenarios_passed=p, scenarios_failed=f)


def test_incident_zero_scenarios_is_not_a_pass():
    """behave exits 0 when a tag matches nothing. That must never tick a box."""
    r = result(BEHAVE_NOTHING_MATCHED, 0)
    assert r.exit_code == 0
    assert r.ran_nothing
    assert not r.passed
    assert "no scenarios matched" in r.verdict


def test_a_green_run_passes():
    r = result(BEHAVE_GREEN, 0)
    assert r.passed and r.verdict == "PASS"


def test_a_failed_scenario_fails_even_on_exit_zero():
    r = result(BEHAVE_RED, 0)
    assert not r.passed


def test_unparseable_output_is_not_a_pass():
    r = result("the runner crashed before it printed anything", 0)
    assert not r.passed


def test_incident_evidence_is_never_a_tick():
    """`crew evidence` reports a build. Only a real suite run changes a box."""
    b = B.Board(checkpoints=[B.Checkpoint("CP1", "worker responds")])
    assert not b.get("CP1").done
    assert b.tick("CP1").get("CP1").done
    assert not b.tick("CP1").tick("CP1", False).get("CP1").done


def test_incident_own_homework_is_detectable():
    """QA must be able to see who posted the evidence before it verifies."""
    comments = [{"body": marker(role="engineering", kind="evidence", cp="CP1", result="pass") + "\nbuilt it",
                 "author": {"login": "chidionyema"}, "createdAt": "2026-08-22T07:00:00Z"}]
    ev = latest(parse_comments(comments), kind="evidence", cp="CP1")
    assert ev is not None and ev.role == "engineering"


def test_a_comment_without_a_marker_is_not_crew_state():
    assert parse_comments([{"body": "looks good to me", "author": {"login": "x"}}]) == []


def test_find_feature_needs_the_tag(tmp_path: Path):
    (tmp_path / "a.feature").write_text("@cp2\nFeature: b\n")
    assert bdd.find_feature(tmp_path, "@cp2") is not None
    assert bdd.find_feature(tmp_path, "@cp1") is None


def test_incident_markdown_heading_in_origin_is_not_a_section_break():
    """Found 2026-08-22 by the round-trip property, on the origin "## 0".

    The parser started a new section on any line beginning "## ", so a brief
    containing a markdown heading lost that heading and everything under it the
    next time any crew command rewrote the issue body. Silent data loss in the
    one place the crew keeps its shared state.
    """
    from crew import board as B

    brief = "The shop must survive a fire.\n\n## Background\n\nOne box, one region."
    b = B.Board(origin=brief, checkpoints=[B.Checkpoint(id="CP1", title="it serves", done=False)])
    got = B.parse(B.render(b))
    assert got.origin == brief
    assert got.checkpoints == b.checkpoints


def test_incident_doctor_does_not_name_a_config_file_that_is_absent(tmp_path, monkeypatch):
    """Found 2026-08-22. `crew doctor` printed

        PASS  config for chidionyema/crew  /Users/.../crew/.crew.json

    in a repo with no .crew.json. `config.load` falls back to the git remote,
    which is correct, but doctor reported the fallback as a file on disk. A
    green line naming a path that is not there is the false-green class.
    """
    import subprocess, sys, os
    repo = tmp_path / "r"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "remote", "add", "origin",
                    "git@github.com:someone/thing.git"], cwd=repo, check=True)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = subprocess.run([sys.executable, "-m", "crew.cli", "doctor"],
                         cwd=repo, capture_output=True, text=True,
                         env={**os.environ, "PYTHONPATH": root})
    line = next((l for l in (out.stdout + out.stderr).splitlines() if "config for" in l), "")
    assert line, f"doctor printed no config line:\n{out.stdout}{out.stderr}"
    assert ".crew.json" not in line.split("config for")[-1].split("  ", 1)[-1] or "no .crew.json" in line, \
        f"doctor named a config file that is not on disk: {line}"


# --- the pytest adapter -------------------------------------------------------

def test_pytest_summary_is_read_the_same_way_as_behave():
    """crew is not behave-only. A repo already testing with pytest keeps its
    runner and its checkpoints, instead of writing Gherkin to describe python.
    """
    from crew import bdd

    assert bdd.runner_kind(".venv/bin/behave --tags={tag}") == "behave"
    assert bdd.runner_kind(".venv/bin/python -m pytest -q -m {cp}") == "pytest"

    assert bdd.parse_counts("14 passed in 3.78s") == (14, 0)
    assert bdd.parse_counts("1 failed, 13 passed in 1.98s") == (13, 1)
    assert bdd.parse_counts("===== 2 failed, 1 error, 3 passed in 0.4s =====") == (3, 3)
    assert bdd.parse_counts("3 passed, 2 skipped in 0.1s") == (3, 0)
    # behave still wins when both shapes could appear
    assert bdd.parse_counts("2 scenarios passed, 0 failed\n5 passed in 1s") == (2, 0)


def test_incident_an_empty_pytest_run_is_never_a_pass():
    """The whole reason this module exists, in the second runner.

    `pytest -m cp9` with no test marked cp9 prints "no tests ran in 0.01s" and
    exits 5. Nothing about that is a passing checkpoint, and a parser that
    shrugged and returned (0, 0) without the ran_nothing guard would tick the
    box on an empty run.
    """
    from crew import bdd

    assert bdd.parse_counts("no tests ran in 0.01s") == (0, 0)
    r = bdd.Result(cp="CP9", tag="@cp9", command="pytest -m cp9", exit_code=5,
                   output="no tests ran in 0.01s", scenarios_passed=0, scenarios_failed=0)
    assert r.ran_nothing
    assert not r.passed
    assert r.verdict.startswith("FAIL")

    # and the same run reported with exit code 0, which is the dangerous shape
    r0 = bdd.Result(cp="CP9", tag="@cp9", command="pytest -m cp9", exit_code=0,
                    output="no tests ran in 0.01s", scenarios_passed=0, scenarios_failed=0)
    assert not r0.passed
