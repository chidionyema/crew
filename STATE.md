# Estate snapshot

**Generated 2026-08-28 17:15 UTC** by `scripts/estate-snapshot`. Every row is a command and its
output. A row that could not be measured says NOT RUN, never PASS.

Read this before asking anyone anything. Regenerate it rather than trusting it:
`scripts/estate-snapshot`.

| what | state | measured by |
|---|---|---|
| The Architect | GREEN | `bin/verify`: PASS  dispatch claims agent-go and never icebox 3 passed in 6.79s |
| &nbsp;&nbsp;failing | | FAIL  generated files match templates     CUTOVER.md Run bin/render to fix, or move your edit into templates/. |
| &nbsp;&nbsp;failing | | FAIL  agent is the pinned commit         36510d1f6c (want 6c5b805196) |
| maestro | GREEN | last cycle 3 min ago (`INTENT-20260828-171251-0d20f3e7.json`) |
| &nbsp;&nbsp;skills | GREEN | 3 skill(s) it can heal with |
| Fly | NOT RUN | `flyctl apps list` failed: No apps found |
| estate spend | RED | $932/day 7-day mean against a $120 cap (`spend_daily`, warehouse.db) |
| revenue | NOT RUN | store not measured at 2026-08-28T12:37:36Z: MEDUSA_ADMIN_TOKEN not set (vault entry medusa-admin) |
| ci runs | NOT RUN | last measurement 2026-08-27T03:28:24Z is 38h old (bar 30h) |
| delivery | RED | 1455 commits on no remote (oldest 6.3d), 49 dirty files, 7 live repos (`git log --branches --not --remotes`) |
| &nbsp;&nbsp;shipped | >=1000 merged | non-bot PRs merged across the estate in 7d (`gh search prs`) |
| &nbsp;&nbsp;stranded | .idp-state | 687 commits no remote holds, oldest 3.9d, 1 dirty |
| &nbsp;&nbsp;stranded | .crew-state | 370 commits no remote holds, oldest 6.3d, 1 dirty |
| &nbsp;&nbsp;stranded | scripts | 349 commits no remote holds, oldest 5.1d, 20 dirty |
| founder cost | GREEN | 2941 msgs / 5% complaints this week against 4230 / 8% last (`attention_daily`) |
| live checkout | RED | on `detached HEAD`, 15 commit(s) behind origin/main; the scheduled jobs run that. Path back: `git -C /Users/chidionyema/dev/code/crew switch main` |
| collectors | NOT RUN | warehouse last rebuilt 5h ago; `com.founder.sciencecollect` is not running |
| data map | RED | 6999 producers, 64080 measurables, 222 in gaps with a ticket, 11 unexplained, blind: cluster_live (`science/datamap.py --check`) |
| &nbsp;&nbsp;violation | | 11 producer(s) UNEXPLAINED (first: mac/ledger/~/.claude/state/crew-science-worktree/science/ships.jsonl) |
| science plane: warehouse | RED | DuckDB+dbt, 1 dbt model(s), rebuilt 5h ago (`science/warehouse.db`) |
| science plane: scheduler | GREEN | Dagster, 7 process(es) (`pgrep -f dagster`; `idp/scheduler/`) |
| science plane: experiment tracker | ABSENT | no MLflow anywhere; R34 names it as the one tracker (`command -v mlflow`) |
| science plane: forecast ledger | RED | 22 forecast(s), 0 scored against reality (`science/predictions.jsonl`); Brier needs both |
| science plane: declared stores | 44 | `science/sources.json` |
| research | GREEN | 30 entries in 7d, 30 total, 30 with a decision fed, last 2026-08-27 (`RESEARCH-LEDGER.jsonl`) |
| hooks | GREEN | 127105 runs in 24h, 668 refused (most: idle-guard.py 176), slowest 104612 ms, 18 overturned by a marker (`hook-outcomes.jsonl`) |
| GitHub Actions | GREEN operational | githubstatus.com; a red row means pending CI is theirs, not yours |
| OCI verification identity | RED 2/2 scheduled runs failed | idp verify-drill.yml scheduled runs, last 24h, on the estate-ci machine identity (crew#345) |
| crew P1 | 25 open | the fires nobody has put out |
| &nbsp;&nbsp;#567 board: crew#527 CP1 is ticked as scheduled and nothing schedules it, so CP5 can never come true | | |
| &nbsp;&nbsp;#566 science: a --domains run skips the census but still grades the ceiling, so a filtered --check always pass | | |
| &nbsp;&nbsp;#565 science: the bootstrap ceiling states its own measurement three different ways (crew#558) | | |
| &nbsp;&nbsp;#529 Independent certification: The Architect's hermes-v2 gateway self-audit (founder ask, 2026-08-27) | | |
| &nbsp;&nbsp;#527 The board applies science: lanes, measured velocity, finish-first rank, and the board assigns the ticket | | |
| &nbsp;&nbsp;#526 Open count never goes down: guard-filed issues carry a Closes-when command and a nightly closer | | |
| &nbsp;&nbsp;#508 Science is every lane at once: one page shows progress across all lanes, every lane feeds the warehouse,  | | |
| &nbsp;&nbsp;#503 Founder dashboard and every surface polished: no broken link, no unstyled UI (high alert, last mile) | | |
| &nbsp;&nbsp;#345 Platform-level: OCI session expires every ~1-2h, blocking all live verification — durable identity, not r | | |
| &nbsp;&nbsp;#340 Langfuse (langfuse-web) healthcheck failing 2+ days, unnoticed — same silent-failure class as crew#308 | | |
| &nbsp;&nbsp;#326 Incident: ~/.estate/guards/hooks/_router overwritten with a refuse-all stub at 17:06Z; every commit and p | | |
| &nbsp;&nbsp;#325 idp architectural review 2026-08-26: cluster layer KEEP, README/STANDARDS/tests/sovereign REWORK | | |
| &nbsp;&nbsp;#318 P0: MacBook load average 555/530/336 — machine is in genuine distress, not "feels slow" | | |
| &nbsp;&nbsp;#313 LiteLLM proxy down: colima not running, blocking CP1 photo intake and every LLM call routed through it | | |
| &nbsp;&nbsp;#311 Class: the estate-operators policy lives outside tofu, so every new statement needs a founder browser sig | | |
| &nbsp;&nbsp;#290 Continuity: reach Otto/the estate through any single loss — phone, laptop, or one cloud provider | | |
| &nbsp;&nbsp;#283 Science & ML: close the 3 measured gaps before adding capability (readerless metrics, unrun experiments,  | | |
| &nbsp;&nbsp;#279 Estate MCP needs a write-side ledger tool: architecture changes reach agents hours late | | |
| &nbsp;&nbsp;#248 Prospector scheduler runs nowhere: no re-verification since 2026-08-16 | | |
| &nbsp;&nbsp;#116 Spec: the Fly-exit rehearsal drill passes, repeatably, for £0 | | |
| &nbsp;&nbsp;#85 Machine overload: load 255 on 12 cores with founder at keyboard — no cross-session load governor | | |
| &nbsp;&nbsp;#71 1,064 field paths, 0 declared: the warehouse has no schema, no owner, no retention and no sensitivity on a | | |
| &nbsp;&nbsp;#32 prospector is still in ~/Documents/code — the move to ~/dev/code has never been applied | | |
| &nbsp;&nbsp;#26 Estate spend is $866/day against a $120 cap, and one owner is 69% of it | | |
| &nbsp;&nbsp;#13 Retire the Hermes estate — unconditional, Hermes is discontinued | | |
| portability | GREEN | ready 2/38 layers on a cluster with no OCI (floor 2) (idp run 33193146025, 0.2h ago (bar 194h)) |
| &nbsp;&nbsp;second provider | | provider=github-hosted-azure distro=k3s wall_clock=658s cost=£0.00 (public repository, GitHub-hosted ubuntu-latest) |
| laptop VM (R26) | GREEN | `no-local-vm-guard.sh` -> no colima/lima process, no VM LaunchAgent |
| OKE nodes | NOT RUN | `kubectl get nodes` rc=1 'ERROR: The config file at ~/.oci/config is invalid:\n\n+Config Errors+---------+--' |
| OKE flux | NOT RUN | `kubectl get kustomizations -A` rc=1 'ERROR: The config file at ~/.oci/config is invalid:\n\n+Config Errors+---------+--' |
| elite grade | 7 GAP, 9 BLIND | 304 ELITE of 320 entities; page docs/SHOWCASE.md in idp, gaps first (crew#474) |
