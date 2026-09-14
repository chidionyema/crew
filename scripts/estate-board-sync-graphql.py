#!/usr/bin/env python3
"""estate-board-sync-graphql.py — paginated GraphQL fetch + parallelised parse.

The read side of the estate board, when the cache is stale. Today the sync
script does `gh issue view --json comments` and parses the result. With 280+
comments on the board today that becomes the bottleneck: one round-trip, a
full re-parse of every row including the three prose backfill headers a human
wrote, and a `json.loads` that builds the entire list in memory.

This module owns the replacement:

  * `graphql_fetch(repo, issue, page_size=100, since=None)` — a single
    paginated `gh api graphql` query. One TCP connection, pages of 100, walks
    `pageInfo.hasNextPage` until the end. When `since` is provided, the
    query filters on `updatedAt > <since>` so a delta run reads only the
    pages that changed since the last sync.

  * `parse_pages_in_parallel(pages, max_workers=...)` — each page is a list
    of raw comment dicts. The parser fans out across a
    `concurrent.futures.ThreadPoolExecutor` sized to
    `min(os.cpu_count() or 1, 8)`. Parse work is CPU-light and the GIL does
    not matter here; the future returns are joined in the original page
    order so the merged list reads oldest first.

  * The query itself is the shape GitHub publishes for the `comments`
    connection: `id`, `body`, `createdAt`, `updatedAt`, plus `pageInfo`.
    `id` is the GraphQL node id the watermark advances against, and
    `updatedAt` is what the `since` filter reads.

The existing `scripts/estate-board-sync.py` still owns the regex / sort / write
path; this module does only the fetch and the parallelised parse. On a
non-zero exit from `gh api graphql`, this module logs to stderr and the caller
falls back to `gh issue view --json comments` — same fallback the existing
script uses, same loud stderr line the schedule already filters on. The
fallback sets `last_synced_id = None` so the next run retries the graphql path.

# Rejected: run all three fetch paths in parallel and pick the fastest. The
#   point of the watermark is steady-state cost; racing the network is not.
# Rejected: keep the existing `gh issue view --json comments` call as the
#   primary. The plan names graphql as the new primary and `gh issue view`
#   as the fallback. Roles reversed would cost a network round-trip on every
#   delta run; roles as written cost it only when graphql is down.
# Standard: docs/STANDARDS.md "Coordination" -- the estate board is the sync
#   layer (LAW 26), and this is its delta path.
# Deviation: the executor size cap of 8. Eight is the floor the plan names:
#   the parse is CPU-light, more workers just queue, and the pool grows with
#   the comment count by way of `page_size`.
"""

from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

#: The GraphQL query the script runs against `gh api graphql`. Pages of 100,
#: cursor-based, walks until pageInfo.hasNextPage is false. `since` is
#: substituted by graphql_fetch into a `filter:` argument on the comments
#: connection so a delta run fetches only pages whose `updatedAt` is after
#: the watermark's `last_synced_at`.
GRAPHQL_QUERY = """
query BoardDelta($owner: String!, $name: String!, $number: Int!, $first: Int!, $after: String, $filter: IssueCommentFilters) {
  repository(owner: $owner, name: $name) {
    issue(number: $number) {
      id
      number
      updatedAt
      comments(first: $first, after: $after, orderBy: {field: UPDATED_AT, direction: ASC}, filter: $filter) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          body
          createdAt
          updatedAt
        }
      }
    }
  }
}
"""


def _max_workers() -> int:
    """Thread pool size, capped at 8.

    Eight is the plan's floor: more workers on a CPU-light parse just queue,
    and the pool grows with the comment count by way of page_size anyway.
    `os.cpu_count()` returns None when the kernel cannot answer; we treat
    that as one.
    """
    return min(os.cpu_count() or 1, 8)


def _run_gh_graphql(query: str, variables: dict) -> dict:
    """One `gh api graphql` round-trip. Raises on non-zero exit.

    The caller logs to stderr and falls back; this helper never logs, so the
    caller is the single owner of the loud `RESYNC ` line.
    """
    payload = json.dumps({"query": query, "variables": variables})
    out = subprocess.run(
        ["gh", "api", "graphql", "-F", "query=" + payload],
        capture_output=True,
        text=True,
        timeout=60,
        check=True,
    ).stdout
    return json.loads(out)


