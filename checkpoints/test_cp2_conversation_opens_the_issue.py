"""CP2: a conversation becomes a tracked issue with no person typing `crew plan`.

Wire A in docs/explanation/CLOSING_THE_LOOP.md. Fails until it is built, which is the point:
an unbuilt checkpoint is a red box on the issue, not a silence.
"""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.cp2
def test_a_listener_exists_that_turns_a_conversation_into_a_brief():
    listener = ROOT / "integrations" / "claude-code" / "hooks" / "crew-listener.py"
    assert listener.exists(), (
        "no listener. Wire A: something has to notice the founder describing work "
        "and hand the conversation to pm-agent, without him typing a command."
    )


@pytest.mark.cp2
def test_the_listener_does_not_open_an_issue_for_ordinary_conversation():
    """The rejected design opened an issue on any sentence containing "should"
    or "fix". A queue full of noise is worse than no queue."""
    import subprocess
    import sys

    listener = ROOT / "integrations" / "claude-code" / "hooks" / "crew-listener.py"
    if not listener.exists():
        pytest.fail("no listener yet")
    for benign in ["what should I read first?", "that fix looks fine", "thanks"]:
        out = subprocess.run([sys.executable, str(listener), "--dry-run"],
                             input=benign, capture_output=True, text=True, check=False)
        assert "OPEN" not in out.stdout, f"the listener would open an issue for: {benign!r}"
