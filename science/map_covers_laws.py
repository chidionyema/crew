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
LAWS = os.path.expanduser("~/AGENTS.md")


def titles(path):
    #: `#+`, not `#`. For a few minutes on 2026-08-23 the headings were `##` and
    #: this file read zero laws, which made every entry look like an orphan and
    #: buried the real change under the noise.
    return dict(re.findall(r"^#+\s*LAW (\d+)\s*[—-]\s*(.+)$",
                           open(path, encoding="utf-8").read(), re.M))


SNAPSHOT = os.path.expanduser("~/.claude/AGENTS.snapshot.md")


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
    now = {int(k): v.strip() for k, v in titles(LAWS).items()}
    if not now:
        print(f"NO LAW HEADINGS FOUND in {LAWS}. The parser and the file "
              f"disagree; fix the parser before trusting any count below.")
        return 1

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
    try:
        same = open(SNAPSHOT, encoding="utf-8").read() == open(LAWS, encoding="utf-8").read()
    except OSError:
        same = False
    if not same:
        print(f"TRACKED COPY IS STALE    : {SNAPSHOT} differs from {LAWS}")

    was_sha = (m.get("laws_commit") or {}).get("sha", "")
    now_sha = laws_commit_now()
    if was_sha and now_sha and was_sha != now_sha:
        print(f"laws moved since the map : written against {was_sha[:7]}, "
              f"tracked copy is now {now_sha[:7]}")

    print(f"laws in AGENTS.md        : {len(now)}")
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
