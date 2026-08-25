# Estate snapshot

**Generated 2026-08-25 17:09 UTC** by `scripts/estate-snapshot`. Every row is a command and its
output. A row that could not be measured says NOT RUN, never PASS.

Read this before asking anyone anything. Regenerate it rather than trusting it:
`scripts/estate-snapshot`.

| what | state | measured by |
|---|---|---|
| The Architect | NOT RUN | bin/verify produced no verdict line |
| maestro | GREEN | last cycle 2 min ago (`INTENT-20260825-170402-0d20f3e7.json`) |
| &nbsp;&nbsp;skills | GREEN | 3 skill(s) it can heal with |
| Fly | NOT RUN | `flyctl apps list` failed: No apps found |
| estate spend | NOT RUN | `spend_daily` view did not answer |
| delivery | RED | 20 commits on no remote (oldest 1.3d), 15 dirty files, 6 live repos (`git log --branches --not --remotes`) |
| &nbsp;&nbsp;shipped | 418 merged | non-bot PRs merged across the estate in 7d (`gh search prs`) |
| &nbsp;&nbsp;stranded | scripts | 18 commits no remote holds, oldest 1.2d, 0 dirty |
| &nbsp;&nbsp;stranded | .crew-state | 1 commits no remote holds, oldest 1.3d, 0 dirty |
| &nbsp;&nbsp;stranded | .wt-backstage-proof | 1 commits no remote holds, oldest 0.5d, 3 dirty |
| founder cost | NOT RUN | `attention_daily` did not answer |
| collectors | NOT RUN | `ingest_log` did not answer |
| crew P1 | 14 open | the fires nobody has put out |
| &nbsp;&nbsp;#220 Daily teardown-and-rebuild drill of the OKE stack: one-shot rebuild, zero hand steps, every failure mode  | | |
| &nbsp;&nbsp;#219 KINI spec: all 42 requirements met, acceptance executable (founder 2026-08-25) | | |
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
| colima dockerd | RED | socket gave nothing in 8s -- every estate container is unserved; do NOT restart colima, route to the firefighter |
