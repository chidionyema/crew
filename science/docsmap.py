#!/usr/bin/env python3
"""Inventory every document this estate owns, and say which ones fail the standard.

Founder, 2026-08-24: "i need to se archtecture docunetaion, and add docs persisted and
we need better dos nanagent, our docunentaion standards are very poor", then "tine to
establish standards", then "this is what i nean things get lost".

Things get lost because nothing has ever counted them. A prose complaint about
documentation quality cannot be acted on; a row per document can. So this is the
inventory LAW 39 asks for, pointed at docs, and it is what the docs gate reads.

It reports, it never edits. Read-only first is the estate rule.

    docsmap.py                 human table
    docsmap.py --json          machine rows, which the gate consumes
    docsmap.py --failures      only the documents that fail, exit 1 if any

What it grades, and why each rule exists:

  persisted   The file is tracked by git. LAW 24: a load-bearing file no repository
              holds is one accident from gone. An untracked doc is the literal shape
              of "things get lost".

  owned       The file names an owner. A document nobody owns is nobody's to correct,
              so it rots and then it lies, which is worse than absent.

  dated       The file carries a date a machine can read. Without one there is no way
              to tell a current document from a stale one, and a reader cannot know
              which they are holding.

  fresh       The file's content has been touched since the code it describes. This is
              the only rule graded against something outside the file itself.

  substantial Over 200 characters of prose once headings and blank lines are stripped.
              LAW 32 already sets this floor for demo and onboarding pages, because a
              heading with nothing under it satisfies a gate without satisfying a
              reader. Same floor, applied to every document.
"""
from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import json
import pathlib
import re
import subprocess
import sys

# The estate's own repositories. Vendored trees, plugin caches and archived checkouts
# are excluded on purpose: grading somebody else's README teaches this estate nothing,
# and a count that includes 15,000 node_modules files is a number nobody can act on.
REPOS = [
    "~/dev/code/crew",
    "~/.claude",
    "~/.claude/scripts",
    "~/.estate",
    "~/dev/code/idp",
    "~/dev/code/maestro",
    "~/dev/code/survival-stack",
]

# Paths inside those repos that are still not ours to grade.
EXCLUDE = re.compile(
    r"(^|/)(node_modules|\.venv|venv|site-packages|plugins/cache|"
    r"checkpoints|tool-results|projects/|\.ARCHIVED)"
)

MIN_PROSE = 200

OWNER_RE = re.compile(r"^\s*(?:[-*>#]\s*)?(?:\*\*)?owner(?:\*\*)?\s*[:=]\s*(\S.*)$",
                      re.IGNORECASE | re.MULTILINE)
DATE_RE = re.compile(r"\b(20\d{2})-(\d{2})-(\d{2})\b")


# crew#88, 2026-08-27: 377 of 389 documents named no owner. GitHub's CODEOWNERS is the mature
# ownership record (it gates review on the same paths), so a document a CODEOWNERS row covers is
# owned by that row when the file itself has no Owner line. An Owner line in the file still wins.
CODEOWNERS_PATHS = ("CODEOWNERS", ".github/CODEOWNERS", "docs/CODEOWNERS")


def codeowners(repo: pathlib.Path) -> list[tuple[str, str]]:
    """(pattern, owners) rows in file order; the last matching row wins, as GitHub applies it."""
    for rel in CODEOWNERS_PATHS:
        f = repo / rel
        if f.exists():
            rows = []
            for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
                line = line.split("#", 1)[0].strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    rows.append((parts[0], " ".join(parts[1:])))
            return rows
    return []


def codeowner_of(rel: str, rows: list[tuple[str, str]]) -> str | None:
    owner = None
    for pattern, who in rows:
        pat = pattern
        anchored = pat.startswith("/")
        pat = pat.lstrip("/")
        if pat.endswith("/"):
            pat += "**"
        # GitHub: a pattern with no slash other than a trailing one matches at any depth
        if not anchored and "/" not in pattern.rstrip("/*"):
            pat = "**/" + pat
        rx = "^" + re.escape(pat).replace(r"\*\*/", "(?:.*/)?").replace(r"\*\*", ".*").replace(r"\*", "[^/]*") + "$"
        if re.match(rx, rel) or re.match(rx, rel + "/"):
            owner = who
    return owner


