# Estate snapshot

**Generated 2026-08-28 05:03 UTC** by `scripts/estate-snapshot`. Every row is a command and its
output. A row that could not be measured says NOT RUN, never PASS.

Read this before asking anyone anything. Regenerate it rather than trusting it:
`scripts/estate-snapshot`.

| what | state | measured by |
|---|---|---|
| The Architect | GREEN | `bin/verify`: PASS  dispatch claims agent-go and never icebox 3 passed in 1.60s |
| &nbsp;&nbsp;failing | | FAIL  agent is the pinned commit         36510d1f6c (want 6c5b805196) |
| &nbsp;&nbsp;failing | | FAIL  the URL card is pinned and current 44 links, pinned msg 14008 |
| &nbsp;&nbsp;failing | | FAIL  launchd runs the plist on disk     no plist at /Users/chidionyema/Library/LaunchAgents/ai.architect.gateway.plist |
| &nbsp;&nbsp;failing | | FAIL  one launchd label runs the gateway no gateway label is loaded |
| maestro | GREEN | last cycle 6 min ago (`INTENT-20260828-045135-0d20f3e7.json`) |
| &nbsp;&nbsp;skills | GREEN | 3 skill(s) it can heal with |
| Fly | NOT RUN | `flyctl apps list` failed: No apps found |
| estate spend | NOT RUN | `spend_daily` view did not answer |
| revenue | NOT RUN | last measurement 2026-08-27T01:23:38Z is 28h old (bar 24h) |
| ci runs | GREEN | 49 workflows, 2479 runs/24h, 1876/2469 passed, slowest median 819.0s (haworks-platform/codeql.yml), measured 2026-08-27T03:28:24Z (`outcomes.py ci`) |
| delivery | RED | 1471 commits on no remote (oldest 5.8d), 39 dirty files, 7 live repos (`git log --branches --not --remotes`) |
| &nbsp;&nbsp;shipped | >=1000 merged | non-bot PRs merged across the estate in 7d (`gh search prs`) |
| &nbsp;&nbsp;stranded | .idp-state | 688 commits no remote holds, oldest 3.4d, 1 dirty |
| &nbsp;&nbsp;stranded | .crew-state | 380 commits no remote holds, oldest 5.8d, 1 dirty |
| &nbsp;&nbsp;stranded | scripts | 346 commits no remote holds, oldest 4.6d, 10 dirty |
| founder cost | NOT RUN | `attention_daily` did not answer |
| collectors | NOT RUN | `ingest_log` did not answer |
| data map | NOT RUN | `science/datamap.py --check --json` did not answer |
| science plane: warehouse | RED | DuckDB+dbt, 0 dbt model(s), rebuilt 83h ago (`science/warehouse.db`) |
| science plane: scheduler | GREEN | Dagster, 10 process(es) (`pgrep -f dagster`; `idp/scheduler/`) |
| science plane: experiment tracker | ABSENT | no MLflow anywhere; R34 names it as the one tracker (`command -v mlflow`) |
| science plane: forecast ledger | RED | 15 forecast(s), 0 scored against reality (`science/predictions.jsonl`); Brier needs both |
| science plane: declared stores | 40 | `science/sources.json` |
| research | GREEN | 25 entries in 7d, 25 total, 25 with a decision fed, last 2026-08-27 (`RESEARCH-LEDGER.jsonl`) |
| hooks | GREEN | 108774 runs in 24h, 702 refused (most: rule-guard.py 204), slowest 47605 ms (`hook-outcomes.jsonl`) |
| GitHub Actions | GREEN operational | githubstatus.com; a red row means pending CI is theirs, not yours |
| crew P1 | 24 open | the fires nobody has put out |
| &nbsp;&nbsp;#539 Nothing watched the estate: langfuse 503 for ≥5 min found by a PR link checker; no PrometheusRule, no HTT | | |
| &nbsp;&nbsp;#529 Independent certification: The Architect's hermes-v2 gateway self-audit (founder ask, 2026-08-27) | | |
| &nbsp;&nbsp;#527 The board applies science: lanes, measured velocity, finish-first rank, and the board assigns the ticket | | |
| &nbsp;&nbsp;#526 Open count never goes down: guard-filed issues carry a Closes-when command and a nightly closer | | |
| &nbsp;&nbsp;#516 Mac exit: plan and execute the move of every estate workload off the founder MacBook (founder 2026-08-27) | | |
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
| laptop VM (R26) | GREEN | `no-local-vm-guard.sh` -> no colima/lima process, no VM LaunchAgent |
| OKE nodes | NOT RUN | `kubectl get nodes` rc=1 'ERROR: The config file at ~/.oci/config is invalid:\n\n+Config Errors+---------+--' |
| OKE flux | NOT RUN | `kubectl get kustomizations -A` rc=1 'ERROR: The config file at ~/.oci/config is invalid:\n\n+Config Errors+---------+--' |
| elite grade | 7 GAP, 9 BLIND | 304 ELITE of 320 entities; page docs/SHOWCASE.md in idp, gaps first (crew#474) |
