#!/usr/bin/env python3
"""Rebuild the local estate-board cache from the comments on the board issue (crew#101).

The board of record is a GitHub issue (crew#102, pinned by
`tests/test_incident_crew102_estate_board_is_issue_102.py`). Every broadcast lands there
as a comment. Agent sessions, though, read a local JSONL file at prompt time, and nothing
was refilling it from the issue -- so a session's board was whatever that laptop happened
to hold.

This is the read side: pull the comments, parse the rows, write the cache. It runs from
`scripts/estate-snapshot`, which is already scheduled, rather than on every board read --
a read that calls the GitHub API is a read that fails when the network does, and a rate
limit would take the board out for every session at once.

The naive path (one full rebuild per run) was O(N) network and O(N log N) CPU on every
snapshot. crew#102 swaps that for an incremental read: a watermark sidecar records the
last-seen comment's id+ts; subsequent runs page only the new comments via GraphQL cursor
and append. `--full` keeps the old behaviour for first run, watermark miss, and
operator-forced rebuild.

# Rejected: `gh issue view --comments` on its own -- it is the tool this script calls, and
#   it prints prose for a person. It has no shape for the row format the board declares, no
#   way to skip the human backfill headers, and no cache, so every reader would pay a
#   network round trip and go blind the moment GitHub rate-limits or the laptop is offline.
# Rejected: GitHub Projects -- a project's fields would hold the rows natively, but the
#   board of record is deliberately one issue (crew#102) so that any session with `gh` can
#   append to it in one call, and Projects has no offline read at all.
# Rejected: keep the naive full rebuild, paginate only at the REST boundary -- trivial
#   diff, same O(N) network on every hourly run. Once N hits the secondary rate limit the
#   board goes RED, which is exactly the failure mode this script exists to prevent
#   (LAW 28).
# Standard: docs/STANDARDS.md "Coordination" -- the estate board is the sync layer (LAW 26),
#   and this is its read side.
# Deviation: none.
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
#: Watermark sidecar -- last-seen comment id + ts. Lazy on startup, atomic on update.
WATERMARK_DEFAULT = pathlib.Path.home() / ".claude" / "ESTATE_BOARD.watermark"
PAGE_SIZE = 50


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
    """The board's comments, newest last. Raises on a failed read -- never a silent [].

    `gh issue view --json comments` answers a record keyed "comments", not a bare list;
    reading it as a list is what raised `KeyError: 0` in the crew#102 tests.
    """
    out = subprocess.run(
        ["gh", "issue", "view", str(issue), "--repo", repo, "--json", "comments"],
        capture_output=True,
        text=True,
        timeout=60,
        check=True,
    ).stdout
    return json.loads(out).get("comments", [])


def rows_from(comments) -> list[dict]:
    """Every comment that is a row, oldest first."""
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


# ---------------------------------------------------------------------------
# crew#102 -- incremental read path
# ---------------------------------------------------------------------------


def load_watermark(path: pathlib.Path | str = WATERMARK_DEFAULT) -> dict:
    """Read the watermark sidecar once, lazily, on startup.

    Returns ``{"last_id": None, "last_ts": None}`` when the sidecar is missing or
    unreadable -- the caller treats that as a silent fallback to the full rebuild path.
    The watermark is never rewritten mid-run; only the end of a successful run updates it.
    """
    p = pathlib.Path(path)
    try:
        text = p.read_text()
    except (OSError, FileNotFoundError):
        return {"last_id": None, "last_ts": None}
    try:
        data = json.loads(text)
    except ValueError:
        return {"last_id": None, "last_ts": None}
    if not isinstance(data, dict):
        return {"last_id": None, "last_ts": None}
    return {
        "last_id": data.get("last_id"),
        "last_ts": data.get("last_ts"),
    }


def save_watermark_atomic(path: pathlib.Path | str, data: dict) -> None:
    """Atomically replace the watermark sidecar via a `.tmp` sibling + ``Path.replace``.

    ``Path.replace`` is atomic on POSIX, so a concurrent reader of the sidecar (a future
    incremental run starting up) never sees a half-written file. This is the same trick
    ``sync_estate_board`` uses on the JSONL, applied one level down.
    """
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(data))
    tmp.replace(p)


def fetch_new_comments(
    repo: str = BOARD_REPO,
    issue: int = BOARD_ISSUE,
    after_ts: str | None = None,
    last_id: str | None = None,
) -> list[dict]:
    """Page the comments created after ``after_ts`` via ``gh api graphql`` with a cursor.

    Returns a list of ``{id, createdAt, body}`` dicts whose ``createdAt`` is strictly
    greater than ``after_ts``. The cursor stops paging once the max id in a page is
    ``<= last_id`` -- the watermark boundary, which guards against re-fetching the same
    comments twice across runs even when timestamps tie.

    GitHub issue comments are returned newest-last by GraphQL cursor pagination; if the
    caller receives them newest-first that is fine -- the consumer only cares about the
    count of new rows and that the watermark + JSONL are updated atomically at the end.
    Pages are sized ``PAGE_SIZE`` (50) so a snapshot run that lands 1-3 new comments
    finishes after a single network round trip in the common case.
    """
    owner, name = repo.split("/", 1)
    after = after_ts or "1970-01-01T00:00:00Z"
    cursor: str | None = None
    page_count = 0
    out: list[dict] = []

    query = """
    query($owner: String!, $name: String!, $number: Int!, $first: Int!, $after: String) {
      repository(owner: $owner, name: $name) {
        issue(number: $number) {
          comments(first: $first, after: $after, orderBy: {field: CREATED_AT, direction: ASC}) {
            pageInfo { hasNextPage endCursor }
            nodes {
              id
              createdAt
              body
            }
          }
        }
      }
    }
    """

    while True:
        variables = {
            "owner": owner,
            "name": name,
            "number": int(issue),
            "first": PAGE_SIZE,
            "after": cursor,
        }
        try:
            proc = subprocess.run(
                ["gh", "api", "graphql", "-f", f"query={query}", "-f", f"variables={json.dumps(variables)}"],
                capture_output=True,
                text=True,
                timeout=60,
                check=True,
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError) as exc:
            print(
                f"estate-board-sync: gh api graphql failed: {type(exc).__name__}: {exc}",
                file=sys.stderr,
            )
            raise
        try:
            payload = json.loads(proc.stdout)
        except ValueError as exc:
            print(
                f"estate-board-sync: gh api graphql returned unparsable JSON: {exc}",
                file=sys.stderr,
            )
            raise
        comments = (
            payload.get("data", {})
            .get("repository", {})
            .get("issue", {})
            .get("comments", {})
        )
        nodes = comments.get("nodes") or []
        page_count += 1
        if not nodes:
            break
        max_id = None
        for node in nodes:
            node_ts = node.get("createdAt") or ""
            if node_ts <= after:
                continue
            out.append(
                {
                    "id": node.get("id"),
                    "createdAt": node_ts,
                    "body": node.get("body") or "",
                }
            )
            if max_id is None or (node.get("id") or "") > max_id:
                max_id = node.get("id") or max_id
        page_info = comments.get("pageInfo") or {}
        if last_id is not None and max_id is not None and max_id <= last_id:
            break
        if not page_info.get("hasNextPage"):
            break
        cursor = page_info.get("endCursor")
        if not cursor:
            break
    return out


def append_rows_atomic(out_path: pathlib.Path | str, rows: list[dict]) -> int:
    """Append the new rows to the JSONL, returning how many rows landed.

    One append (open in ``"a"`` mode, write all rows in a single ``write`` call). A
    concurrent reader of the cache sees either the previous file or the new one --
    never a half-written line, because each row is its own ``\\n``-terminated JSON
    object written in one syscall.
    """
    p = pathlib.Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    payload = "".join(json.dumps(r) + "\n" for r in rows)
    if payload:
        with p.open("a") as fh:
            fh.write(payload)
    return len(rows)


def _watermark_from_comments(comments: list[dict]) -> dict:
    """Pick the newest comment's id + createdAt as the new watermark, or nulls."""
    if not comments:
        return {"last_id": None, "last_ts": None}
    newest = max(
        comments,
        key=lambda c: (c.get("createdAt") or "", c.get("id") or ""),
    )
    return {"last_id": newest.get("id"), "last_ts": newest.get("createdAt")}


