# Estate snapshot

**Generated 2026-10-18 01:51 UTC** by `scripts/estate-snapshot`. Every row is a command and its
output. A row that could not be measured says NOT RUN, never PASS.

Read this before asking anyone anything. Regenerate it rather than trusting it:
`scripts/estate-snapshot`.

| what | state | measured by |
|---|---|---|
| The Architect | NOT RUN | `/Users/roseonyema/dev/code/hermes-v2` does not exist |
| estate board | RED | cache not rebuilt from crew#102: TypeError: unsupported operand type(s) for |: 'type' and 'NoneType' |
| maestro | NOT RUN | no INTENT files, so nothing has sensed |
| Fly | NOT RUN | `flyctl apps list` failed: /bin/sh: flyctl: command not found |
| estate spend | NOT RUN | `spend_daily` view did not answer |
| revenue | NOT RUN | last measurement 2026-08-28T12:37:36Z is 1213h old (bar 24h) |
| ci runs | NOT RUN | last measurement 2026-08-27T03:28:24Z is 1246h old (bar 30h) |
| delivery | GREEN | 0 commits on no remote (oldest 0.0d), 10 dirty files, 1 live repos (`git log --branches --not --remotes`) |
| &nbsp;&nbsp;shipped | 337 merged | non-bot PRs merged across the estate in 7d (`gh search prs`) |
| founder cost | NOT RUN | `attention_daily` did not answer |
| live checkout | RED | on `state/snapshot-20261018`, 0 commit(s) behind origin/main; the scheduled jobs run that. Path back: `git -C /Users/roseonyema/Documents/code/crew-worktrees/state switch main` |
| collectors | NOT RUN | `ingest_log` did not answer |
| data map | RED | 89 producers, 649 measurables, 0 in gaps with a ticket, 0 unexplained, blind: mac, cluster, cluster_live, endpoint (`science/datamap.py --check`) |
| &nbsp;&nbsp;violation | | domain mac BLIND and not allowed: ImportError: cannot import name 'UTC' from 'datetime' (/Library/Developer/Co |
| &nbsp;&nbsp;violation | | domain cluster BLIND and not allowed: FileNotFoundError: no idp checkout at /Users/roseonyema/dev/code/idp |
| &nbsp;&nbsp;violation | | domain cluster_live BLIND and not allowed: RuntimeError: no receipt body in the last 8 oke-check.yml run(s): 3 |
| science plane: warehouse | GREEN | DuckDB+dbt, 0 dbt model(s), rebuilt 0h ago (`science/warehouse.db`) |
| science plane: scheduler | RED | Dagster, 0 process(es) (`pgrep -f dagster`; `idp/scheduler/`) |
| science plane: experiment tracker | ABSENT | no MLflow anywhere; R34 names it as the one tracker (`command -v mlflow`) |
| science plane: forecast ledger | RED | 15 forecast(s), 0 scored against reality (`science/predictions.jsonl`); Brier needs both |
| science plane: declared stores | 44 | `science/sources.json` |
| research | NOT RUN | AttributeError: module 'datetime' has no attribute 'UTC' |
| hooks | NOT RUN | AttributeError: module 'datetime' has no attribute 'UTC' |
| GitHub Actions | GREEN operational | githubstatus.com; a red row means pending CI is theirs, not yours |
| OCI verification identity | RED 0 scheduled runs in 24h | idp verify-drill.yml scheduled runs, last 24h, on the estate-ci machine identity (crew#345); the cron never fired |
| crew P1 | 30 open | the fires nobody has put out |
| &nbsp;&nbsp;#1008 BUG: Scheduled jobs dead since 2026-09-23: Dagster started by launchd | | |
| &nbsp;&nbsp;#1007 BUG: Otto: metrics push and 5 provider keys broken; watch jobs skip on model drift | | |
| &nbsp;&nbsp;#1006 BUG: Otto: terminal sandbox does not exist; terminal runs beside secrets | | |
| &nbsp;&nbsp;#1005 BUG: Otto: memory-store job fails every run; long-term memory not written | | |
| &nbsp;&nbsp;#1004 BUG: Otto: paid OpenRouter fallback enabled with no approval | | |
| &nbsp;&nbsp;#1003 BUG: Otto: two long-lived GitHub App write tokens and mac-run act without approval | | |
| &nbsp;&nbsp;#1002 BUG: Otto: no evidence it answered, used a tool or asked approval in 72h | | |
| &nbsp;&nbsp;#1001 BUG: ci-success fails on cancelled dependencies | | |
| &nbsp;&nbsp;#1000 BUG: X-Idp-Signed trailer checked for presence only | | |
| &nbsp;&nbsp;#999 BUG: Main is red and silent: security-scan 425 gitleaks hits, 1 critical npm advisory, 2 BDD failures | | |
| &nbsp;&nbsp;#998 BUG: CI/CD: two designed rulesets never installed; no drift detection | | |
| &nbsp;&nbsp;#997 BUG: CI/CD: bot authors skip fast-gate yet it reports green | | |
| &nbsp;&nbsp;#996 BUG: CI/CD: main requires zero review; CODEOWNERS not enforced | | |
| &nbsp;&nbsp;#995 BUG: CI/CD: gate files unguarded, so any PR can rewrite workflows, rulesets and founder.pub | | |
| &nbsp;&nbsp;#994 BUG: FleetView writes are attributed to 'reactor', never to the signed-in user | | |
| &nbsp;&nbsp;#993 BUG: FleetView director crash-loops since 2026-09-27; the movie has no input | | |
| &nbsp;&nbsp;#992 BUG: FleetView Stop/Kill/Approve/Deny buttons can never work | | |
| &nbsp;&nbsp;#859 Store CP4 — checkout ends at a running capability, not at a pull request to review (crew#847) | | |
| &nbsp;&nbsp;#858 Store CP3 — connections are shown at the moment of choosing, not discovered later (crew#847) | | |
| &nbsp;&nbsp;#857 Store CP1+CP2 — the catalogue prices itself, and the form stops being hand-copied (crew#847) | | |
| &nbsp;&nbsp;#856 CP1 — the workforce runs as a Flow with state that survives the pod (crew#850) | | |
| &nbsp;&nbsp;#855 CP6 — the company becomes departments the workforce staffs, as data (crew#850) | | |
| &nbsp;&nbsp;#854 CP5 — CrewAI 1.9.3 to 1.15.20, with native planning, reasoning and evaluation (crew#850) | | |
| &nbsp;&nbsp;#853 CP4 — one memory, scoped per department, on the estate's own layer (crew#850) | | |
| &nbsp;&nbsp;#852 CP3 — the authority boundary becomes an enforced control, not an absent tool (crew#850) | | |
| &nbsp;&nbsp;#851 CP2 — the estate answers for itself: MCP tools replace the hand-written client (crew#850) | | |
| &nbsp;&nbsp;#795 Squad model: Claude plans and manages, cheap models execute, Kimi and Gemini consult (R69) | | |
| &nbsp;&nbsp;#718 The founder cannot open five of the eight monitoring tools, and nothing human reads any of them | | |
| &nbsp;&nbsp;#668 Incident ledger: every outage is a traced, classed, machine-readable row, the report is the what-not-to-d | | |
| &nbsp;&nbsp;#667 Hazard register to zero: every open row closes by a command, three need one founder word (founder 2026-08 | | |
| portability | RED | ready 11/43 (root-red 2 all named, cascaded 27, pending 3) on a cluster with no OCI (floor 10); the cascade waits 22 on secret-store, 3 on observability, 2 on prospector-platform (idp run 33265235988, 1184.6h ago (bar 194h)) |
| &nbsp;&nbsp;second provider | | provider=github-hosted-azure distro=k3s wall_clock=379s cost=£0.00 (public repository, GitHub-hosted ubuntu-latest) |
| laptop VM (R26) | NOT RUN | guard missing at ~/.claude/scripts/no-local-vm-guard.sh |
| OKE nodes | NOT RUN | `kubectl get nodes` rc=1 'ERROR: The config file at ~/.oci/config is invalid:\n\n+Config Errors--------+----' |
| OKE flux | NOT RUN | `kubectl get kustomizations -A` rc=1 'ERROR: The config file at ~/.oci/config is invalid:\n\n+Config Errors--------+----' |
| elite grade | 25 GAP, 17 BLIND | 380 ELITE of 422 entities; page docs/SHOWCASE.md in idp, gaps first (crew#474) |
| memory drain attribution | no agents= yet (pre-attribution drain) | last `agents=` on a ~/.estate/graph-drain.log run line |
| memory spool ownership | spool empty or unlabeled | agent= stamps in ~/.estate/graph-spool/*.md |
| memory server road | DOWN (URLError) | GET 127.0.0.1:18000/ (any HTTP answer means the road is up; ai.estate.memory-forward) |
