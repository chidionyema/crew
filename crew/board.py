"""Board indexing: a flat row per issue, cached, merged across repos.

Source swap (issue #102): the index is now built from
``gh search issues --paginate`` per repo, in parallel, with a per-repo
``updatedAt`` watermark so steady-state re-runs do zero network work.
Public names and the ``format_index_row(row)`` contract are unchanged.
"""

from __future__ import annotations

import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable

from crew import config as crew_config
from crew.errors import CrewError
from crew.gh import gh_with_retry, run_gh

log = logging.getLogger(__name__)

_REQUIRED_KEYS = ("number", "title", "labels", "state", "updatedAt")


# ---------------------------------------------------------------------------
# Cache + watermark
# ---------------------------------------------------------------------------


def _load_cache(cache_path: str) -> dict[str, dict[str, Any]]:
    """Return ``{f"{repo}#{number}": row, ...}`` from disk, or empty.

    Rows are kept as-is so ``format_index_row`` keeps working without change.
    """
    if not cache_path or not os.path.exists(cache_path):
        return {}
    try:
        with open(cache_path, "r", encoding="utf-8") as fh:
            payload = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise CrewError(f"could not read index cache {cache_path!r}: {exc}") from exc
    if not isinstance(payload, dict):
        return {}
    return {k: v for k, v in payload.items() if isinstance(v, dict)}


def _watermark_path(cache_path: str) -> str:
    """Sidecar path for per-repo ``updatedAt`` watermarks."""
    if not cache_path:
        return ""
    base, _ = os.path.splitext(cache_path)
    return f"{base}.watermarks.json"


def _load_watermark(cache_path: str, repo: str) -> str | None:
    """Return the last seen ``max(updatedAt)`` for ``repo``, or ``None``."""
    path = _watermark_path(cache_path)
    if not path or not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as fh:
            payload = json.load(fh)
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict):
        return None
    value = payload.get(repo)
    return value if isinstance(value, str) else None


def _save_watermark(cache_path: str, repo: str, updated_at: str) -> None:
    """Persist ``repo -> updated_at`` in the watermark sidecar.

    Best-effort: never raises, because a watermark is a perf optimisation,
    not a correctness invariant.
    """
    path = _watermark_path(cache_path)
    if not path or not updated_at:
        return
    payload: dict[str, str] = {}
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                existing = json.load(fh)
            if isinstance(existing, dict):
                payload = {k: v for k, v in existing.items() if isinstance(v, str)}
        except (OSError, json.JSONDecodeError):
            payload = {}
    payload[repo] = updated_at
    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, sort_keys=True)
    except OSError as exc:  # pragma: no cover - disk failure is non-fatal
        log.debug("watermark write failed for %s: %s", repo, exc)


# ---------------------------------------------------------------------------
# Source: gh search issues --paginate
# ---------------------------------------------------------------------------


def _repo_scopes_from_config(config: Any) -> list[str]:
    """Return the list of repos the index should cover.

    Mirrors whatever ``crew.config`` already exposes — if the project
    keeps a ``repos`` attribute we use that; otherwise we fall back to a
    ``get("repos", [])`` shim so this stays a leaf module.
    """
    repos: list[str] = []
    getter: Callable[[], Any] | None = None
    if hasattr(config, "repos"):
        getter = lambda: getattr(config, "repos")
    elif hasattr(config, "get"):
        getter = lambda: config.get("repos", [])
    if getter is not None:
        try:
            value = getter() or []
        except Exception:  # pragma: no cover - defensive
            value = []
        if isinstance(value, (list, tuple)):
            repos = [str(r) for r in value if r]
    # Stable, de-duplicated order so the watermark sidecar is deterministic.
    seen: set[str] = set()
    unique: list[str] = []
    for r in repos:
        if r not in seen:
            seen.add(r)
            unique.append(r)
    return unique


def _search_repo_issues(repo: str, since: str | None = None) -> list[dict[str, Any]]:
    """Fetch every issue for ``repo`` via ``gh search issues --paginate``.

    ``since`` is an optional ``updatedAt`` watermark; when set, the call
    passes ``--search-updated >=...`` so unchanged repos cost zero pages.
    """
    args: list[str] = [
        "search",
        "issues",
        "--json",
        "number,title,labels,state,updatedAt",
        "--limit",
        "200",
        "--state",
        "all",
        "--sort",
        "updated",
        "--order",
        "desc",
        "--paginate",
        "--repo",
        repo,
    ]
    if since:
        args.extend(["--search-updated", f">={since}"])

    output = gh_with_retry(lambda: run_gh(*args))

    rows: list[dict[str, Any]] = []
    if not output:
        return rows
    # ``gh --paginate`` emits JSON when the consumer asks for ``--json``;
    # accept either a JSON array or newline-delimited JSON, just like
    # the previous ``gh issue list`` consumer did.
    text = output.strip()
    if not text:
        return rows
    if text.startswith("["):
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            parsed = []
        if isinstance(parsed, list):
            rows = [r for r in parsed if isinstance(r, dict)]
    else:
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                parsed = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                rows.append(parsed)
    return rows


