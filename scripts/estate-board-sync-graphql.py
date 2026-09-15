#!/usr/bin/env python3
"""estate-board-sync-graphql.py — paginated GraphQL fetch + parallelised parse (crew#102).

The read side of the estate board, when the cache is stale. The primary path
fetches comments via `gh api graphql` with cursor pagination; the parse work
fans out across a `concurrent.futures.ThreadPoolExecutor` only when the page
count justifies the thread spin-up.

The threshold is N > 32: below that the executor spin-up eats the win and the
planner picks serial. `os.cpu_count()` returns None when the kernel cannot
answer; we treat that as one. When parallel is selected, the worker cap is
`min(N, os.cpu_count())`.

The query itself is the shape GitHub publishes for the `comments` connection:
`id`, `body`, `createdAt`, `updatedAt`, plus `pageInfo`. `id` is the GraphQL
node id; `updatedAt` is what the sync script's pre-probe reads cheaply.

The existing `scripts/estate-board-sync.py` still owns the regex / sort / write
path; this module does only the fetch and the parallelised parse. On a non-zero
exit from `gh api graphql`, the caller falls back to `gh issue view --json
comments` — same fallback the existing script uses.

# Rejected: keep the executor at a fixed cap of 8. The plan names 32 as the
#   threshold; a fixed cap either spins up workers when N <= 32 (wastes the
#   win) or caps at 8 when N is in the hundreds (leaves cores idle).
# Rejected: always parallel. Same reason — the thread spin-up eats the win
#   below the threshold.
"""

from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

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

#: Plan threshold: serial below 32 (thread spin-up eats the win), parallel at or
#: above with worker count `min(N, os.cpu_count())`.
PARALLEL_THRESHOLD = 32


def _max_workers(n: int) -> int:
    """Worker count for a parse of N comments. 0 means serial.

    Threshold is 32: below that the executor spin-up eats the win. When
    parallel is selected, the cap is `min(N, os.cpu_count())` so a 4-core
    machine never spins up more than 4 workers even on a 200-comment board.
    """
    if n <= PARALLEL_THRESHOLD:
        return 0
    return min(n, os.cpu_count() or 1)


def _run_gh_graphql(query: str, variables: dict) -> dict:
    """One `gh api graphql` round-trip. Raises on non-zero exit."""
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
    None when the issue had no comments at all.

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
    """Parse a list of pages into rows, in parallel when N > 32.

    When `max_workers` is 0 (the serial case) the parse runs in the calling
    thread with no executor spin-up. Otherwise the parse fans out across a
    `ThreadPoolExecutor` sized to `min(N, os.cpu_count())`. The parse is
    CPU-light and the GIL does not matter here; the futures are joined in
    page order so the merged list reads in API order. The existing
    `rows_from` does the final sort by timestamp.

    The parse is the existing `parse_comment` from
    `scripts/estate-board-sync.py` — no second regex, no second copy.
    """
    from importlib.util import module_from_spec, spec_from_file_location

    here = pathlib.Path(__file__).resolve().parent / "estate-board-sync.py"
    spec = spec_from_file_location("estate_board_sync", here)
    if spec is None or spec.loader is None:
        return [r for page in pages for r in (c.get("body", "") for c in page)]
    ebs = module_from_spec(spec)
    spec.loader.exec_module(ebs)
    parse = ebs.parse_comment

    n = sum(len(page) for page in pages)
    workers = max_workers if max_workers is not None else _max_workers(n)

    if workers <= 0:
        # Serial path. No executor spin-up; the plan's threshold reason.
        flat: list[dict] = []
        for page in pages:
            for c in page:
                row = parse(c.get("body", ""))
                if row is not None:
                    flat.append(row)
        return flat

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
                sys.stderr.write(f"parse_page error: {type(exc).__name__}: {exc}\n")
                rows[idx] = []
    flat_outer: list[dict] = []
    for page_rows in rows:
        flat_outer.extend(page_rows)
    return flat_outer


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
