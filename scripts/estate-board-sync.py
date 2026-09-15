#!/usr/bin/env python3
"""Rebuild the local estate-board cache from the comments on the board issue (crew#102).

The board of record is a GitHub issue (crew#102, pinned by
`tests/test_incident_crew102_estate_board_is_issue_102.py`). Every broadcast lands there
as a comment. Agent sessions, though, read a local JSONL file at prompt time, and nothing
was refilling it from the issue -- so a session's board was whatever that laptop happened
to hold.

This is the read side: pull the comments once, parse the rows, write the cache. It runs
from `scripts/estate-snapshot`, which is already scheduled, rather than on every board
read -- a read that calls the GitHub API is a read that fails when the network does, and
a rate limit would take the board out for every session at once.

# Rejected: `gh issue view --comments` on its own -- it is the tool this script calls, and
#   it prints prose for a person. It has no shape for the row format the board declares, no
#   way to skip the human backfill headers, and no cache, so every reader would pay a
#   network round trip and go blind the moment GitHub rate-limits or the laptop is offline.
# Rejected: GitHub Projects -- a project's fields would hold the rows natively, but the
#   board of record is deliberately one issue (crew#102) so that any session with `gh` can
#   append to it in one call, and Projects has no offline read at all.
# Standard: docs/STANDARDS.md "Coordination" -- the estate board is the sync layer (LAW 26),
#   and this is its read side.
# Deviation: none.

# Optimisation (crew#102, plan in issue body): the read path now selects only `body` and
# `databaseId` over GraphQL (`gh api graphql`), pages at 100 per request following
# `pageInfo.endCursor` while `hasNextPage` is true, and memoises a high-water mark in
# `~/.claude/state/board-sync.cursor` as {last_ts, last_count, last_comment_id}. Each
# cold-path run writes the cursor only after the atomic rename succeeds; each warm-path
# run fires a single `comments(last: 1)` query and short-circuits when the newest `ts`
# matches the cursor, skipping parse, sort, and write. The full fetch is hard-capped at
# 1000 comments with a loud stderr note when the cap is reached. Parse and sort stay lazy
# and run only when the cursor check fails; identity (same len, same max ts) also skips
# the write. The two compiled regexes stay module-scope.
"""

import json
import os
import pathlib
import re
import subprocess
import sys
from datetime import datetime

#: The format the board issue's own body declares: `ts` **from** (kind/priority): message.
COMMENT_FULL_RE = re.compile(
    r"^`(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)`\s+\*\*([^*]+?)\*\*"
    r"\s+\(([^/]+?)/([^)]+?)\):\s+(.*)$"
)
#: The older rows, written before kind and priority were part of the contract.
COMMENT_SIMPLE_RE = re.compile(
    r"^`(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)`\s+\*\*([^*]+?)\*\*:\s+(.*)$"
)

BOARD_REPO = os.environ.get("ESTATE_BOARD_REPO", "chidionyema/crew")
BOARD_ISSUE = int(os.environ.get("ESTATE_BOARD_ISSUE", "102"))
DEFAULT_CACHE = pathlib.Path.home() / ".claude" / "ESTATE_BOARD.jsonl"
CURSOR_PATH = pathlib.Path.home() / ".claude" / "state" / "board-sync.cursor"
PAGE_SIZE = 100
MAX_COMMENTS = 1000


def _owner_name(repo: str) -> tuple[str, str]:
    """Split `owner/name` once. Raises ValueError on a malformed repo string."""
    if "/" not in repo:
        raise ValueError(f"expected 'owner/name' for repo, got {repo!r}")
    owner, name = repo.split("/", 1)
    if not owner or not name:
        raise ValueError(f"expected 'owner/name' for repo, got {repo!r}")
    return owner, name


def _ts_from_body(body: str) -> str:
    """Return the `ts` at the head of a comment body, or '' when neither regex matches.

    Used by `latest_ts` to read the newest comment's timestamp without bringing every
    field across the wire.
    """
    if not body:
        return ""
    body = body.lstrip()
    m = COMMENT_FULL_RE.match(body) or COMMENT_SIMPLE_RE.match(body)
    if m:
        return m.group(1)
    return ""


def parse_comment(comment_body: str) -> dict | None:
    """One comment to one board row, or None when the comment is not a row.

    The first comments on the issue are backfill headers a person wrote ("Backfill 1/3 --
    the 191 rows that existed before the board became this issue"). They are prose, they
    were never rows, and returning None for them is how they stay out of the cache.
    """
    body = (comment_body or "").strip()
    m = COMMENT_FULL_RE.match(body)
    if m:
        ts, frm, kind, priority, message = m.groups()
        return {
            "ts": ts,
            "from": frm.strip(),
            "kind": kind.strip(),
            "priority": priority.strip(),
            "message": message.strip(),
        }
    m = COMMENT_SIMPLE_RE.match(body)
    if m:
        ts, frm, message = m.groups()
        return {
            "ts": ts,
            "from": frm.strip(),
            "kind": "unclassified",
            "priority": "info",
            "message": message.strip(),
        }
    return None


