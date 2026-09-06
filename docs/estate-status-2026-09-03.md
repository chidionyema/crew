# Estate status — 2026-09-03

Written to close crew#59, the auto-opened "get up to speed on the estate" issue. The founder
asked, in his own words, to be brought up to speed on everything that has happened on this
estate in the last week or so and what the current agent sessions are working on. This page is
that report, kept in the repo so a command proves the outcome rather than an agent's word.

Every number below is quoted from a measured source in this repo (`STATE.md`, generated
2026-09-03 11:03 UTC by `scripts/estate-snapshot`) or from the ESTATE 360 recon of 2026-08-23.
Regenerate rather than trust: `scripts/estate-snapshot`.

## What is live and selling

- mumchimp.com store is LIVE and selling (store-api deployed 08-20, store-web 08-21). The
  engine runs on the laptop via launchd from prospector-live.
- Fly account is PAST_DUE: the engine app has been suspended since 18:00, 14 merged PRs cannot
  reach production, and production is not running main.

## What is broken or down

- The Architect's Telegram gateway (`ai.architect.gateway`) is NOT running. Five more launchd
  jobs exit non-zero: consultd, boardserve, kimi-bridge, deepseek-bridge, aiden.watch. The
  founder's inbound channel and the consult layer are down together.
- Fly: `flyctl apps list` fails — no access token available.
- estate spend, revenue, ci runs, founder cost, collectors, runtime: all NOT RUN (their data
  sources did not answer).
- OCI verification identity: RED — 0 scheduled runs in 24h; the cron never fired (crew#345).
- science plane: warehouse RED (0 dbt models, rebuilt 233h ago); experiment tracker ABSENT (no
  MLflow); forecast ledger RED (15 forecasts, 0 scored against reality).
- data map RED: 4077 producers, 33908 measurables, 283 in gaps with a ticket, 18 unexplained,
  domain cluster_live BLIND.

## Money

- 14-day total $10,189.55; $727.83/day mean vs a $120 cap. Week-over-week +41.8%.
- Today Opus-5 is 99% of spend; cache transport is 82% of all cost; interactive sessions are
  62–69% of spend on peak days.
- The brake (estate_cost_sentinel) can only pause prospector-daemon = 0.1–2% of spend. halt_usd
  is 0 (disarmed). The brake does not reach the thing that spends.

## The scatter, measured

- ~470 commits/7d across guards/hermes-v2/estate/crew/maestro plus ~1,500 in prospector,
  against 3 open PRs, all drafts.
- Dirty trees across ~/.claude/scripts, crew, hermes-v2, maestro; prospector is on a detached
  HEAD with 17 dirty worktrees and several ahead-of-origin branches with no PR.
- Board: 17 real active issues, 2 needs-founder, 8 captured-prompt noise issues.
- Rust engine: spec complete, ~48K lines exist in prospector-rust, 0% further movement —
  stopped on one founder decision (claude_cli in a container).
- Maestro: alive, cycling, 2 unpushed fix commits; spec contradiction MAE-040 vs MAE-050.

## Current agent sessions and lanes

The board's P1 list (30 open) is the fires nobody has put out. The top rows:

- #795 Squad model: Claude plans and manages, cheap models execute, Kimi and Gemini consult.
- #791 / #790 INC2 and INC1: Kustomizations fail to reconcile on a kyverno admission webhook EOF.
- #718 The founder cannot open five of the eight monitoring tools.
- #668 Incident ledger; #667 Hazard register to zero; #652 Audit of the guards.
- #626 DEFECTS on the god view; #620 Strict shell practice estate-wide.
- #609 Product function (stealth); #607 PR age; #568 unified provider-agnostic model stack.
- #345 OCI session expiry; #340 Langfuse healthcheck; #326 _router overwrite incident.
- #318 P0: MacBook load average 555/530/336 — machine in genuine distress.
- #313 LiteLLM proxy down; #311 estate-operators policy outside tofu; #290 continuity.
- #283 Science & ML gaps; #279 Estate MCP write-side ledger.

The 2026-08-31 surface map (`docs/plans/2026-08-31-crew-surface-map.md`) is the agreed plan for
the next cycle: one estate config, one scheduler, a knowledge store, crewAI Crew with Agent
defs, task↔issue sync, duckdb/MLflow cutovers, rules extracted to OPA, bridges retired onto
LiteLLM lanes, auto-merge native, launchd retirement, store consolidation, root-doc dedupe,
literal sweep, and a Vale output gate. Every deletion lands only behind a CONFIRM on the board.

## Three founder decisions, stated once

1. Pay the Fly invoice — unblocks #35 #679 #673 #661, 14 PRs, and makes #38's exit drill
   testable.
2. claude_cli container decision (A OAuth-in-container / B metered API / C drop) — unblocks the
   Rust migration.
3. iCloud: delete or archive the 67 container-only dirs — unblocks the rescue session.

## Definition of done for this issue

- [x] Built: this report is merged and CI is green.
- [x] Proved: `scripts/estate-snapshot` regenerates the source of every number above.
- [ ] Founder used it and confirmed (receipt: the comment or message where he said so).
