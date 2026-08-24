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
import hashlib
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
        p = subprocess.run(args, capture_output=True, text=True, timeout=timeout,
                           check=False, **kw)
    except subprocess.TimeoutExpired as e:
        raise Fail(f"{args[0]} did not finish inside {timeout}s") from e
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


def evidence_name(dest: Path, src: Path, stamp: str, i: int) -> tuple[str, bool]:
    """The filename this image gets in dest, and whether it still needs writing.

    An image whose bytes are ALREADY in dest keeps the name it already has, and is not
    written again. This is the whole of the duplicate fix.

    attach copies, commits, and only THEN pushes, so a refused push leaves the commit
    standing. Pushes are refused here as a matter of routine: the branch-freshness fence
    refuses a branch behind main, and the dead-branch guard refuses a branch whose pull
    request already merged. The retry used to mint a fresh timestamp, so the same bytes
    were committed a second time. Measured on prospector origin/main, 2026-08-23:
    docs/evidence/pr-669/ holds three byte-identical 106 KB copies, all sha256
    80291a6991ea..., and pr-674 collected two the same way. Retrying a failed push has
    to be free, or the repository grows a copy of the evidence per refusal.
    """
    digest = hashlib.sha256(src.read_bytes()).hexdigest()
    for existing in sorted(dest.iterdir()):
        if existing.is_file() and hashlib.sha256(existing.read_bytes()).hexdigest() == digest:
            return existing.name, False
    return f"{stamp}-{i}{src.suffix or '.png'}", True


def commit_evidence(root: Path, rels: list[str], caption: str) -> list[str]:
    """Commit exactly these paths, and return what actually went into the commit.

    This used to be `git add <images>` then a bare `git commit`, which commits the
    whole index. On 2026-08-24 that turned one screenshot into crew 097eccd: the
    commit also deleted two merged evidence images, reverted the --selftest alias
    below, and re-applied a stale copy of two verify.d gates, because the checkout
    it ran in had those changes sitting staged from earlier work.

    The class is not "that worktree was dirty". It is that a tool which is handed
    a list of files must commit that list and nothing else. A pathspec commit does
    exactly that: it takes the working-tree content of the named paths, ignores the
    rest of the index, and leaves other staged work staged for whoever staged it.

    An empty result is the ordinary retry, not an error: an earlier run already
    committed these exact bytes and only its push failed. `git commit` on an empty
    change exits 1, which would abort the retry before it reached the push.
    """
    abs_paths = [str(root / r) for r in rels]
    run(["git", "add", "--", *abs_paths], cwd=root)
    staged = [p for p in run(["git", "diff", "--cached", "--name-only", "--",
                              *abs_paths], cwd=root).split("\n") if p.strip()]
    if staged:
        run(["git", "commit", "-m", f"evidence: {caption}", "--", *abs_paths], cwd=root)
    return staged


def warn_if_behind_main(root: Path) -> bool:
    """Say so, loudly, when this branch is behind the default branch.

    The other half of 097eccd. This does not refuse: refusing to record evidence
    because a branch is stale would be LAW 38, a guard that blocks correct work,
    and the evidence is usually the last thing standing between a fix and a merge.
    It prints the count and the command, at the moment a session is about to push.
    """
    try:
        base = run(["git", "symbolic-ref", "--short", "refs/remotes/origin/HEAD"],
                   cwd=root).strip() or "origin/main"
    except Fail:
        base = "origin/main"
    try:
        behind = int(run(["git", "rev-list", "--count", f"HEAD..{base}"], cwd=root).strip())
    except (Fail, ValueError):
        return False        # no such ref here; nothing to compare against
    if behind:
        print(f"WARNING: this branch is {behind} commit(s) behind {base}. LAW 7: "
              f"refresh before review, `git merge {base}`. The evidence still attaches.")
    return bool(behind)


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
        name, write = evidence_name(dest, src, stamp, i)
        if write:
            shutil.copyfile(src, dest / name)
        links.append(f"docs/evidence/pr-{n}/{name}")

    warn_if_behind_main(root)
    commit_evidence(root, links, caption)
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
    rows = "\n".join(f"| {caption} | ![{Path(rel).name}]({url_for(rel)}) | [open]({url_for(rel)}) |"
                     for rel in links)
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