def fetch_comments(repo: str = BOARD_REPO, issue: int = BOARD_ISSUE) -> list[dict]:
    """All board comments, oldest first, projected to {databaseId, body} only.

    Uses `gh api graphql` with `first: 100` per page, following `pageInfo.endCursor`
    while `hasNextPage` is true. The selection set is exactly `databaseId` and `body`
    -- everything else (user, author_association, createdAt, updatedAt, node_id,
    reactions, performed_via_github_app) never crosses the wire.

    Hard-capped at MAX_COMMENTS. Hitting the cap emits a loud stderr note and stops
    walking pages -- the cap exists to bound memory; hitting it is a "something is
    wrong" signal, not a silent truncation.

    Raises on subprocess failure or non-JSON output -- never returns [] silently.
    """
    owner, name = _owner_name(repo)
    collected: list[dict] = []
    cursor: str | None = None
    cap_hit = False
    while True:
        page_query = (
            "query($owner: String!, $name: String!, $number: Int!, $first: Int!"
            + (", $after: String" if cursor else "")
            + ") { repository(owner: $owner, name: $name) {"
            " issue(number: $number) { comments(first: $first"
            + (", after: $after" if cursor else "")
            + ") { nodes { databaseId body } pageInfo { hasNextPage endCursor } } } } }"
        )
        cmd = [
            "gh", "api", "graphql",
            "-F", f"query={page_query}",
            "-F", f"owner={owner}",
            "-F", f"name={name}",
            "-F", f"number={issue}",
            "-F", "first=100",
        ]
        if cursor:
            cmd += ["-F", f"after={cursor}"]
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60, check=True
        )
        try:
            payload = json.loads(proc.stdout)
        except (ValueError, TypeError) as exc:
            raise ValueError(f"graphql page was not JSON: {exc}: {proc.stdout[:200]!r}") from exc
        comments = (
            payload.get("data", {})
            .get("repository", {})
            .get("issue", {})
            .get("comments", {})
        )
        nodes = comments.get("nodes") or []
        for node in nodes:
            if not isinstance(node, dict):
                continue
            collected.append(
                {"databaseId": node.get("databaseId"), "body": node.get("body", "") or ""}
            )
        page_info = comments.get("pageInfo") or {}
        if len(collected) >= MAX_COMMENTS:
            cap_hit = True
            break
        if not page_info.get("hasNextPage"):
            break
        cursor = page_info.get("endCursor")
        if not cursor:
            break
    if cap_hit and page_info.get("hasNextPage"):
        print(
            f"estate-board-sync: hard cap of {MAX_COMMENTS} comments reached -- investigate",
            file=sys.stderr,
        )
    collected.reverse()  # GraphQL returns newest-first; oldest-first for the sort.
    return collected


def latest_ts(repo: str = BOARD_REPO, issue: int = BOARD_ISSUE) -> str:
    """The `ts` of the newest comment on the board, or '' if there is no parseable row yet.

    One-shot GraphQL with `comments(last: 1)` selecting only `body`. Used by the warm
    path: when this equals the persisted `last_ts`, the board has not advanced.
    """
    owner, name = _owner_name(repo)
    query = (
        "query($owner: String!, $name: String!, $number: Int!) {"
        " repository(owner: $owner, name: $name) {"
        " issue(number: $number) { comments(last: 1) { nodes { body } } } } }"
    )
    proc = subprocess.run(
        [
            "gh", "api", "graphql",
            "-F", f"query={query}",
            "-F", f"owner={owner}",
            "-F", f"name={name}",
            "-F", f"number={issue}",
        ],
        capture_output=True, text=True, timeout=30, check=True,
    )
    try:
        payload = json.loads(proc.stdout)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"latest_ts graphql was not JSON: {exc}: {proc.stdout[:200]!r}") from exc
    nodes = (
        payload.get("data", {})
        .get("repository", {})
        .get("issue", {})
        .get("comments", {})
        .get("nodes")
        or []
    )
    if not nodes:
        return ""
    return _ts_from_body(nodes[0].get("body", "") or "")


def read_cursor(path=CURSOR_PATH) -> dict | None:
    """The persisted {last_ts, last_count, last_comment_id}, or None on missing/corrupt.

    A missing cursor or one that fails to parse is the cold path, not an error.
    """
    p = pathlib.Path(path)
    try:
        text = p.read_text()
    except (OSError, FileNotFoundError):
        return None
    try:
        data = json.loads(text)
    except (ValueError, TypeError):
        return None
    if not isinstance(data, dict):
        return None
    return data


