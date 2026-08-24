# Estate snapshot

**Generated 2026-08-24 02:59 UTC** by `scripts/estate-snapshot`. Every row is a command and its
output. A row that could not be measured says NOT RUN, never PASS.

Read this before asking anyone anything. Regenerate it rather than trusting it:
`scripts/estate-snapshot`.

| what | state | measured by |
|---|---|---|
| The Architect | NOT RUN | bin/verify produced no verdict line |
| maestro | GREEN | last cycle 5 min ago (`INTENT-20260824-024946-0d20f3e7.json`) |
| &nbsp;&nbsp;skills | GREEN | 3 skill(s) it can heal with |
| Fly | 2 deployed, 12 suspended | `flyctl apps list` |
| estate spend | RED | $806/day 7-day mean against a $120 cap (`spend_daily`, warehouse.db) |
| delivery | RED | 17 commits on no remote (oldest 3.6d), 45 dirty files, 8 live repos (`git log --branches --not --remotes`) |
| &nbsp;&nbsp;shipped | 294 merged | non-bot PRs merged across the estate in 7d, ~$19 of estate spend per shipped change (`gh search prs`) |
| &nbsp;&nbsp;stranded | crew | 11 commits no remote holds, oldest 1.7d, 5 dirty |
| &nbsp;&nbsp;stranded | prospector-main | 3 commits no remote holds, oldest 3.6d, 7 dirty |
| &nbsp;&nbsp;stranded | scripts | 3 commits no remote holds, oldest 0.2d, 4 dirty |
| founder cost | GREEN | 4225 msgs / 7% complaints this week against 1698 / 8% last (`attention_daily`) |
| collectors | RED | 2 of the estate's data stores stopped being written: decisions silent 58h; would_have_fired silent 53h |
| crew P1 | 10 open | the fires nobody has put out |
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