OPTIONS_HEAD = re.compile(r"^\s*#{1,4}\s*options considered\s*$", re.I | re.M)
#: The verdict line. A bullet marker is optional, and so is markdown emphasis around the word,
#: because "**Chosen:** the tick" is the way anybody writing a PR body actually types it. The
#: old pattern was ``[-*]?\s*chosen`` which ate the first asterisk of ``**`` and then failed on
#: the second, so a correct body was refused (measured on PR #77, 2026-08-24). LAW 38: a guard
#: that refuses correct work is an outage, not a rough edge.
OPTIONS_CHOSEN = re.compile(r"^\s*(?:[-*+]\s+)?(?:\*\*|__|\*|_)?\s*chosen\s*:", re.I | re.M)

#: A bullet has to say something. Measured on the LAW 32 gate, which had to add the same floor:
#: a heading with nothing under it satisfies a word search and satisfies nobody reading it.
OPTION_MIN_CHARS = 40

#: Every file in a diff opens with this header, and for a BINARY file it is the only place the
#: path appears in full. git prints no `---`/`+++` lines and no hunks for a binary; it prints
#: one line, `Binary files /dev/null and b/<path> differ`. Evidence is screenshots, so a pattern
#: written for text hunks matches nothing at all -- measured against #137's own diff on
#: 2026-08-24, where `+++ b/` found 0 paths while the image sat committed in the branch.
DIFF_SECTION = re.compile(r"^diff --git a/\S+ b/(\S+)$", re.M)
#: What a section says when it REMOVES the file instead of adding it. Any one of these and the
#: post-image is /dev/null whatever the header said. Without this a pull request could satisfy
#: the gate by deleting somebody else's screenshot.
DELETED_SECTION = re.compile(
    r"^(?:deleted file mode|\+\+\+ /dev/null|Binary files a/.* and /dev/null differ)", re.M)
def evidence_dir(number=None) -> str:
    """The directory fragment that counts as evidence, for one pull request or for any.

    `attach` always writes under the pull request's OWN number, so scoping to it is what
    the tool already produces. It also closes a hole: #137 restores two screenshots deleted
    from #120 and #128, and without the scope those restorations read as #137's own
    verification. A pull request could then pass the gate by restoring somebody else's
    evidence, which is the mirror of passing it by deleting somebody else's.

    Measured before narrowing it, 2026-08-24: of the 10 open pull requests, 6 have evidence
    in their diff and all 6 have it under their own number, so this refuses none of them
    (LAW 38).
    """
    n = re.escape(str(number)) if number is not None else r"\d+"
    return f"docs/evidence/pr-{n}/"


def added_evidence(diff: str, number=None) -> set:
    """Every evidence file a diff ADDS or MODIFIES, by path, ignoring the ones it deletes.

    Reads the diff a file at a time rather than pattern-matching the whole blob, because the
    only fact that decides an evidence path is whether ITS OWN section is a deletion. A regex
    over the whole text cannot tell which section a `deleted file mode` line belongs to.
    """
    diff = diff or ""
    wanted = re.compile("^" + evidence_dir(number) + ".")
    marks = list(DIFF_SECTION.finditer(diff))
    out = set()
    for i, m in enumerate(marks):
        path = m.group(1)
        if not wanted.match(path):
            continue
        end = marks[i + 1].start() if i + 1 < len(marks) else len(diff)
        if DELETED_SECTION.search(diff[m.end():end]):
            continue
        out.add(path)
    return out


EVIDENCE_SECTION = re.compile(r"^#{1,4}\s*verification evidence\s*$", re.I | re.M)
NEXT_HEADING = re.compile(r"^#{1,4}\s+\S", re.M)
FENCE = re.compile(r"```[^\n]*\n(.*?)```", re.S)
#: A fence has to contain something. Same floor, and the same reason, as OPTION_MIN_CHARS.
TRANSCRIPT_MIN_CHARS = 40


def transcript_evidence(body: str) -> int:
    """How many command transcripts the Verification evidence section actually contains.

    Not every pull request can produce a screenshot. #139 changes one markdown file and one
    ledger, and its evidence is pasted `git status` and secret-scan output -- which is the
    form this estate asks for everywhere else ("show the green run, do not describe it").
    Requiring an image would refuse correct work, and a guard that refuses correct work is
    an outage (LAW 38).

    This still is not grading a proxy. The proxy was the marker comment, which asserted that
    a section existed; an empty section satisfied it. What is counted here is the transcript
    itself, which is the evidence a text change can offer.
    """
    m = EVIDENCE_SECTION.search(body or "")
    if not m:
        return 0
    tail = body[m.end():]
    nxt = NEXT_HEADING.search(tail)
    section = tail[:nxt.start()] if nxt else tail
    return sum(1 for block in FENCE.findall(section)
               if len(block.strip()) >= TRANSCRIPT_MIN_CHARS)


