# AUDIT 2 of 2 — is every platform tool configured to its fullest potential

Source: config files in `~/dev/code/idp/platform/<dir>` and `~/dev/code/idp/backstage/app-config.yaml`, read directly (not code). No new vendors, no new spend proposed — config-only wins ranked first per tool.

---

## Backstage
`idp/backstage/app-config.yaml`, `idp/platform/backstage/`

| what we use today | headline features NOT used | cost to enable | first move |
|---|---|---|---|
| Catalog + RBAC read of the live cluster (pods, nodes, Flux HelmReleases/Kustomizations, Alertmanager proxy); TechDocs (`builder: local`, `publisher: local`); Kubernetes plugin; `permission.enabled: true`; GitHub integration (PAT); MCP actions (`mcpActions` block); 4 scaffolder templates (`enable-platform-feature`, `estate-component`, `external-integration`, `founder-actions`); a `/estate-state` proxy endpoint | **Search** — CORRECTED 2026-08-31: search is fully wired and live. The backend registers the search plugin, the Postgres engine and the catalog+techdocs collators (`idp/backstage/packages/backend/src/index.ts` lines 54-62), `app.packages: all` auto-discovers the frontend plugin, the sidebar's Find door points at `/search`, and the login drill grades that page on its own content (run green 2026-08-31T09:03Z). The missing `search:` block is optional tuning only; the original row overstated the gap. **Notifications/Signals plugin** — Backstage ships an in-app notification center; unused, while Flux's Telegram alert is currently `suspend: true` (see Flux row) because it spammed the founder's DM — this is the built-in replacement. **Scorecards / Cost Insights** — no entity health/cost badges on catalog pages. `clientIdMetadataDocuments.enabled: false` (MCP client auth) — off by default, fine. | config-only (Postgres already running; notifications plugin ships in the same backend image) | Wire `search` to the Postgres collator already backing the catalog DB, and turn on the Notifications plugin as the in-app channel for the alerts Flux's Telegram provider is currently barred from sending |

## FluxCD
`idp/platform/image-automation/`, `idp/platform/alerts*/`

| what we use today | headline features NOT used | cost | first move |
|---|---|---|---|
| **Image automation is on and real**: `ImageRepository`/`ImagePolicy` for backstage, prospector, hermes-agent, sovereign-worker, estate-mcp, backed by a GitHub App writer (no PAT) and an image-update-pr workflow with auto-merge. Notification-controller: `reconcile-ledger` Alert → `github-dispatch` provider posts every Kustomization/HelmRelease event to the idp Actions log. HelmRelease remediation (`retries`, `uninstall` strategy on upgrade failure). Kyverno-compliant postRenderers on every chart. | **Telegram alerting is built but suspended** — `idp/platform/alerts/alert.yaml` has `suspend: true` since 2026-08-29 because it fired into the founder's private DM; the fix (point `flux-telegram.channel` at a group chat) was never applied, so Flux's own alerting stays off pending that one-line change. Flux **commit-status back to GitHub PRs** (a second notification provider type) is not configured. No `eventMetadata`/severity-based routing (everything is one Alert per source kind). | config-only | Point `flux-telegram.channel` (the Secret behind `idp/platform/alerts-secret/flux-telegram.yaml`) at an alerts group and flip `suspend: false` — the provider, Alert and event sources are already written |

## LiteLLM router
`idp/platform/llm/config.yaml`, `litellm.yaml`

| what we use today | headline features NOT used | cost | first move |
|---|---|---|---|
| Fallback chains per model, `num_retries: 2`, `allowed_fails: 3`, `cooldown_time: 60`; a global daily budget (`max_budget: 5.0`, `budget_duration: 1d`); OTel + Langfuse success/failure callbacks on every call; virtual keys minted from the Admin UI (`store_model_in_db: true`); SSO through the estate identity domain; one audited pass-through endpoint (MiniMax image, `auth: true`). | **Caching** — no `litellm_settings.cache` block at all; LiteLLM's built-in response/semantic cache (in-memory or Redis) is unused, so repeated identical prompts (e.g. the research worker's embeddings, retried consensus calls) pay full price every time. **Per-key/per-team budgets and RPM/TPM limits** — only the one global `max_budget`; no `max_budget`/`rpm`/`tpm` on individual virtual keys, so one caller can exhaust the whole estate's daily $5. **Spend alerting/webhooks** on budget thresholds — not configured. `background_health_checks: false` — model-down detection is reactive (a failed call), not proactive. | config-only (in-memory cache needs no new infra; per-key budgets are UI/API calls against the already-running proxy) | Turn on `litellm_settings.cache: {type: local}` — zero new infra, directly cuts spend on repeated calls, which is the founder's own cost-mindfulness ask |

