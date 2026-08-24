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

    run(["git", "add", *[str(dest / Path(l).name) for l in links]], cwd=root)
    # Nothing staged means an earlier run already committed these exact bytes and only
    # its push failed. That is the ordinary retry, not an error, and `git commit` with
    # an empty index exits 1 and would abort the retry before it reached the push.
    if run(["git", "diff", "--cached", "--name-only"], cwd=root).strip():
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
        return False, ("'Options considered' lists %d real option(s), needs 2. A bullet under %d "
                       "characters does not count as an option that was weighed"
                       % (len(bullets), OPTION_MIN_CHARS))
    if not OPTIONS_CHOSEN.search("\n".join(block)):
        return False, ("'Options considered' has no 'Chosen:' line. Two options and no verdict is "
                       "a list, not a decision")
    return True, "%d options weighed, with a stated choice" % len(bullets)


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
    what = ", ".join(sorted({"%s in %s" % (k, f) for k, f, _ in hits}))
    if not COUPLING_HEAD.search(body or ""):
        return False, ("adds provider coupling (%s) with no '## Provider coupling' section. "
                       "LAW 34: name what is coupled and add a 'Swap:' line saying what replaces "
                       "it and how long that takes" % what)
    block = []
    for line in body[COUPLING_HEAD.search(body).end():].splitlines():
        if line.strip().startswith("#"):
            break
        block.append(line)
    joined = "\n".join(block)
    if len(re.sub(r"[^A-Za-z0-9 ]", "", joined).strip()) < OPTION_MIN_CHARS:
        return False, ("'Provider coupling' is a heading with nothing under it. Say what is "
                       "coupled (%s) and what replaces it" % what)
    if not COUPLING_SWAP.search(joined):
        return False, ("'Provider coupling' has no 'Swap:' line. Naming a dependency without "
                       "naming its replacement is a description, not an exit")
    return True, "%d coupling(s) declared with a swap" % len(hits)


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
    """The infra files this diff touches, from the +++ headers — [] when it touches none."""
    return [line[6:].strip() for line in (diff or "").splitlines()
            if line.startswith("+++ b/") and INFRA_PATH.search(line[6:].strip())]


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
            return True, "%s line covers %d infra file(s)" % (m.group(1).capitalize(), len(touched))
    what = ", ".join(sorted(touched)[:5])
    return False, ("touches infra (%s) with no 'Standard:' or 'Deviation:' line. R7/LAW 44: add "
                   "'Standard: <the docs/STANDARDS.md row this uses>' or 'Deviation: <what and "
                   "why>' to the body. A deviation is allowed — stating it is the whole ask"
                   % what)


def check(pr: str, repo: str | None) -> tuple[bool, str]:
    info = pr_info(pr, repo)
    body = info.get("body") or ""
    if MARKER not in body:
        return False, (f"#{info['number']} has no verification evidence. "
                       f"LAW 7: attach a screenshot with `pr-evidence.py attach --pr {info['number']} …`")
    # Each image appears twice in a row, inline and as a link. Count the file,
    # not the mention, or the gate reports double what is there.
    imgs = set(re.findall(r"/docs/evidence/pr-\d+/[^)\s?]+", body))
    if not imgs:
        return False, f"#{info['number']} has an evidence section with no image in it"
    ok_opts, why_opts = options_considered(body)
    if not ok_opts:
        return False, "#%s %s" % (info["number"], why_opts)
    args = ["pr", "diff", pr] + (["--repo", repo] if repo else [])
    try:
        diff = gh(args)
    except Exception:
        # A diff we cannot fetch is not a pass. Say which check did not run, because a gate
        # that goes quiet on its own failure is the shape LAW 28 forbids.
        return False, "#%s: could not fetch the diff, so LAW 34 coupling was not checked" % info["number"]
    ok_cpl, why_cpl = provider_coupling(body, diff)
    if not ok_cpl:
        return False, "#%s %s" % (info["number"], why_cpl)
    # REPORT-ONLY while crew#135 measures the estate (LAW 45 step 4: report mode first, with
    # the would-fail count on the record). Flipping this to a refusal is its own reviewed PR.
    ok_std, why_std = standards_line(body, diff)
    std = why_std if ok_std else "WOULD FAIL once crew#135 blocks — " + why_std
    return True, "#%s carries %d evidence image(s), %s, %s; standards (report-only): %s" % (
        info["number"], len(imgs), why_opts, why_cpl, std)


def selftest_options() -> int:
    """The options gate, proved on literal bodies. Paired controls, as everywhere else here."""
    fails, ran = [], []

    def check_one(name, got, want):
        ran.append(name)
        if got == want:
            print("  ok   %s" % name)
        else:
            print("  FAIL %s: got %r, want %r" % (name, got, want))
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
        check_one("a %s Swap line is accepted" % label,
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
    print("selftest-options: %d/%d passed" % (len(ran) - len(fails), len(ran)))
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

    ns = ap.parse_args()
    if ns.cmd == "selftest-options":
        return selftest_options()
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
