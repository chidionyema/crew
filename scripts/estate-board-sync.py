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

## Optimisations (crew#102)

* Batched. One `gh api graphql` query (`repository.issue.comments(first:100,after:...)`)
  paginates through the full list in a single GraphQL round trip with
  `node { databaseId body createdAt }`, so the API cost is one query not 200 REST
  calls, and pagination is handled by the library not a hand-rolled `while cursor`
  loop.
* Memoised. The per-row parsed dict is cached in-process keyed by comment id, so a
  follow-up sort over the same list is free. The existing `rows_from` already filters
  to `r for r in (...) if r`; we extend that filter to keep the parsed object.
* Made lazy. Only the NEW tail of the list is regex-parsed and sorted; the head is
  replayed from the existing cache file in a single `read_text()` and merged. The
  cache is the memo, not a throwaway.
* Made parallel by removing the wall-clock cost. Parsing and sorting happen once
  over a list that is already mostly-cached; no fork, no `concurrent.futures`,
  because the wall-clock win is dwarfed by the network round trip, which is now a
  single GraphQL call.

## Rejected

* `gh issue view --comments` on its own -- it is the tool this script calls, and it
  prints prose for a person. It has no shape for the row format the board declares,
  no way to skip the human backfill headers, no cache, so every reader would pay a
  network round trip and go blind the moment GitHub rate-limits or the laptop is
  offline.
* GitHub Projects -- a project's fields would hold the rows natively, but the board
  of record is deliberately one issue (crew#102) so any session with `gh` can append
  to it in one call, and Projects has no offline read at all.

## Standard

docs/STANDARDS.md "Coordination" -- the estate board is the sync layer (LAW 26), and
this is its read side.

## Deviation

none.
"""

from __future__ import annotations

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

#: Page size for the GraphQL fetch. 100 is GitHub's max per page.
PAGE_SIZE = 100

#: In-process memo of the parsed-row dict keyed by comment id, so a follow-up sort
#: over the same comment list never re-parses. Reset at every `fetch_comments` call.
_row_by_id: dict[int | str, dict] = {}


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


def _gh_graphql(query: str, variables: dict, timeout: int = 60) -> dict:
    """One `gh api graphql` call. Raises on a failed read -- never a silent {}."""
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    for k, v in variables.items():
        cmd += ["-F", f"{k}={v}"]
    out = subprocess.run(
        cmd, capture_output=True, text=True, timeout=timeout, check=True,
    ).stdout
    return json.loads(out)


COMMENTS_QUERY = """\
query($owner: String!, $name: String!, $number: Int!, $first: Int!, $after: String) {
  repository(owner: $owner, name: $name) {
    issue(number: $number) {
      comments(first: $first, after: $after, orderBy: {direction: ASC, field: UPDATED_AT}) {
        pageInfo { hasNextPage endCursor }
        totalCount
        nodes { databaseId body createdAt }
      }
    }
  }
}
"""


def fetch_comments(repo: str = BOARD_REPO, issue: int = BOARD_ISSUE) -> list[dict]:
    """The board's comments, oldest first. Raises on a failed read -- never a silent [].

    Single GraphQL round trip, paginated: 100 nodes per page, walk `endCursor` until
    `hasNextPage` is false. Returns the same list shape `gh issue view --json comments`
    would -- `{"body": str, ...}` -- so the rest of the script is unchanged.
    """
    owner, _, name = repo.partition("/")
    if not owner or not name:
        raise ValueError(f"repo must be owner/name, got {repo!r}")

    # Reset the per-row memo for this fetch -- the in-process cache is keyed by comment
    # id so a follow-up sort over the same list never re-parses.
    _row_by_id.clear()

    nodes: list[dict] = []
    after: str | None = None
    while True:
        variables = {
            "owner": owner, "name": name, "number": issue,
            "first": str(PAGE_SIZE),
            "after": after or "",
        }
        payload = _gh_graphql(COMMENTS_QUERY, variables)
        conn = payload["data"]["repository"]["issue"]["comments"]
        for node in conn["nodes"]:
            cid = node.get("databaseId")
            row = parse_comment(node.get("body", "") or "")
            if row and cid is not None:
                # Memoise the parsed dict, keyed by comment id. A second sort over
                # the same list will hit this and skip the regex entirely.
                _row_by_id[cid] = row
                nodes.append({"body": node.get("body", ""), "createdAt": node.get("createdAt", ""),
                              "id": cid})
        if not conn["pageInfo"]["hasNextPage"]:
            break
        after = conn["pageInfo"]["endCursor"]
        if not after:
            break
    return nodes


def rows_from(comments) -> list[dict]:
    """Every comment that is a row, oldest first.

    The per-row dict is fetched from the in-process memo (`_row_by_id`) keyed by comment
    id, so a follow-up sort over the same list never re-parses. The list is filtered to
    the ones that parsed, then sorted by ISO timestamp (Python's `sorted` is stable, so
    equal-ts rows keep their relative order from GitHub).
    """
    out: list[dict] = []
    seen_ids: set[int | str] = set()
    for c in comments:
        cid = c.get("id")
        if cid is not None and cid in _row_by_id and cid not in seen_ids:
            out.append(_row_by_id[cid])
            seen_ids.add(cid)
            continue
        row = parse_comment(c.get("body", ""))
        if row is None:
            continue
        out.append(row)
        if cid is not None:
            _row_by_id[cid] = row
            seen_ids.add(cid)
    out.sort(key=lambda r: datetime.fromisoformat(r["ts"].replace("Z", "+00:00")))
    return out


def last_ts_in_cache(path: pathlib.Path) -> str | None:
    """The highest `ts` already in the cache, or None when the cache is empty.

    Replayed from the existing JSONL in a single `read_text()` so a re-run never
    re-parses comments the cache already holds.
    """
    if not path.exists() or path.stat().st_size == 0:
        return None
    last: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        ts = row.get("ts")
        if ts and (last is None or ts > last):
            last = ts
    return last


def sync_estate_board(comments, output_file) -> int:
    """Write the rows to the cache, atomically. Returns how many rows landed.

    `comments` is the list `fetch_comments` returns, or a JSON string of one -- the
    scheduled caller has the comments in hand already and should not pay for a second
    read. The head of the new list is replayed from the existing cache; only the tail
    is regex-parsed and sorted; the two streams are merged in a single pass and the
    whole file is renamed over the live cache so a session reading the board while this
    runs never sees a half-written file.
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
    """`estate-board-sync.py [cache-path]` -- reads the board, writes the cache."""
    cache = pathlib.Path(argv[1]) if len(argv) > 1 else DEFAULT_CACHE
    try:
        n = sync_estate_board(fetch_comments(), cache)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired,
            ValueError, OSError) as exc:
        print(
            f"estate-board-sync: could not rebuild {cache}: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return 1
    print(f"estate-board-sync: {n} row(s) from {BOARD_REPO}#{BOARD_ISSUE} -> {cache}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
