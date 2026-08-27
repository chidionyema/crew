#!/usr/bin/env python3
"""Scheduled outward research intake (crew#508 CP8).

Founder, 2026-08-27: "there is wealth of info and data out there and we need to be future
proof, we cant afford to rest on laurels and fall behind on research". Every tool named on a
docs/STANDARDS.md row is watched through science/research-sources.json. Once a day this
pulls the newest release of each repo from the GitHub Releases API (the mature source; a
tag list is the fallback for repos that publish no releases) and files every release the
estate has not seen as a *candidate* row on science/RESEARCH-INTAKE.jsonl. A candidate is
adopted or declined by hand, with a ticket; research_grade.py grades both the freshness of
the last pull and how many candidates sit unanswered.

    python3 science/research_intake.py pull      # pull every watched repo, file new candidates
    python3 science/research_intake.py --print   # the intake table, written nowhere
    python3 science/research_intake.py --check   # exit 1 when the last pull is >2 days old
                                                 # or a candidate is >7 days unanswered

Rejected (LAW 43): Renovate and Dependabot watch dependency manifests, not a standards page,
and produce pull requests, not a graded ledger; the GitHub Releases API is what both read.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import shutil
import subprocess
import sys
import urllib.request

SCIENCE = pathlib.Path(__file__).resolve().parent
SOURCES = SCIENCE / "research-sources.json"
INTAKE = SCIENCE / "RESEARCH-INTAKE.jsonl"
STATE = SCIENCE / "research-intake-state.json"
FRESH_DAYS = 2
ANSWER_DAYS = 7
STATUSES = ("baseline", "candidate", "adopted", "declined")


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.UTC).replace(microsecond=0)


def watched(path: pathlib.Path = SOURCES) -> list[dict]:
    return json.loads(path.read_text())["watch"]


def read_rows(path: pathlib.Path = INTAKE) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(ln) for ln in path.read_text().splitlines() if ln.strip()]


def _gh_json(endpoint: str) -> list | dict | None:
    """One GitHub REST call: `gh api` when installed (its auth and rate handling), else
    anonymous urllib. None on any failure, so one dead repo never stops the pull."""
    try:
        if shutil.which("gh"):
            out = subprocess.run(["gh", "api", endpoint], capture_output=True, text=True, timeout=60, check=False)
            return json.loads(out.stdout) if out.returncode == 0 and out.stdout.strip() else None
        with urllib.request.urlopen(f"https://api.github.com/{endpoint}", timeout=60) as r:
            return json.load(r)
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


def latest_release(repo: str, fetch=_gh_json) -> dict | None:
    """{'tag', 'published_at', 'url'} for the newest release, else newest tag, else None."""
    rel = fetch(f"repos/{repo}/releases/latest")
    if isinstance(rel, dict) and rel.get("tag_name"):
        return {"tag": rel["tag_name"], "published_at": rel.get("published_at"),
                "url": rel.get("html_url") or f"https://github.com/{repo}/releases/tag/{rel['tag_name']}"}
    tags = fetch(f"repos/{repo}/tags?per_page=1")
    if isinstance(tags, list) and tags and tags[0].get("name"):
        return {"tag": tags[0]["name"], "published_at": None,
                "url": f"https://github.com/{repo}/releases/tag/{tags[0]['name']}"}
    return None


def pull(sources: list[dict], rows: list[dict], now: dt.datetime, fetch=_gh_json) -> tuple[list[dict], dict]:
    """Return (new rows, state). A release is new when no row carries its repo+tag. The first
    release ever seen for a repo is the *baseline* (what the estate watched from), not a
    candidate: only releases that arrive after watching began are questions to answer."""
    seen = {(r["repo"], r["tag"]) for r in rows}
    known = {r["repo"] for r in rows}
    new, unreachable = [], []
    for src in sources:
        got = latest_release(src["repo"], fetch)
        if got is None:
            unreachable.append(src["repo"])
            continue
        if (src["repo"], got["tag"]) in seen:
            continue
        seen.add((src["repo"], got["tag"]))
        new.append({"seen": now.isoformat(timespec="seconds"), "row": src["row"], "repo": src["repo"],
                    "tag": got["tag"], "published_at": got["published_at"], "url": got["url"],
                    "status": "candidate" if src["repo"] in known else "baseline", "ticket": None})
        known.add(src["repo"])
    state = {"last_pull": now.isoformat(timespec="seconds"), "watched": len(sources),
             "unreachable": unreachable, "new": len(new)}
    return new, state


def _when(raw) -> dt.datetime | None:
    if not isinstance(raw, str) or not raw.strip():
        return None
    try:
        t = dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
    return t if t.tzinfo else t.replace(tzinfo=dt.UTC)


def grade(rows: list[dict], state: dict | None, sources: list[dict], now: dt.datetime) -> dict:
    """Counted, never estimated. `fresh` is False when there was never a pull."""
    last = _when((state or {}).get("last_pull"))
    age_days = None if last is None else (now - last).total_seconds() / 86400
    fresh = age_days is not None and age_days <= FRESH_DAYS
    candidates = [r for r in rows if r.get("status") == "candidate"]
    late = []
    for r in candidates:
        seen = _when(r.get("seen"))
        if seen is not None and (now - seen).days > ANSWER_DAYS:
            late.append({**r, "age_days": (now - seen).days})
    return {"watched": len(sources), "unreachable": list((state or {}).get("unreachable", [])),
            "last_pull": None if last is None else last.isoformat(timespec="seconds"),
            "age_days": None if age_days is None else round(age_days, 1), "fresh": fresh,
            "rows": len(rows), "candidates": len(candidates),
            "baseline": sum(r.get("status") == "baseline" for r in rows),
            "adopted": sum(r.get("status") == "adopted" for r in rows),
            "declined": sum(r.get("status") == "declined" for r in rows), "late": late}


def render(g: dict, rows: list[dict]) -> str:
    age = "" if g["age_days"] is None else f", {g['age_days']}d ago"
    out = ["## Outward intake — releases the world shipped, and what the estate did with them", "",
           "Source: `science/RESEARCH-INTAKE.jsonl`, watch list `science/research-sources.json`.", "",
           "| What | Value | How it is counted |", "|---|---|---|",
           f"| Last pull | {'never' if g['last_pull'] is None else g['last_pull']} "
           f"({'fresh' if g['fresh'] else 'RED'}{age}) "
           f"| `science/research-intake-state.json` `last_pull`, red past {FRESH_DAYS} days |",
           f"| Repos watched | {g['watched']} ({len(g['unreachable'])} unreachable on the last pull) | `research-sources.json` `watch` |",
           f"| Releases filed | {g['rows']} ({g['baseline']} baseline) | rows on the intake ledger; baseline = first release seen per repo |",
           f"| Candidates unanswered | {g['candidates']} ({len(g['late'])} RED, >{ANSWER_DAYS}d) | `status == candidate` |",
           f"| Adopted / declined | {g['adopted']} / {g['declined']} | `status` with a ticket |", ""]
    if g["late"]:
        out += ["| Age | Row | Release | Ticket |", "|---|---|---|---|"]
        out += [f"| RED {r['age_days']}d | {r['row']} | [{r['repo']} {r['tag']}]({r['url']}) | {r.get('ticket') or '-'} |"
                for r in g["late"]]
        out.append("")
    recent = sorted(rows, key=lambda r: r.get("seen") or "", reverse=True)[:10]
    if recent:
        out += ["| Seen | Row | Release | Status |", "|---|---|---|---|"]
        out += [f"| {r['seen'][:10]} | {r['row']} | [{r['repo']} {r['tag']}]({r['url']}) | {r['status']} |" for r in recent]
        out.append("")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("cmd", nargs="?", choices=["pull"])
    ap.add_argument("--print", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    now = dt.datetime.now(dt.UTC)
    sources, rows = watched(), read_rows()
    if a.cmd == "pull":
        new, state = pull(sources, rows, now)
        with INTAKE.open("a") as fh:
            fh.writelines(json.dumps(r) + "\n" for r in new)
        STATE.write_text(json.dumps(state, indent=2) + "\n")
        rows += new
        print(f"pulled {state['watched']} repos, {state['new']} new, "
              f"{len(state['unreachable'])} unreachable {state['unreachable'] or ''}".rstrip())
    state = json.loads(STATE.read_text()) if STATE.exists() else None
    g = grade(rows, state, sources, now)
    if a.print or a.cmd == "pull":
        print(render(g, rows))
    if a.check:
        bad = []
        if not g["fresh"]:
            bad.append(f"last pull {'never' if g['last_pull'] is None else g['last_pull']} is older than {FRESH_DAYS} days")
        if g["late"]:
            bad.append(f"{len(g['late'])} candidates unanswered past {ANSWER_DAYS} days")
        for b in bad:
            print(f"RED: {b}")
        return 1 if bad else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
