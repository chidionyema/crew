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
