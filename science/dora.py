#!/usr/bin/env python3
"""DORA four keys for the estate, measured from GitHub, never from memory (crew#495 CP9).

    python3 science/dora.py                 # idp and crew, last 7 days, one line per repo
    python3 science/dora.py --days 30 --repo chidionyema/idp --json

Deploy frequency = pull requests merged to main per day. Lead time = PR created -> merged,
median and p90 in hours. Change failure rate = issues labelled P1 opened in the window over
merges in the window. MTTR = P1 created -> closed, median hours over the P1s closed in the
window. The P1 label is the denominator (a title search misses them, comment
crew#495/5438270290). Pages are followed to the end, so a count is a count, not a page cap.
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
import subprocess
import re
import sys
from datetime import UTC, datetime, timedelta

DEFAULT_REPOS = os.environ.get("DORA_REPOS", "chidionyema/idp,chidionyema/crew").split(",")


def _ts(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def _p(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    v = sorted(values)
    return v[min(len(v) - 1, int(len(v) * q))]


_REVERT_RE = re.compile(r'^\s*revert\s*[:"“]?\s*"?(.*?)"?\s*$', re.IGNORECASE)


def reverted_title(title: str) -> str | None:
    """The title a revert PR names, or None. GitHub's revert button titles the PR
    `Revert "<original title>"`; a hand-written `revert: <title>` counts the same."""
    m = _REVERT_RE.match(title or "")
    return m.group(1).strip() if m and m.group(1).strip() else None


def four_keys(prs: list[dict], p1s: list[dict], since: datetime, days: int, now: datetime | None = None) -> dict:
    """The four numbers from GitHub rows. Pure, so the incident test runs it on fixtures.

    prs: {createdAt, mergedAt, baseRefName, title?}; p1s: {createdAt, closedAt}. Rows outside
    the window are dropped here, so a caller may hand over a whole listing.

    crew#368 act/task_outcome adds the denominator for quality: `reverts` is the merged PRs in
    the window whose title is a revert; `held_7d` is the merged PRs at least 7 days old (so
    a window under 8 days always reads 0) whose title no revert in the listing names.
    `now` defaults to since + days, which is what a caller with a real clock passes.
    """
    now = now or since + timedelta(days=days)
    merged = [p for p in prs if p.get("mergedAt") and p.get("baseRefName") == "main" and _ts(p["mergedAt"]) >= since]
    reverts = [p for p in merged if reverted_title(p.get("title", ""))]
    named = {reverted_title(p.get("title", "")) for p in reverts}
    held = [p for p in merged
            if _ts(p["mergedAt"]) <= now - timedelta(days=7)
            and not reverted_title(p.get("title", "")) and (p.get("title") or "") not in named]
    lead = [(_ts(p["mergedAt"]) - _ts(p["createdAt"])).total_seconds() / 3600 for p in merged]
    opened = [i for i in p1s if _ts(i["createdAt"]) >= since]
    closed = [i for i in p1s if i.get("closedAt") and _ts(i["closedAt"]) >= since]
    mttr = [(_ts(i["closedAt"]) - _ts(i["createdAt"])).total_seconds() / 3600 for i in closed]
    return {
        "deploys": len(merged),
        "deploys_per_day": round(len(merged) / days, 2),
        "lead_time_h_median": round(statistics.median(lead), 2) if lead else 0.0,
        "lead_time_h_p90": round(_p(lead, 0.9), 2),
        "p1_opened": len(opened),
        "change_failure_rate_pct": round(100 * len(opened) / len(merged), 1) if merged else None,
        "p1_closed": len(closed),
        "mttr_h_median": round(statistics.median(mttr), 2) if mttr else None,
        "reverts": len(reverts),
        "held_7d": len(held),
    }


def _gh(path: str, **params: str) -> list[dict]:
    q = "&".join(f"{k}={v}" for k, v in params.items())
    out = subprocess.run(["gh", "api", "--paginate", f"{path}?{q}"], capture_output=True, text=True, check=False)
    if out.returncode:
        sys.exit(f"gh api {path}: {out.stderr.strip()[:200]}")
    rows: list[dict] = []
    dec = json.JSONDecoder()
    s, i = out.stdout, 0
    while i < len(s):  # --paginate concatenates one JSON array per page
        while i < len(s) and s[i].isspace():
            i += 1
        if i >= len(s):
            break
        obj, i = dec.raw_decode(s, i)
        rows.extend(obj)
    return rows


def fetch(repo: str, since: datetime) -> tuple[list[dict], list[dict]]:
    prs = []
    for p in _gh(f"repos/{repo}/pulls", state="closed", base="main", sort="updated", direction="desc", per_page="100"):
        if _ts(p["updated_at"]) < since:
            break
        prs.append({"createdAt": p["created_at"], "mergedAt": p.get("merged_at"), "baseRefName": p["base"]["ref"],
                    "title": p.get("title") or ""})
    p1s = [{"createdAt": i["created_at"], "closedAt": i.get("closed_at")}
           for i in _gh(f"repos/{repo}/issues", state="all", labels="P1", since=since.strftime("%Y-%m-%dT%H:%M:%SZ"), per_page="100")
           if "pull_request" not in i]
    return prs, p1s


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="DORA four keys from the GitHub API")
    ap.add_argument("--repo", action="append", help="owner/name; repeatable (default: DORA_REPOS or idp,crew)")
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--jsonl", metavar="PATH",
                    help="append one row per repo {at, day, repo, days, <keys>} to PATH: the "
                         "`dora` source in science/sources.json (crew#368 act/task_outcome)")
    a = ap.parse_args(argv)
    now = datetime.now(UTC)
    since = now - timedelta(days=a.days)
    out = {}
    for repo in a.repo or DEFAULT_REPOS:
        prs, p1s = fetch(repo, since)
        out[repo] = four_keys(prs, p1s, since, a.days, now)
    if a.jsonl:
        at = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        with open(a.jsonl, "a") as fh:
            for repo, k in out.items():
                fh.write(json.dumps({"at": at, "day": at[:10], "repo": repo, "days": a.days, **k},
                                    separators=(",", ":")) + "\n")
        print(f"dora: {len(out)} row(s) appended to {a.jsonl}")
    if a.json:
        print(json.dumps({"measured_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "days": a.days, "repos": out}, indent=1))
        return 0
    print(f"DORA, last {a.days} days to {now:%Y-%m-%dT%H:%MZ}, from the GitHub API (merges to main; P1 by label)")
    for repo, k in out.items():
        cfr = "n/a" if k["change_failure_rate_pct"] is None else f"{k['change_failure_rate_pct']}%"
        mttr = "n/a" if k["mttr_h_median"] is None else f"{k['mttr_h_median']}h"
        print(f"{repo}: deploys={k['deploys']} ({k['deploys_per_day']}/day) | lead time median={k['lead_time_h_median']}h "
              f"p90={k['lead_time_h_p90']}h | change failure rate={cfr} (P1 opened={k['p1_opened']}) | MTTR median={mttr} (P1 closed={k['p1_closed']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
