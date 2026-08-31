---
captured: 2026-08-01T04:32:58+00:00
session: 66f3f988-1f3b-4c2e-bc9a-3ee7e0090a7b
cwd: /Users/chidionyema/Documents/code/prospector
chars: 4862
source: founder prompt, verbatim (founder-doc-capture.py)
---

also you need to address 
https://github.com/chidionyema/prospector/pull/21 — 4 files, +394/-7, based on origin/main, POPDD gate passed (980 passed, 0 failed, chain valid: True), full suite 979 passed, 5 skipped on the clean base. The guard test was re-confirmed RED with the fix reverted.

I built it in a throwaway worktree off origin/main and re-typed my two edits by hand rather than extracting patches, so there was no mechanism by which the other agent's work could ride along. git diff --cached --stat showed exactly four files.

The analysis you asked for — my "untouched and fine" was half right

"Untouched" was correct. "Fine" was not, and I shouldn't have implied it.

12 files are simultaneously dirty locally and modified by the 11 upstream commits. That's the live hazard, and I measured it rather than repeating the checkpoint's warning:

┌─────────────────────┬───────────────────┬─────────────────────────────────────────────────────────┐
│        file         │ dirty vs upstream │                      what it means                      │
├─────────────────────┼───────────────────┼─────────────────────────────────────────────────────────┤
│ globals.css         │ +51 / −64         │ has 6 of upstream's 11 --font-serif/font-sans-pref refs │
├─────────────────────┼───────────────────┼─────────────────────────────────────────────────────────┤
│ index.tsx           │ +24 / −72         │ large net deletion                                      │
├─────────────────────┼───────────────────┼─────────────────────────────────────────────────────────┤
│ _app.tsx            │ +36 / −20         │                                                         │
├─────────────────────┼───────────────────┼─────────────────────────────────────────────────────────┤
│ MarketingLayout.tsx │ +22 / −1          │                                                         │
└─────────────────────┴───────────────────┴─────────────────────────────────────────────────────────┘

A git commit -a on this branch would delete 5 of the 11 webfont references — i.e. partially revert PR #18, the fix that made the storefront's downloaded webfont actually render. The design files are the real landmine.

The scheduler files are not in the same danger. I checked specifically: the dirty run_scheduled.py still carries PR #16's _TICK_HARD_DEADLINE_S = 10800, and a function-by-function comparison shows it loses nothing upstream has. Their actual functional additions there are _moat_preflight() and _next_market() — the WS1 reliability and WS3 market-rotation work your checkpoint recorded as proven. That work is sound; it's just sitting on a stale base.

One correction to my own earlier message: I described their hunks as "check_parallelism, vet_workers, batch_size, market-rotation". check_parallelism and vet_workers are the config side; the substantive code is _moat_preflight / _next_market. Same conclusion, more accurate naming.

Insurance taken                                                                                                                                                             
That work existed only in the working tree — 85 dirty entries, 52 modified files, no commit, no stash, no backup. I've written a read-only snapshot to the scratchpad:      
scratchpad/dirty-tree-backup-20260801/                                                                                                                                        tracked-modifications.patch   (12,295 lines)
  untracked-list.txt            (32 files)                                                                                                                                    base-commit.txt               (37b79d5)
                                                                                                                                                                            Nothing in your tree was modified — still 85 dirty entries, exactly as bef
                                                                                                                                                                            What I'd do next, and what I won't do unasked
                                                                                                                                                                            The design files need someone to rebase onto origin/main and re-apply theiing upstream's version of the webfont and teal work. That's the parallelsession's call — it's their work, they know which of those −64 lines were deliberate. I'm not going to touch it.                                                            
Meanwhile the daemon keeps running the combined tree, so the lane fix is live regardless of when their work lands. First lane-tagged dossiers in roughly 90 minutes; verify with §5 of the runbook.
