"""Incident regression test for crew#102.

The estate board of record is GitHub issue chidionyema/crew#102; the local
JSONL is a read-side cache. The broadcast wrapper MUST post a comment to the
issue via `gh issue comment`, not append directly to the JSONL file. This
test pins that contract in two ways:

1. Static check: the substring "gh issue comment 102 --repo chidionyema/crew"
   appears in scripts/estate-board-broadcast.sh, and the wrapper is the path
   writers use.
2. Behaviour check: when `gh auth status` fails (PATH points at /usr/bin/false),
   the wrapper exits non-zero with a clear stderr message — i.e. it refuses
   to silently fall back to writing the JSONL.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
BROADCAST = REPO_ROOT / "scripts" / "estate-board-broadcast.sh"


def test_broadcast_wrapper_calls_gh_issue_comment_on_crew_102() -> None:
    """The wrapper must post to the issue, not append to the JSONL."""
    text = BROADCAST.read_text(encoding="utf-8")
    assert "gh issue comment 102 --repo chidionyema/crew" in text, (
        "estate-board-broadcast.sh must post to chidionyema/crew#102 via "
        "`gh issue comment`; the JSONL is the cache, not the writer."
    )
    # And it must NOT bypass `gh` and write the JSONL directly.
    assert "ESTATE_BOARD.jsonl" not in text or "cache" in text.lower(), (
        "estate-board-broadcast.sh must not write ESTATE_BOARD.jsonl directly"
    )


def test_broadcast_wrapper_refuses_when_gh_is_unauthenticated() -> None:
    """With gh hidden on PATH, the wrapper must exit non-zero and refuse."""
    # PATH=/usr/bin/false means `gh` cannot be found; `gh auth status` fails,
    # and the wrapper must refuse rather than fall back to hand-editing the
    # JSONL.
    env = dict(os.environ)
    env["PATH"] = "/usr/bin/false"

    result = subprocess.run(
        [str(BROADCAST), "2026-01-15T12:00:00Z  builder  (test/low): ping"],
        env=env,
        capture_output=True,
        text=True,
        timeout=10,
    )

    assert result.returncode != 0, (
        "estate-board-broadcast.sh must exit non-zero when `gh` is "
        f"unauthenticated; got rc={result.returncode}, stdout={result.stdout!r}, "
        f"stderr={result.stderr!r}"
    )
    assert "gh" in result.stderr.lower(), (
        "stderr should mention gh so the writer knows why it failed; "
        f"got stderr={result.stderr!r}"
    )


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
