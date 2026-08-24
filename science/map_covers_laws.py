#!/usr/bin/env python3
"""Every law in AGENTS.md has a check written for it in enforcement-map.json.

The map is the compiler from prose to machine. It is hand-written, so it rots
in three ways and this refuses all three:

  a law exists and nothing checks it
  a check exists for a law that has been deleted
  a check exists for a law NUMBER whose meaning has changed underneath it

The third one is the reason this file was rewritten. On 2026-08-23 the founder
cut 32 laws to 10 and the numbers moved. Entry 3 went on describing "never make
the same mistake twice" while LAW 3 had become "think it through". Nothing
failed, because a number still matched a number. Now the title has to match too.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAP  = os.path.join(HERE, "enforcement-map.json")
#: The laws do not always live in one file. At 03:37 on 2026-08-24 a session split
#: them: ~/AGENTS.md kept the table and the working rules, and the 42 law bodies
#: moved to ~/AGENTS-FULL.md, which cut about 80 KB off every session's injected
#: context. That is a good change and this file broke on it within the hour,
#: exiting 1 with "NO LAW HEADINGS FOUND" and taking G1, the law-coverage metric,
#: down with it. Naming one path was the defect. Ask which file actually holds the
#: bodies rather than assuming, and say which one was read.
LAW_FILES = [os.path.expanduser(p) for p in ("~/AGENTS.md", "~/AGENTS-FULL.md")]

HEADING = re.compile(r"^#+\s*LAW (\d+)\s*[—-]\s*(.+)$", re.M)


def titles(path):
    #: `#+`, not `#`. For a few minutes on 2026-08-23 the headings were `##` and
    #: this file read zero laws, which made every entry look like an orphan and
    #: buried the real change under the noise.
    try:
        return dict(HEADING.findall(open(path, encoding="utf-8").read()))
    except OSError:
        return {}


def law_source():
    """The file that actually carries the law bodies, and its titles.

    Whichever candidate yields the most headings wins, so a split, a rename or a
    move back into one file all keep working without an edit here. Returning zero
    from every candidate is a real finding and stays a hard failure.
    """
    best = ("", {})
    for p in LAW_FILES:
        t = titles(p)
        if len(t) > len(best[1]):
            best = (p, t)
    return best


SNAPSHOT = os.path.expanduser("~/.claude/AGENTS.snapshot.md")


def snapshot_for(path):
    """The tracked copy that should hold this law file.

    `~/AGENTS.md` keeps its historical snapshot name so the existing sync and the
    git history that goes with it are untouched. Anything else takes its own
    basename, so `~/AGENTS-FULL.md` wants `~/.claude/AGENTS-FULL.snapshot.md`.
    """
    if os.path.abspath(path) == os.path.expanduser("~/AGENTS.md"):
        return SNAPSHOT
    stem = os.path.basename(path)[:-3] if path.endswith(".md") else os.path.basename(path)
    return os.path.expanduser(f"~/.claude/{stem}.snapshot.md")


def laws_commit_now():
    """The sha of the last commit that changed the tracked copy of the laws.

    ~/AGENTS.md is not inside any repository, so `git log` on it shows nothing
    and the laws look frozen since 2026-08-22. The tracked copy is the snapshot
    beside it. Comparing shas answers "have the laws moved since these checks
    were written" without asking a person.
    """
    import subprocess
    try:
        return subprocess.run(["git", "-C", os.path.dirname(SNAPSHOT), "log", "-1",
                               "--format=%H", "--", os.path.basename(SNAPSHOT)],
                              capture_output=True, text=True, timeout=15).stdout.strip()
    except Exception:
        return ""


def main():
    m = json.load(open(MAP))
    entries = m["laws"]
    laws_path, raw = law_source()
    now = {int(k): v.strip() for k, v in raw.items()}
    if not now:
        print(f"NO LAW HEADINGS FOUND in any of {', '.join(LAW_FILES)}. The parser "
              f"and the files disagree; fix the parser before trusting any count below.")
        return 1
    print(f"laws read from {laws_path}  ({len(now)} laws)")

    live    = [e for e in entries if e.get("law") is not None]
    retired = [e for e in entries if e.get("law") is None]

    #: A judgement rule is one the map says will never be code. It needs an
    #: entry saying so, and saying so IS the derivation. Demanding a check
    #: would push somebody to invent a fake test.
    def has_check(e):
        return e.get("verdict") == "judgement" or bool((e.get("check") or "").strip())

    covered = {e["law"] for e in live if has_check(e)}
    missing = sorted(set(now) - covered)
    orphan  = sorted({e["law"] for e in live if e["law"] not in now})
    renamed = [(e["rule"], e["law"], e.get("law_title") or "(none recorded)",
                now.get(e["law"], "(law is gone)"))
               for e in live if (e.get("law_title") or "").strip() != now.get(e["law"], "")]
    ownerless = [e["rule"] for e in retired if not e.get("retired_to")]

    #: A copy is not the thing. If the sync that writes the snapshot stops, the
    #: laws leave version control and nothing goes red, so say it here.
    #:
    #: Every law file gets its own check, not just the one the injector reads.
    #: Measured 2026-08-24 03:37: the split moved all 42 law bodies into
    #: ~/AGENTS-FULL.md, no repository held that file, and this check stayed quiet
    #: because it only ever looked at ~/AGENTS.md. A missing snapshot is a louder
    #: finding than a stale one and is reported as its own line (LAW 24).
    for path in LAW_FILES:
        if not os.path.exists(path):
            continue
        snap = snapshot_for(path)
        if not os.path.exists(snap):
            print(f"LAWS NOT IN VERSION CONTROL : {path} has no tracked copy at {snap}")
            continue
        try:
            same = open(snap, encoding="utf-8").read() == open(path, encoding="utf-8").read()
        except OSError:
            same = False
        if not same:
            print(f"TRACKED COPY IS STALE    : {snap} differs from {path}")

    was_sha = (m.get("laws_commit") or {}).get("sha", "")
    now_sha = laws_commit_now()
    if was_sha and now_sha and was_sha != now_sha:
        print(f"laws moved since the map : written against {was_sha[:7]}, "
              f"tracked copy is now {now_sha[:7]}")

    print(f"laws found               : {len(now)}")
    print(f"checks in the map        : {len(live)} bound to a law, {len(retired)} retired to a machine")
    print(f"laws with at least one   : {len(covered & set(now))}")
    if missing:
        print(f"NO CHECK WRITTEN         : {missing}")
    if orphan:
        print(f"CHECK FOR A LAW THAT IS GONE: {orphan}")
    if renamed:
        print(f"CHECK POINTS AT A DIFFERENT LAW THAN IT WAS WRITTEN FOR: {len(renamed)}")
        for rule, n, was, isnow in renamed:
            print(f"    {rule}  (LAW {n})")
            print(f"      written for : {was}")
            print(f"      now says    : {isnow}")
    if ownerless:
        #: Not a failure. A law retired to a guard that does not exist is a
        #: deleted law, so it is named every run until somebody writes the guard.
        print(f"RETIRED WITH NO OWNER    : {len(ownerless)}  {', '.join(ownerless)}")
    return 1 if (missing or orphan or renamed) else 0


if __name__ == "__main__":
    sys.exit(main())
