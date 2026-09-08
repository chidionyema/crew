#!/usr/bin/env python3
"""estate-broadcast.py — write every broadcast row to the estate board (crew#102).

The board is GitHub issue crew#102, not a laptop file. The local file at
~/.claude/ESTATE_BOARD.jsonl is only the offline cache the prompt hooks read.
On transport failure (network drop, 5xx, auth loss), the row MUST be appended
to the dead-letter file (read from bin/board-target) and a loud warning
emitted to stderr — never silently dropped.

Each row carries an idempotency key derived from its payload so a retry of
the same row is a no-op (it does not double-post to the board).

Constants live in bin/board-target — never typed here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def _read_board_target() -> dict:
    """Read the single source of truth: bin/board-target."""
    target = REPO_ROOT / "bin" / "board-target"
    if not target.exists():
        raise SystemExit(f"board-target missing: {target}")
    out = {}
    for line in target.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, _, v = line.partition("=")
        out[k.strip()] = v.strip()
    required = {"repo", "issue", "dead_letter"}
    missing = required - set(out)
    if missing:
        raise SystemExit(f"board-target missing keys: {sorted(missing)}")
    return out


def _idempotency_key(payload: dict) -> str:
    """Deterministic key for the row's payload (sha256, first 16 hex chars)."""
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()[:16]


def _post_to_board(repo: str, issue: str, body: str) -> None:
    """Call gh issue comment and raise on non-zero exit."""
    gh = shutil.which("gh")
    if gh is None:
        raise RuntimeError("gh CLI not on PATH")
    proc = subprocess.run(
        [gh, "issue", "comment", issue, "--repo", repo, "-b", body],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"gh issue comment failed rc={proc.returncode}: "
            f"{proc.stderr.strip()}"
        )


def _dead_letter(dead_letter_path: str, row: dict, key: str) -> None:
    """Append row to dead-letter file with loud stderr warning. Idempotent on key."""
    p = Path(dead_letter_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    existing_keys: set[str] = set()
    if p.exists():
        for line in p.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                existing_keys.add(json.loads(line).get("idempotency_key", ""))
            except json.JSONDecodeError:
                continue
    if key in existing_keys:
        print(
            f"BOARD DEAD-LETTER: idempotency_key={key} already present, "
            "retry is a no-op",
            file=sys.stderr,
        )
        return
    payload = dict(row)
    payload["idempotency_key"] = key
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, separators=(",", ":")) + "\n")
    print(
        f"BOARD DEAD-LETTER: row appended to {dead_letter_path} "
        f"(idempotency_key={key})",
        file=sys.stderr,
    )


def broadcast(payload: dict) -> int:
    """Broadcast a row to crew#102; dead-letter on failure. Returns 0 on success."""
    target = _read_board_target()
    key = _idempotency_key(payload)
    body = (
        f"`{payload['ts']}` **{payload['from']}** "
        f"({payload['kind']}/{payload['priority']}): {payload['message']}"
    )
    try:
        _post_to_board(target["repo"], target["issue"], body)
    except Exception as exc:  # noqa: BLE001 — boundary; loud on any failure
        print(f"BOARD WRITE FAILED: {exc}", file=sys.stderr)
        _dead_letter(target["dead_letter"], payload, key)
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Estate board broadcast")
    parser.add_argument("--from", dest="frm", required=True)
    parser.add_argument("--kind", required=True)
    parser.add_argument("--priority", required=True)
    parser.add_argument("--message", required=True)
    parser.add_argument("--ts", default=None)
    args = parser.parse_args()
    payload = {
        "ts": args.ts or __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "from": args.frm,
        "kind": args.kind,
        "priority": args.priority,
        "message": args.message,
    }
    return broadcast(payload)


if __name__ == "__main__":
    raise SystemExit(main())
