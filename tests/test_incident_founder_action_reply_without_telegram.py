"""Incident test (rung 4). 2026-08-25: the founder missed the Oracle sign-in twice because the
blocker reached one terminal of eight and never Telegram. Rule: a reply carrying FOUNDER ACTION:
is refused unless a founder-blocker Telegram row with a message_id landed in the last hour.
"""
import importlib.util
import pathlib

_P = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "claude-scripts" / "blocker-guard.py"
_spec = importlib.util.spec_from_file_location("blocker_guard", _P)
assert _spec is not None and _spec.loader is not None
bg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bg)

NOW = 1_000_000.0
REPLY = "BLOCKED: x\nFOUNDER ACTION: sign in"


def _row(age_s, msg_id=13825, source="founder-blocker", outcome="sent"):
    return {"source": source, "outcome": outcome, "msg_id": msg_id, "ts": NOW - age_s}


def test_refused_when_nothing_was_sent():
    assert bg.verdict(REPLY, [], NOW)[0] == 2


def test_refused_when_the_send_is_older_than_an_hour():
    assert bg.verdict(REPLY, [_row(7200)], NOW)[0] == 2


def test_refused_when_the_row_has_no_message_id():
    assert bg.verdict(REPLY, [_row(60, msg_id=0)], NOW)[0] == 2


def test_permitted_when_a_fresh_pinned_send_exists():
    assert bg.verdict(REPLY, [_row(60)], NOW) == (0, "")


def test_permitted_when_the_reply_has_no_founder_action():
    assert bg.verdict("INVENTORY: nothing blocked", [], NOW) == (0, "")


def test_blind_permits_and_says_so():
    code, msg = bg.verdict(REPLY, None, NOW)
    assert code == 0 and "BLIND" in msg


def test_session_flag_with_a_space_is_not_a_target():
    # defect (2) from review: `--session <id>` was parsed as the positional target
    src = (_P.parent / "founder-blocker.py").read_text()
    assert 'a == "--session" and i + 1 < len(argv)' in src
