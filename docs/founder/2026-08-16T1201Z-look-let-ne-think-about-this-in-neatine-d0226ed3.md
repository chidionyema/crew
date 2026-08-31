---
captured: 2026-08-16T12:01:29+00:00
session: 4c49b786-9dd7-4240-ae83-d8d976d6f90c
cwd: /Users/chidionyema/Documents/code/prospector
chars: 3310
source: founder prompt, verbatim (founder-doc-capture.py)
---

look let ne think about this, in neatine 
✻ Brewed for 29s · 1 shell still running

⏺ Background command "Compute minimal covering set and list open PRs" completed (exit code 0)

  Read 1 file

One thing to check before I report: prospector-ruff carries 54fecb7c7 docs: the gate is back on, and the line for turning it on was inert — which may be the same CLAUDE.md fix I just made by hand.

  Ran 2 shell commands

DONE: surveyed. 39 worktrees hold 83 distinct unmerged patches; 26 of those worktrees carry zero unmerged work and are pure noise.

The recurring-problem answer is concrete. The fix for today's pre-commit confusion already exists: commit 54fecb7c7 docs: the gate is back on, and the line for turning it on was inert, authored 15 Aug 18:58 on chore/ruff-clean-for-precommit-gate. It has never shipped. I hand-wrote the same fix ten minutes ago before finding it, and reverted mine. Work isn't being lost, it's being stranded — 83 patches deep.

Second root cause: local main is 138 commits behind origin/main. Every "am I ahead?" measured against it is wrong. My own first survey read 135 unmerged for the trunk; against origin/main it is 46.

The commit running in this checkout (pid 65673, 8m46s) is the gate working normally, not wedged.

---
Coverage: 13 worktrees hold everything; 26 can be deleted

┌────────────────────────────────────────────────────────┬──────────┬─────────────────────────────────────────────────────────┐
│                        Worktree                        │ Unmerged │                          Note                           │
├────────────────────────────────────────────────────────┼──────────┼─────────────────────────────────────────────────────────┤
│ prospector (integrate/minimax-into-main)               │ 45       │ the trunk, 31 behind origin/main, 158 dirty, commit in  │
│                                                        │          │ flight                                                  │
├────────────────────────────────────────────────────────┼──────────┼─────────────────────────────────────────────────────────┤
│ wt-research                                            │ 12       │ tone/lint/retrieval batch                               │
├────────────────────────────────────────────────────────┼──────────┼─────────────────────────────────────────────────────────┤
│ prospector-us                                          │ 6        │ US market + money rail                                  │
├────────────────────────────────────────────────────────┼──────────┼─────────────────────────────────────────────────────────┤
│ prospector-ruff                                        │ 4        │ the gate fix + 12 ruff errors on main                   │
├────────────────────────────────────────────────────────┼──────────┼─────────────────────────────────────────────────────────┤
│ wt-226, wt-audit-med                                   │ 3 each   │                                                         │
├────────────────────────────────────────────────────────┼──────────┼─────────────────────────────────────────────────────────┤
│ wt-merge, wt-ceiling, wt-price-tool                    │ 2 each   │                                                         │
├────────────────────────────────────────────────── /pack page review,
