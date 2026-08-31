"""Second pass over worktrees.jsonl: which local commits never reached GitHub?

`rev-list HEAD --not --remotes` counts every commit on no remote ref, so a squash-merged branch
whose remote branch was deleted reads as unpushed although its PR merged. The precise and cheap
test: a commit that was the head of a merged PR (headRefOid) is merged, and so is everything
below it; only commits above the newest merged PR head are missing. Uncommitted edits are missing
by definition. One `gh pr list` per repo, then `rev-list` per worktree; no diff, no worktree walk.
"""

import json
import os
import subprocess
import sys

src, dst = sys.argv[1], sys.argv[2]


def sh(args, cwd=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False).stdout


heads = {}  # repo -> {sha: "#n STATE"}


def pr_heads(repo):
    if repo not in heads:
        rows = json.loads(
            sh(
                [
                    "gh",
                    "pr",
                    "list",
                    "-R",
                    f"chidionyema/{repo}",
                    "--state",
                    "all",
                    "--limit",
                    "3000",
                    "--json",
                    "headRefOid,number,state",
                ]
            )
        )
        heads[repo] = {p["headRefOid"]: f"#{p['number']} {p['state']}" for p in rows}
    return heads[repo]


out = open(dst, "w")  # noqa: SIM115
for line in open(src):  # noqa: SIM115
    if not line.strip():
        continue
    r = json.loads(line)
    r["missing_commits"] = 0
    r["merged_at_commit"] = ""
    if r["verdict"] not in ("EMPTY", "GONE") and os.path.isdir(r["path"]) and r["unpushed"]:
        shas = sh(["git", "rev-list", "HEAD", "--not", "--remotes"], r["path"]).split()
        known = pr_heads(r["repo"])
        above = 0
        for sha in shas:  # newest first
            if sha in known and known[sha].endswith("MERGED"):
                r["merged_at_commit"] = known[sha]
                break
            above += 1
        r["missing_commits"] = above if r["merged_at_commit"] else len(shas)
    r["missing"] = bool(r["dirty"]) or r["missing_commits"] > 0
    out.write(json.dumps(r) + "\n")
    out.flush()
    if r["missing"]:
        print(
            f"MISSING {r['repo']} {r['branch']} dirty={r['dirty']} commits={r['missing_commits']} pr={r['pr']} {r['merged_at_commit']} {r['path'].split('/')[-1]}",
            flush=True,
        )
print("refine finished", flush=True)