def evidence_paths(body: str, diff: str, number=None) -> tuple:
    """(paths, where) for a pull request's evidence: ask the diff first, the body second.

    INCIDENT, 2026-08-24. `check` decided a pull request had no evidence by looking for one
    marker comment in the body. A body is prose. `gh pr edit --body-file` replaces it whole
    and takes the marker with it, which is the ordinary way a body gets rewritten, and the
    image it pointed at is untouched in the commit the whole time. It red-lit #156 and #159
    that day, and left #137 red while `docs/evidence/pr-137/20260824T080641Z-1.png` sat
    committed in #137's own diff.

    The class is grading a proxy. A marker in editable prose is a CLAIM that evidence exists;
    the file the diff adds IS the evidence, and no body edit can take it away. crew#161 is the
    same class seen from the other end -- an evidence link written as `blob/<branch>/...` dies
    when the branch is pruned -- and a SHA permalink does not fix it, because the grader would
    still be reading prose.

    The body stays as the fallback for the one case the diff is not available, so a pull
    request that links evidence it did not commit is still read the way it always was.
    """
    added = added_evidence(diff, number)
    if added:
        return added, "committed in the diff"
    #: The same files as the body links them, inline and as a link, hence the set.
    linked = re.compile("/" + evidence_dir(number) + r"[^)\s?]+")
    return set(linked.findall(body or "")), "linked from the body"


def options_considered(body: str) -> tuple:
    """(ok, message) for the requirement that a pull request shows the roads it did not take.

    Founder, 2026-08-23: "every pr nust prove they ehauseted all opttions".

    Two bullets and a chosen line is the bar, not a design document. The point is not the writing,
    it is that a cheaper option was named and rejected on the record rather than never looked for.
    LAW 23 already says take the smaller road when both arrive; this is the place that asks whether
    anybody checked there was one.
    """
    m = OPTIONS_HEAD.search(body or "")
    if not m:
        return False, ("no '## Options considered' section. Name at least two options, one line "
                       "each, and a 'Chosen:' line saying which won and why")
    block, bullets = [], []
    for line in body[m.end():].splitlines():
        if line.strip().startswith("#"):
            break
        block.append(line)
        s = line.strip()
        if s.startswith(("-", "*")) and not OPTIONS_CHOSEN.match(line):
            if len(re.sub(r"[^A-Za-z0-9 ]", "", s)) >= OPTION_MIN_CHARS:
                bullets.append(s)
    if len(bullets) < 2:
        return False, (f"'Options considered' lists {len(bullets)} real option(s), needs 2. "
                       f"A bullet under {OPTION_MIN_CHARS} characters does not count as an "
                       "option that was weighed")
    if not OPTIONS_CHOSEN.search("\n".join(block)):
        return False, ("'Options considered' has no 'Chosen:' line. Two options and no verdict is "
                       "a list, not a decision")
    return True, f"{len(bullets)} options weighed, with a stated choice"


#: What day-0 lock-in actually looks like in a diff. Each of these names one vendor and cannot be
#: satisfied by another, so a line that adds one has chosen a provider on behalf of the estate.
#: Deliberately narrow. A pattern that fires on innocent code trains agents to route around the
#: gate, and a gate agents route around is worse than no gate because it reads as coverage.
LOCKIN = [
    ("model id", re.compile(r"\b(claude-(?:opus|sonnet|haiku|fable|instant|\d)|gpt-[45]|o[13]-(?:mini|preview)"
                            r"|gemini-(?:\d|pro|flash)|grok-\d|llama-\d)", re.I)),
    ("api endpoint", re.compile(r"\b(api\.anthropic\.com|api\.openai\.com|api\.x\.ai"
                                r"|generativelanguage\.googleapis\.com)", re.I)),
    ("vendor sdk", re.compile(r"^\s*(?:from|import)\s+(anthropic|openai|google\.generativeai|cohere)\b", re.M)),
    ("transcript layout", re.compile(r"\.claude/projects|\.codex/sessions|\.gemini/tmp")),
]

