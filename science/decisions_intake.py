#!/usr/bin/env python3
"""Decision intake from merged pull requests (crew#366, act/agent_decisions).

The registry row was NEVER_EMITTED: `~/.claude/scripts/decision-log.py --decide` exists and
13 rows were written by hand between 2026-08-21 and 2026-08-24, then nobody called it again.
Meanwhile every pull request already carries the decision, because pr-evidence.py refuses a
body without `## Options considered` (two roads named, one `Chosen:`). This pulls each newly
merged PR of the estate's repositories, reads that block, and appends one `kind: decision`
row to the same log decision-log.py writes, in its row shape, so `--check`, `--standing` and
the warehouse view `decisions_by_session` read hand-written and merged decisions alike.

Standard: Observability row, docs/STANDARDS.md (every data point in the registry has a
writer and a reader). Rejected: a GitHub Action per repository posting to the log -- three
copies of one poll, and the log lives on the estate host where its readers are; and asking
every session to call decision-log.py --decide -- that is the writer that died after 3 days.

    python3 science/decisions_intake.py pull      # file every merged PR not yet on the log
    python3 science/decisions_intake.py --print   # the table, written nowhere

Rejected (LAW 43): asking sessions to remember `--decide` (that is the 55-hour-dead writer
this replaces); a GitHub Action per repo (three copies of one poll, and the log lives on the
estate host where the other readers are). The block's grammar is pr-evidence.py's, imported
so the two never drift.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import subprocess
import sys

SCIENCE = pathlib.Path(__file__).resolve().parent
STATE = SCIENCE / "decisions-intake-state.json"
LOG = pathlib.Path(os.environ.get("DECISION_LOG") or (pathlib.Path.home() / ".claude" / "DECISIONS.jsonl"))
REPOS = ("chidionyema/idp", "chidionyema/crew", "chidionyema/claude-guards")
AUTHOR_RE = re.compile(r"^\s*Author-session:\s*([A-Za-z0-9_-]+)", re.I | re.M)


def _grammar():
    spec = importlib.util.spec_from_file_location("pr_evidence", SCIENCE.parent / "scripts" / "pr-evidence.py")
    if spec is None or spec.loader is None:
        raise SystemExit("decisions_intake: scripts/pr-evidence.py is not importable; the grammar lives there")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.OPTIONS_HEAD, mod.OPTIONS_CHOSEN


OPTIONS_HEAD, OPTIONS_CHOSEN = _grammar()


def parse_options(body: str) -> tuple[list[str], str | None]:
    """(rejected options, chosen line) from the `## Options considered` block; ([], None) when
    the body has no block or no Chosen line -- a PR that names no decision files no row."""
    m = OPTIONS_HEAD.search(body or "")
    if not m:
        return [], None
    rejected, chosen = [], None
    for line in body[m.end():].splitlines():
        s = line.strip()
        if s.startswith("#"):
            break
        if OPTIONS_CHOSEN.match(line):
            chosen = OPTIONS_CHOSEN.sub("", line).strip().strip("*_ ").strip()
        elif s.startswith(("-", "*", "+")):
            rejected.append(s.lstrip("-*+ ").strip())
    return (rejected, chosen) if chosen else ([], None)


def row_for(pr: dict, repo: str) -> dict | None:
    rejected, chosen = parse_options(pr.get("body") or "")
    if not chosen:
        return None
    url = pr.get("html_url") or f"https://github.com/{repo}/pull/{pr['number']}"
    sid = AUTHOR_RE.search(pr.get("body") or "")
    return {"id": "d" + hashlib.sha256(url.encode()).hexdigest()[:11], "kind": "decision",
            "ts": pr.get("merged_at"), "session": (sid.group(1) if sid else "unknown")[:8],
            "question": pr.get("title") or "", "options": rejected, "chosen": chosen,
            "why": f"merged as {url}", "rests_on": [], "reversible": True,
            "undo": f"git revert {pr.get('merge_commit_sha') or ''}".strip(), "revisit_when": "",
            "status": "standing", "superseded_by": None, "pr": url, "repo": repo}


def known_prs(log: pathlib.Path = LOG) -> set[str]:
    if not log.exists():
        return set()
    out = set()
    for ln in log.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            r = json.loads(ln)
        except json.JSONDecodeError:
            continue
        if r.get("kind") == "decision" and r.get("pr"):
            out.add(r["pr"])
    return out


def fetch(repo: str, since: str) -> list[dict]:
    out = subprocess.run(["gh", "api", "--paginate", f"repos/{repo}/pulls?state=closed&base=main&sort=updated&direction=desc&per_page=50"],
                         capture_output=True, text=True, check=False, timeout=120)
    if out.returncode:
        print(f"decisions_intake: gh api {repo}: {out.stderr.strip()[:200]}", file=sys.stderr)
        return []
    rows, dec, s, i = [], json.JSONDecoder(), out.stdout, 0
    while i < len(s):
        while i < len(s) and s[i].isspace():
            i += 1
        if i >= len(s):
            break
        obj, i = dec.raw_decode(s, i)
        rows.extend(obj)
    return [p for p in rows if p.get("merged_at") and p["merged_at"] >= since]


def pull(log: pathlib.Path = LOG, fetcher=fetch, state: pathlib.Path = STATE, now: dt.datetime | None = None) -> int:
    now = now or dt.datetime.now(dt.UTC).replace(microsecond=0)
    st = json.loads(state.read_text()) if state.exists() else {}
    since = st.get("since") or (now - dt.timedelta(days=14)).strftime("%Y-%m-%dT%H:%M:%SZ")
    seen, added = known_prs(log), 0
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8") as fh:
        for repo in REPOS:
            for pr in fetcher(repo, since):
                row = row_for(pr, repo)
                if row and row["pr"] not in seen:
                    fh.write(json.dumps(row, ensure_ascii=False) + "\n")
                    seen.add(row["pr"])
                    added += 1
    # the next pull starts a day back from now, so a PR merged during this run is not skipped
    state.write_text(json.dumps({"since": (now - dt.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                                 "last_pull": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "added": added}) + "\n")
    print(f"decisions_intake: {added} decision row(s) added from merged PRs since {since}")
    return 0


def table(log: pathlib.Path = LOG) -> str:
    per: dict[str, list[int]] = {}
    for ln in (log.read_text(encoding="utf-8", errors="replace").splitlines() if log.exists() else []):
        try:
            r = json.loads(ln)
        except json.JSONDecodeError:
            continue
        if r.get("kind") != "decision":
            continue
        c = per.setdefault(r.get("session") or "unknown", [0, 0, 0])
        c[0] += 1
        c[1] += len(r.get("options") or [])
        c[2] += 1 if r.get("status") == "superseded" else 0
    lines = ["session   decisions  options_rejected  reversals"]
    for s, (d, o, rv) in sorted(per.items(), key=lambda kv: -kv[1][0]):
        lines.append(f"{s:<9} {d:>9}  {o:>16}  {rv:>9}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    ap.add_argument("verb", nargs="?", choices=["pull"])
    ap.add_argument("--print", action="store_true")
    a = ap.parse_args(argv)
    if a.verb == "pull":
        return pull()
    print(table())
    return 0


if __name__ == "__main__":
    sys.exit(main())