## Langfuse
`idp/platform/observability/langfuse-values.yaml`

| what we use today | headline features NOT used | cost | first move |
|---|---|---|---|
| Self-hosted 4.24.0, ingesting every routed LLM call as a trace via the LiteLLM callback (dual-write bridge for the v4 migration), OIDC SSO through the front door, `signUpDisabled: true`, `telemetryEnabled: false`. | **Evaluations** (LLM-as-judge / rule-based scorers running against live traces) — unused; the estate has no automated quality signal on router output. **Prompt Management** (versioned, served-from-Langfuse prompts) — prompts still live in code, not tracked/audited here. **Datasets & experiment tracking** for prompt/model comparisons — unused. **Annotation queues** for human review of traces — unused. **Trace-level alerts** (cost/latency/score thresholds) — unused. | config-only — all of these are app features of the already-deployed Langfuse instance, no new workload | Turn on Prompt Management so router-facing prompts are versioned in Langfuse instead of hardcoded — matches the estate's own "attribute before repair" discipline and costs nothing new to enable |

## SigNoz
`idp/platform/observability/signoz.yaml`, `signoz-retention.yaml`

| what we use today | headline features NOT used | cost | first move |
|---|---|---|---|
| Traces/metrics/logs store, ClickHouse-backed; a daily CronJob that enforces the retention knob (7 days, `signoz-retention.yaml`) against the admin API so the tier promise can't drift from the actual TTL; root user provisioned from vault (no sign-up-page takeover); `telemetry-coverage.yaml` admission gate proving every workload emits. | **Native SigNoz alert rules + notification channels** — none found configured as code (Flux/GitHub have their own alerting; SigNoz's own alerting on trace/metric thresholds, e.g. LiteLLM error rate or pod restarts, is unused). **Saved/custom dashboards as code** — none checked in; whatever exists in the UI isn't version-controlled. **Log pipelines** (parsing, PII redaction, enrichment processors on the OTel collector) — collector config only carries the Kyverno security patches, no processor pipeline. | config-only | Add SigNoz alert rules (via its API, same pattern as `signoz-retention-apply.py`) for LiteLLM error rate and pod-restart count, routed to the same alerts channel the Flux fix above creates |

## MLflow
searched all of `idp/platform` and the whole `idp` repo

| finding |
|---|
| **No MLflow deployment or config exists anywhere in `idp/platform` or the rest of the `idp` repo** — zero HelmRelease, Deployment, or values file. The estate's experiment-adjacent services are `platform/science/` (facts only, no MLflow) and `platform/hindsight/` (a plain Postgres-backed service). This tool cannot be graded on unused features because it is not running — either it isn't actually part of the stack yet, or "science"/"hindsight" were meant to absorb its job and never got MLflow's tracking/registry/model-serving capabilities. Flag for the founder rather than assume a gap that isn't there. |

## Windmill
searched all of `idp/platform` and the whole `idp` repo

