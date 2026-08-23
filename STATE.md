# Estate snapshot

**Generated 2026-08-23 23:58 UTC** by `scripts/estate-snapshot`. Every row is a command and its
output. A row that could not be measured says NOT RUN, never PASS.

Read this before asking anyone anything. Regenerate it rather than trusting it:
`scripts/estate-snapshot`.

| what | state | measured by |
|---|---|---|
| The Architect | RED | `bin/verify`: 15 passed, 2 failed |
| &nbsp;&nbsp;failing | | FAIL  README describes what ships        docs/demo/claim-gate.md is in the repo, and the README never says why |
| &nbsp;&nbsp;failing | | FAIL  agent is the pinned commit         b3ec1c9bc3 (want 1220c4ad24) |
| maestro | GREEN | last cycle 3 min ago (`INTENT-20260823-235326-0d20f3e7.json`) |
| &nbsp;&nbsp;skills | GREEN | 3 skill(s) it can heal with |
| Fly | 3 deployed, 11 suspended | `flyctl apps list` |
| estate spend | RED | $764/day 7-day mean against a $120 cap (`spend_daily`, warehouse.db) |
| founder cost | GREEN | 4678 msgs / 7% complaints this week against 1479 / 9% last (`attention_daily`) |
| collectors | RED | 2 of the estate's data stores stopped being written: decisions silent 55h; would_have_fired silent 50h |
| crew P1 | 5 open | the fires nobody has put out |
| &nbsp;&nbsp;#38 The exit from Fly has never once been drilled: the escape hatch cannot pass as written | | |
| &nbsp;&nbsp;#35 Fly.io refuses to build: the account has overdue invoices, and production is 10 commits behind | | |
| &nbsp;&nbsp;#26 Estate spend is $431/day against a $120 cap and the only brake reaches 0.03% of it | | |
| &nbsp;&nbsp;#22 Observability: the proposed architecture covers a third of the estate — audit, and the smaller next step | | |
| &nbsp;&nbsp;#13 Retire the Hermes estate — unconditional, Hermes is discontinued | | |