COUPLING_HEAD = re.compile(r"^\s*#{1,4}\s*provider coupling\s*$", re.I | re.M)
#: Same shape as OPTIONS_CHOSEN above, and for the same reason. This pattern was left as
#: ``[-*]?\s*swap`` when the Chosen one was fixed, so it kept the bug: the ``[-*]?`` eats the
#: first asterisk of ``**Swap:**`` and then the pattern fails on the second, and a body that
#: declared its coupling correctly was refused (measured on PR #19, 2026-08-24). Fixing one
#: copy of a bug and leaving the other is how it comes back.
COUPLING_SWAP = re.compile(r"^\s*(?:[-*+]\s+)?(?:\*\*|__|\*|_)?\s*swap\s*:", re.I | re.M)

#: Prose and evidence are exempt. This law's own onboarding page names every vendor in the table
#: above, and a gate that refuses the document explaining it is a gate that gets deleted.
#:
#: This file exempts itself for the same reason, and it is not a loophole: the table above IS a
#: list of vendor names, so without the carve-out the first pull request refused by this gate is
#: the one that adds it. Measured, not predicted -- the gate flagged itself 6 times on its own
#: source before this line existed.
EXEMPT = re.compile(r"\.(md|txt|png|jpg|svg|lock)$|^docs/|/fixtures?/|^tests?/fixtures/"
                    r"|(^|/)pr-evidence\.py$")


def coupling_markers(diff: str) -> list:
    """Every vendor name this diff ADDS to code, as (kind, file, line) — [] when it adds none.

    Added lines only. A diff that deletes `import anthropic` is doing the opposite of taking a
    dependency, and counting it would make removing lock-in harder than adding it.
    """
    hits, path = [], ""
    for line in (diff or "").splitlines():
        if line.startswith("+++ b/"):
            path = line[6:].strip()
            continue
        if not line.startswith("+") or line.startswith("+++"):
            continue
        if not path or EXEMPT.search(path):
            continue
        text = line[1:]
        for kind, pat in LOCKIN:
            if pat.search(text):
                hits.append((kind, path, text.strip()[:80]))
                break
    return hits


def provider_coupling(body: str, diff: str) -> tuple:
    """(ok, message) for LAW 34. A pull request that adds a vendor name says how it is swapped.

    Founder, 2026-08-23: "we need to be provider agnostic from day 0", "every agent session and
    pr needs to reinforce", "and you need to include claude".

    This does not refuse the coupling. Taking a dependency is often right and LAW 19 already
    covers living with one. It refuses the SILENT coupling: a vendor written into a code path
    where nobody wrote down what replaces it. The answer may be one line, and one line is the
    whole ask, because the cost of an exit is set on the day the dependency goes in and never
    gets cheaper afterwards.

    A diff that adds no vendor name passes without the author writing anything.
    """
    hits = coupling_markers(diff)
    if not hits:
        return True, "adds no new provider coupling"
    what = ", ".join(sorted({f"{k} in {f}" for k, f, _ in hits}))
    head = COUPLING_HEAD.search(body or "")
    if not head:
        return False, (f"adds provider coupling ({what}) with no '## Provider coupling' section. "
                       "LAW 34: name what is coupled and add a 'Swap:' line saying what replaces "
                       "it and how long that takes")
    block = []
    for line in body[head.end():].splitlines():
        if line.strip().startswith("#"):
            break
        block.append(line)
    joined = "\n".join(block)
    if len(re.sub(r"[^A-Za-z0-9 ]", "", joined).strip()) < OPTION_MIN_CHARS:
        return False, ("'Provider coupling' is a heading with nothing under it. Say what is "
                       f"coupled ({what}) and what replaces it")
    if not COUPLING_SWAP.search(joined):
        return False, ("'Provider coupling' has no 'Swap:' line. Naming a dependency without "
                       "naming its replacement is a description, not an exit")
    return True, f"{len(hits)} coupling(s) declared with a swap"


#: Where a change is infra work and must name its standard. Exactly the paths crew#135 names,
#: no wider: scripts/, workflows, launchd plists, and docs/STANDARDS.md itself — editing the
#: standard IS infra work. Other docs prose stays exempt for the same reason EXEMPT exists
#: above: a gate that refuses the page explaining it is a gate that gets deleted.
INFRA_PATH = re.compile(r"^(scripts/|\.github/)|\.plist$|^docs/STANDARDS\.md$")

