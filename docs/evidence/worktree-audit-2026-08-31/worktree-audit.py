#!/usr/bin/env python3
"""Every git worktree of every repo under the code root, graded for work that never reached a
pull request: UNPUSHED (commits on no remote branch), DIRTY (uncommitted edits), OPEN (its PR is
open), MERGED (its PR merged), EMPTY (nothing beyond origin/main, clean), GONE (directory missing).
Reads git and one `gh pr list` per repo; never scans the disk."""

import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(os.environ.get("CODE_ROOT") or Path.home() / "dev" / "code")
REPOS = [
    r
    for r in os.environ.get("REPOS", "idp crew hermes-v2 prospector-main").split()
    if (ROOT / r / ".git").exists()
]


def git(cwd, *a):
    p = subprocess.run(["git", "-C", str(cwd), *a], capture_output=True, text=True, check=False)
    return p.returncode, p.stdout.strip()


rows = []
for repo in REPOS:
    main = ROOT / repo
    rc, out = git(main, "worktree", "list", "--porcelain")
    prs = {}
    p = subprocess.run(
        [
            "gh",
            "pr",
            "list",
            "-R",
            f"chidionyema/{repo}",
            "--state",
            "all",
            "--limit",
            "1000",
            "--json",
            "headRefName,number,state",
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=main,
    )
    if p.returncode == 0:
        for pr in json.loads(p.stdout):
            prs.setdefault(pr["headRefName"], pr)  # newest first
    blocks = [b for b in out.split("\n\n") if b.strip()]
    for b in blocks:
        f = dict(ln.split(" ", 1) if " " in ln else (ln, "") for ln in b.splitlines())
        path = Path(f["worktree"])
        branch = f.get("branch", "").replace("refs/heads/", "") or "(detached)"
        if path == main:
            continue
        row = {"repo": repo, "path": str(path).replace(str(ROOT) + "/", ""), "branch": branch}
        if not path.exists():
            row.update(verdict="GONE", dirty=0, unpushed=0, ahead=0, last="", pr="")
            rows.append(row)
            print(json.dumps(row), file=sys.stderr, flush=True)
            continue
        _, dirty = git(path, "status", "--porcelain", "--untracked-files=no")
        _, ahead = git(path, "rev-list", "--count", "origin/main..HEAD")
        _, contained = git(path, "branch", "-r", "--contains", "HEAD")
        _, unpushed = git(path, "rev-list", "--count", "HEAD", "--not", "--remotes")
        _, last = git(path, "log", "-1", "--format=%cs")
        pr = prs.get(branch)
        row.update(
            dirty=len(dirty.splitlines()),
            ahead=int(ahead or 0),
            unpushed=int(unpushed or 0),
            last=last,
            pr=f"#{pr['number']} {pr['state']}" if pr else "",
        )
        if row["dirty"]:
            v = "DIRTY"
        elif row["unpushed"]:
            v = "UNPUSHED"
        elif pr and pr["state"] == "OPEN":
            v = "OPEN"
        elif pr and pr["state"] == "MERGED":
            v = "MERGED"
        elif row["ahead"] == 0:
            v = "EMPTY"
        else:
            v = "PUSHED-NO-PR" if not pr else "CLOSED"
        row["verdict"] = v
        rows.append(row)
        print(json.dumps(row), file=sys.stderr, flush=True)

order = ["DIRTY", "UNPUSHED", "PUSHED-NO-PR", "CLOSED", "OPEN", "MERGED", "EMPTY", "GONE"]
rows.sort(key=lambda r: (order.index(r["verdict"]), r["repo"], r["path"]))
c = Counter(r["verdict"] for r in rows)
print(f"# Worktree audit, {len(rows)} worktrees across {', '.join(REPOS)}\n")
print("| verdict | count | meaning |\n|---|---|---|")
meaning = {
    "DIRTY": "uncommitted edits: missing work",
    "UNPUSHED": "commits on no remote branch: missing work",
    "PUSHED-NO-PR": "pushed, never opened as a PR",
    "CLOSED": "PR closed unmerged",
    "OPEN": "the PR is open: a live lane",
    "MERGED": "PR merged: delete",
    "EMPTY": "nothing beyond origin/main, clean: delete",
    "GONE": "directory missing: prune",
}
for v in order:
    if c[v]:
        print(f"| {v} | {c[v]} | {meaning[v]} |")
print(
    "\n| verdict | repo | worktree | branch | dirty | unpushed | ahead of main | last commit | PR |\n|---|---|---|---|---|---|---|---|---|"
)
for r in rows:
    print(
        f"| {r['verdict']} | {r['repo']} | `{r['path']}` | `{r['branch']}` | {r['dirty']} | {r['unpushed']} | {r['ahead']} | {r['last']} | {r['pr']} |"
    )
with open(os.environ.get("OUT_JSON", "/dev/null"), "w") as fh:
    json.dump(rows, fh, indent=1)
