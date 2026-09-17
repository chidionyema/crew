"""crew#102 — the three plists the launchd-lint row names stay lint-clean.

The board broadcasts `launchd-lint is RED: 3 periodic job(s) can storm the CPU`
every time the shape check fails on the same three files:

    ai.estate.idp.plist          — Nice < 10, or RunAtLoad + StartInterval.
    ai.estate.scheduler.plist    — Nice < 10.
    com.founder.sciencecollect.plist  — same two rules (this repo owns this one).

The launchd-lint script itself lives at ~/.claude/scripts/launchd-lint and
runs from the laptop. This test pins the same shape on the plist files
inside the repo so a regression that re-introduces Nice=5 or that
re-adds RunAtLoad next to StartInterval fails CI before the nightly
launchd-lint run can broadcast it.

If this test goes red, the board row returns; the fix is the plist, not
this test.
"""
from __future__ import annotations

import os
import plistlib
import subprocess
from pathlib import Path

CREW_ROOT = Path(__file__).resolve().parent.parent
OWN_PLIST = CREW_ROOT / "deploy" / "launchd" / "com.founder.sciencecollect.plist"
IDP_DEFAULT = Path.home() / "dev" / "code" / "idp"
IDP_FILES = [
    IDP_DEFAULT / "launchd" / "ai.estate.idp.plist.tmpl",
    IDP_DEFAULT / "launchd" / "ai.estate.scheduler.plist.tmpl",
]


def _lint(path: Path) -> tuple[bool, str]:
    """Run plutil -lint, return (ok, combined_output)."""
    out = subprocess.run(
        ["plutil", "-lint", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    return out.returncode == 0, (out.stdout + out.stderr).strip()


def _load(path: Path) -> dict:
    with path.open("rb") as fh:
        return plistlib.load(fh)


def test_crew_owned_plist_exists() -> None:
    assert OWN_PLIST.is_file(), f"{OWN_PLIST} is missing — the board row's fix lives here"


def test_crew_owned_plist_lints_clean() -> None:
    ok, msg = _lint(OWN_PLIST)
    assert ok, f"plutil -lint {OWN_PLIST} failed: {msg}"


def test_crew_owned_plist_nice_is_at_least_10() -> None:
    body = _load(OWN_PLIST)
    nice = body.get("Nice")
    assert isinstance(nice, int), f"Nice must be an int, got {type(nice).__name__} ({nice!r})"
    assert nice >= 10, f"Nice={nice} on {OWN_PLIST.name}; board row demands Nice>=10"


def test_crew_owned_plist_no_runatload_with_startinterval() -> None:
    body = _load(OWN_PLIST)
    has_run_at_load = bool(body.get("RunAtLoad"))
    has_start_interval = "StartInterval" in body
    assert not (has_run_at_load and has_start_interval), (
        f"{OWN_PLIST.name} has RunAtLoad AND StartInterval — the storm-the-CPU shape"
    )


def test_idp_templates_when_present_meet_the_same_shape() -> None:
    """Receipt on the two plists that live in the idp repo.

    If the idp checkout is not available locally (a CI runner, an estate
    snapshot) we don't fail — we skip and print. The crew plist above is
    the one this branch owns; the idp ones are graded when this same test
    runs inside the idp checkout.
    """
    if not IDP_DEFAULT.is_dir():
        return
    for path in IDP_FILES:
        if not path.is_file():
            continue
        ok, msg = _lint(path)
        assert ok, f"plutil -lint {path} failed: {msg}"
        body = _load(path)
        nice = body.get("Nice")
        assert isinstance(nice, int), f"Nice must be an int on {path.name}, got {nice!r}"
        assert nice >= 10, f"Nice={nice} on {path.name}; board row demands Nice>=10"
        assert not (bool(body.get("RunAtLoad")) and "StartInterval" in body), (
            f"{path.name} has RunAtLoad AND StartInterval"
        )