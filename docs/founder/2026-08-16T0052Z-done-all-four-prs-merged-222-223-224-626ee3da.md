---
captured: 2026-08-16T00:52:45+00:00
session: 74570eb1-485f-4cb4-8e5c-19e59adeec34
cwd: /Users/chidionyema/Documents/code/prospector
chars: 3249
source: founder prompt, verbatim (founder-doc-capture.py)
---

DONE: all four PRs merged (#222, #223, #224, #225); #226 is armed to land on CI. Both copy defects are fixed and on main, and the live backfill is built and dry-run clean.

The backfill has not been applied — three things still block it, listed below.

---
Merged. #224 engine info out of the pack · #223 unban leverage/ecosystem · #222 mobile visual system · #225 the two copy defects. Verified the copy fix survived the #222 merge: git show origin/main:.../pack/[id].tsx | rg -c "You get the checking already done" → 1.

What the live measurement changed (all 61 packs, not a sample):

┌──────────────────────────────────────────────┬──────────────────────────────────────────────────────────────────────────────┐
│                                              │                                                                              │
├──────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
│ index.html carries "How it scored"           │ 61/61                                                                        │
├──────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
│ Complete_Pack.pdf carries it too             │ 3/3 sampled — both are rendered, so no in-place edit                         │
├──────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
│ manifest.jsonld                              │ 61/61 already clean — the previous session's "10/12 ruledBy" read the wrong  │
│                                              │ object                                                                       │
├──────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
│ scorecard.json/.csv/.svg                     │ never ship                                                                   │
├──────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
│ pre-conversion object with the .md still in  │ 59/61                                                                        │
│ R2                                           │                                                                              │
└──────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────┘

Dry-run over all 61: would-convert=56, already-correct=1, no-source=2, error=2.

The three blockers, in order:

1. Two packs error — d8aa7528aa73eabb and one other: "rebuilt reader STILL carries ['composite ']". That is my pre-upload guard firing; likely legitimate prose ("aluminium composite"), not a real leak, but unverified.
2. Two packs have no pre-conversion object to render from.
3. STORE_INTERNAL_API_KEY is unset, so --apply refuses at startup. R2 read creds are set.

Correction: the "standing ban" I quoted was not yours — it was an unverified line in the previous session's handoff. I've recorded that in the checkpoint so it doesn't get repeated.

Safe point — type /clear (state saved, nothing will be lost). how do we solve
