#!/usr/bin/env python3
"""Sync the estate board JSONL cache to GitHub issue #102.

Reads rows from ~/.claude/ESTATE_BOARD.jsonl (the offline cache the prompt hooks
read) and posts each row as a comment on the GitHub issue that IS the board.
A row that fails to land is dead-lettered to ~/.claude/state/board-deadletter.jsonl
and warned loudly - never dropped silently.

Comment format on the issue: `- `ts` **from** (kind/priority): message`.

Idempotent via a marker file at ~/.claude/state/board-sync.lastid that stores
the numeric ID of the highest comment successfully posted on the previous run.

Exit codes:
    0 - all rows posted successfully
    1 - some rows dead-lettered (partial success)
    2 - total failure (could not read cache, etc.)
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Tuple

CACHE_PATH = Path(os.path.expanduser("~/.claude/ESTATE_BOARD.jsonl"))
DEADLETTER_PATH = Path(os.path.expanduser("~/.claude/state/board-deadletter.jsonl"))
MARKER_PATH = Path(os.path.expanduser("~/.claude/state/board-sync.lastid"))
STATE_DIR = Path(os.path.expanduser("~/.claude/state"))

DEFAULT_REPO = "chidionyema/crew"
DEFAULT_ISSUE = 102

API_BASE = "https://api.github.com"


def _state_dir() -> Path:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    return STATE_DIR


def load_marker() -> int:
    """Return the highest comment ID already posted, or 0 if none."""
    try:
        text = MARKER_PATH.read_text(encoding="utf-8").strip()
        return int(text) if text else 0
    except (FileNotFoundError, ValueError):
        return 0


def save_marker(comment_id: int) -> None:
    _state_dir()
    MARKER_PATH.write_text(str(comment_id), encoding="utf-8")


def format_comment(row: Dict[str, Any]) -> str:
    """Render a board row as the markdown comment shown on the issue."""
    ts = row.get("ts", "?")
    frm = row.get("from", "?")
    kind = row.get("kind", "info")
    priority = row.get("priority", "info")
    message = row.get("message", "")
    return f"- `{ts}` **{frm}** ({kind}/{priority}): {message}"


def read_cache(path: Path) -> Iterable[Tuple[int, Optional[Dict[str, Any]], Optional[str]]]:
    """Yield (lineno, row_or_None, error_or_None) for each non-empty line.

    Malformed JSON yields (lineno, None, error_string) so the caller can
    dead-letter it without aborting the whole sync.
    """
    with path.open("r", encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, start=1):
            line = raw.strip()
            if not line:
                continue
            try:
                yield lineno, json.loads(line), None
            except json.JSONDecodeError as exc:
                yield lineno, None, str(exc)


def post_comment(repo: str, issue_number: int, body: str, token: Optional[str]) -> int:
    """POST a comment to GitHub and return its numeric ID.

    Raises urllib.error.HTTPError on 4xx/5xx, OSError on network failure.
    """
    url = f"{API_BASE}/repos/{repo}/issues/{issue_number}/comments"
    payload = json.dumps({"body": body}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "estate-board-sync/1.0",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=15) as resp:  # nosec - URL is a constant
        data = json.loads(resp.read().decode("utf-8"))
        return int(data["id"])


def dead_letter(target_issue: int, row: Any, error: str) -> None:
    """Append a failure record to the dead-letter file."""
    _state_dir()
    record = {
        "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "target": f"issue#{target_issue}",
        "row": row,
        "error": error,
    }
    with DEADLETTER_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"DEAD-LETTERED issue#{target_issue}: {error}", file=sys.stderr)


def sync(
    repo: Optional[str] = None,
    issue_number: Optional[int] = None,
    token: Optional[str] = None,
    cache_path: Optional[Path] = None,
    *,
    max_post: Optional[int] = None,
) -> int:
    """Run one sync pass. Returns the exit code."""
    repo = repo or os.environ.get("GITHUB_REPO", DEFAULT_REPO)
    issue_number = int(issue_number or os.environ.get("ISSUE_NUMBER", DEFAULT_ISSUE))
    token = token if token is not None else os.environ.get("GITHUB_TOKEN")
    cache_path = cache_path or CACHE_PATH

    if not cache_path.exists():
        print(f"cache not found: {cache_path}", file=sys.stderr)
        return 2

    marker = load_marker()
    posted = 0
    dead_lettered = 0
    seen = 0

    for lineno, row, err in read_cache(cache_path):
        seen += 1
        if row is None:
            dead_letter(issue_number, {"lineno": lineno, "raw_error": "malformed JSON"}, err or "malformed JSON")
            dead_lettered += 1
            continue

        comment_id_marker = row.get("id")
        if isinstance(comment_id_marker, int) and comment_id_marker <= marker:
            continue

        if max_post is not None and posted >= max_post:
            break

        body = format_comment(row)
        try:
            new_id = post_comment(repo, issue_number, body, token)
        except urllib.error.HTTPError as exc:
            dead_letter(issue_number, row, f"HTTP {exc.code}: {exc.reason}")
            dead_lettered += 1
            continue
        except (urllib.error.URLError, OSError, TimeoutError) as exc:
            dead_letter(issue_number, row, f"network: {exc}")
            dead_lettered += 1
            continue

        save_marker(new_id)
        marker = new_id
        posted += 1

    print(f"sync: seen={seen} posted={posted} dead_lettered={dead_lettered} marker={marker}")
    if dead_lettered == 0:
        return 0
    if posted == 0:
        return 2
    return 1


def main(argv: Optional[Iterable[str]] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    return sync()


if __name__ == "__main__":
    raise SystemExit(main())
