"""The one place that talks to GitHub. Swap this file to leave GitHub."""

from __future__ import annotations

import json
import shutil
import subprocess

from .errors import CrewError

COMMENT_LIMIT = 60000  # GitHub's ceiling is 65536; leave room for the wrapper.


def _gh(args: list[str], stdin: str | None = None) -> str:
    if shutil.which("gh") is None:
        raise CrewError("the GitHub CLI `gh` is not on PATH")
    p = subprocess.run(["gh", *args], input=stdin, capture_output=True, text=True)
    if p.returncode != 0:
        raise CrewError(f"gh {' '.join(args)} failed:\n{(p.stderr or p.stdout).strip()}")
    return p.stdout


def issue_view(repo: str, number: int) -> dict:
    out = _gh([
        "issue", "view", str(number), "--repo", repo,
        "--json", "number,title,body,state,url,comments,assignees,labels",
    ])
    return json.loads(out)


def issue_create(repo: str, title: str, body: str, labels: list[str] | None = None) -> int:
    args = ["issue", "create", "--repo", repo, "--title", title, "--body-file", "-"]
    for label in labels or []:
        args += ["--label", label]
    url = _gh(args, stdin=body).strip().splitlines()[-1]
    try:
        return int(url.rstrip("/").rsplit("/", 1)[-1])
    except ValueError as e:
        raise CrewError(f"could not read an issue number out of: {url}") from e


def issue_set_body(repo: str, number: int, body: str) -> None:
    _gh(["issue", "edit", str(number), "--repo", repo, "--body-file", "-"], stdin=body)


def issue_comment(repo: str, number: int, body: str) -> None:
    if len(body) > COMMENT_LIMIT:
        body = body[:COMMENT_LIMIT] + "\n\n_(truncated by crew)_"
    _gh(["issue", "comment", str(number), "--repo", repo, "--body-file", "-"], stdin=body)


def issue_close(repo: str, number: int, comment: str | None = None) -> None:
    args = ["issue", "close", str(number), "--repo", repo]
    if comment:
        args += ["--comment", comment]
    _gh(args)


def ensure_label(repo: str, name: str, colour: str, description: str) -> None:
    p = subprocess.run(
        ["gh", "label", "create", name, "--repo", repo,
         "--color", colour, "--description", description, "--force"],
        capture_output=True, text=True,
    )
    if p.returncode != 0 and "already exists" not in (p.stderr + p.stdout):
        raise CrewError(f"could not create label {name}: {(p.stderr or p.stdout).strip()}")