#: Same emphasis-tolerant shape as OPTIONS_CHOSEN and COUPLING_SWAP, for the same measured
#: reason (PR #19): people write `**Standard:**` and a pattern that only accepts the bare form
#: refuses correct work, which LAW 38 calls an outage.
STANDARDS_MARK = re.compile(r"^\s*(?:[-*+]\s+)?(?:\*\*|__|\*|_)?\s*(standard|deviation)\s*:"
                            r"(?:\*\*|__|\*|_)?\s*(.*)$", re.I | re.M)


def infra_paths(diff: str) -> list:
    """The infra files this diff touches — [] when it touches none.

    All four header shapes, not just `+++ b/`: the first version read added files only, so a
    PR DELETING `scripts/backup.py` because restic replaced it — exactly the change R7 wants a
    line on — passed with nothing written, and a 100% rename emits no +++/--- lines at all,
    only `rename from/to`. Demonstrated by code-3a on the #138 review; the goal-guard names
    this exact class: an allow-list with a silent miss case. /dev/null never matches a prefix
    below, so deletions surface through their `--- a/` side.
    """
    paths = set()
    for line in (diff or "").splitlines():
        if line.startswith(("+++ b/", "--- a/")):
            p = line[6:].strip()
        elif line.startswith(("rename from ", "rename to ")):
            p = line.split(" ", 2)[2].strip()
        else:
            continue
        if INFRA_PATH.search(p):
            paths.add(p)
    return sorted(paths)


def standards_line(body: str, diff: str) -> tuple:
    """(ok, message) for R7 / LAW 44. A pull request that touches infra names its standard.

    docs/STANDARDS.md says a component not on the page needs a stated, reviewed deviation, and
    until crew#135 nothing enforced that — a law without a protocol is a wish (LAW 44). The ask
    is one line in the body: `Standard: <the STANDARDS.md row this uses>` or `Deviation: <what
    and why>`. A deviation is never refused here — stating it is the whole requirement; the
    review grades it (LAW 38: the escape hatch is writing the line, not routing around the gate).

    A diff that touches no infra path passes without the author writing anything.
    """
    touched = infra_paths(diff)
    if not touched:
        return True, "touches no infra path"
    for m in STANDARDS_MARK.finditer(body or ""):
        if len(re.sub(r"[^A-Za-z0-9 ]", "", m.group(2)).strip()) >= 3:
            return True, f"{m.group(1).capitalize()} line covers {len(touched)} infra file(s)"
    what = ", ".join(sorted(touched)[:5])
    return False, (f"touches infra ({what}) with no 'Standard:' or 'Deviation:' line. R7/LAW 44: add "
                   "'Standard: <the docs/STANDARDS.md row this uses>' or 'Deviation: <what and "
                   "why>' to the body. A deviation is allowed — stating it is the whole ask")


def check(pr: str, repo: str | None) -> tuple[bool, str]:
    info = pr_info(pr, repo)
    body = info.get("body") or ""
    # The diff is fetched before anything is graded, because the evidence lives in it. See
    # evidence_paths: reading the body's marker first is what made a body edit look like
    # missing evidence.
    args = ["pr", "diff", pr] + (["--repo", repo] if repo else [])
    try:
        diff = gh(args)
    except Exception:  # noqa: BLE001
        # Blind on purpose, fail-closed: ANY fetch error must become a FAIL verdict, not a
        # crash. A diff we cannot fetch is not a pass. Say which check did not run, because
        # a gate that goes quiet on its own failure is the shape LAW 28 forbids.
        return False, ("#{}: could not fetch the diff, so neither the evidence nor LAW 34 "
                       "coupling was checked".format(info["number"]))
    imgs, where = evidence_paths(body, diff, info["number"])
    transcripts = transcript_evidence(body)
    if not imgs and not transcripts:
        return False, (f"#{info['number']} has no verification evidence. "
                       f"LAW 7: attach a screenshot with `pr-evidence.py attach --pr {info['number']} …`, "
                       f"or paste the command output under `## Verification evidence`")
    if not imgs:
        where = f"{transcripts} command transcript(s) in the body"
    ok_opts, why_opts = options_considered(body)
    if not ok_opts:
        return False, "#{} {}".format(info["number"], why_opts)
    ok_cpl, why_cpl = provider_coupling(body, diff)
    if not ok_cpl:
        return False, "#{} {}".format(info["number"], why_cpl)
    # REPORT-ONLY while crew#135 measures the estate (LAW 45 step 4: report mode first, with
    # the would-fail count on the record). Flipping this to a refusal is its own reviewed PR.
    ok_std, why_std = standards_line(body, diff)
    std = why_std if ok_std else "WOULD FAIL once crew#135 blocks — " + why_std
    carries = f"{len(imgs)} evidence image(s) {where}" if imgs else where
    return True, (f"#{info['number']} carries {carries}, {why_opts}, "
                  f"{why_cpl}; standards (report-only): {std}")