def _index_one_repo(
    repo: str,
    cache_path: str,
    cache: dict[str, dict[str, Any]],
) -> tuple[str, list[dict[str, Any]], str | None]:
    """Pull one repo's delta, return ``(repo, rows, max_updated_at)``.

    Rows are stamped with their source repo so the merge step is keyed
    by ``f"{repo}#{number}"`` — the same shape the cache already uses.
    """
    since = _load_watermark(cache_path, repo)
    rows = _search_repo_issues(repo, since=since)

    max_updated: str | None = None
    for row in rows:
        row.setdefault("_repo", repo)
        updated = row.get("updatedAt")
        if isinstance(updated, str) and (max_updated is None or updated > max_updated):
            max_updated = updated
    if max_updated is None and since:
        # No new pages: keep the existing watermark.
        max_updated = since
    return repo, rows, max_updated


# ---------------------------------------------------------------------------
# Index entry point
# ---------------------------------------------------------------------------


def build_index(
    cache_path: str,
    *,
    config: Any | None = None,
    repos: list[str] | None = None,
) -> dict[str, dict[str, Any]]:
    """Rebuild (or incrementally refresh) the on-disk issue index.

    The output is the same ``{f"{repo}#{number}": row, ...}`` mapping
    the rest of the project already consumes. Empty scope short-circuits
    with no HTTP call.
    """
    if repos is None:
        repos = _repo_scopes_from_config(config if config is not None else crew_config)
    if not repos:
        # No scope, no work. The cache on disk is the truth until the
        # operator widens the config.
        return _load_cache(cache_path)

    cache = _load_cache(cache_path)
    fetched: dict[str, list[dict[str, Any]]] = {r: [] for r in repos}
    watermarks: dict[str, str | None] = {}

    workers = min(8, len(repos))
    if workers == 1:
        for repo in repos:
            _, rows, mark = _index_one_repo(repo, cache_path, cache)
            fetched[repo] = rows
            watermarks[repo] = mark
    else:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {
                pool.submit(_index_one_repo, repo, cache_path, cache): repo
                for repo in repos
            }
            for fut in futures:
                repo = futures[fut]
                _, rows, mark = fut.result()
                fetched[repo] = rows
                watermarks[repo] = mark

    # Merge: ``f"{repo}#{number}"`` is the canonical key.
    merged: dict[str, dict[str, Any]] = {}
    for repo, rows in fetched.items():
        for row in rows:
            number = row.get("number")
            if number is None:
                continue
            row["_repo"] = repo
            merged[f"{repo}#{number}"] = row
    # Carry over cached rows for repos we didn't touch this run.
    for key, row in cache.items():
        if key not in merged:
            merged[key] = row

    # Write the index exactly once.
    if cache_path:
        try:
            os.makedirs(os.path.dirname(cache_path) or ".", exist_ok=True)
            with open(cache_path, "w", encoding="utf-8") as fh:
                json.dump(merged, fh, sort_keys=True)
        except OSError as exc:
            raise CrewError(f"could not write index cache {cache_path!r}: {exc}") from exc

    # Persist watermarks after the index write so a half-failed run
    # still leaves the cache consistent with the sidecar.
    for repo, mark in watermarks.items():
        if mark:
            _save_watermark(cache_path, repo, mark)

    log.info("indexed %d", len(merged))
    return merged


# ---------------------------------------------------------------------------
# Row formatter (unchanged contract)
# ---------------------------------------------------------------------------


def format_index_row(row: dict[str, Any]) -> str:
    """Render one row of the issue index as a single line.

    Public contract: the row dict must expose ``number``, ``title``,
    ``labels``, ``state`` and ``updatedAt``. ``labels`` may be a list of
    dicts (real ``gh`` output) or a list of strings; both are accepted.
    """
    number = row.get("number")
    title = (row.get("title") or "").replace("\n", " ").strip()
    state = row.get("state") or ""
    updated_at = row.get("updatedAt") or ""
    labels_raw = row.get("labels") or []
    label_names: list[str] = []
    for lab in labels_raw:
        if isinstance(lab, dict):
            name = lab.get("name") or lab.get("title") or ""
        else:
            name = str(lab)
        if name:
            label_names.append(name)
    label_csv = ",".join(label_names)
    return f"#{number:<5} {state:<10} {updated_at}  {label_csv}  {title}"


__all__ = [
    "build_index",
    "format_index_row",
    "_load_cache",
    "_load_watermark",
    "_save_watermark",
    "_repo_scopes_from_config",
    "_search_repo_issues",
    "_index_one_repo",
]
