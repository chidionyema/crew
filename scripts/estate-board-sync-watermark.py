#!/usr/bin/env python3
"""estate-board-sync-watermark.py — the watermark file that memoises the board sync.

The board of record is GitHub issue chidionyema/crew#102. Every hour, on the hourly
estate-snapshot cadence, the sync script re-reads the issue and rebuilds the
local cache at ~/.claude/ESTATE_BOARD.jsonl. Without a watermark, the only answer
to "did the cache change since the last run" is "did the file's mtime move",
and the file's mtime moves on a no-op rename (LAW 28 trap the plan names:
a session that grades the cache by age reads "fresh" forever even when nothing
changed).

This module owns the watermark contract:

    ~/.claude/state/estate-board-sync.watermark
        {"last_synced_id":  <graphql node id or null>,
         "last_synced_at": <ISO 8601 timestamp>,
         "cache_total":    <int or null>}

`last_synced_id` is the last comment's GraphQL node id. `cache_total` is the
number of rows in the cache file as the sync that wrote the watermark left it;
the next sync compares that against the live cache and rejects the watermark
when they disagree -- the cache was hand-edited, rotated, or truncated, and a
silent delta would be a silent partial. The rejection is loud: a single stderr
line starting with `RESYNC ` and a forced full re-fetch.

The watermark is written to a temporary file in the same directory and renamed
into place, mirroring the cache's own atomic-write pattern. The caller is
responsible for advancing the watermark AFTER the cache rename succeeds; a
failing rename must not advance the watermark, and the regression test
`tests/test_incident_crew102_watermark_advances_only_on_rename.py` pins that.

This module is additive. The existing `scripts/estate-board-sync.py` still
exposes the contract `parse_comment`, `fetch_comments`, `rows_from`,
`sync_estate_board`, `main`, `COMMENT_FULL_RE`, `COMMENT_SIMPLE_RE`; this
module is loaded by it and by the graphql helper, never replaces it.

# Rejected: store the watermark inside the cache file itself. The cache is JSONL,
#   every line a board row, and the writer would have to either prepend a
#   meta-line (a different file format, breaking the read contract) or read the
#   last line and overload it (one more thing to break). A sidecar file keeps
#   the cache's read contract one shape.
# Rejected: store the watermark in git. The board comment stream moves faster
#   than a commit can carry it, and committing on every sync is a commit storm
#   the user's laptop cannot afford. The watermark is local state, like the
#   cache itself; both live in ~/.claude and both are recreated on a fresh home.
# Standard: docs/STANDARDS.md "Coordination" -- the estate board is the sync
#   layer (LAW 26), and the watermark is part of it.
# Deviation: none.
"""

from __future__ import annotations

import json
import os
import pathlib
import time
from datetime import datetime, timezone

#: Where the watermark lives by default. Same convention as the cache: under
#: ~/.claude, with a parallel `state/` directory so future per-sync state does
#: not crowd the read path the prompt hooks follow.
WATERMARK_DEFAULT = pathlib.Path.home() / ".claude" / "state" / "estate-board-sync.watermark"

#: A cache whose mtime is older than `now - SAFETY_WINDOW_S` while the watermark
#: says "I wrote it then" is a watermark that disagreed with the file. SAFETY
#: is generous (one minute) so a slow disk cannot false-trigger RESYNC.
SAFETY_WINDOW_S = 60


def watermark_path(env: dict | None = None) -> pathlib.Path:
    """The watermark path, overridable via ESTATE_BOARD_WATERMARK.

    The override is an absolute path; the default is under ~/.claude. Tests
    point this at tmp_path before exercising the validator.
    """
    env = env if env is not None else os.environ
    override = env.get("ESTATE_BOARD_WATERMARK")
    if override:
        return pathlib.Path(override)
    return WATERMARK_DEFAULT


def load_watermark(path: pathlib.Path | None = None) -> dict | None:
    """Read the watermark file. Returns None on missing/corrupt/invalid.

    The caller treats None as "no watermark -> full fetch". A file that exists
    but is not a JSON object with the three keys is treated the same way: a
    partial watermark is a silent partial, and silent partials are the trap.
    """
    p = path or watermark_path()
    if not p.exists():
        return None
    try:
        payload = json.loads(p.read_text())
    except (OSError, ValueError):
        return None
    if not isinstance(payload, dict):
        return None
    if not {"last_synced_id", "last_synced_at", "cache_total"}.issubset(payload.keys()):
        return None
    return payload


def save_watermark(path: pathlib.Path | None, payload: dict) -> None:
    """Write the watermark atomically (tmp + rename).

    A crash between the tmp write and the rename leaves the previous watermark
    in place; a crash between the cache rename and this one leaves the cache
    without a watermark and the next sync does a full fetch. The caller does
    NOT advance the watermark if the cache rename failed; that is what
    `tests/test_incident_crew102_watermark_advances_only_on_rename.py` pins.
    """
    p = path or watermark_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, separators=(",", ":"), sort_keys=True) + "\n")
    tmp.replace(p)


def now_iso() -> str:
    """An ISO 8601 UTC timestamp with a trailing Z.

    The same shape the board's own comments carry, so the watermark and the
    cache rows read the same way to the same reader.
    """
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def watermark_valid(
    watermark: dict | None,
    cache_path: pathlib.Path,
    now_epoch: float | None = None,
) -> bool:
    """True when the watermark still agrees with the cache.

    Two checks, both required, neither alone sufficient:

      1. `last_synced_at` is not older than the cache's mtime minus SAFETY.
         A watermark that points at the past while the cache file was rewritten
         afterwards is a watermark that was written, the cache then moved, and
         the watermark is now stale.
      2. `cache_total` matches `wc -l` of the cache. A watermark that says
         "I wrote 282 rows" and a cache that holds 281 is a watermark whose
         cache was rotated or hand-edited.

    Both checks failing open would be the silent partial. Failing closed
    triggers a loud `RESYNC ` line and a full fetch.
    """
    if not watermark:
        return False
    if not cache_path.exists():
        return False
    now = now_epoch if now_epoch is not None else time.time()
    try:
        mtime = cache_path.stat().st_mtime
    except OSError:
        return False
    try:
        last_synced = datetime.strptime(
            str(watermark.get("last_synced_at")), "%Y-%m-%dT%H:%M:%SZ"
        ).replace(tzinfo=timezone.utc).timestamp()
    except (TypeError, ValueError):
        return False
    if last_synced < mtime - SAFETY_WINDOW_S:
        return False
    try:
        total = int(watermark.get("cache_total"))
    except (TypeError, ValueError):
        return False
    try:
        with cache_path.open() as f:
            actual = sum(1 for ln in f if ln.strip())
    except OSError:
        return False
    return total == actual


def emit_resync(reason: str, path: pathlib.Path | None = None) -> None:
    """One stderr line, starting `RESYNC `. Loud, single line, machine-parseable.

    The session reads stderr through `launchd`/`UserPromptSubmit` and parses it
    on the same prefix every other board-sync grade uses. The format is part
    of the contract; the regression tests pin the prefix and the `path=`
    marker so a future rewrite cannot quietly change it.
    """
    import sys

    p = path or watermark_path()
    sys.stderr.write(f"RESYNC watermark<->cache mismatch: {reason}; path={p}\n")