def selftest_commit_scope() -> int:
    """commit_evidence commits what it was handed, in a throwaway repository.

    Four controls, and two of them are the tool saying yes. The incident (crew
    097eccd) is control B: unrelated work was staged, and the evidence commit
    swallowed it. Control A is the paired half, because a guard only ever seen
    refusing has never been shown to permit.
    """
    fails, ran = [], []

    def check_one(name, got, want):
        ran.append(name)
        if got == want:
            print(f"  ok   {name}")
        else:
            print(f"  FAIL {name}: got {got!r}, want {want!r}")
            fails.append(name)

    work = Path(tempfile.mkdtemp(prefix="pr-evidence-scope-"))
    try:
        # os.environ goes FIRST so these four win. The other order let an ambient
        # GIT_AUTHOR_NAME silently replace the selftest's identity.
        env = {**os.environ,
               "GIT_AUTHOR_NAME": "selftest", "GIT_AUTHOR_EMAIL": "selftest@localhost",
               "GIT_COMMITTER_NAME": "selftest", "GIT_COMMITTER_EMAIL": "selftest@localhost"}
        run(["git", "init", "-q", "-b", "main", str(work)], env=env)
        # The identity has to live in the repository, not just in this env dict, because
        # the subject of the test -- commit_evidence -- runs git without it. On any
        # machine with a global user.name that difference is invisible. A CI runner has
        # none, so the selftest died with `fatal: empty ident name` on ubuntu-latest
        # while passing here. Reproduce that locally with GIT_CONFIG_GLOBAL=/dev/null.
        run(["git", "config", "user.email", "selftest@localhost"], cwd=work, env=env)
        run(["git", "config", "user.name", "selftest"], cwd=work, env=env)
        (work / "keep.txt").write_text("as merged\n")
        run(["git", "add", "keep.txt"], cwd=work, env=env)
        run(["git", "commit", "-q", "-m", "base"], cwd=work, env=env)

        # The dirty index that caused the incident: an unrelated file rewritten and
        # staged, exactly as a stale checkout leaves it.
        (work / "keep.txt").write_text("a rider from another branch\n")
        run(["git", "add", "keep.txt"], cwd=work, env=env)

        ev = work / "docs" / "evidence" / "pr-1"
        ev.mkdir(parents=True)
        (ev / "shot.png").write_bytes(b"\x89PNG evidence")
        rel = "docs/evidence/pr-1/shot.png"

        staged = commit_evidence(work, [rel], "a screenshot")
        in_commit = sorted(p for p in run(["git", "show", "--pretty=", "--name-only", "HEAD"],
                                          cwd=work, env=env).split("\n") if p.strip())

        check_one("A the evidence image is in the commit", in_commit, [rel])
        check_one("B the unrelated staged file is NOT in the commit",
                  "keep.txt" in in_commit, False)
        check_one("C the unrelated change is still staged, for whoever staged it",
                  run(["git", "diff", "--cached", "--name-only"], cwd=work,
                      env=env).strip(), "keep.txt")
        # The retry path: same bytes, nothing to commit, and no exception. This is
        # what a refused push leaves behind, and it has to stay free.
        check_one("D re-attaching the same bytes commits nothing and does not raise",
                  commit_evidence(work, [rel], "a screenshot"), [])
        check_one("E the first call did report what it committed", staged, [rel])
    finally:
        shutil.rmtree(work, ignore_errors=True)

    print(f"selftest-commit-scope: {len(ran) - len(fails)}/{len(ran)} passed")
    return 1 if fails else 0