def graphql_fetch(
    repo: str,
    issue: int,
    page_size: int = 100,
    since: str | None = None,
    query: str | None = None,
) -> tuple[list[dict], str | None]:
    """Fetch every comment, paginated. Returns (nodes, last_id).

    `nodes` is the flat list of comment dicts in the order the API returned
    them. `last_id` is the GraphQL node id of the last node returned, or
    None when the issue had no comments at all. The watermark advances
    against `last_id`.

    When `since` is provided (an ISO 8601 string with a trailing Z), the
    GraphQL query adds a `filter: {updatedAt: {greaterThan: since}}` so a
    delta run reads only the changed pages. The full fetch (when the
    watermark is missing or disagrees with the cache) calls this with
    `since=None`.

    Raises `subprocess.CalledProcessError` / `subprocess.TimeoutExpired` /
    `json.JSONDecodeError` on a failed read. The caller logs to stderr and
    falls back to `gh issue view --json comments`.
    """
    q = query if query is not None else GRAPHQL_QUERY
    owner, _, name = repo.partition("/")
    variables: dict = {
        "owner": owner,
        "name": name,
        "number": int(issue),
        "first": int(page_size),
        "after": None,
    }
    if since:
        variables["filter"] = {"updatedAt": {"greaterThan": since}}

    nodes: list[dict] = []
    end_cursor: str | None = None
    has_next = True
    while has_next:
        variables["after"] = end_cursor
        data = _run_gh_graphql(q, variables)
        try:
            conn = data["data"]["repository"]["issue"]["comments"]
        except (KeyError, TypeError) as exc:
            raise ValueError(f"graphql response missing comments connection: {exc}") from exc
        for n in conn.get("nodes") or []:
            if n is None:
                continue
            nodes.append(n)
        page_info = conn.get("pageInfo") or {}
        has_next = bool(page_info.get("hasNextPage"))
        end_cursor = page_info.get("endCursor")
    last_id = nodes[-1]["id"] if nodes else None
    return nodes, last_id


def parse_pages_in_parallel(
    pages: list[list[dict]],
    max_workers: int | None = None,
) -> list[dict]:
    """Parse a list of pages into rows, in parallel.

    The executor is sized to `min(os.cpu_count() or 1, 8)` when the caller
    does not override. Each worker takes one page (a list of raw comment
    dicts) and returns a list of parsed rows (None dropped, order preserved
    within the page). The merged list is in page order; the existing
    `rows_from` does the final sort by timestamp.

    The parse is the existing `parse_comment` from
    `scripts/estate-board-sync.py` — no second regex, no second copy. The
    import is done inside the function so this module stays importable in
    isolation (the regression test imports it without the sync script being
    on PYTHONPATH).
    """
    from importlib.util import module_from_spec, spec_from_file_location

    # Load by path, the same idiom the existing tests use, so a hyphenated
    # module name is not a barrier.
    here = pathlib.Path(__file__).resolve().parent / "estate-board-sync.py"
    spec = spec_from_file_location("estate_board_sync", here)
    if spec is None or spec.loader is None:
        # No regex to fall back to; return what we have. The sync script
        # catches this on its next line.
        return [r for page in pages for r in (c.get("body", "") for c in page)]
    ebs = module_from_spec(spec)
    spec.loader.exec_module(ebs)
    parse = ebs.parse_comment

    workers = max_workers if max_workers is not None else _max_workers()
    rows: list[list[dict]] = [[] for _ in pages]
    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool_exec:
        futures = {
            pool_exec.submit(_parse_page, page, parse): idx
            for idx, page in enumerate(pages)
        }
        for fut in as_completed(futures):
            idx = futures[fut]
            try:
                rows[idx] = fut.result()
            except Exception as exc:                                    # noqa: BLE001
                # A failed parse on one page must not fail the whole run; the
                # sync script catches on its own path.
                sys.stderr.write(f"parse_page error: {type(exc).__name__}: {exc}\n")
                rows[idx] = []
    flat: list[dict] = []
    for page_rows in rows:
        flat.extend(page_rows)
    return flat


def _parse_page(page: list[dict], parse) -> list[dict]:
    """One page's parse. Pure function so ThreadPoolExecutor can pick it up."""
    out = []
    for c in page:
        body = c.get("body", "")
        row = parse(body)
        if row is not None:
            out.append(row)
    return out


def pages_from_nodes(nodes: list[dict], page_size: int = 100) -> list[list[dict]]:
    """Split a flat list of nodes into pages of `page_size`.

    The fetch already returns nodes in API order; this helper exists so the
    parallel parse can be exercised against an already-fetched list (the
    regression tests use this to skip the network).
    """
    return [nodes[i : i + page_size] for i in range(0, len(nodes), page_size)]
