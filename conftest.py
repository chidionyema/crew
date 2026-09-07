"""Pytest conftest for the estate.

Boards the board-target constants at the module level so test collection does not
re-source bin/board-target on every test. The dead-letter path is exposed as a
session-scoped fixture so tests can point it at tmp_path and never touch HOME.

Issue #102 — bin/board-target is the single source of truth for the three
constants the writer (estate-broadcast.py), the doc (CREW-BOARD-VISIBILITY.md),
and these tests read from.
"""

from __future__ import annotations

import os
import pathlib
import subprocess

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent
BOARD_TARGET = REPO_ROOT / "bin" / "board-target"


@pytest.fixture(scope="session")
def board_target() -> dict[str, str]:
    """Source bin/board-target and return its key=value constants as a dict."""
    assert BOARD_TARGET.is_file(), f"missing {BOARD_TARGET}"
    out = subprocess.check_output(
        ["bash", "-c", f". '{BOARD_TARGET}' && env"],
        text=True,
    )
    keys = ("BOARD_REPO", "BOARD_ISSUE", "BOARD_DEAD_LETTER", "BOARD_COMMENT_FORMAT")
    env: dict[str, str] = {}
    for line in out.splitlines():
        for k in keys:
            if line.startswith(f"{k}="):
                env[k] = line.split("=", 1)[1]
    return env


@pytest.fixture(scope="session")
def dead_letter_path(board_target, tmp_path_factory) -> pathlib.Path:
    """Materialise the dead-letter file under a per-session tmp dir so tests
    never write HOME. The path is exposed to the test as a pathlib.Path."""
    p = pathlib.Path(
        board_target["BOARD_DEAD_LETTER"].replace("${HOME}", str(tmp_path_factory.mktemp("dl")))
    )
    p.parent.mkdir(parents=True, exist_ok=True)
    p.touch()
    os.environ["BOARD_DEAD_LETTER"] = str(p)
    return p
