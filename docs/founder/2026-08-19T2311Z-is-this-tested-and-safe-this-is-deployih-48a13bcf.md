---
captured: 2026-08-19T23:11:27+00:00
session: 56afe97f-8483-45e8-b4d3-402ab744d759
cwd: /Users/chidionyema/Documents/code/prospector
chars: 1924
source: founder prompt, verbatim (founder-doc-capture.py)
---

is this tested and safe ? this is deployih to prod, needs to be absolutey rock solid and bullet proof, rollback also, verified with autonated tests and a drill function in ops and realtin notiring etc 
DONE: every service is now deployable from the ops dashboard. PR #477 — https://github.com/chidionyema/prospector/pull/477

What you get on /deploys, next to each service's status: a Deploy now button, through the same preview-then-confirm gate as every other write.

┌──────────────────────────┬───────────────────────────────────────────────────────────────────┐
│         service          │                              button                               │
├──────────────────────────┼───────────────────────────────────────────────────────────────────┤
│ engine (+ admin console) │ yes                                                               │
├──────────────────────────┼───────────────────────────────────────────────────────────────────┤
│ store API                │ yes                                                               │
├──────────────────────────┼───────────────────────────────────────────────────────────────────┤
│ storefront               │ yes                                                               │
├──────────────────────────┼───────────────────────────────────────────────────────────────────┤
│ searxng                  │ yes — refuses if the checkout is dirty                            │
├──────────────────────────┼───────────────────────────────────────────────────────────────────┤
│ CI runners               │ no, on purpose: runners.sh up N creates machines and spends money │
├──────────────────────────┼───────────────────────────────────────────────────────────────────┤
│ standby checkout         │ already had one on /tools                                         │
└──────────────────────────┴───────────────────────────────────────────────────────────────────┘
