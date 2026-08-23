#!/usr/bin/env python3
"""Every law in AGENTS.md has a check written for it in enforcement-map.json.

The founder's words: laws held as verbatim prose are "not good, better to have
laws explicitly derived into automatable machine code". This is the check that
says whether that derivation is complete. It does not ask whether the check is
wired up -- law_enforcement.py answers that, and the answer is currently 9 of
17. It asks the narrower question that has to be true first: has anybody
written down what would decide this law.

Exit 0 when every law has a check. Exit 1 naming the ones that do not.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAP = os.path.join(HERE, "enforcement-map.json")
LAWS = os.path.expanduser("~/AGENTS.md")


def main():
    m = json.load(open(MAP))
    entries = {l["id"]: l for l in m["laws"]}
    #: `#+`, not `#`. On 2026-08-23 the law headings went from `# LAW 1` to
    #: `## LAW 1` and this check silently read zero laws, which made every
    #: map entry look like an orphan and hid the real change underneath the
    #: noise. Match the same shape law_enforcement.py matches.
    declared = {int(x) for x in
                re.findall(r"^#+\s*LAW (\d+)\b", open(LAWS).read(), re.M)}
    if not declared:
        print("NO LAW HEADINGS FOUND in %s. The parser and the file "
              "disagree; fix the parser before trusting any count below."
              % LAWS)
        return 1
    #: A judgement law is one the map says will never be code. It needs an
    #: entry saying so, and saying so IS the derivation. It does not need a
    #: check, and demanding one would push somebody to invent a fake test.
    #: A check is bound to a law by its NUMBER, and on 2026-08-23 the numbers
    #: moved: 32 laws were consolidated into 10, so map entry 3 went on quietly
    #: describing "never make the same mistake twice" while LAW 3 had become
    #: "think it through". Nothing failed. The orphan list below catches a law
    #: that vanished; only the title catches a law that was REPLACED.
    titles = dict(re.findall(r"^#+\s*LAW (\d+)\s*[\u2014-]\s*(.+)$",
                             open(LAWS).read(), re.M))
    renamed = []
    for i in sorted(declared & set(entries)):
        now = titles.get(str(i), "").strip()
        was = (entries[i].get("law_title") or "").strip()
        if was != now:
            renamed.append((i, was or "(none recorded)", now))

    judgement = {i for i, l in entries.items() if l.get("verdict") == "judgement"}
    written = {i for i, l in entries.items() if (l.get("check") or "").strip()}
    missing = sorted((declared - set(entries))
                     | ((declared & set(entries)) - written - judgement))
    orphan = sorted(set(entries) - declared)
    print(f"laws in AGENTS.md      : {len(declared)}")
    print(f"declared judgement     : {len(judgement)}  (an entry, no check, by design)")
    print(f"laws with a check      : {len(declared & written)}")
    if missing:
        print(f"NO CHECK WRITTEN       : {missing}")
    if orphan:
        print(f"ENTRY FOR A LAW THAT IS GONE: {orphan}")
    if renamed:
        print(f"CHECK POINTS AT A DIFFERENT LAW THAN IT WAS WRITTEN FOR: {len(renamed)}")
        for i, was, now in renamed:
            print(f"    LAW {i:<3} map wrote it for : {was}")
            print(f"    {'':<7} the file now says: {now}")
    return 1 if (missing or orphan or renamed) else 0


if __name__ == "__main__":
    sys.exit(main())
