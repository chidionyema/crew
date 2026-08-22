#!/usr/bin/env python3
"""Screenshot evidence on a pull request. LAW 22.

Three commands, no dependencies outside the standard library and the tools that
are already on this machine.

    pr-evidence.py shot <url|screen> --out shot.png
    pr-evidence.py attach --pr 4 shot.png --caption "cp3 green, 5 of 5"
    pr-evidence.py check --pr 4

`attach` commits the image into the pull request's own branch under
docs/evidence/pr-<n>/ and links it from the body. That is deliberate. An image
uploaded to GitHub's attachment store lives in GitHub and leaves with GitHub,
which LAW 19 will not have. An image committed to the branch is in the git
bundle, so the evidence survives the exit drill along with the code.

`check` exits 1 when a pull request carries no evidence. It is what a gate calls.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MARKER = "<!-- pr-evidence -->"
END = "<!-- /pr-evidence -->"
SECTION = "## Verification evidence"


class Fail(Exception):
    pass


def run(args, timeout: int = 90, **kw):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=timeout, **kw)
    except subprocess.TimeoutExpired:
        raise Fail(f"{args[0]} did not finish inside {timeout}s")
    if p.returncode != 0:
        raise Fail(f"{args[0]} failed ({p.returncode}): {(p.stderr or p.stdout).strip()[:400]}")
    return p.stdout


def gh(args, stdin=None):
    return run(["gh", *args], input=stdin)


# ----------------------------------------------------------------- capture

def shot(target: str, out: Path, width: int, height: int, wait: float) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    # The capture below treats "the file is there" as "Chrome has finished".
    # When a previous run already left an image at this path that is true on
    # the first iteration, so Chrome was killed before writing and the OLD
    # image survived while the tool printed a success line. Re-rendering
    # evidence was a silent no-op, which is the exact failure LAW 22 exists to
    # prevent: a picture that looks like proof of the run you just did.
    # Measured 2026-08-22: two different inputs, same sha256 out.
    out.unlink(missing_ok=True)
    if target == "screen":
        if not shutil.which("screencapture"):
            raise Fail("screencapture is not on this machine")
        run(["screencapture", "-x", str(out)])
    else:
        if not Path(CHROME).exists():
            raise Fail(f"no Chrome at {CHROME}; pass a file:// URL to a rendered page instead")
        # Chrome refuses to start headless without a writable profile of its own,
        # and it will not share the one the founder has open.
        with tempfile.TemporaryDirectory(prefix="pr-evidence-") as profile:
            # Two things measured on this machine, 2026-08-22. `--headless=new`
            # writes nothing at all. Plain `--headless` writes the png and then
            # never exits, so waiting for the exit code waits forever. The file
            # appearing is the signal; the process is killed once it is there.
            cmd = [CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                   "--hide-scrollbars", "--force-color-profile=srgb",
                   f"--user-data-dir={profile}",
                   f"--screenshot={out}", f"--window-size={width},{height}", target]
            proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            deadline = time.time() + wait + 30
            try:
                while time.time() < deadline:
                    if out.exists() and out.stat().st_size > 0:
                        time.sleep(0.4)  # let the last bytes land
                        break
                    if proc.poll() is not None:
                        break
                    time.sleep(0.2)
            finally:
                proc.kill()
                proc.wait(timeout=10)
    if not out.exists() or out.stat().st_size == 0:
        raise Fail(f"no image came out at {out}")
    return out


def shot_text(text: str, out: Path, title: str, width: int, height: int) -> Path:
    """Command output is evidence too. Render it and photograph the render."""
    esc = (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    html = Path(str(out) + ".html")
    html.parent.mkdir(parents=True, exist_ok=True)
    html.write_text(
        "<style>body{background:#0d1117;color:#c9d1d9;font:13px/1.5 ui-monospace,Menlo,monospace;"
        "margin:0;padding:18px}h1{font-size:13px;color:#58a6ff;margin:0 0 12px}"
        "pre{white-space:pre-wrap;margin:0}</style>"
        f"<h1>{title}</h1><pre>{esc}</pre>")
    try:
        return shot(html.as_uri(), out, width, height, 1.0)
    finally:
        html.unlink(missing_ok=True)


# ------------------------------------------------------------------ github

def pr_info(pr: str, repo: str | None) -> dict:
    args = ["pr", "view", pr, "--json", "number,headRefName,body,url"]
    if repo:
        args += ["--repo", repo]
    return json.loads(gh(args))


def repo_root() -> Path:
    return Path(run(["git", "rev-parse", "--show-toplevel"]).strip())


def attach(pr: str, images: list[Path], caption: str, repo: str | None, push: bool) -> str:
    info = pr_info(pr, repo)
    n, branch = info["number"], info["headRefName"]
    root = repo_root()
    dest = root / "docs" / "evidence" / f"pr-{n}"
    dest.mkdir(parents=True, exist_ok=True)

    current = run(["git", "rev-parse", "--abbrev-ref", "HEAD"]).strip()
    if current != branch:
        raise Fail(f"you are on {current}; the pull request's branch is {branch}. "
                   f"Check it out first, so the evidence lands with the change it proves.")

    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    links = []
    for i, src in enumerate(images, 1):
        if not src.exists():
            raise Fail(f"no such image: {src}")
        name = f"{stamp}-{i}{src.suffix or '.png'}"
        shutil.copyfile(src, dest / name)
        links.append(f"docs/evidence/pr-{n}/{name}")

    run(["git", "add", *[str(dest / Path(l).name) for l in links]], cwd=root)
    run(["git", "commit", "-m", f"evidence: {caption}"], cwd=root)
    if push:
        run(["git", "push", "origin", branch], cwd=root)

    body = info.get("body") or ""
    # An absolute URL on the head branch, not a relative path. GitHub resolves a
    # relative link in a pull request body against the DEFAULT branch, so it 404s
    # until the branch merges — which is exactly when the reviewer needs to see it.
    slug = run(["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
               cwd=root).strip()
    def url_for(rel):
        return f"https://github.com/{slug}/blob/{branch}/{rel}?raw=1"
    # The image inlines on a public repo. On a private one GitHub cannot fetch it
    # without the viewer's token, so the link beside it is what actually works.
    rows = "\n".join(f"| {caption} | ![{Path(l).name}]({url_for(l)}) | [open]({url_for(l)}) |"
                     for l in links)
    block = (f"{MARKER}\n{SECTION}\n\n"
             f"| what it proves | image | link |\n|---|---|---|\n{rows}\n{END}\n")
    if MARKER in body:
        body = re.sub(rf"{re.escape(MARKER)}.*?(?:{re.escape(END)}|\Z)",
                      lambda _: block, body, flags=re.S)
    else:
        body = (body.rstrip() + "\n\n" + block).lstrip()

    args = ["pr", "edit", str(n), "--body-file", "-"]
    if repo:
        args += ["--repo", repo]
    gh(args, stdin=body)
    return f"{len(links)} image(s) on {info['url']} and committed to {branch}"


def check(pr: str, repo: str | None) -> tuple[bool, str]:
    info = pr_info(pr, repo)
    body = info.get("body") or ""
    if MARKER not in body:
        return False, (f"#{info['number']} has no verification evidence. "
                       f"LAW 22: attach a screenshot with `pr-evidence.py attach --pr {info['number']} …`")
    # Each image appears twice in a row, inline and as a link. Count the file,
    # not the mention, or the gate reports double what is there.
    imgs = set(re.findall(r"/docs/evidence/pr-\d+/[^)\s?]+", body))
    if not imgs:
        return False, f"#{info['number']} has an evidence section with no image in it"
    return True, f"#{info['number']} carries {len(imgs)} evidence image(s)"


# -------------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(prog="pr-evidence.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("shot", help="capture a page, the screen, or a command's output")
    s.add_argument("target", help="a URL, the word 'screen', or '-' to read text on stdin")
    # Resolved, because the text renderer turns this into a file:// URI and a
    # relative path cannot be one. `--out docs/evidence/pr-1/x.png` used to die
    # on ValueError from pathlib rather than saying which argument was wrong.
    s.add_argument("--out", required=True, type=lambda p: Path(p).resolve())
    s.add_argument("--title", default="command output")
    s.add_argument("--width", type=int, default=1280)
    s.add_argument("--height", type=int, default=900)
    s.add_argument("--wait", type=float, default=2.0)

    a = sub.add_parser("attach", help="commit images to the PR branch and link them in the body")
    a.add_argument("images", nargs="+", type=Path)
    a.add_argument("--pr", required=True)
    a.add_argument("--caption", required=True, help="what the image proves, in one line")
    a.add_argument("--repo")
    a.add_argument("--no-push", action="store_true")

    c = sub.add_parser("check", help="exit 1 if the PR carries no evidence")
    c.add_argument("--pr", required=True)
    c.add_argument("--repo")

    ns = ap.parse_args()
    try:
        if ns.cmd == "shot":
            if ns.target == "-":
                out = shot_text(sys.stdin.read(), ns.out, ns.title, ns.width, ns.height)
            else:
                out = shot(ns.target, ns.out, ns.width, ns.height, ns.wait)
            print(f"{out}  {out.stat().st_size} bytes")
            return 0
        if ns.cmd == "attach":
            print(attach(ns.pr, ns.images, ns.caption, ns.repo, not ns.no_push))
            return 0
        ok, msg = check(ns.pr, ns.repo)
        print(msg)
        return 0 if ok else 1
    except Fail as e:
        print(f"pr-evidence: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
