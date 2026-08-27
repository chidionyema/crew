# Leaving the MacBook: what runs where, and the gaps

Measured 2026-08-27 15:45–16:00Z by session 78caaa17 on the founder Mac. Every number below is from a command run this turn; the command is named beside it. Founder asked for this as one file to return to. Tracked on crew#458 (VM), crew#247 (no Mac-bound layer), crew#300 (recover on any machine).

## The one-sentence answer

The cluster (OKE, `idp/clusters/oke`) already holds the platform — Backstage, observability, identity, secret store, LLM router, Temporal, SPIRE, Healthchecks, chaos, edge, alerts — but **the Mac still runs 20 Dagster schedules, 10 launchd daemons, a 5 GiB colima VM with 14 containers (three of them second copies of a cluster row), and the hermes gateway**, and nobody can verify the cluster from a runner for longer than an OCI session lasts (crew#345). The laptop is still the scheduler, the model router for local sessions, and the only place the science warehouse is written.

## What is in the cloud today

| Layer | On OKE | Evidence |
|---|---|---|
| GitOps | Flux (`flux-system`, gotk-sync) | `idp/clusters/oke/flux-system/` |
| Portal + catalog | Backstage | `clusters/oke/platform.yaml` Kustomization `backstage` |
| Observability | OTel collector → SigNoz | Kustomization `observability` (HelmRelease ×2); signoz-0 CrashLoop today (crew#495) |
| Identity / secrets | external-secrets, `secret-store`, SPIRE | Kustomizations `identity`, `spire`, `secrets.yaml` |
| Model router | LiteLLM at `llm.<zone>` | Kustomization `llm` |
| Durable workflows | Temporal | Kustomization `temporal` |
| Job monitoring | Healthchecks | Kustomization `healthchecks` |
| Chaos | chaos-mesh + `chaos-pod-kill` drill | Kustomization `chaos` |
| Front door | Gateway API + external-dns (`edge.yaml`) | `clusters/oke/edge.yaml` |
| Store | prospector store on OKE at mumchimp.com | memory `store-runs-on-oke-mumchimp`; Fly has zero apps |
| Provisioning | Terraform in `platform/oci` (oke, iam, langfuse, healthchecks) run from Actions, not the Mac | crew#247 measurement: 7 of 8 jobs on ubuntu-latest |
| Code escape | git bundles of 24 repos to object storage, restore verified | `estate-bundlepush.out.log` 05:50Z: `BUNDLE PUSH GREEN repos=24 restore=git clone <bundle>` |
| Cluster receipt | `oke-check` hourly | 14:27Z run: cluster-state, kini-state, telemetry-coverage **red**; check, free-tier, chaos-drill, founder-links green |

## What still runs only on the Mac

| Workload | Count | Evidence | Cloud home / ticket |
|---|---|---|---|
| Dagster schedules (science-collect, idp reconcile, friction relay, cost sentinel, downshift, drills, key escrow, law writer, bundle push, …) | 20 RUNNING | Dagster GraphQL `localhost:3210` this turn | Argo Workflows / CronJobs on OKE — STANDARDS row "Scheduling: partially live"; crew#247 step 1 |
| launchd daemons: `ai.estate.{cockpit,consultd,deepseek-bridge,kimi-bridge,scheduler,session-timeout,sovereign-worker,temporal}`, `com.founder.{boardserve,estate-awake}` | 10 loaded | `launchctl list` | none named; `ai.estate.temporal` duplicates the OKE Temporal row |
| colima VM: x86_64, 2 CPU, **5 GiB of 16**, up 20h15m | 14 containers | `colima list`; crew#458 body | crew#458: langfuse-web, litellm-proxy, otel-fallback are second copies of cluster rows; mcp-estate/github/agentgateway, prospector-edge, store-api have no cluster row yet |
| Science warehouse + ledgers (`science/warehouse.db`, 40 sources) | written only here | `com.founder.sciencecollect` skipped 4 of last 5 ticks on load ceiling (crew#90) | none; the data lane has no cluster writer |
| Claude Code sessions themselves (the agents) and their guards (`~/.claude/scripts`) | 4 live | ListAgents | crew#396: KINI as Temporal workflows, "close the laptop" |
| Hermes stack | see section below | | |
| Dead weight: 40 `.bak`/`.RETIRED`/`.DISABLED` plists incl. 4 GitHub Actions runners | 0 left | archived to `~/.claude/state/archive/launchagents-dead-2026-08-27.tgz` (40 entries, 12 KB) and removed 16:10Z — CP7 | crew#478 (24 launchd jobs last exited non-zero) still open |

## Hermes stack

Recon 2026-08-27 16:05Z (read-only over `hermes-v2`, `idp/platform/hermes-agent`, `~/Library/LaunchAgents`).

| Component | Mac | OKE | Verdict |
|---|---|---|---|
| Gateway ("The Architect", Telegram) | `launchctl list` → `ai.architect.gateway` live, PID 60109; plist runs `hermes-v2/.venv/bin/python -m hermes_cli.main gateway run` from `~/dev/code/hermes-v2`; catalog `port-9900` bound to 127.0.0.1 on the Mac | `idp/platform/hermes-agent/gateway.yaml` Deployment `hermes-agent-gateway` (replicas 1, probes on 9900, secrets via ExternalSecret) wired by `clusters/oke/edge.yaml:151-159`; header says "Mac is primary, Oracle is active standby … NOT wired into any Ingress/Certificate/DNS" | **Mac-only in practice.** Standby built, never routed; gated on crew#227 CP3 |
| watch / work lanes (`cron/watch.jobs`, `cron/work.jobs`) | ticked inside the Mac process; `cron/work.jobs` header: "An asleep laptop misses ticks" | none — no CronJob or Deployment under `idp/platform` or `idp/clusters` | **Mac-only by design** |
| Agent runtime image | buildable locally (`.venv`, `hermes-agent/docker-compose.yml`) | `Dockerfile` → `.github/workflows/build-agent-image.yml` → `ghcr.io/chidionyema/hermes-agent` (arm64 for the Ampere pool); `gateway.yaml:90` pulls `set-by-an-overlay` | **Cloud home exists**; the one component with a real deploy path |
| `bin/verify-consult` | README:290 "still runs off the founder's laptop" (rows that cannot apply SKIP) | — | Mac-only |
| Prospector store (`store-web`, `store-api`) | — | `estate.yaml:14-24`: on OKE behind mumchimp.com / api.mumchimp.com, measured 200 on 2026-08-26 | Cloud — but this is the store, not hermes |
| Fly leftovers | `deploy/fly/{fly.toml,finish-cutover.sh,entrypoint.sh,age-drill*.sh}`, `deploy/secrets/claude-credentials.json.age`, `CUTOVER.md` last line still `./deploy/fly/finish-cutover.sh` | n/a | **Drift against R1.** `bin/check-platform.py estate.yaml` is clean (exit 0) but the runbook on disk still points at Fly |
| `estate.yaml` | gitignored (`.gitignore:50`), generated by `./install`; on disk modified 27 Aug 13:18 | — | local-only config; drifts from `estate.example.yaml` (the 2026-08-26 incident) |
| Old label `ai.hermes.gateway` | three `.bak` plists beside the live `ai.architect.gateway.plist` — archived to `~/.claude/state/archive/launchagents-dead-2026-08-27.tgz` this turn (CP7) | — | guarded by `tests/test_incident_crew284_one_gateway_label.py` |

**What moves (crew#516 CP4):** route traffic to `hermes-agent-gateway` (Ingress + Certificate + DNS in `edge.yaml`, the overlay tag on the image), turn `cron/watch.jobs` and `cron/work.jobs` into CronJobs in `idp/platform/hermes-agent`, then unload `ai.architect.gateway`. The Telegram token can be held by exactly one of the two (crew#284), so the cutover is a swap, not a period of overlap. **Delete first:** `deploy/fly/` and the `CUTOVER.md` Fly line (R1).

## Platform portability

| Check | Result today | Evidence |
|---|---|---|
| Cloud-agnostic gate (R36: provider names only in `platform/oci`, secret-store, clusters) | **1 line leaks**: `platform/access/backend_override.tf:6` names an Oracle S3-compat endpoint | `bin/cloud-agnostic-gate` this turn |
| Provider mentions outside allowed dirs (`rg -il 'oci\|oracle'` in bin, .github, platform) | 58 files | same run; most are login/bootstrap scripts, needs a sweep against the gate's allow-list |
| Code portability | 24 repos bundled offsite, restore verified | bundle push 05:50Z |
| Data portability | DuckDB/Parquet standard, `science/export_drill.py` exists, hand-run only | STANDARDS row "Data"; showcase Capabilities table |
| Images | multi-arch gated in idp (R24) | STANDARDS row "Container images" |
| Recover on a clean machine (any OS) | **never run** | crew#300: all 4 boxes open |
| Verify the cluster without the founder logging in | **blocked**: OCI session expires ~1-2h; `kubectl` from this Mac failed this turn | crew#345: all 3 boxes open |
| Deploy from the phone | `workflow_dispatch` on rebuild/apply exists; Telegram command path not built | crew#247 |
| Backups | restic "to adopt", not live | STANDARDS row "Backups" |

## The gaps, in the order to close them (tracked as crew#516 CP1–CP9)

1. **Durable cluster identity (crew#345).** Until a runner can reach OKE for 24h without a founder login, nothing else can be proved off the Mac. Scoped service principal in Terraform.
2. **Scheduler off the Mac (crew#247 step 1).** 20 Dagster schedules → Argo Workflows/CronJobs reconciled by Flux; retire `ai.estate.scheduler`, `idp-install-launchd`, `scheduler-migrate`.
3. **Kill the VM (crew#458).** Repoint `~/.claude.json` MCP entries to the cluster; give mcp-estate/mcp-github/agentgateway, prospector-edge and store-api a cluster row or delete them; `colima stop && colima delete`. Recovers 5 GiB and 2 cores today.
4. **Hermes gateway to the cluster** (`idp/platform/hermes-agent` exists; see the section above for what is still local).
5. **Science lane writer on the cluster.** The warehouse is written by a laptop job that skips under load; move `science-collect` with the scheduler, ledgers to object storage.
6. **Recovery drill (crew#300)** on a clean runner: clone from bundles, boot, run `oke-check`. Never run.
7. **Portability sweep**: fix `backend_override.tf:6`, grade the 58 provider-named files against the allow-list, make the gate a required check.
8. ~~Delete the 40 dead plists~~ done 16:10Z (CP7); crew#478 still open.

## Where to check next time

- `bin/cloud-agnostic-gate` (idp) — portability
- `gh run list -R chidionyema/idp --workflow oke-check.yml` — cluster receipt
- `launchctl list | grep -E 'ai.estate|com.founder'` and `colima list` — what the Mac still carries
- Dagster `localhost:3210` schedules — what the Mac still schedules
- `~/.claude/state/logs/estate-bundlepush.out.log` — code escape
