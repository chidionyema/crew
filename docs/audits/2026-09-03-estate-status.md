# Estate status report — 2026-09-03

**Issue 59.** A session started changing files without a ticket, so this issue was opened
automatically. The founder asked to get up to speed on everything that has happened on this
estate recently, and on what the current agent sessions are working on. This report is the
answer, synthesised from the estate's own state files so nothing is re-derived by hand.

Sources (each is the estate's own record, dated and measured):
- `STATE.md` — generated estate snapshot, 2026-09-03 11:03 UTC.
- `ESTATE_STATE.md` — the estate state board (R16: only the founder declares something live).
- `docs/audits/2026-09-03-unshipped-7day.md` — the built-but-not-shipped audit.
- `CREW-BOARD-VISIBILITY.md` — how to read the board and what is on it.
- The ESTATE 360 comment on issue 59 (2026-08-23) — the earlier comprehensive overview.

## Platform

- The mumchimp.com store is live and selling (store-api deployed 08-20, store-web 08-21).
  Engine runs on the laptop via launchd from prospector-live.
- Fly account was PAST_DUE as of the ESTATE 360 comment (08-23): engine app suspended, 14
  merged PRs unreachable, production not running main. The 7-day audit and STATE.md do not
  re-measure Fly (STATE.md row: `flyctl apps list` failed with no access token).
- The Architect is GREEN per STATE.md (`bin/verify`: PASS dispatch claims agent-go and never
  icebox, 3 passed in 17.66s), with three failing rows: generated files match templates, agent
  is the pinned commit, and the URL card is pinned and current.
- maestro is GREEN, last cycle 7 min ago, 3 skills it can heal with.

## Money

- ESTATE 360 (08-23): 14-day total $10,189.55; $727.83/day mean vs $120 cap; week-over-week
  +41.8%. Today Opus-5 was 99% of $602.62; cache transport 82% of all cost; interactive
  sessions 62-69% of spend on peak days. The brake (estate_cost_sentinel) can only pause
  prospector-daemon = 0.1-2% of spend; halt_usd is 0 (disarmed).
- STATE.md (09-03): estate spend NOT RUN (`spend_daily` view did not answer); founder cost NOT
  RUN (`attention_daily` did not answer); revenue NOT RUN (last measurement 08-28 is 142h old).

## The scatter, measured

- ESTATE 360 (08-23): ~470 commits/7d across guards/hermes-v2/estate/crew/maestro + ~1,500 in
  prospector, against 3 open PRs, all drafts. Board: 17 real active issues, 2 needs-founder,
  8 captured-prompt noise issues.
- 7-day audit (09-03): three leaks in order of loss risk — (1) Mac-only work never pushed
  (dies with the laptop), (2) pushed-but-never-PR'ed (~90 branches across repos), (3) open PRs
  nobody is driving. ~120 local idp branches ahead of or absent from origin. 20 worktrees with
  uncommitted tracked edits. `~/dev/code` itself is a git repo with NO remote (LAW 24 violation
  as a standing state).
- STATE.md (09-03): delivery RED — 368 commits on no remote (oldest 10.8d), 23 dirty files, 6
  live repos. crew P1: 30 open fires.

## What the current agent sessions are working on

From STATE.md (09-03), the open P1 fires that sessions are driving include:
- #795 Squad model: Claude plans and manages, cheap models execute, Kimi and Gemini consult.
- #791 / #790 INC2 and INC1: Kustomization failures on a kyverno admission webhook EOF.
- #718 The founder cannot open five of the eight monitoring tools.
- #668 Incident ledger: every outage is a traced, classed, machine-readable row.
- #667 Hazard register to zero.
- #652 Audit of the guards.
- #626 DEFECTS on the god view.
- #620 Strict shell practice estate-wide.
- #609 Product function (stealth).
- #607 PR age: 4 machine-hours maximum.
- #527 The board applies science.
- #526 Open count never goes down.
- #508 Science is every lane at once.
- #503 Founder dashboard and every surface polished.
- #345 Platform-level OCI session expiry.
- #340 Langfuse healthcheck failing unnoticed.
- #326 Incident: guards hook router overwritten with a refuse-all stub.
- #325 idp architectural review.
- #318 P0: MacBook load average 555/530/336.
- #313 LiteLLM proxy down.
- #311 Class: estate-operators policy lives outside tofu.
- #290 Continuity: reach Otto/the estate through any single loss.
- #283 Science & ML: close the 3 measured gaps.
- #279 Estate MCP needs a write-side ledger tool.

## Three founder decisions, stated once (everything else proceeds without him)

From the ESTATE 360 comment (08-23):
1. Pay the Fly invoice — unblocks #35 #679 #673 #661, 14 PRs, and makes #38's exit drill
   testable.
2. claude_cli container decision (A OAuth-in-container / B metered API / C drop) — unblocks
   #33 Rust migration.
3. iCloud: delete or archive the 67 container-only dirs — unblocks the rescue session.

From the 7-day audit (09-03), one-word decisions queued:
- REDIS: rebase `feat/litellm-redis`, PR it with the waiver design — or say TWO-REPLICAS.
- SPECS: land the crew spec/ruling branches (otto-platform-v1, r75, ultimate-edict,
  research-engine) to crew main.
- TRIAGE: the 42 idp never-PR'ed branches get a one-line verdict each (ship / close /
  superseded), batched, one pass.

## How to read this report

This report is a synthesis of the estate's own records, each dated and measured. It is not a
re-measurement. To get a fresher picture, regenerate the source of truth rather than trusting
this page: `scripts/estate-snapshot` regenerates `STATE.md`. Every number above traces to a
line in one of the cited files.
