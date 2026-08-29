"""crew#626 CP19, founder 2026-08-29: "WE ARE NOT USING ACCEPTANCE CRITERIA".

A pull request body must carry an `Accept when:` line naming the observable state that
counts as done, and `pr-evidence.py check` refuses one that does not. Proved both ways on
literal bodies, no network.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "pr-evidence.py"


def _load():
    spec = importlib.util.spec_from_file_location("pr_evidence", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_a_body_with_a_real_criterion_passes():
    mod = _load()
    ok, why = mod.accept_when(
        "## Fix\nOne value.\n\nAccept when: `gh run view 1 --log | grep landed` prints `0 password field(s)`.\n"
    )
    assert ok, why
    ok, _ = mod.accept_when(
        "**Accept when:** the drill prints the landing path and no password box.\n"
    )
    assert ok


def test_a_body_without_the_line_or_with_a_bare_word_is_refused():
    mod = _load()
    ok, why = mod.accept_when("## Fix\nOne value.\n")
    assert not ok and "Accept when" in why
    ok, why = mod.accept_when("Accept when: green\n")
    assert not ok and "not a criterion" in why


def test_check_wires_the_criterion_in():
    src = SCRIPT.read_text()
    assert "ok_acc, why_acc = accept_when(body)" in src
    assert "selftest_accept" in src
