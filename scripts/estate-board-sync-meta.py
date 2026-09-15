#!/usr/bin/env python3
"""estate-board-sync-meta.py — the meta.json that memoises the board sync (crew#102).

The board of record is GitHub issue chidionyema/crew#102. On the hourly cadence,
the sync script re-reads the issue and rebuilds the local cache at
~/.claude/ESTATE_BOARD.jsonl. Without a watermark, the only answer to "did the
cache change since the last run" is "did the file's mtime move", and a no-op
rename moves the mtime without moving any bytes (LAW 28).

This module owns the meta.json contract that the plan names:

    ~/.claude/ESTATE_BOARD.meta.json
        {"updatedAt": <issue's updatedAt, ISO 8601 with trailing Z>,
         "sha256":    <hex digest of the cache file content>}

`updatedAt` is the issue's own `updatedAt` field, read cheaply via
`gh issue view <issue> --json updatedAt`. The next sync passes that value
back as a tag; on match, the body fetch is skipped and the script goes
straight to the hash compare.

`sha256` is `hashlib.sha256(cache_bytes).hexdigest()`. The next sync hashes
the joined would-be output and compares; on match, the cache rename is
skipped and the run is logged as "fetch: cache-hit" / "write: skipped
(hash unchanged)".

The meta.json is written to a temporary file in the same directory and
renamed into place, mirroring the cache's own atomic-write pattern. A
failing rename must not advance the meta.json; a stale meta.json drops
back to a full fetch.

This module is additive. The existing `scripts/estate-board-sync.py` and
its sibling `estate-board-sync-watermark.py` continue to expose their
existing contracts. The plan's proof lines — `--prove`, "fetch: cache-hit",
"write: skipped (hash unchanged)" — are wired here.

# Rejected: store the meta inside the cache file itself. The cache is JSONL,
#   every line a board row, and the writer would have to either prepend a
#   meta-line (a different file format, breaking the read contract) or read the
#   last line and overload it (one more thing to break). A sidecar file keeps
#   the cache's read contract one shape.
# Rejected: store the meta in git. The board comment stream moves faster
#   than a commit can carry it, and committing on every sync is a commit storm
#   the user's laptop cannot afford. The meta is local state, like the cache
#   itself; both live in ~/.claude and both are recreated on a fresh home.
# Standard: docs/STANDARDS.md "Coordination" -- the estate board is the sync
#   layer (LAW 26), and the meta is part of it.
# Deviation: coexists with the in-flight watermark module rather than replacing
#   it. The plan names updatedAt + sha256 as the meta contract; the watermark
#   module keeps its last_synced_id / last_synced_at / cache_total contract
#   unchanged.
"""

from __future__ import annotations

import hashlib
import json
import os
import pathlib

#: Where the meta.json lives by default. Sidecar to the cache, no `state/`
#: subdir, so the read side finds it without descending.
META_DEFAULT = pathlib.Path.home() / ".claude" / "ESTATE_BOARD.meta.json"


def meta_path(env: dict | None = None) -> pathlib.Path:
    """The meta.json path, overridable via ESTATE_BOARD_META.

    The override is an absolute path; the default is under ~/.claude. Tests
    point this at tmp_path before exercising the validator.
    """
    env = env if env is not None else os.environ
    override = env.get("ESTATE_BOARD_META")
    if override:
        return pathlib.Path(override)
    return META_DEFAULT


def load_meta(path: pathlib.Path | None = None) -> dict | None:
    """Read the meta.json. Returns None on missing/corrupt/invalid.

    The caller treats None as "no meta.json -> full fetch". A file that exists
    but is not a JSON object with the two required keys is treated the same
    way: a partial meta is a silent partial, and silent partials are the trap.
    """
    p = path or meta_path()
    if not p.exists():
        return None
    try:
        payload = json.loads(p.read_text())
    except (OSError, ValueError):
        return None
    if not isinstance(payload, dict):
        return None
    if not {"updatedAt", "sha256"}.issubset(payload.keys()):
        return None
    return payload


def save_meta(path: pathlib.Path | None, payload: dict) -> None:
    """Write the meta.json atomically (tmp + rename).

    A crash between the tmp write and the rename leaves the previous meta.json
    in place; a crash between the cache rename and this one leaves the cache
    without a meta.json and the next sync does a full fetch.
    """
    p = path or meta_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, separators=(",", ":"), sort_keys=True) + "\n")
    tmp.replace(p)


def compute_sha256(cache_path: pathlib.Path) -> str | None:
    """sha256 of the cache file's bytes, or None if the file does not exist."""
    try:
        return hashlib.sha256(cache_path.read_bytes()).hexdigest()
    except OSError:
        return None


def hash_joined(rows: list[dict]) -> str:
    """sha256 of the would-be JSONL output, the line shape the cache writer uses.

    Sorting the keys keeps the digest stable across Python dict orderings; the
    trailing newline matches what `sync_estate_board` writes.
    """
    joined = "".join(json.dumps(r, sort_keys=True) + "\n" for r in rows)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()
