# Estate snapshot

**Generated 2026-08-27 04:17 UTC** by `scripts/estate-snapshot`. Every row is a command and its
output. A row that could not be measured says NOT RUN, never PASS.

Read this before asking anyone anything. Regenerate it rather than trusting it:
`scripts/estate-snapshot`.

| what | state | measured by |
|---|---|---|
| The Architect | GREEN | `bin/verify`: PASS  dispatch claims agent-go and never icebox 3 passed in 5.37s |
| &nbsp;&nbsp;failing | | FAIL  README describes what ships        .github/workflows/build-agent-image.yml is in the repo, and the README never says why |
| &nbsp;&nbsp;failing | | FAIL  the URL card is pinned and current 4 links, pinned msg 14008 |
| maestro | GREEN | last cycle 6 min ago (`INTENT-20260827-040532-0d20f3e7.json`) |
| &nbsp;&nbsp;skills | GREEN | 3 skill(s) it can heal with |
| Fly | NOT RUN | `flyctl apps list` failed: No apps found |
| estate spend | RED | $866/day 7-day mean against a $120 cap (`spend_daily`, warehouse.db) |
| delivery | RED | 24 commits on no remote (oldest 2.7d), 45 dirty files, 6 live repos (`git log --branches --not --remotes`) |
| &nbsp;&nbsp;shipped | 688 merged | non-bot PRs merged across the estate in 7d, ~$9 of estate spend per shipped change (`gh search prs`) |
| &nbsp;&nbsp;stranded | scripts | 21 commits no remote holds, oldest 2.7d, 16 dirty |
| &nbsp;&nbsp;stranded | .idp-state | 2 commits no remote holds, oldest 0.4d, 0 dirty |
| &nbsp;&nbsp;stranded | .crew-state | 1 commits no remote holds, oldest 0.3d, 1 dirty |
| founder cost | GREEN | 3127 msgs / 5% complaints this week against 3683 / 9% last (`attention_daily`) |
| collectors | NOT RUN | warehouse last rebuilt 4h ago; `com.founder.sciencecollect` is not running |
| data map | RED | 8199 producers, 77111 measurables, 7862 in gaps with a ticket, 6 unexplained, blind: cluster_live (`science/datamap.py --check`) |
| &nbsp;&nbsp;violation | | 6 producer(s) UNEXPLAINED (first: mac/ledger/~/.claude/scripts/.wt-crew325/state/drills.jsonl) |
| crew P1 | 25 open | the fires nobody has put out |
| &nbsp;&nbsp;#407 SECURITY INCIDENT: a credential was sent over Telegram (crew#400 login, session a0d64ea4, 2026-08-27); tr | | |
| &nbsp;&nbsp;#396 LAW: KINI checkpoints run as durable workflows on the estate's Temporal; 'Finish KINI' then close the lap | | |
| &nbsp;&nbsp;#395 LAW: a founder directive rewrites every live session's goal by itself; no session reads a transcript and  | | |
| &nbsp;&nbsp;#345 Platform-level: OCI session expires every ~1-2h, blocking all live verification — durable identity, not r | | |
| &nbsp;&nbsp;#340 Langfuse (langfuse-web) healthcheck failing 2+ days, unnoticed — same silent-failure class as crew#308 | | |
| &nbsp;&nbsp;#326 Incident: ~/.estate/guards/hooks/_router overwritten with a refuse-all stub at 17:06Z; every commit and p | | |
| &nbsp;&nbsp;#325 idp architectural review 2026-08-26: cluster layer KEEP, README/STANDARDS/tests/sovereign REWORK | | |
| &nbsp;&nbsp;#320 LAW: every WIRED_NEVER / NEVER_EMITTED row in datamap.py becomes a tracked ticket, permanently -- 17 + 8  | | |
| &nbsp;&nbsp;#319 RED ALERT: session transcripts (76k files, 6.5GB, WIRED_NEVER) are the estate's largest unread asset -- d | | |
| &nbsp;&nbsp;#318 P0: MacBook load average 555/530/336 — machine is in genuine distress, not "feels slow" | | |
| &nbsp;&nbsp;#313 LiteLLM proxy down: colima not running, blocking CP1 photo intake and every LLM call routed through it | | |
| &nbsp;&nbsp;#311 Class: the estate-operators policy lives outside tofu, so every new statement needs a founder browser sig | | |
| &nbsp;&nbsp;#301 oke-rebuild --check red: tofu-plan and flux rows broken (drill 2026-08-26T10:42Z) | | |
| &nbsp;&nbsp;#290 Continuity: reach Otto/the estate through any single loss — phone, laptop, or one cloud provider | | |
| &nbsp;&nbsp;#283 Science & ML: close the 3 measured gaps before adding capability (readerless metrics, unrun experiments,  | | |
| &nbsp;&nbsp;#279 Estate MCP needs a write-side ledger tool: architecture changes reach agents hours late | | |
| &nbsp;&nbsp;#248 Prospector scheduler runs nowhere: no re-verification since 2026-08-16 | | |
| &nbsp;&nbsp;#116 Spec: the Fly-exit rehearsal drill passes, repeatably, for £0 | | |
| &nbsp;&nbsp;#114 Fully operational today — the day board, 2026-08-24 | | |
| &nbsp;&nbsp;#85 Machine overload: load 255 on 12 cores with founder at keyboard — no cross-session load governor | | |
| &nbsp;&nbsp;#74 Build the real data pipeline: DuckDB + DuckLake + fastjsonschema, and grade each dependency on use, distri | | |
| &nbsp;&nbsp;#71 1,064 field paths, 0 declared: the warehouse has no schema, no owner, no retention and no sensitivity on a | | |
| &nbsp;&nbsp;#32 prospector is still in ~/Documents/code — the move to ~/dev/code has never been applied | | |
| &nbsp;&nbsp;#26 Estate spend is $866/day against a $120 cap, and one owner is 69% of it | | |
| &nbsp;&nbsp;#13 Retire the Hermes estate — unconditional, Hermes is discontinued | | |
| docker context | RED | `docker context show` -> default; sessions' docker commands are landing off the standard runtime |
| second container runtime | GREEN | `pgrep -f 'Docker.app/Contents/MacOS' | wc -l` -> 0 |
| colima dockerd | GREEN | socket answered containers/json |
