# Estate snapshot

**Generated 2026-08-24 17:43 UTC** by `scripts/estate-snapshot`. Every row is a command and its
output. A row that could not be measured says NOT RUN, never PASS.

Read this before asking anyone anything. Regenerate it rather than trusting it:
`scripts/estate-snapshot`.

| what | state | measured by |
|---|---|---|
| The Architect | NOT RUN | bin/verify produced no verdict line |
| maestro | GREEN | last cycle 2 min ago (`INTENT-20260824-173742-0d20f3e7.json`) |
| &nbsp;&nbsp;skills | GREEN | 3 skill(s) it can heal with |
| Fly | NOT RUN | `flyctl apps list` failed: TIMED OUT after 45s |
| estate spend | NOT RUN | `spend_daily` view did not answer |
| delivery | GREEN | 0 commits on no remote (oldest 0.0d), 10 dirty files, 4 live repos (`git log --branches --not --remotes`) |
| &nbsp;&nbsp;shipped | 350 merged | non-bot PRs merged across the estate in 7d (`gh search prs`) |
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
