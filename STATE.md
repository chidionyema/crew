# Estate snapshot

**Generated 2026-08-24 17:41 UTC** by `scripts/estate-snapshot`. Every row is a command and its
output. A row that could not be measured says NOT RUN, never PASS.

Read this before asking anyone anything. Regenerate it rather than trusting it:
`scripts/estate-snapshot`.

| what | state | measured by |
|---|---|---|
| The Architect | GREEN | `bin/verify`: 18 passed, 0 failed |
| maestro | GREEN | last cycle 6 min ago (`INTENT-20260824-173041-0d20f3e7.json`) |
| &nbsp;&nbsp;skills | GREEN | 3 skill(s) it can heal with |
| Fly | 3 deployed, 11 suspended | `flyctl apps list` |
| &nbsp;&nbsp;hermes-ci | suspended, last release Aug 19 2026 13:03 | R1: it does not come back on Fly |
| &nbsp;&nbsp;prospector-hermes | suspended, last release Aug 21 2026 22:34 | R1: it does not come back on Fly |
| &nbsp;&nbsp;prospector-hermes-v2 | suspended, last release Aug 22 2026 13:54 | R1: it does not come back on Fly |
| &nbsp;&nbsp;prospector-searxng | suspended, last release Aug 18 2026 08:42 | R1: it does not come back on Fly |
| &nbsp;&nbsp;tie-api | suspended, last release Jun 13 2026 12:22 | R1: it does not come back on Fly |
| &nbsp;&nbsp;tie-smoke | suspended, last release Jun 13 2026 03:36 | R1: it does not come back on Fly |
| estate spend | NOT RUN | no warehouse: run `science/collect.py` |
| delivery | STALE | 1 commits on no remote (oldest 0.3d), 8 dirty files, 5 live repos (`git log --branches --not --remotes`) |
| &nbsp;&nbsp;shipped | 350 merged | non-bot PRs merged across the estate in 7d (`gh search prs`) |
| &nbsp;&nbsp;stranded | .crew-state | 1 commits no remote holds, oldest 0.3d, 0 dirty |
| founder cost | NOT RUN | `attention_daily` did not answer |
| collectors | NOT RUN | `ingest_log` did not answer |
| crew P1 | 12 open | the fires nobody has put out |
| &nbsp;&nbsp;#116 Spec: the Fly-exit rehearsal drill passes, repeatably, for £0 | | |
| &nbsp;&nbsp;#114 Fully operational today — the day board, 2026-08-24 | | |
| &nbsp;&nbsp;#85 Machine overload: load 255 on 12 cores with founder at keyboard — no cross-session load governor | | |
| &nbsp;&nbsp;#78 Decommission Fly, move to Kubernetes — architecture decision, scope not yet defined | | |
| &nbsp;&nbsp;#74 Build the real data pipeline: DuckDB + DuckLake + fastjsonschema, and grade each dependency on use, distri | | |
| &nbsp;&nbsp;#71 1,064 field paths, 0 declared: the warehouse has no schema, no owner, no retention and no sensitivity on a | | |
| &nbsp;&nbsp;#69 32 of 59 scripts are wired into nothing, and one of them is the LAW 22 evidence tool | | |
| &nbsp;&nbsp;#38 The exit from Fly has never once been drilled: the escape hatch cannot pass as written | | |
| &nbsp;&nbsp;#35 Fly.io refuses to build: the account has overdue invoices, and production is 10 commits behind | | |
| &nbsp;&nbsp;#26 Estate spend is $866/day against a $120 cap, and one owner is 69% of it | | |
| &nbsp;&nbsp;#22 Observability: the proposed architecture covers a third of the estate — audit, and the smaller next step | | |
| &nbsp;&nbsp;#13 Retire the Hermes estate — unconditional, Hermes is discontinued | | |
| docker context | GREEN | `docker context show` -> colima |
| second container runtime | GREEN | `pgrep -f 'Docker.app/Contents/MacOS' | wc -l` -> 0 |
| colima dockerd | GREEN | socket answered containers/json |
