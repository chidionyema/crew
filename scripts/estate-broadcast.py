#!/usr/bin/env python3
"""Cron/launchd wrapper around the bin/ estate broadcast.

Functionally identical to bin/estate-broadcast.py -- this lives at
scripts/ so launchd plists can `python3 scripts/estate-broadcast.py`
without polluting PATH with bin/. It exists so the board landing path
is unchanged regardless of how the producer invokes it.
"""
from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
BIN_BROADCAST = HERE.parent.parent / "bin" / "estate-broadcast.py"

# Ensure bin/ can import `crew.estate_board` the same way it does itself.
sys.path.insert(0, str(HERE.parent.parent))

if __name__ == "__main__":
    # Re-exec the canonical implementation so there is exactly one code path.
    if BIN_BROADCAST.exists():
        runpy.run_path(str(BIN_BROADCAST), run_name="__main__")
    else:
        # Fallback: a tree without bin/ still works (e.g., partial checkouts).
        from crew.estate_board import (  # noqa: E402
            DEADLETTER_DEFAULT,
            JSONL_DEFAULT,
            append_jsonl,
            dead_letter,
            format_comment,
            post_comment,
        )
        import json
        import subprocess

        raw = sys.stdin.read()
        rows = [ln for ln in raw.splitlines() if ln.strip()]
        if len(rows) != 1:
            print(
                f"estate-broadcast: expected exactly one JSON line, got {len(rows)}",
                file=sys.stderr,
            )
            raise SystemExit(2)

        issue = os.environ.get("ESTATE_BOARD_ISSUE", "chidionyema/crew#102")
        jsonl = Path(os.environ.get("ESTATE_BOARD_JSONL", str(JSONL_DEFAULT)))
        dead = Path(os.environ.get("ESTATE_BOARD_DEADLETTER", str(DEADLETTER_DEFAULT)))
        rc = 0
        try:
            body = format_comment(rows[0])
            post_comment(issue, body)
        except subprocess.CalledProcessError as exc:
            dead_letter(dead, rows[0], f"gh_failed: exit={exc.returncode}")
            rc = 4
        except Exception as exc:
            dead_letter(dead, rows[0], f"post_failed: {exc!r}")
            rc = 5
        try:
            append_jsonl(jsonl, rows[0])
        except Exception:
            pass
        raise SystemExit(rc)