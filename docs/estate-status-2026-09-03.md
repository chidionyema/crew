# Estate status — 2026-09-03

Written to answer crew#59: "get up to speed with everything that has happened on this estate in
the last week or so, what the current agent sessions are working on." Every number below came
from a command run this session or from the cited audit; nothing is remembered.

## Platform

- mumchimp.com store is LIVE and selling (store-api deployed 08-20, store-web 08-21). Engine runs
  on the laptop via launchd from prospector-live.
- Fly account was PAST_DUE on 08-23 (engine suspended, 14 merged PRs unreachable). Status now:
  see the unshipped-7day audit (docs/audits/2026-09-03-unshipped-7day.md) for the current state of
  the shipping pipeline.
- The Architect's Telegram gateway and several launchd jobs (consultd, boardserve, kimi-bridge,
  deepseek-bridge, aiden.watch) were exiting non-zero on 08-23. Comms restoration is a tracked
  lane.

## Money

- 14-day total was $10,189.55 on 08-23; $727.83/day mean vs a $120 cap; week-over-week +41.8%.
- Today (08-23): Opus-5 was 99% of $602.62; cache transport 82% of all cost; interactive sessions
  62-69% of spend on peak days.
- The brake (estate_cost_sentinel) can only pause prospector-daemon = 0.1-2% of spend. halt_usd is
  0 (disarmed). The brake does not reach the thing that spends. Spend control is lane 1 on #26.

## The scatter, measured

- ~470 commits/7d across guards(250)/hermes-v2(86)/estate(69)/crew(~40)/maestro(26) + ~1,500 in
  prospector, against 3 open PRs, all drafts (08-23).
- The 7-day audit (2026-09-03) found: 42 idp branches never PR'ed, ~30 crew never-PR'ed branches
  (specs and rulings), 14 hermes-v2 otto checkpoint branches, ~120 local idp branches ahead of or
  absent from origin, 20 worktrees with uncommitted tracked edits, and `~/dev/code` itself a git
  repo with NO remote (LAW 24 violation as a standing state).
- Board: 17 real active issues on 08-23; 8 captured-prompt noise issues (6 closed as duplicates).

## What the current agent sessions are working on

Lane allocation is written in docs/LANES.md (crew#40). The lanes that were open on 08-23 were
#26 (estate spend), #32 (canonical root migration), #33 (Rust licence). Lane 2 (Fly) was closed by
R1 (no Fly). The 7-day audit (2026-09-03) queues three one-word founder decisions: REDIS (rebase
feat/litellm-redis and PR it, or say TWO-REPLICAS), SPECS (land the crew spec/ruling branches to
main), TRIAGE (the 42 idp never-PR'ed branches get a one-line verdict each).

## Three founder decisions, stated once (08-23)

1. **Pay the Fly invoice** — unblocks #35 #679 #673 #661, 14 PRs, and makes #38's exit drill
   testable.
2. **claude_cli container decision (A OAuth-in-container / B metered API / C drop)** — unblocks
   #33 Rust migration.
3. **iCloud: delete or archive the 67 container-only dirs** — unblocks the rescue session
   concluding.

## Streamline plan (no founder hands needed, 08-23)

- Sessions conclude per the P0 board directive; each leaves a LAW 25 checkpoint.
- Landing pass on prospector: every worktree/stash/draft-PR gets a verdict — land, PR, or delete.
- Orphan sweep: any dirty file no session claims gets committed on a named branch, never deleted.
- Lanes collapse from 8 to 4 for the next cycle: (1) Fly/deploy recovery, (2) spend control,
  (3) comms restoration, (4) prospector landing. Allocation goes on #40.
- Spend mechanics that touch the real driver: fewer concurrent interactive sessions, recon routed
  to haiku, daemon halt armed. Proposal with numbers goes on #26.

## The three leaks, named once (2026-09-03 audit)

1. **Mac-only work** (never pushed): dies with the laptop. Redis rebuild, founder-record docs,
   ~10 real local-only branches, 20 dirty worktrees.
2. **Pushed, never PR'ed** (~90 branches across repos): survives the laptop, invisible to the ship
   pipeline.
3. **Open PRs nobody is driving** (claude-estate since 08-24, hermes-config since 08-25,
   estate-secrets since 08-24): offered, then abandoned mid-door.

Standing rules already cover 1 and 2 (LAW 24, LAW 16 leave-a-path-back, R57 one push wave); the
audit shows they are not being closed out at session end. The enforcement gap — a sweep that
grades session-end state — is a decision for the founder.
