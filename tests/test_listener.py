"""What the listener must open, and what it must leave alone.

The checkpoint test in checkpoints/test_cp2_*.py only asserts the negatives, so
a listener that always says no would pass it. These are the positives. Without
them the guarantee is one-sided and a stub satisfies the contract.
"""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "crew_listener", ROOT / "integrations" / "claude-code" / "hooks" / "crew-listener.py")
listener = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(listener)


WORK = [
    "wire the lab lease into the test runner",
    "build a QA workflow that runs off this machine",
    "ok get all the rest done",
    "add a --dry-run flag to the triage tool",
    "the listener should also handle the JSON payload from Claude Code",
    "we need to migrate the DNS off the old registrar",
    "please remove the second config loader, it is the one that lies",
]

NOT_WORK = [
    "what should I read first?",
    "that fix looks fine",
    "thanks",
    "ok",
    "lgtm",
    "is the repo pushed?",
    "do you know where the evidence lives?",
    "how many items of work left",
    "why did doctor print PASS for a file that is not there",
    "status",
    "show me the board",
    "",
    "   ",
]


@pytest.mark.parametrize("text", WORK)
def test_an_instruction_opens_a_brief(text):
    work, why = listener.decide(text)
    assert work, f"the listener ignored a request: {text!r} ({why})"


@pytest.mark.parametrize("text", NOT_WORK)
def test_ordinary_conversation_is_left_alone(text):
    work, why = listener.decide(text)
    assert not work, f"the listener would open an issue for: {text!r} ({why})"


def test_it_reads_the_hook_payload_as_well_as_a_bare_sentence():
    """Claude Code sends JSON. A person piping a sentence sends a sentence."""
    assert listener.read_prompt('{"prompt": "add a flag"}') == "add a flag"
    assert listener.read_prompt("add a flag") == "add a flag"
    assert listener.read_prompt("") == ""


def test_every_decision_carries_a_reason():
    """A queue entry nobody can explain is a queue entry he will not trust."""
    for text in WORK + NOT_WORK:
        _, why = listener.decide(text)
        assert why and len(why) > 8, f"no reason given for {text!r}"
