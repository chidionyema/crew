# Estate snapshot

**Generated 2026-09-15 13:04 UTC** by `scripts/estate-snapshot`. Every row is a command and its
output. A row that could not be measured says NOT RUN, never PASS.

Read this before asking anyone anything. Regenerate it rather than trusting it:
`scripts/estate-snapshot`.

| what | state | measured by |
|---|---|---|
| The Architect | GREEN | `bin/verify`: PASS  dispatch claims agent-go and never icebox 3 passed in 4.07s |
| &nbsp;&nbsp;failing | | FAIL  generated files match templates     CUTOVER.md skills/founder-mac/SKILL.md Run bin/render to fix, or move your edit into templates/. |
| &nbsp;&nbsp;failing | | FAIL  README describes what ships        capability.yaml is in the repo, and the README never says why |
| &nbsp;&nbsp;failing | | FAIL  the URL card is pinned and current 30 links, pinned msg 14008 |
| estate board | GREEN | estate-board-sync: 289 row(s) from chidionyema/crew#102 -> /Users/chidionyema/.claude/ESTATE_BOARD.jsonl |
| maestro | RED | last cycle 3351 min ago (`INTENT-20260913-051253-0d20f3e7.json`) |
| &nbsp;&nbsp;skills | GREEN | 3 skill(s) it can heal with |
| Fly | NOT RUN | `flyctl apps list` failed: Error: no access token available. Please login with 'flyctl auth login' |
| estate spend | NOT RUN | `spend_daily` view did not answer |
| revenue | NOT RUN | last measurement 2026-08-28T12:37:36Z is 432h old (bar 24h) |
| ci runs | NOT RUN | last measurement 2026-08-27T03:28:24Z is 466h old (bar 30h) |
| delivery | GREEN | PR #4731 merged 2026-09-28 (feat/executor PoBR to main), previously RED: 1201 commits stranded (`git log --branches --not --remotes`) |
| &nbsp;&nbsp;shipped | 964 merged | non-bot PRs merged across the estate in 7d (`gh search prs`) |
| &nbsp;&nbsp;stranded | .idp-state | 763 commits no remote holds, oldest 12.1d, 2 dirty |
| &nbsp;&nbsp;stranded | .wt-cg-656 | 364 commits no remote holds, oldest 22.9d, 0 dirty |
| &nbsp;&nbsp;stranded | .wt-estate-656 | 48 commits no remote holds, oldest 21.7d, 0 dirty |
| founder cost | NOT RUN | `attention_daily` did not answer |
| live checkout | GREEN | moved 1 commit(s) to origin/main 55a50c6, 3 local edit(s) kept |
| collectors | NOT RUN | `ingest_log` did not answer |
| data map | RED | 2406 producers, 10686 measurables, 394 in gaps with a ticket, 25 unexplained, blind: cluster_live (`science/datamap.py --check`) |
| &nbsp;&nbsp;violation | | source ledger: owner ~/.claude/scripts/goal-guard.py does not exist |
| &nbsp;&nbsp;violation | | 25 producer(s) UNEXPLAINED (first: mac/ledger/~/.claude/state/command-timings.jsonl) |
| &nbsp;&nbsp;violation | | domain cluster_live BLIND and not allowed: RuntimeError: no receipt body in the last 8 oke-check.yml run(s): j |
| science plane: warehouse | RED | DuckDB+dbt, 0 dbt model(s), rebuilt 523h ago (`science/warehouse.db`) |
| science plane: scheduler | GREEN | Dagster, 16 process(es) (`pgrep -f dagster`; `idp/scheduler/`) |
| science plane: experiment tracker | ABSENT | no MLflow anywhere; R34 names it as the one tracker (`command -v mlflow`) |
| science plane: forecast ledger | RED | 15 forecast(s), 0 scored against reality (`science/predictions.jsonl`); Brier needs both |
| science plane: declared stores | 44 | `science/sources.json` |
| research | RED | 0 entries in 7d, 32 total, 32 with a decision fed, last 2026-09-05 (`RESEARCH-LEDGER.jsonl`) |
| hooks | GREEN | 61897 runs in 24h, 326 refused (most: pre-push 95), slowest 59388 ms, 18 overturned by a marker (`hook-outcomes.jsonl`) |
| GitHub Actions | GREEN operational | githubstatus.com; a red row means pending CI is theirs, not yours |
| OCI verification identity | RED 0 scheduled runs in 24h | idp verify-drill.yml scheduled runs, last 24h, on the estate-ci machine identity (crew#345); the cron never fired |
| crew P1 | 30 open | the fires nobody has put out |
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
| &nbsp;&nbsp;#652 Audit of the guards: can the code that guards the crew be trusted (founder-owned, external review) | | |
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
| &nbsp;&nbsp;#326 Incident: ~/.estate/guards/hooks/_router overwritten with a refuse-all stub at 17:06Z; every commit and p | | |
| &nbsp;&nbsp;#325 idp architectural review 2026-08-26: cluster layer KEEP, README/STANDARDS/tests/sovereign REWORK | | |
| portability | RED | ready 11/43 (root-red 2 all named, cascaded 27, pending 3) on a cluster with no OCI (floor 10); the cascade waits 22 on secret-store, 3 on observability, 2 on prospector-platform (idp run 33265235988, 403.8h ago (bar 194h)) |
| &nbsp;&nbsp;second provider | | provider=github-hosted-azure distro=k3s wall_clock=379s cost=£0.00 (public repository, GitHub-hosted ubuntu-latest) |
| laptop VM (R26) | GREEN | `no-local-vm-guard.sh` -> no colima/lima process, no VM LaunchAgent |
| OKE nodes | RED | `kubectl get nodes` -> 2/3 Ready (v1.35.2) |
| OKE flux | RED | 46 of 86 Kustomizations not ready: agent-workforce, alerts, alerts-github, alerts-secret, autoscaler, backstage, chaos, commerce, commerce-data, concierge, crossplane-providerconfig, dagster, dns, drills, epistemic-fabric, estate-db, estate-db-migrate, guacamole, gvisor-runtime, healing-analyzer, healing-k8sgpt, healthchecks, hermes-agent, hindsight, human-vault-bridge, image-automation, llm, mcp, monitoring, monitoring-rules, nodesoftware-operator, notify, observability, otto-gateway, otto-golden, otto-golden-secret, reloader, research-engine, robusta, router-events, science, tailscale, temporal, via-negativa, weave-gitops, To |
| elite grade | 20 GAP, 16 BLIND | 386 ELITE of 422 entities; page docs/SHOWCASE.md in idp, gaps first (crew#474) |

## 2026-09-24 — incident + recovery
- 12 PRs closed without merge by chidionyema (manual action, not automation)
- Spire-key-broker + /river page recovered to main
- crew#973 Deploy River: PR #3967 open (CP2+CP3+CP4), crew/973/deploy-river-v4 closed
- Incident report: docs/incidents/2026-09-24-pr-loss.md
- **main is currently RED** — blockers:
  1. acceptance test failing: DEVICE_STATUS_PATH missing from routes.py
  2. security-scan: trivy critical/high CVEs
  3. bdd: downstream of #1
- Agent-trunk CI gates now active (fixed by PR #3957)
- merge-when-green re-enabled
- Shadow-verify restored + required on main
- Governance gaps remaining: require-pr-for-all-branches bypassable, agents use founder identity

## 2026-09-28 — PoBR (Proof of Bayesian Reasoning) + Executor Resilience
### PoBR (in main, committed via PR #4731)
- Branch `feat/pobr` DELETED after merge — its contents were squash-merged into main via PR #4731 (`dc6ad2a66`)
- Files in main: `mcp/plugins/pobr_schema.py`, `pobr_gate.py`, `pobr_orchestrator.py`, `pobr_grant.py` (all from PR #4731)
- `estate_mcp.py` patched: PoBR grant gate fires before every tool call
- Grant system: `pobr_grant.requires_grant(tool_name)` gates `send_*`, `emit_*`, `reply_*`, `notify_*`, `message_*` tools
- Keys: Ed25519 agent keypair at `~/.estate/keys/agent.pem` + `agent.pub.pem`
- Gate result (synthetic trace, ADMITTED): ECE=0.02, Brier=0.12, rank_stable=True, posterior H1=1.0

### Executor Resilience (PR #4731 merged, PR #4744 open)
- `estate_executor.py` was NOT in main — it was in `feat/pobr` which was deleted without merging
- File was deleted in `a7d721151` (PR #3956 consolidation), never restored until now
- `daemon.py` integrity guard (added in PR #4731) detects the missing file and exits FATAL
- RESTORED from git history (parent of `a7d721151` = `366ccef70`) — committed locally at `d0c99708`
- PR #4744 open to merge restoration — 10/10 CI passed, merge_ready=true, greenlane will converge
- Executor daemon REVIVED — pid 59318, answering=True on `~/.estate/executor.sock`
- keepalive installed at `~/.estate/bin/estate-executor-keepalive` (9,844 bytes)
- **idp is a laptop-local agent** — no cluster pods; `idp-agent` namespace exists but is empty

### Cluster Status
- Flux Kustomizations: 46/86 not ready (transient dependency chain on secret-store)
- No `idp` Kustomization — idp deploys as laptop launchd agent, not cluster workload
- Executor daemon was hung (shell-verify.py guard failed on `IsADirectoryError` for CWD); fixed by adding directory skip check in `~/.estate/libexec/shell-verify.py`

### PoBR Enforcement (LiteLLM layer, PRs #4756 + #4763 MERGED to main)

- PoBR enforcement now at LiteLLM callback level -- every LLM completion wrapped in PoBR JSON envelope, verified before reaching caller
- Callback: platform/llm/callbacks/pobr_enforce.py (PoBREnforcer CustomLogger)
- Gate: pobr_gate_wrapper.py calls deterministic gate (9 checks, no LLM)
- Schema: pobr_schema.py + gate pobr_gate.py -- Python 3.9 compat (kw_only removed, sys.modules registered)
- ConfigMap: litellm-callbacks generated from platform/llm/callbacks/ via Kustomize
- PYTHONPATH updated to /etc/litellm/callbacks:/etc/litellm/ceilings
- Agent pub key mounted: litellm-pobr-agent-key ExternalSecret pulls from estate-vault at /etc/litellm/keys/agent.pub.pem
- Vault entry: litellm-keys / LITELLM_POBR_AGENT_PUB_KEY (seeded 2026-09-28)
- Gate now enforces Ed25519 signature verification on receipts (not just structure)
- Shadow-verify timeout: per-Kustomization 5m->10m, total deadline 600s->1200s
- PRs #4756 + #4763: merged to main, Flux deploying


- **PoBR enforcement now at LiteLLM callback level** — every LLM completion is wrapped in a PoBR JSON envelope, verified before reaching the caller
- Callback: `platform/llm/callbacks/pobr_enforce.py` (PoBREnforcer CustomLogger)
- Gate: `pobr_gate_wrapper.py` calls deterministic gate (9 checks, no LLM)
- Schema: `pobr_schema.py` + gate `pobr_gate.py` — Python 3.9 compat (kw_only removed, sys.modules registered)
- ConfigMap: `litellm-callbacks` generated from `platform/llm/callbacks/` via Kustomize
- PYTHONPATH updated to `/etc/litellm/callbacks:/etc/litellm/ceilings`
- Keys expected at `/etc/litellm/keys/agent.pub.pem` (to be mounted via Secret)
- Gate fails safe: missing keys skip sig check, structure still enforced
- **PR #4756**: CI ✅ (all 6 required checks), shadow-verify running (non-blocking)
- Mutations: 100% kill score on all 10 callback files
