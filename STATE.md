# Estate snapshot

**Generated 2026-09-01 21:08 UTC** by `scripts/estate-snapshot`. Every row is a command and its
output. A row that could not be measured says NOT RUN, never PASS.

Read this before asking anyone anything. Regenerate it rather than trusting it:
`scripts/estate-snapshot`.

| what | state | measured by |
|---|---|---|
| The Architect | GREEN | `bin/verify`: PASS  dispatch claims agent-go and never icebox 3 passed in 10.17s |
| &nbsp;&nbsp;failing | | FAIL  generated files match templates     CUTOVER.md skills/founder-mac/SKILL.md Run bin/render to fix, or move your edit into templates/. |
| &nbsp;&nbsp;failing | | FAIL  agent is the pinned commit         36510d1f6c (want 6c5b805196) |
| &nbsp;&nbsp;failing | | FAIL  the URL card is pinned and current 30 links, pinned msg 14008 |
| maestro | GREEN | last cycle 2 min ago (`INTENT-20260901-210140-0d20f3e7.json`) |
| &nbsp;&nbsp;skills | GREEN | 3 skill(s) it can heal with |
| Fly | NOT RUN | `flyctl apps list` failed: Error: no access token available. Please login with 'flyctl auth login' |
| estate spend | NOT RUN | `spend_daily` view did not answer |
| revenue | NOT RUN | last measurement 2026-08-28T12:37:36Z is 105h old (bar 24h) |
| ci runs | NOT RUN | last measurement 2026-08-27T03:28:24Z is 138h old (bar 30h) |
| delivery | RED | 1612 commits on no remote (oldest 10.5d), 23 dirty files, 7 live repos (`git log --branches --not --remotes`) |
| &nbsp;&nbsp;shipped | >=1000 merged | non-bot PRs merged across the estate in 7d (`gh search prs`) |
| &nbsp;&nbsp;stranded | .idp-state | 849 commits no remote holds, oldest 8.1d, 1 dirty |
| &nbsp;&nbsp;stranded | .wt-cg-656 | 352 commits no remote holds, oldest 9.2d, 0 dirty |
| &nbsp;&nbsp;stranded | .crew-state | 288 commits no remote holds, oldest 10.5d, 3 dirty |
| founder cost | NOT RUN | `attention_daily` did not answer |
| live checkout | GREEN | moved 1 commit(s) to origin/main 3522b8f, 3 local edit(s) kept |
| collectors | NOT RUN | `ingest_log` did not answer |
| data map | RED | 4198 producers, 35280 measurables, 280 in gaps with a ticket, 17 unexplained, blind: cluster_live (`science/datamap.py --check`) |
| &nbsp;&nbsp;violation | | source ledger: owner ~/.claude/scripts/goal-guard.py does not exist |
| &nbsp;&nbsp;violation | | 17 producer(s) UNEXPLAINED (first: mac/ledger/~/.estate/claims.jsonl) |
| &nbsp;&nbsp;violation | | domain cluster_live BLIND and not allowed: RuntimeError: no receipt body in the last 8 oke-check.yml run(s): j |
| science plane: warehouse | RED | DuckDB+dbt, 0 dbt model(s), rebuilt 195h ago (`science/warehouse.db`) |
| science plane: scheduler | GREEN | Dagster, 11 process(es) (`pgrep -f dagster`; `idp/scheduler/`) |
| science plane: experiment tracker | ABSENT | no MLflow anywhere; R34 names it as the one tracker (`command -v mlflow`) |
| science plane: forecast ledger | RED | 15 forecast(s), 0 scored against reality (`science/predictions.jsonl`); Brier needs both |
| science plane: declared stores | 44 | `science/sources.json` |
| research | GREEN | 3 entries in 7d, 31 total, 31 with a decision fed, last 2026-08-28 (`RESEARCH-LEDGER.jsonl`) |
| hooks | GREEN | 34027 runs in 24h, 307 refused (most: rule-guard.py 103), slowest 52015 ms, 46 overturned by a marker (`hook-outcomes.jsonl`) |
| GitHub Actions | GREEN operational | githubstatus.com; a red row means pending CI is theirs, not yours |
| OCI verification identity | RED 0 scheduled runs in 24h | idp verify-drill.yml scheduled runs, last 24h, on the estate-ci machine identity (crew#345); the cron never fired |
| crew P1 | 30 open | the fires nobody has put out |
| &nbsp;&nbsp;#795 Squad model: Claude plans and manages, cheap models execute, Kimi and Gemini consult (R69) | | |
| &nbsp;&nbsp;#791 INC2 and class: edge Kustomization failed once on a kyverno admission webhook EOF (13:20Z to 13:36Z); the | | |
| &nbsp;&nbsp;#790 INC1: chaos Kustomization fails to reconcile when the chaos-mesh admission webhook returns EOF; 12 times  | | |
| &nbsp;&nbsp;#718 The founder cannot open five of the eight monitoring tools, and nothing human reads any of them | | |
| &nbsp;&nbsp;#668 Incident ledger: every outage is a traced, classed, machine-readable row, the report is the what-not-to-d | | |
| &nbsp;&nbsp;#667 Hazard register to zero: every open row closes by a command, three need one founder word (founder 2026-08 | | |
| &nbsp;&nbsp;#652 Audit of the guards: can the code that guards the crew be trusted (founder-owned, external review) | | |
| &nbsp;&nbsp;#631 Verification Plane: no work item closes without a fresh signed verdict from a prover the agent cannot run | | |
| &nbsp;&nbsp;#626 DEFECTS on the god view: guards, Kubernetes tooling, Dagster, inventory and guard control missing; 'thing | | |
| &nbsp;&nbsp;#620 Strict shell practice estate-wide: shellcheck, shfmt, strict mode, trap, bats; enforced in the hook route | | |
| &nbsp;&nbsp;#609 Product function (stealth): audit, research, bootstrap in five checkpoints | | |
| &nbsp;&nbsp;#607 PR age: 4 machine-hours maximum — green merges itself, red gets a clock, the board sees the rest | | |
| &nbsp;&nbsp;#568 we had an architecture for a future prrof uified provider agnostic nodel stack for all ... | | |
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
| portability | GREEN | ready 11/43 (root-red 2 all named, cascaded 27, pending 3) on a cluster with no OCI (floor 10); the cascade waits 22 on secret-store, 3 on observability, 2 on prospector-platform (idp run 33265235988, 75.9h ago (bar 194h)) |
| &nbsp;&nbsp;second provider | | provider=github-hosted-azure distro=k3s wall_clock=379s cost=£0.00 (public repository, GitHub-hosted ubuntu-latest) |
| runtime | NOT RUN | IndexError: list index out of range |
| elite grade | 7 GAP, 10 BLIND | 323 ELITE of 340 entities; page docs/SHOWCASE.md in idp, gaps first (crew#474) |