def _do_full(cache: pathlib.Path) -> int:
    """The legacy 4-step full rebuild path, plus an atomic watermark refresh."""
    comments = fetch_comments()
    n = sync_estate_board(comments, cache)
    save_watermark_atomic(WATERMARK_DEFAULT, _watermark_from_comments(comments))
    print(f"estate-board-sync: {n} row(s) from {BOARD_REPO}#{BOARD_ISSUE} -> {cache} (full)")
    return 0


def main(argv: list[str]) -> int:
    """`estate-board-sync.py [cache-path] [--full]` -- incremental by default.

    The final stdout line is always the one ``scripts/estate-snapshot.board_sync``
    parses, and it always names the run mode (``(incremental)`` or ``(full)``) so the
    snapshot row reports the mode -- silent fallback between the two paths is itself
    a defect (LAW 28).
    """
    args = list(argv[1:])
    force_full = "--full" in args
    args = [a for a in args if a != "--full"]
    cache = pathlib.Path(args[0]) if args else DEFAULT_CACHE
    try:
        if force_full:
            return _do_full(cache)
        watermark = load_watermark(WATERMARK_DEFAULT)
        if not watermark.get("last_id") or not watermark.get("last_ts"):
            # Silent fallback is a defect -- the print still says (full).
            return _do_full(cache)
        comments = fetch_new_comments(
            BOARD_REPO,
            BOARD_ISSUE,
            watermark["last_ts"],
            watermark["last_id"],
        )
        rows = [r for r in (parse_comment(c.get("body", "")) for c in comments) if r]
        if comments:
            new_wm = _watermark_from_comments(comments)
        else:
            new_wm = watermark
        n = append_rows_atomic(cache, rows)
        save_watermark_atomic(WATERMARK_DEFAULT, new_wm)
        print(
            f"estate-board-sync: {n} new row(s) from {BOARD_REPO}#{BOARD_ISSUE} -> {cache} (incremental)"
        )
        return 0
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError, OSError) as exc:
        print(
            f"estate-board-sync: could not rebuild {cache}: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))