| finding |
|---|
| **No Windmill config exists anywhere in the repo** (`grep -ril windmill` across `idp/` returns nothing outside old worktree prose docs). Team memory records a founder ruling that Windmill is the named fallback for Temporal in infra (crew#695), but the config on disk still runs **Temporal** (`idp/platform/temporal/temporal.yaml`, `worker.yaml`) and schedules through **Dagster** (run by launchd via `idp/bin/scheduler-up`, not a cluster manifest), not Windmill. This is a decision-vs-config gap worth surfacing plainly: the ruling was made, nothing was built or migrated. |

## Tailscale
`idp/platform/tailscale/policy.hujson`, `operator.yaml`

| what we use today | headline features NOT used | cost | first move |
|---|---|---|---|
| Deny-by-default ACL: `tag:k8s` → founder-mac:22/5900 only; `group:founder` → founder-mac:* and `autogroup:self`; `tagOwners` locked to admins ([] = nobody can self-tag); OAuth client credentials via ExternalSecret, never pasted; operator deployed with the restricted security profile; `apiServerProxyConfig.mode: "false"` (deliberately off — the operator is for ACL/identity, not k8s API access). No `ssh` ACL section — deliberate, documented (Tailscale SSH doesn't run in the founder's sandboxed Mac client). | **ACL tests** (`tests` key in the policy file) — Tailscale supports declarative access tests co-located in the ACL JSON; the estate has a CI applier (`bin/idp-tailscale-policy`) but nothing that proves the ACL does what it claims before it ships. **Funnel/Serve** — not configured (likely correctly out of scope). **Device posture / approval requirements** — new devices aren't gated on posture checks. | config-only | Add a `tests` block to `policy.hujson` asserting `tag:k8s`↛anything but founder-mac:22/5900 and `group:founder`→founder-mac:* — the same CI step that applies the policy can run it, closing the one real gap (an unreviewed ACL edit reaching the tailnet) |

## External Secrets Operator + OCI Vault
`idp/platform/secret-store/store.yaml`, `idp/platform/secrets/external-secrets.yaml`

| what we use today | headline features NOT used | cost | first move |
|---|---|---|---|
| One `ClusterSecretStore` (`estate-vault`) against OCI Vault via instance principal — no static cloud credential anywhere; ExternalSecrets throughout with `refreshInterval` (mostly `1h`); templated secrets (`engineVersion: v2`); Reloader rolls pods on secret change; liveness/readiness probes explicitly enabled (fixed a chart default gap). | **PushSecret** — ESO's reverse-sync (write a K8s-generated secret, e.g. a minted key, back into OCI Vault) is unused anywhere in the repo; every flow is vault→cluster only. **Generator resources** (`ClusterGenerator`, e.g. Vault dynamic-secret or Fake generators for on-demand minting) — unused. No OCI Vault-native secret **auto-rotation schedule** configured for long-lived secrets (rotation is manual/tofu-driven per the R52 note, not automatic). | config-only for PushSecret wiring; OCI Vault rotation schedules are Terraform-only, no new vendor | Add `PushSecret` for any cluster-minted credential that currently only lives as a Kubernetes Secret (e.g. a rotated key from a Job) so the vault stays the single source of truth in both directions, not just one |

## GitHub Actions
`idp/platform/github/*.json`, `idp/platform/github-app/`

| what we use today | headline features NOT used | cost | first move |
|---|---|---|---|
| Rulesets: `estate-default-branch-protection` (deletion + non-fast-forward blocked), `idp-required-checks` (6 required status checks: offline-gate, bdd, security-scan, spec-gate, operating-model-gate, verify/verdict-fresh), `estate-security-scan` (security-scan + spec-gate); PR approval policy scoped to first-time contributors; GitHub App (not a PAT) for the Flux writer with scoped, no-admin permissions; `security-scan.yml`, `stale.yml`, `wake-blocked.yml` workflows. | **`strict_required_status_checks_policy` is `false`** on `idp-required-checks` — merges are allowed even when the branch isn't up to date with main, so two independently-green PRs can still land a broken merge tree (matches the "a local gate run grades the branch, not the merge tree" memory note — this is the GitHub-side fix for that exact class). **Merge queue** — not configured; would batch-validate PRs against the true merge tree instead. **Required commit signing** — not enforced in either ruleset. **Environments with required reviewers** for deploy-shaped workflows — none found. (No required-approving-review-count is intentional — memory: "peer review is off".) | config-only — one JSON field per ruleset | Flip `strict_required_status_checks_policy` to `true` on `idp-required-checks` — directly closes the known "branch passed locally, merge tree didn't" failure class, one field, no new infra |

---

## Top 5 config-only wins

1. **LiteLLM: turn on response caching** (`litellm_settings.cache`) — zero new infra, directly cuts spend on repeated calls, which is the founder's own cost-mindfulness ask.
2. **GitHub: set `strict_required_status_checks_policy: true`** on `idp-required-checks` — one JSON field, closes the exact "green branch, broken merge tree" failure class already logged as a known incident.
3. **Flux: un-suspend the Telegram alert** by pointing `flux-telegram.channel` at an alerts group — the provider, Alert and event sources are already written; only the channel target and the `suspend: true` flag need to change.
4. **Backstage: wire `search` to the already-running Postgres** backing the catalog, and turn on the Notifications plugin as the in-app channel Flux's alert can safely target instead of the founder's DM.
5. **SigNoz: add native alert rules** (LiteLLM error rate, pod restarts) using the same authenticated-API pattern the retention CronJob already proves works, routed to the same alerts channel.
