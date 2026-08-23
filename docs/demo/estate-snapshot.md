# Demo: estate-snapshot

This is a real run, pasted as it came back. Nothing here is invented.

## The command

```
cd ~/dev/code/crew && ./scripts/estate-snapshot
```

## What it printed, 2026-08-23 19:48 UTC

```
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
| &nbsp;&nbsp;#22 Observability: the proposed architecture covers a third of the estate | | |
| &nbsp;&nbsp;#13 Retire the Hermes estate: unconditional, Hermes is discontinued | | |
```

## What that run actually established

The Architect passed 16 of its 17 checks. The single failure is `every service answers`, and
the service that does not answer is `prospector-engine`, which has zero machines on Fly. That
is a Fly problem, not an Architect problem, and the snapshot shows which check failed so nobody
has to go and find out.

maestro sensed the estate two minutes before the run and holds one skill it can repair with.
That distinguishes a healthy maestro from a dead one, which silence never could.

Three Fly apps are deployed and eleven are suspended, and five P1 crew issues are open. Two of
those five are the same wall: Fly will not build because the account has overdue invoices.

## What it looks like when something cannot be measured

If `bin/verify` produces no verdict line, or the INTENT directory is empty, or `gh` fails, the
row says `NOT RUN` and names why. It never says PASS. A checker that has died and an estate
that is healthy must never produce the same output, because a green board nobody can distrust
is how four days of broken coordination went unnoticed.