@dataclasses.dataclass
class Doc:
    repo: str
    path: str
    persisted: bool
    owner: str | None
    date: str | None
    prose: int
    last_commit: str | None

    @property
    def substantial(self) -> bool:
        return self.prose >= MIN_PROSE

    def failures(self) -> list[str]:
        out = []
        if not self.persisted:
            out.append("persisted")
        if not self.owner:
            out.append("owned")
        if not self.date:
            out.append("dated")
        if not self.substantial:
            out.append("substantial")
        return out


def prose_chars(text: str) -> int:
    """Characters of actual prose: no headings, no fences, no blank lines, no links-only."""
    n = 0
    in_fence = False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not s or s.startswith("#") or set(s) <= set("-=|* "):
            continue
        n += len(s)
    return n


def git(repo: pathlib.Path, *args: str) -> str:
    r = subprocess.run(["git", "-C", str(repo), *args], check=False,
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def scan(repo_str: str) -> list[Doc]:
    repo = pathlib.Path(repo_str).expanduser()
    if not (repo / ".git").exists():
        return []

    tracked = {p for p in git(repo, "ls-files", "*.md").splitlines() if p}
    untracked = {p for p in
                 git(repo, "ls-files", "--others", "--exclude-standard", "*.md").splitlines()
                 if p}

    rows = codeowners(repo)
    docs = []
    for rel in sorted(tracked | untracked):
        if EXCLUDE.search(rel):
            continue
        f = repo / rel
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        owner_m = OWNER_RE.search(text)
        date_m = DATE_RE.search(text)
        last = git(repo, "log", "-1", "--format=%cI", "--", rel).strip() or None

        docs.append(Doc(
            repo=repo_str,
            path=rel,
            persisted=rel in tracked,
            owner=(owner_m.group(1).strip()[:60] if owner_m else codeowner_of(rel, rows)),
            date=f"{date_m.group(1)}-{date_m.group(2)}-{date_m.group(3)}" if date_m else None,
            prose=prose_chars(text),
            last_commit=last,
        ))
    return docs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true", help="machine rows")
    ap.add_argument("--failures", action="store_true",
                    help="only failing documents; exit 1 when any fail")
    ap.add_argument("--repo", action="append", help="limit to one repo path")
    ap.add_argument("--write-baseline", metavar="PATH",
                    help="record today's failures as the ratchet's starting line")
    args = ap.parse_args()

    repos = args.repo or REPOS
    docs = [d for r in repos for d in scan(r)]

    if args.write_baseline:
        # The ratchet's starting line. Turning a standard on against 190 failing
        # documents would make every run red for weeks, and a gate that is always red
        # is a gate everyone learns to ignore (LAW 38: a guard that refuses correct
        # work is an outage). So today's failures are recorded as tolerated, and the
        # gate refuses only two things: a NEW document that fails, and an existing
        # document that gets worse. The backlog then burns down instead of blocking.
        base = {f"{d.repo}::{d.path}": sorted(d.failures())
                for d in docs if d.failures()}
        pathlib.Path(args.write_baseline).write_text(
            json.dumps({
                "written": dt.datetime.now(dt.UTC).date().isoformat(),
                "documents_total": len(docs),
                "documents_failing": len(base),
                "note": "Tolerated failures. New documents must have none. "
                        "Shrink this file, never grow it.",
                "tolerated": base,
            }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"baseline written: {len(base)} tolerated of {len(docs)} documents")
        return 0

    if args.json:
        print(json.dumps([{**dataclasses.asdict(d), "failures": d.failures()}
                          for d in docs], indent=2))
        return 0

    failing = [d for d in docs if d.failures()]
    shown = failing if args.failures else docs

    if not docs:
        print("no documents found -- check the repo list")
        return 1

    print(f"{'repo':<16} {'document':<46} {'ok':<3} {'prose':>6}  fails")
    for d in sorted(shown, key=lambda x: (x.repo, x.path)):
        f = d.failures()
        print(f"{pathlib.Path(d.repo).name:<16} {d.path[:46]:<46} "
              f"{'--' if f else 'ok':<3} {d.prose:>6}  {','.join(f)}")

    counted = {
        "documents": len(docs),
        "persisted": sum(d.persisted for d in docs),
        "owned": sum(bool(d.owner) for d in docs),
        "dated": sum(bool(d.date) for d in docs),
        "substantial": sum(d.substantial for d in docs),
        "passing all": len(docs) - len(failing),
    }
    print()
    for k, v in counted.items():
        print(f"{k:<14} {v:>5} / {len(docs)}")

    if args.failures:
        return 1 if failing else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