def write_cursor(
    last_ts: str,
    last_count: int,
    last_comment_id,
    path=CURSOR_PATH,
) -> None:
    """Persist the high-water mark atomically. tmp -> rename, mkdir -p."""
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(
        json.dumps(
            {"last_ts": last_ts, "last_count": int(last_count), "last_comment_id": last_comment_id},
            separators=(",", ":"),
            sort_keys=True,
        )
        + "\n"
    )
    tmp.replace(p)


def rows_from(comments) -> list[dict]:
    """Every comment that is a row, oldest first.

    Accepts both the projected shape ({databaseId, body}) and the legacy shape
    ({body, ...}); both expose `body`. The two compiled regexes stay module-scope so a
    re-import is not a re-compile, and prose comments skip both `fromisoformat` and the
    sort by returning None from `parse_comment`.
    """
    rows = [r for r in (parse_comment(c.get("body", "")) for c in comments) if r]
    rows.sort(key=lambda r: datetime.fromisoformat(r["ts"].replace("Z", "+00:00")))
    return rows


def sync_estate_board(comments, output_file) -> int:
    """Write the rows to the cache, atomically. Returns how many rows landed.

    `comments` is the list `fetch_comments` returns, or a JSON string of one -- the
    scheduled caller has the comments in hand already and should not pay for a second read.

    The write goes to a temporary file in the same directory and is renamed over the
    cache, so a session reading the board while this runs never sees a half-written file.
    """
    if isinstance(comments, (str, bytes)):
        comments = json.loads(comments)
    rows = rows_from(comments)
    out = pathlib.Path(output_file)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(out.suffix + ".tmp")
    tmp.write_text("".join(json.dumps(r) + "\n" for r in rows))
    tmp.replace(out)
    return len(rows)


def main(argv: list[str]) -> int:
    """`estate-board-sync.py [cache-path]` -- reads the board, writes the cache.

    Warm path (the common case): if the cursor file exists, fetch only the newest
    comment's `ts` and compare. When it matches `cursor["last_ts"]`, return the
    persisted count without re-parsing, re-sorting, or touching the filesystem.

    Cold path: full projected, paginated fetch; lazy parse+sort; identity short-circuit
    before opening the tmp file; atomic write; cursor advance.
    """
    cache = pathlib.Path(argv[1]) if len(argv) > 1 else DEFAULT_CACHE
    cursor = read_cursor()

    if cursor is not None and cursor.get("last_ts"):
        try:
            remote_latest = latest_ts()
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError, ValueError) as exc:
            print(
                f"estate-board-sync: latest_ts failed, falling through to cold path "
                f"({type(exc).__name__}: {exc})",
                file=sys.stderr,
            )
            remote_latest = None
        if remote_latest and remote_latest == cursor["last_ts"]:
            try:
                with pathlib.Path(cache).open() as f:
                    n = sum(1 for ln in f if ln.strip())
            except (OSError, FileNotFoundError):
                n = int(cursor.get("last_count") or 0)
            print(
                f"estate-board-sync: warm path, board unchanged "
                f"({n} row(s) from {BOARD_REPO}#{BOARD_ISSUE} -> {cache})"
            )
            return 0

    try:
        comments = fetch_comments()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError, OSError) as exc:
        print(
            f"estate-board-sync: could not rebuild {cache}: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return 1

    rows = rows_from(comments)
    new_count = len(rows)
    new_max_ts = max((r["ts"] for r in rows), default="")
    newest_id = next((c.get("databaseId") for c in reversed(comments)), None)

    if (
        cursor is not None
        and new_count == int(cursor.get("last_count") or 0)
        and new_max_ts == cursor.get("last_ts")
    ):
        write_cursor(new_max_ts, new_count, newest_id)
        print(
            f"estate-board-sync: identity short-circuit, no rewrite "
            f"({new_count} row(s) from {BOARD_REPO}#{BOARD_ISSUE} -> {cache})"
        )
        return 0

    try:
        n = sync_estate_board(comments, cache)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError, OSError) as exc:
        print(
            f"estate-board-sync: could not rebuild {cache}: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return 1

    try:
        write_cursor(new_max_ts, n, newest_id)
    except OSError as exc:
        print(
            f"estate-board-sync: cache written but cursor could not be saved "
            f"({type(exc).__name__}: {exc}); next run will resync",
            file=sys.stderr,
        )

    print(f"estate-board-sync: {n} row(s) from {BOARD_REPO}#{BOARD_ISSUE} -> {cache}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))