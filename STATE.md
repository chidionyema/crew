# Estate snapshot

**Generated 2026-08-23 19:48 UTC** by `scripts/estate-snapshot`. Every row is a command and its
output. A row that could not be measured says NOT RUN, never PASS.

Read this before asking anyone anything. Regenerate it rather than trusting it:
`scripts/estate-snapshot`.

| what | state | measured by |
|---|---|---|
| The Architect | RED | `bin/verify`: 16 passed, 1 failed |
| &nbsp;&nbsp;failing | | FAIL  every service answers |
| maestro | GREEN | last cycle 2 min ago (`INTENT-20260823-194521-0d20f3e7.json`) |
| &nbsp;&nbsp;skills | GREEN | 1 skill(s) it can heal with |
| Fly | 3 deployed, 11 suspended | `flyctl apps list` |
| crew P1 | 5 open | the fires nobody has put out |
| &nbsp;&nbsp;#38 The exit from Fly has never once been drilled: the escape hatch cannot pass as written | | |
| &nbsp;&nbsp;#35 Fly.io refuses to build: the account has overdue invoices, and production is 10 commits behind | | |
| &nbsp;&nbsp;#26 Estate spend is $431/day against a $120 cap and the only brake reaches 0.03% of it | | |
| &nbsp;&nbsp;#22 Observability: the proposed architecture covers a third of the estate — audit, and the smaller next step | | |
| &nbsp;&nbsp;#13 Retire the Hermes estate — unconditional, Hermes is discontinued | | |
