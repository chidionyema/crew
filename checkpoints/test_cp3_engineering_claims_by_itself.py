"""CP3: engineering claims a checkpoint and posts evidence with no person typing.

Wire B in docs/explanation/CLOSING_THE_LOOP.md.
"""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.cp3
def test_an_engineering_runner_exists():
    runner = ROOT / "integrations" / "claude-code" / "crew-engineer.py"
    assert runner.exists(), (
        "no engineering runner. Wire B: something has to read the open checkpoints, "
        "claim one, build until its test passes, and post evidence."
    )


@pytest.mark.cp3
def test_the_engineering_runner_cannot_tick_a_box():
    runner = ROOT / "integrations" / "claude-code" / "crew-engineer.py"
    if not runner.exists():
        pytest.fail("no engineering runner yet")
    src = runner.read_text()
    assert "crew verify" not in src, (
        "the engineering runner calls `crew verify`. The whole guarantee is that the "
        "role which built the thing cannot be the role that ticks its box."
    )
