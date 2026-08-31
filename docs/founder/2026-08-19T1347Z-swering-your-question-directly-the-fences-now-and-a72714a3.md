---
captured: 2026-08-19T13:47:20+00:00
session: 9ddde4bb-7cfc-445d-b504-bf96307acbd4
cwd: /Users/chidionyema/Documents/code/prospector
chars: 1507
source: founder prompt, verbatim (founder-doc-capture.py)
---

swering your question directly — the fences now, and the two that were genuinely missing:

┌───────────────────────────────┬───────────────────────────────────────────────────┬──────────────────────┐
│            Failure            │                       Fence                       │        State         │
├───────────────────────────────┼───────────────────────────────────────────────────┼──────────────────────┤
│ Stale-base merge reddens main │ automerge.yml refuses behind_by > 0               │ Live — b87dea3b      │
├───────────────────────────────┼───────────────────────────────────────────────────┼──────────────────────┤
│ Merge lands but never deploys │ DEPLOY path map, automerge.yml:87-91              │ Live                 │
├───────────────────────────────┼───────────────────────────────────────────────────┼──────────────────────┤
│ CI queue starves              │ ci-autoscale.yml + deploy/runners.sh              │ Live — #396          │
├───────────────────────────────┼───────────────────────────────────────────────────┼──────────────────────┤
│ UI regression reaches prod    │ e2e/fold-budget.spec.ts in CI's nextjs job        │ PR #414, CI running  │
├───────────────────────────────┼───────────────────────────────────────────────────┼──────────────────────┤
│ Live check goes red silently  │ live-red issue, opened on failure, closed on pass │ PR #416, just opened │
└───────────────────────────────┴───────────────────────────────────────────────────┴──────────────────────┘
