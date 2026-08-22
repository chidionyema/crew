from crew.cli import parse_brief
from crew.errors import CrewError
import pytest

BRIEF = """\
# Build: Survival Stack

I need to not lose sleep. Failover between providers, cold start from my phone.

- CP1: Worker and Telegram bot responding
- CP2: Primary and standby healthy, auto-failover works
"""


def test_brief_yields_title_prose_and_checkpoints():
    title, prose, cps = parse_brief(BRIEF)
    assert title == "Build: Survival Stack"
    assert "cold start from my phone" in prose
    assert cps == [("CP1", "Worker and Telegram bot responding"),
                   ("CP2", "Primary and standby healthy, auto-failover works")]


def test_a_brief_with_no_checkpoints_is_refused():
    with pytest.raises(CrewError):
        parse_brief("# Title\n\njust prose\n")


def test_a_brief_with_no_title_is_refused():
    with pytest.raises(CrewError):
        parse_brief("- CP1: something\n")
