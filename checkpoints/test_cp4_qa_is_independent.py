"""CP4: QA verifies on a runner engineering does not control.

Wire C in docs/explanation/CLOSING_THE_LOOP.md. A gate on the same machine as the builder is
a gate the builder can edit.
"""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "crew-qa.yml"


@pytest.mark.cp4
def test_a_qa_workflow_runs_off_this_machine():
    assert WORKFLOW.exists(), (
        "no .github/workflows/crew-qa.yml. Wire C: QA has to run somewhere the "
        "engineering agent cannot reach."
    )


@pytest.mark.cp4
def test_the_gate_refuses_a_pull_request_with_no_screenshot():
    if not WORKFLOW.exists():
        pytest.fail("no QA workflow yet")
    src = WORKFLOW.read_text()
    assert "pr-evidence check" in src, (
        "the gate does not call `pr-evidence check`. LAW 22 is enforced by the tool "
        "that counts committed images, not by grepping for a filename."
    )


@pytest.mark.cp4
def test_the_gate_refuses_a_run_that_matched_nothing():
    if not WORKFLOW.exists():
        pytest.fail("no QA workflow yet")
    src = WORKFLOW.read_text()
    assert "crew verify" in src, (
        "the gate does not call `crew verify`, so the zero-scenario refusal is a "
        "second copy of the rule instead of the one crew already enforces."
    )
