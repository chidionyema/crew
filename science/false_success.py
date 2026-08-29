"""False-success rate: how often an agent's "resolved" claim on the board was rejected by the prover (crew#631 CP4).

Every claim is an agent labelling a ticket `RESOLVED_PENDING_VERIFICATION`; the verdict of the
moment is the prover App's next move on that ticket (`ticket-verify: X -> Y ...` comment by
`estate-agents[bot]`, from idp `ticket-verification.yml`). The number is REJECTED / (VERIFIED +
REJECTED) over the window; claims still pending are counted and shown, never folded in. Read
from GitHub every run, never from memory. Usage: python3 science/false_success.py [--days 30]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys

MOVE_RE = re.compile(r"^ticket-verify: (\w+) -> (\w+)\. (.*)$", re.M)
APP = "estate-agents"
CLAIM = "RESOLVED_PENDING_VERIFICATION"


def gh(args: list[str]) -> str:
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=True).stdout


def board(repo: str, since: dt.datetime) -> list[dict]:
    q = f"repos/{repo}/issues?state=all&labels=&since={since:%Y-%m-%dT%H:%M:%SZ}&per_page=100"
    out = []
    for label in (CLAIM, "VERIFIED", "REJECTED"):
        out += json.loads(gh(["api", q.replace("labels=", f"labels={label}"), "--paginate"]))
    seen = {}
    for i in out:
        seen[i["number"]] = i
    return list(seen.values())


def moves(repo: str, number: int) -> list[tuple[str, str, str, str]]:
    """[(when, from, to, why)] from the App's comments on the ticket."""
    cs = json.loads(
        gh(["api", f"repos/{repo}/issues/{number}/comments?per_page=100", "--paginate"])
    )
    rows = []
    for c in cs:
        if not c["user"]["login"].startswith(APP):
            continue
        for a, b, why in MOVE_RE.findall(c["body"]):
            rows.append((c["created_at"], a, b, why))
    return rows


def pair(issues: list[dict], moves_of) -> dict:
    """Each claim paired with the verdict of the moment: the App's first move after it."""
    claims, verified, rejected, pending = [], 0, 0, 0
    for i in issues:
        ms = moves_of(i["number"])
        labels = {label["name"] for label in i.get("labels", [])}
        outcome = "pending"
        for _, a, b, _ in ms:
            if a == CLAIM and b in ("VERIFIED", "REJECTED"):
                outcome = b
        if outcome == "pending" and not (labels & {CLAIM, "VERIFIED", "REJECTED"}):
            continue
        claims.append({"number": i["number"], "title": i["title"][:70], "verdict": outcome})
        verified += outcome == "VERIFIED"
        rejected += outcome == "REJECTED"
        pending += outcome == "pending"
    decided = verified + rejected
    return {
        "claims": claims,
        "verified": verified,
        "rejected": rejected,
        "pending": pending,
        "false_success_pct": round(100 * rejected / decided) if decided else None,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument(
        "--repo", default=None, help="OWNER/crew; default from gh's view of the checkout"
    )
    a = ap.parse_args(argv)
    repo = a.repo or gh(["repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"]).strip()
    since = dt.datetime.now(dt.UTC) - dt.timedelta(days=a.days)
    d = pair(board(repo, since), lambda n: moves(repo, n))
    for c in d["claims"]:
        print(f"{c['verdict']:9} #{c['number']} {c['title']}")
    rate = (
        f"{d['false_success_pct']}%"
        if d["false_success_pct"] is not None
        else "n/a (no decided claim)"
    )
    print(
        f"false-success {rate}: {d['rejected']} rejected of {d['verified'] + d['rejected']} decided claims, {d['pending']} pending, {a.days}d on {repo}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