def selftest_options() -> int:
    """The options gate, proved on literal bodies. Paired controls, as everywhere else here."""
    fails, ran = [], []

    def check_one(name, got, want):
        ran.append(name)
        if got == want:
            print(f"  ok   {name}")
        else:
            print(f"  FAIL {name}: got {got!r}, want {want!r}")
            fails.append(name)

    good = ("## Options considered\n"
            "- Rewrite the sweep as a separate scheduled job of its own\n"
            "- Fold the sweep into the tick that already runs every five minutes\n"
            "- Chosen: the tick, because a second scheduler is a second thing to go quiet\n")
    check_one("two options and a choice pass", options_considered(good)[0], True)
    check_one("no section fails", options_considered("Some prose.")[0], False)
    check_one("one option is not exhausting the options",
              options_considered("## Options considered\n- Fold it into the existing five minute "
                                 "tick\n- Chosen: that one\n")[0], False)
    check_one("two options and no verdict fails",
              options_considered("## Options considered\n"
                                 "- Rewrite the sweep as a separate scheduled job of its own\n"
                                 "- Fold the sweep into the tick that already runs every "
                                 "five minutes\n")[0], False)
    check_one("stub bullets do not count as options",
              options_considered("## Options considered\n- a\n- b\n- Chosen: a\n")[0], False)
    check_one("the section ends at the next heading",
              options_considered(good.replace("- Chosen:", "## Notes\n- Chosen:"))[0], False)
    # A body written by a person uses markdown emphasis. Each of these is a correct decision and
    # the gate must let it through; the refusal above proves it still says no to a missing verdict.
    check_one("bold chosen line passes",
              options_considered(good.replace("- Chosen:", "**Chosen:**"))[0], True)
    check_one("bulleted bold chosen line passes",
              options_considered(good.replace("- Chosen:", "- **Chosen:**"))[0], True)
    check_one("underscore emphasis passes",
              options_considered(good.replace("- Chosen:", "__Chosen:__"))[0], True)
    check_one("bare chosen line passes",
              options_considered(good.replace("- Chosen:", "Chosen:"))[0], True)
    # ---- LAW 34, on literal diffs. Paired controls: every refusal has a pass beside it.
    d_clean = "+++ b/scripts/tick.py\n+    total = count_rows(db)\n"
    d_model = "+++ b/scripts/tick.py\n+    MODEL = \"claude-opus-5\"\n"
    d_sdk = "+++ b/scripts/tick.py\n+import anthropic\n"
    d_docs = "+++ b/docs/onboarding/law-34.md\n+We currently call claude-opus-5 and api.openai.com.\n"
    d_del = "+++ b/scripts/tick.py\n-import anthropic\n+from providers import chat\n"
    declared = ("## Provider coupling\n"
                "The tick names claude-opus-5 directly when it summarises the day.\n"
                "- Swap: any chat model behind providers.chat, about an hour to move\n")

    check_one("a diff with no vendor name passes with nothing written",
              provider_coupling("no section at all", d_clean)[0], True)
    check_one("a model id with no section fails",
              provider_coupling("no section at all", d_model)[0], False)
    check_one("a vendor sdk import with no section fails",
              provider_coupling("no section at all", d_sdk)[0], False)
    check_one("a model id with a declared swap passes",
              provider_coupling(declared, d_model)[0], True)
    check_one("prose and docs are exempt",
              provider_coupling("no section at all", d_docs)[0], True)
    check_one("removing a vendor import is not adding coupling",
              provider_coupling("no section at all", d_del)[0], True)
    check_one("an empty heading does not count",
              provider_coupling("## Provider coupling\n\n## Next", d_model)[0], False)
    check_one("a coupling named with no Swap line fails",
              provider_coupling("## Provider coupling\nWe call claude-opus-5 in the daily "
                                "summary path and it works well.\n", d_model)[0], False)
    # The paired half: the gate has to say yes to a body that is correct. Every one of these
    # is how somebody actually types the line, and the old pattern refused the first three.
    for label, line in (("bold", "**Swap:** any chat model behind providers.chat, an hour"),
                        ("bold bullet", "- **Swap:** any chat model behind providers.chat, an hour"),
                        ("underscore bold", "__Swap:__ any chat model behind providers.chat, an hour"),
                        ("bare", "Swap: any chat model behind providers.chat, an hour"),
                        ("plain bullet", "- Swap: any chat model behind providers.chat, an hour")):
        check_one(f"a {label} Swap line is accepted",
                  provider_coupling("## Provider coupling\nThe tick names claude-opus-5 "
                                    "directly when it summarises the day.\n" + line + "\n",
                                    d_model)[0], True)
    check_one("claude gets no exemption from the law it is named in",
              provider_coupling("no section at all",
                                "+++ b/scripts/t.py\n+p = HOME / \".claude/projects\"\n")[0], False)
    # ---- R7 / LAW 44 standards line, on literal diffs. Paired controls again: every refusal
    # has the pass that shows the gate still says yes to correct work (LAW 38).
    d_scripts = "+++ b/scripts/tick.py\n+    total = count_rows(db)\n"
    d_wf = "+++ b/.github/workflows/crew-qa.yml\n+      - name: step\n"
    d_plist = "+++ b/ops/com.founder.board.plist\n+<key>Label</key>\n"
    d_page = "+++ b/docs/STANDARDS.md\n+| a row |\n"
    d_prose = "+++ b/docs/onboarding/law-44.md\n+Some words about the gate.\n"
    named = "Standard: launchd, per the substrate row\n"

    check_one("a non-infra diff passes with nothing written",
              standards_line("no line at all", d_prose)[0], True)
    check_one("a scripts/ diff with no line fails",
              standards_line("no line at all", d_scripts)[0], False)
    check_one("a workflow diff with no line fails",
              standards_line("no line at all", d_wf)[0], False)
    check_one("a plist diff with no line fails",
              standards_line("no line at all", d_plist)[0], False)
    check_one("editing STANDARDS.md itself is infra work",
              standards_line("no line at all", d_page)[0], False)
    check_one("a Standard line passes", standards_line(named, d_scripts)[0], True)
    check_one("a Deviation line passes",
              standards_line("Deviation: cron here because launchd lacks a calendar for it\n",
                             d_scripts)[0], True)
    check_one("a bold Standard line passes",
              standards_line("**Standard:** launchd, per the substrate row\n", d_scripts)[0], True)
    check_one("a bulleted bold Deviation line passes",
              standards_line("- **Deviation:** cron here, launchd lacks the trigger\n",
                             d_scripts)[0], True)
    check_one("a Standard line with nothing after the colon fails",
              standards_line("Standard:\n", d_scripts)[0], False)
    # The miss case code-3a demonstrated on the #138 review: deletions carry only a `--- a/`
    # header and pure renames carry only `rename from/to` lines. Paired both ways again.
    d_del = "--- a/scripts/backup.py\n+++ /dev/null\n"
    d_ren = ("diff --git a/scripts/old-name.sh b/scripts/new-name.sh\n"
             "rename from scripts/old-name.sh\nrename to scripts/new-name.sh\n")
    check_one("deleting an infra file with no line fails",
              standards_line("no line at all", d_del)[0], False)
    check_one("deleting an infra file with a Deviation line passes",
              standards_line("Deviation: backup.py deleted, restic owns backups now\n",
                             d_del)[0], True)
    check_one("a pure rename of an infra file with no line fails",
              standards_line("no line at all", d_ren)[0], False)
    check_one("deleting a docs prose file passes with nothing written",
              standards_line("no line at all", "--- a/docs/onboarding/old.md\n+++ /dev/null\n")[0],
              True)
    print(f"selftest-options: {len(ran) - len(fails)}/{len(ran)} passed")
    return 1 if fails else 0


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

    sub.add_parser("selftest-options",
                   help="prove the options gate on literal bodies, no network")
    sub.add_parser("selftest-commit-scope",
                   help="prove the evidence commit takes only its own files, in a temp repo")

    # estate-selftest.py runs every script under ~/.claude/scripts that accepts
    # `--selftest`, once an hour, and this file is symlinked in there. It was
    # reported as NO SELFTEST because the cases live behind a subcommand with a
    # different name, so 24 paired-control cases sat on disk and nothing ran them.
    # A control nobody runs is not a control, so the estate's spelling is accepted
    # as an alias for the subcommand rather than the cases being moved.
    if "--selftest" in sys.argv[1:]:
        # Every suite in this file, not the first one that was written. A second
        # suite added beside a hardcoded call is a suite the hourly run never sees.
        return max(selftest_options(), selftest_commit_scope())

    ns = ap.parse_args()
    if ns.cmd == "selftest-options":
        return selftest_options()
    if ns.cmd == "selftest-commit-scope":
        return selftest_commit_scope()
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
