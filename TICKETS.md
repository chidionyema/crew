# Hermes Estate — Engineering Ticket Registry

**Created:** 2026-09-16  
**Scope:** OKE Kubernetes estate running Hermes AI agents (Telegram delivery path)  
**Current performance:** ~1/100 functional on Telegram  
**Basis:** Full forensic audit completed 2026-09-15  

---

## Summary Table

| Ticket | Title | Class | Priority | Phase | Status |
|--------|-------|-------|----------|-------|--------|
| T001 | No OWNER.yaml for Telegram bot | 1 — Single Writer | P0 | 0 | open |
| T002 | hermes-agent ExternalSecret disables token via rename | 1 — Single Writer | P0 | 1 | open |
| T003 | jit-broker calls Telegram directly (409 loop) | 1 — Single Writer | P1 | 1 | open |
| T004 | telegram-mirror.yaml brittle Traefik mirroring | 1 — Single Writer | P1 | 1 | open |
| T005 | otto-gateway has no real /readyz | 2 — Readiness Fake | P0 | 2 | open |
| T006 | Flux healthCheck watches Deployment Available (meaningless) | 2 — Readiness Fake | P0 | 2 | open |
| T007 | 46/86 Kustomizations NOT READY (2026-09-15) | 2 — Readiness Fake | P0 | 2+3 | open |
| T008 | otto-golden /healthz always 200, real readiness never checked | 2 — Readiness Fake | P1 | 2 | open |
| T009 | otto-gateway dependsOn alerts-github (wrong healthCheck target) | 3 — Dep Depth | P0 | 3 | open |
| T010 | otto-gateway dependsOn event-bus — verify still required | 3 — Dep Depth | P2 | 3 | open |
| T011 | LAW 50 too strict: OTel down → otto.ingress crash-loop | 3 — Dep Depth | P0 | 3 | open |
| T012 | llm NOT READY → sidecar fallback not verified | 3 — Dep Depth | P1 | 3 | open |
| T013 | hindsight unreachable → answers chars=0 (not graceful) | 3 — Dep Depth | P1 | 3 | open |
| T014 | estate-db NOT READY — schema migrations may be stalled | 3 — Dep Depth | P1 | 3 | open |
| T015 | human-vault-bridge NOT READY — secrets stop refreshing | 3 — Dep Depth | P1 | 3 | open |
| T016 | reloader NOT READY — pods hold stale secrets | 3 — Dep Depth | P1 | 3 | open |
| T017 | Conversation state in emptyDir — lost on pod restart | 4 — State Durability | P0 | 4 | open |
| T018 | Facts stored without vector on embedding timeout (silent drop) | 4 — State Durability | P1 | 4 | open |
| T019 | hindsight write queue has no persistence | 4 — State Durability | P2 | 4 | open |
| T020 | otto-gateway /data is emptyDir — all state lost on restart | 4 — State Durability | P1 | 4 | open |
| T021 | Recall timeout fixed to 30s; no CI measures p99 drift | 5 — Semantic Timeouts | P2 | 5+6 | open |
| T022 | Embedding timeout fixed to 10s; no CI measures drift | 5 — Semantic Timeouts | P2 | 5 | open |
| T023 | OTTO_ROUTER_TIMEOUT_SECONDS=170s not CI-verified vs worst-case | 5 — Semantic Timeouts | P2 | 5 | open |
| T024 | PGCONNECT_TIMEOUT=5s never measured against Postgres p99 | 5 — Semantic Timeouts | P3 | 5 | open |
| T025 | VXLAN failure killed CoreDNS+OTel+LiteLLM+Otto simultaneously | 6 — Failure Domain | P1 | 6 | open |
| T026 | 2/3 OKE nodes Ready — third node identity and cause unknown | 6 — Failure Domain | P0 | immediate | open |
| T027 | No VXLAN/CNI health monitor | 6 — Failure Domain | P1 | 6 | open |
| T028 | CoreDNS: verify 2+ replicas with hard anti-affinity | 6 — Failure Domain | P1 | 6 | open |
| T029 | OTel collector: verify DaemonSet + Deployment topology | 6 — Failure Domain | P1 | 6 | open |
| T030 | otto-brain LiteLLM virtual key mismatch (fixed); CI test missing | 7 — Credential Provenance | P1 | 2 | open |
| T031 | GitHub App token stale without Reloader (no checksum annotation) | 7 — Credential Provenance | P1 | 3 | open |
| T032 | ExternalSecret keys lack declared rotation metadata | 7 — Credential Provenance | P3 | 4 | open |
| T033 | channel_registration_ok metric exists but no dashboard | 8 — Observability Gap | P1 | 6 | open |
| T034 | No alert: channel_registration_ok == 0 for >5 min | 8 — Observability Gap | P0 | 6 | open |
| T035 | No chaos drills in CI | 8 — Observability Gap | P1 | 5 | open |
| T036 | No weekly timeout-drift CI job | 8 — Observability Gap | P2 | 5 | open |
| T037 | Maestro stale 3351 min (last cycle 2026-09-13) | Cluster Infra | P1 | immediate | open |
| T038 | openclaw crash-looping since April 2026 | Cluster Infra | P3 | — | open |
| T039 | 46/86 Kustomizations NOT READY — systematic remediation | Cluster Infra | P0 | immediate | open |
| T040 | image-automation NOT READY — deploys may not be landing | Cluster Infra | P0 | immediate | open |
| T041 | `otto_turns` Postgres store: verify schema migrated + env configured | Feature Verify | P0 | 4 | open |
| T042 | `thread.py` SqliteConversationStore is dead code — remove or wire | Feature Verify | P2 | 4 | open |
| T043 | Voice STT (ADR22): verify `wants_voice_reply` and speech transcribed | Feature Verify | P1 | feature | open |
| T044 | Voice TTS reply: verify `send_voice()` sends audio for voice-in msgs | Feature Verify | P1 | feature | open |
| T045 | `OTTO_TOOLSETS` — ALREADY CONFIGURED (terminal,web,search,skills,file,vision,tts,memory,todo,cronjob,code_execution); verify tools actually execute in live pod | Feature Verify | P1 | feature | open |
| T046 | Human gate: verify fail-closed blocks T3 tools and approval path | Feature Verify | P1 | feature | open |
| T047 | Verify lane: confirm `reply_judge` budget configured and runs each turn | Feature Verify | P1 | feature | open |
| T048 | MCP estate server: verify estate toolset wired and queries work | Feature Verify | P1 | feature | open |
| T049 | Multi-bot routing: staging + alerts bots answer through their own token | Feature Verify | P1 | feature | open |
| T050 | Fast recall: verify pgvector search returns relevant facts in production | Feature Verify | P1 | feature | open |
| T051 | Telegram inline buttons: verify `callback_query` events processed | Feature Verify | P2 | feature | open |
| T052 | Explorer lane (crew#892 CP3): N-fold fan-out — verify implementation | Feature Verify | P1 | feature | open |
| T053 | Streaming/live edit (crew#892 CP2): verify `edit_message` wired | Feature Verify | P1 | feature | open |
| T054 | Reasoning lane (`/think`, `/kimi`): verify routes to right model | Feature Verify | P1 | feature | open |
| T055 | Progress placeholder for long answers (PR #91 hands 7) | Feature Verify | P2 | feature | open |
| T056 | Denied command: human-readable denial reaches user (PR #95) | Feature Verify | P1 | feature | open |
| T057 | Conversation history window: 12-turn/12-hour defaults under load | Feature Verify | P2 | feature | open |
| T058 | `reply_binding` envelope field: verify gateway stamps it per event | Feature Verify | P1 | feature | open |
| T059 | Vision (PR #86, #91 hands 4): Otto receives and understands photos | Feature Verify | P1 | feature | open |
| T060 | `InMemoryNotifier` in production — operator blind to NEEDS_HUMAN / QUEUED_BUDGET | 8 — Observability Gap | P0 | immediate | **fixed** |
| T061 | Verify lane silent failure — `reply_judge` offline returns `None`, indistinguishable from budget exhaustion | 8 — Observability Gap | P1 | feature | open |
| T062 | `fast_recall.configured()` returns `""` silently when `otto_facts` schema is broken | 4 — State Durability | P1 | 4 | open |
| T063 | otto-golden webhook registration still points POST to a 404 endpoint | 1 — Single Writer | P1 | 1 | open |

*T017 premise corrected by T041 — active conversation store is Postgres `otto_turns`, not emptyDir SQLite. See T017 body and the correction block below.*

---

## Class 1 — Single Writer Principle

> External singletons must have exactly one legal mutator.

---

### T001 — No OWNER.yaml declares otto-gateway as sole Telegram bot owner

**Class:** 1 — Single Writer Principle  
**Priority:** P0  
**Phase:** 0  
**Status:** open  
**Blocked by:** N/A  
**Description:** Three namespaces — `hermes-agent`, `otto-golden`, and `otto-gateway` — have all held Telegram credentials at different points in the estate's history. There is no `OWNER.yaml` (or equivalent declared ownership artifact in git) that designates `otto-gateway` as the one legal writer for the Telegram webhook. Any operator or future deployment can inadvertently activate a competing setWebhook call from a different namespace, immediately invalidating the registration held by otto-gateway. This is the root architectural gap that permits the entire class of 409 / webhook-conflict incidents.  
**Fix:** Create `platform/ownership/OWNER.yaml` (or a sibling file in the `crew/` mono-repo root) that explicitly declares: owner=`otto-gateway`, resource=`telegram-webhook`, constraint=`single-writer`. Delete or disable all ExternalSecrets surfacing the live bot token into any namespace other than `otto-gateway`. Add a CI lint rule (`bin/idp-rules run`) that fails if `TELEGRAM_BOT_TOKEN` appears in an ExternalSecret spec outside the declared owner namespace.

---

### T002 — hermes-agent ExternalSecret disables token via name rename (workaround)

**Class:** 1 — Single Writer Principle  
**Priority:** P0  
**Phase:** 1  
**Status:** open  
**Blocked by:** T001  
**Description:** `hermes-agent`'s ExternalSecret currently renames `TELEGRAM_BOT_TOKEN` to `DISABLED_TELEGRAM_BOT_TOKEN` as a workaround to prevent the agent from calling Telegram. The vault key still exists in hermes-agent's secret spec and the secret is still fetched — only the env-var name is changed. Any change to the workload's environment mapping, any future operator who doesn't know the convention, or any future feature flag that restores the original name will silently re-activate a competing Telegram writer.  
**Fix:** Remove the vault key `TELEGRAM_BOT_TOKEN` from `hermes-agent`'s ExternalSecret spec entirely. The rename must not persist as a long-term control. After T001's CI lint rule is in place, hermes-agent should be incapable of holding a live bot credential.

---

### T003 — jit-broker calls Telegram directly, causing 409 Conflict every 5 seconds

**Class:** 1 — Single Writer Principle  
**Priority:** P1  
**Phase:** 1  
**Status:** open  
**Blocked by:** T001  
**Description:** `jit-broker` (under `platform/jit/`) was previously calling `deleteWebhook` and `getUpdates` directly against the Telegram API on a ~5-second polling loop. Every call that succeeds in deleting the webhook immediately breaks otto-gateway's registration. The result is a 409 Conflict loop visible in both otto-gateway and jit-broker logs. This has been the most frequent source of Telegram dark periods.  
**Fix:** Architectural: jit-broker must never contact the Telegram API directly. Replace with an internal forward path: `otto.ingress` receives the inbound Telegram update, optionally mirrors or forwards a copy to jit-broker's HTTP API (internal cluster route only). jit-broker becomes a consumer of forwarded updates, not a poller. The feature (job initiation from Telegram) must not be lost — validate end-to-end before merging.

---

### T004 — telegram-mirror.yaml (Traefik TraefikService mirror) is architecturally brittle

**Class:** 1 — Single Writer Principle  
**Priority:** P1  
**Phase:** 1  
**Status:** open  
**Blocked by:** T003  
**Description:** `telegram-mirror.yaml` implements a Traefik `TraefikService` that mirrors Telegram traffic to jit-broker. This depends on `allowCrossNamespace=true` in Traefik's static config and on Traefik v3's backend builder behavior, both of which are brittle upgrade-sensitive settings. A Traefik upgrade or tightened RBAC policy silently drops the mirror. The mirror also feeds the root cause of T003 (jit-broker receiving raw Telegram traffic and making upstream API calls).  
**Fix:** Replace the Traefik mirror with an explicit internal HTTP forward from `otto.ingress` to jit-broker's API. The forward should be a deliberate, auditable code path in otto.ingress, not a mesh-level side-effect. Verify Traefik `allowCrossNamespace` can then be set to `false`. Do not remove the mirror before the explicit forward is tested end-to-end.

---

## Class 2 — Readiness Must Be Self-Verified

> `/readyz` proves the pod can do its job. Always-200 healthz tells nothing.

---

### T005 — otto-gateway has no /readyz endpoint

**Class:** 2 — Readiness Must Be Self-Verified  
**Priority:** P0  
**Phase:** 2  
**Status:** open  
**Blocked by:** N/A  
**Description:** `GET /healthz` on otto-gateway returns HTTP 200 unconditionally regardless of the state of any downstream dependency. The kubelet readiness probe watches `/healthz`. Flux healthChecks watch the resulting Deployment `Available` condition. The entire observability and deployment control plane believes otto-gateway is ready when it may be answering every user turn with `needs_human` because Postgres, LiteLLM, or NATS are unreachable.  
**Fix:** Implement a `/readyz` endpoint with 5 dependency checks, returning 200 only when all critical deps pass:
- Postgres TCP connect + `SELECT 1` — **critical** (503 if down)
- LiteLLM brain sidecar HTTP ping — **critical** (503 if down)
- OTel collector reachability — **degraded** (200 with `degraded=true` body field if down)
- Hindsight HTTP ping — **degraded** (200 with `degraded=true` if down)
- NATS connectivity — **degraded** (200 with `degraded=true` if down)

Response body should be JSON with per-dependency status. The existing `/healthz` can remain as a liveness probe (shallow).

---

### T006 — Flux healthCheck watches Deployment Available (meaningless for correctness)

**Class:** 2 — Readiness Must Be Self-Verified  
**Priority:** P0  
**Phase:** 2  
**Status:** open  
**Blocked by:** T005  
**Description:** Flux's `healthChecks` for the otto-gateway Kustomization watches `Deployment/otto-gateway` `Available` condition. Deployment Available is `True` as long as at least one pod passes its readiness probe — which is `/healthz` (always 200, per T005). So Flux reports the Kustomization as healthy even when otto-gateway is fully non-functional.  
**Fix:** After T005 lands, wire the Deployment's readiness probe to `/readyz`. This automatically propagates: kubelet marks pod Ready only when `/readyz` returns 200, Deployment Available becomes meaningful, Flux healthCheck becomes meaningful. Optionally add a dedicated Flux `HTTPRoute` healthCheck pointing at `/readyz` for belt-and-suspenders.

---

### T007 — 46 of 86 Kustomizations NOT READY (observed 2026-09-15 13:04 UTC)

**Class:** 2 — Readiness Must Be Self-Verified  
**Priority:** P0  
**Phase:** 2 + 3  
**Status:** open  
**Blocked by:** T026, T039, T040  
**Description:** As of 2026-09-15 13:04 UTC, 46 out of 86 Kustomizations across the estate are in a NOT READY state. This is the single largest surface of the estate's dysfunction. Root causes span multiple ticket classes: failed ExternalSecrets (T002, T015), downstream dependency chains (T009, T011), image-automation failures (T040), the degraded node (T026), and OTel-enforced crash-loops (T011). No single fix resolves this — systematic per-Kustomization investigation is required.  
**Fix:** For each NOT READY Kustomization: (1) run `flux get kustomization <name>` and `flux logs --kind=Kustomization --name=<name>` to get the failure reason, (2) map the failure to the appropriate ticket class, (3) create a child ticket or link to the relevant ticket in this registry, (4) remediate. Track count toward zero. Target: 86/86 READY before declaring Phase 3 complete.

---

### T008 — otto-golden readiness probe is /healthz (always 200)

**Class:** 2 — Readiness Must Be Self-Verified  
**Priority:** P1  
**Phase:** 2  
**Status:** open  
**Blocked by:** T005  
**Description:** `otto-golden`'s readiness probe is identical to otto-gateway's pre-fix state: `/healthz` returning 200 unconditionally. The real readiness conditions for otto.boot — does it hold a valid Telegram token? is the allowlist loaded? is the bootstrap database populated? — are never verified by any probe. The pod can be marked Ready while being functionally inert.  
**Fix:** Implement `/readyz` for otto-golden with checks appropriate to otto.boot's role: token present in env (not just env key present — validate format), allowlist non-empty, Postgres reachable if required. Pattern from T005 applies. Liveness stays on `/healthz`.

---

## Class 3 — Dependency Depth Budget

> No more than 2 transitive NOT-READY deps on the critical path.

---

### T009 — otto-gateway dependsOn alerts-github which watches wrong resource

**Class:** 3 — Dependency Depth Budget  
**Priority:** P0  
**Phase:** 3  
**Status:** open  
**Blocked by:** N/A  
**Description:** otto-gateway's Flux Kustomization has a `dependsOn: alerts-github`. The `alerts-github` healthCheck watches the `backstage/catalogue` Deployment — a completely unrelated resource. What otto-gateway actually needs is the `github-app` Secret (used for GitHub API calls from the agent). When the backstage catalogue Deployment is degraded for any reason, alerts-github reports NOT READY, otto-gateway blocks on that dependency, and Telegram goes dark — even though the github-app Secret is perfectly healthy. This is the single most impactful transitive dependency fix available.  
**Fix:** Create a new minimal Kustomization `github-app-creds` that renders only the `github-app` ExternalSecret and nothing else. Point both `alerts-github` and `otto-gateway` to `dependsOn: github-app-creds`. Remove the backstage/catalogue healthCheck from the path that gates otto-gateway. This unblocks otto-gateway immediately without architectural rework.

---

### T010 — otto-gateway dependsOn event-bus — verify dependency is still correct

**Class:** 3 — Dependency Depth Budget  
**Priority:** P2  
**Phase:** 3  
**Status:** open  
**Blocked by:** N/A  
**Description:** otto-gateway has a `dependsOn: event-bus`. event-bus is currently READY (was previously suspended). The dependency itself may be correct (otto-gateway needs NATS/event-bus to process routing messages). However, the dependency has not been verified since event-bus resumed, and it's unclear whether otto-gateway's runtime behavior actually blocks on event-bus being up or merely uses it opportunistically.  
**Fix:** Verify: (1) confirm event-bus is READY and remains stable, (2) review otto-gateway startup code to confirm whether NATS connection failure is fatal or degraded, (3) if degraded, remove the Flux dependsOn and instead reflect NATS status in /readyz as a degraded signal (per T005). If fatal, keep the dependsOn but document the reason.

---

### T011 — LAW 50 too strict: OTel unavailable causes otto.ingress crash-loop

**Class:** 3 — Dependency Depth Budget  
**Priority:** P0  
**Phase:** 3  
**Status:** open  
**Blocked by:** T005  
**Description:** LAW 50 in otto.ingress enforces "no exporter = refuse to start." When the OTel collector is NOT READY (which it is during the current estate degradation, per T007/T029), otto.ingress enters a crash-loop. OTel unavailability is a transitive dependency failure that propagates into a complete inbound traffic blackout. Observability outage should never kill the serving path.  
**Fix:** Change the `instrument(component)` call to `instrument(component, allow_degraded=True)`. When OTel is unreachable: (1) use an in-memory noop exporter — spans are dropped, not errors, (2) expose `degraded=true, reason="otel_unavailable"` in `/readyz` response body, (3) continue serving traffic. Add a metric `otel_exporter_unavailable_total` on a local Prometheus endpoint as a fallback signal. The fix should be a one-line change to the instrument call site plus a noop exporter implementation.

---

### T012 — llm Kustomization NOT READY; sidecar fallback behavior not verified

**Class:** 3 — Dependency Depth Budget  
**Priority:** P1  
**Phase:** 3  
**Status:** open  
**Blocked by:** T007  
**Description:** When the estate's `llm` Kustomization is NOT READY, the central LiteLLM router is unavailable. otto-gateway has an `otto-brain` sidecar intended as a lifeboat: if home-1 (central router) is available, use it; otherwise fall back to the sidecar. Current understanding is that if home-1 is reachable, it works regardless of the `llm` Kustomization's health status. However, this has not been verified with a controlled failure test, and the sidecar startup path when `llm` is NOT READY has not been confirmed to succeed.  
**Fix:** (1) Run a controlled test: suspend the `llm` Kustomization, observe whether otto-brain sidecar successfully starts and handles a request. (2) If the sidecar depends on anything from the `llm` Kustomization (e.g., a shared ConfigMap or Secret), break that dependency. (3) Document the verified fallback behavior. Link to T035 for chaos drill coverage.

---

### T013 — hindsight unreachable causes answers with chars=0 (not graceful degradation)

**Class:** 3 — Dependency Depth Budget  
**Priority:** P1  
**Phase:** 3  
**Status:** open  
**Blocked by:** N/A  
**Description:** hindsight is configured as optional: when `OTTO_MEMORY_HINDSIGHT_URL` is unset, recall is a noop. However, when the URL is set and hindsight is unreachable, the recall call waits for its full timeout before cancelling, and the resulting answer has `chars=0` — a blank response to the user. The distinction between "not configured" and "configured but unreachable" produces different behavior, with the worse outcome for the reachable-but-failing case. This is NOT graceful degradation.  
**Fix:** In the hindsight recall path, treat a connection error or timeout the same as "URL unset": return an empty recall result immediately on the first connection failure (do not wait for the full timeout), log a warning at WARN level, and set `degraded=true, reason="hindsight_unreachable"` in the next `/readyz` response. The semantic timeout for hindsight (per T021) should be retained for the case where hindsight is reachable-but-slow.

---

### T014 — estate-db Kustomization NOT READY — schema migrations may be stalled

**Class:** 3 — Dependency Depth Budget  
**Priority:** P1  
**Phase:** 3  
**Status:** open  
**Blocked by:** T007  
**Description:** The `estate-db` Kustomization is NOT READY. This could indicate: (a) the Kustomization's healthCheck resource is degraded without affecting the actual Postgres service, or (b) schema migrations (run as a Job) have stalled, blocking the ready condition. If (b), otto-gateway's Postgres writes may be failing silently if the schema is out of date.  
**Fix:** (1) Independently verify `estate-rw.estate-db.svc` is responding: `kubectl exec -n estate-db <pod> -- psql -U otto -c "SELECT version();"`. (2) Check migration job status: `kubectl get jobs -n estate-db`. (3) If migrations are stalled, inspect logs and remediate. (4) If the Kustomization healthCheck is misconfigured (watching the wrong resource), fix the healthCheck independently of the DB health.

---

### T015 — human-vault-bridge NOT READY — Bitwarden secrets stop refreshing

**Class:** 3 — Dependency Depth Budget  
**Priority:** P1  
**Phase:** 3  
**Status:** open  
**Blocked by:** T007  
**Description:** `human-vault-bridge` is NOT READY. This bridge is the mechanism by which Bitwarden-sourced secrets are pushed into ESO (External Secrets Operator). When it is down, ExternalSecret resources stop refreshing. Secrets that rotate (GitHub App token every 45min, any Bitwarden-managed credential) become stale. This is a silent failure — the pod holds the last-known-good secret until it restarts, at which point it may fail to fetch a fresh one.  
**Fix:** Short-term: audit which critical secrets (TELEGRAM_BOT_TOKEN, Postgres credentials, github-app key) are sourced through human-vault-bridge and ensure they are also bootstrapped in-cluster (e.g., as a base Secret in git, encrypted with SOPS) so they persist through bridge outages. Long-term: make human-vault-bridge HA (2+ replicas, leader election) or replace with a more reliable ESO provider.

---

### T016 — reloader (Stakater) NOT READY — pods hold stale secrets after rotation

**Class:** 3 — Dependency Depth Budget  
**Priority:** P1  
**Phase:** 3  
**Status:** open  
**Blocked by:** T007, T031  
**Description:** Stakater Reloader is NOT READY. Without it, pods are not automatically restarted when Secrets or ConfigMaps they consume are updated. The most acute impact: `GithubAccessToken` rotates every 45 minutes. Without Reloader, the pod continues using the expired token, and `gh auth` calls fail after 45 minutes of uptime. This is the root scenario for T031.  
**Fix:** Replace the Reloader dependency with a pod-template checksum annotation on all Deployments whose pods consume secrets that rotate. The annotation pattern: `checksum/secret: {{ include (print $.Template.BasePath "/secret.yaml") . | sha256sum }}` — when ESO updates the Secret, a Kustomization re-apply updates the annotation, triggering a rolling restart. No external controller required. This eliminates the single point of failure that Reloader currently represents.

---

## Class 4 — State Durability Class

> Conversation state must survive pod restart.

---

### T017 — Conversation threads (SqliteConversationStore) backed by emptyDir

**Class:** 4 — State Durability Class  
**Priority:** P0  
**Phase:** 4  
**Status:** open  
**Blocked by:** T014  
**Description:** `SqliteConversationStore` stores conversation threads in a SQLite file at `/data/conversations.db`. The `/data` volume is an `emptyDir` (see T020). Every pod restart — caused by a deployment, a crash, a node eviction, or the cluster node issue (T026) — wipes all conversation history. Users experience this as the bot forgetting everything mid-conversation. Measured impact: every Flux reconciliation or rolling restart that touches otto-gateway deletes all active threads.  
**Fix:** Migrate `SqliteConversationStore` to a `PostgresConversationStore` backed by the `otto_gateway` database already used for `channel_binding`. The schema is straightforward (thread_id, user_id, messages JSONB, updated_at). emptyDir at `/data` is permissible only as a local cache (e.g., for embedding vectors that can be recomputed). No conversation state may be stored in emptyDir.

---

### T018 — Facts stored without embedding vector on timeout (silent permanent data loss)

**Class:** 4 — State Durability Class  
**Priority:** P1  
**Phase:** 4  
**Status:** open  
**Blocked by:** N/A  
**Description:** When the embedding API call times out during `store_fact`, the fact is written to the database with a null vector. A fact with a null vector cannot be returned by semantic search — it is permanently invisible to recall, but the caller receives no error and has no way to know the fact was effectively lost. This is silent, permanent data loss. Measured: embedding timeout was 1.5s vs actual p99 of 6s+ (fixed to 10s in T022), meaning this occurred on every store_fact during the degraded period.  
**Fix:** Make embedding an atomic part of the write transaction: (1) attempt embedding with 3 retries using exponential backoff, (2) if all retries exhausted, return an explicit error to the caller — do not write the fact to the database, (3) the caller (agent) surfaces a user-visible degradation message: "I couldn't save that — please try again." Never write a null-vector fact to the store.

---

### T019 — hindsight write queue has no persistence

**Class:** 4 — State Durability Class  
**Priority:** P2  
**Phase:** 4  
**Status:** open  
**Blocked by:** T017  
**Description:** hindsight's memory consolidation pipeline processes facts through an in-memory write queue. If the hindsight pod restarts mid-consolidation (e.g., during a rolling update triggered by T016's rotation, or due to the node issue in T026), all in-flight facts in the queue are lost. There is no replay mechanism.  
**Fix:** Add a SQLite queue file on a dedicated PVC as the write buffer. Facts are written to the queue first (durable), then processed asynchronously. On restart, the worker resumes from the last unprocessed queue position. The PVC should be a `ReadWriteOnce` volume sized to hold at least 24 hours of fact volume at peak load.

---

### T020 — otto-gateway /data volume is emptyDir with 2Gi sizeLimit

**Class:** 4 — State Durability Class  
**Priority:** P1  
**Phase:** 4  
**Status:** open  
**Blocked by:** T017  
**Description:** otto-gateway's pod spec declares `/data` as `emptyDir: {sizeLimit: 2Gi}`. All state that lands in `/data` — currently the SQLite conversation database (T017), and potentially other runtime artifacts — is destroyed on pod restart. The 2Gi sizeLimit additionally risks the pod being evicted if the volume fills, which would itself destroy the state it was supposed to hold.  
**Fix:** After T017 moves conversation state to Postgres, the remaining legitimate uses of `/data` (caches, temp files) can stay in emptyDir. The long-term shape for otto-gateway at 2+ replicas is a StatefulSet with a PVC per replica — but this is blocked until all state is either in Postgres or hindsight and the pod is truly stateless. Track as a follow-on to T017.

---

## Class 5 — Semantic Timeouts

> Timeouts are derived from measured p99 + 50% headroom, verified by CI.

---

### T021 — Recall timeout set to 30s; no CI job detects future drift

**Class:** 5 — Semantic Timeouts  
**Priority:** P2  
**Phase:** 5 (CI impl in Phase 6)  
**Status:** open  
**Blocked by:** T005, T013  
**Description:** `OTTO_MEMORY_RECALL_TIMEOUT_S` was 3s when the measured hindsight p99 was 27–96s. It has been corrected to 30s. However, the underlying problem — no automated measurement verifying the timeout is above the measured p99 — is unfixed. The next time hindsight slows down (new embedding model, larger vector index, index fragmentation), the timeout will again silently become too tight without any CI signal.  
**Fix:** Add a weekly CI job that: (1) sends 50 recall requests to live hindsight with representative query complexity, (2) measures p99 latency, (3) compares against `OTTO_MEMORY_RECALL_TIMEOUT_S`, (4) fails and opens a PR bumping the timeout if measured p99 * 1.5 > current value. Job runs in the estate's existing CI pipeline. Results published to the observability dashboard (T033).

---

### T022 — Embedding timeout set to 10s; no CI job detects drift

**Class:** 5 — Semantic Timeouts  
**Priority:** P2  
**Phase:** 5  
**Status:** open  
**Blocked by:** T021  
**Description:** Embedding timeout was 1.5s when actual p99 was 6s+. Fixed to 10s. Same structural gap as T021: no CI measurement. A model change or embedding service degradation will silently make this too tight again, returning to the T018 silent data-loss scenario.  
**Fix:** Include embedding p99 measurement in the same weekly CI job as T021. Threshold: `OTTO_EMBEDDING_TIMEOUT_S` must be ≥ measured p99 * 1.5. If not, open a PR.

---

### T023 — OTTO_ROUTER_TIMEOUT_SECONDS=170s not verified against worst-case path sum

**Class:** 5 — Semantic Timeouts  
**Priority:** P2  
**Phase:** 5  
**Status:** open  
**Blocked by:** T021  
**Description:** `OTTO_ROUTER_TIMEOUT_SECONDS` was set to 170s based on a measured worst-case path sum: 20s (routing) + 60s (LLM inference) + 20s (tool call) + 20s (embedding) + 25s (hindsight) + loopback overhead ≈ 155s. The 170s value has 10% headroom. However, this calculation was made at a point in time and is not re-verified when any of those component timeouts change (e.g., if hindsight p99 grows to 40s, the path sum becomes 175s, exceeding the router timeout).  
**Fix:** Add to the weekly CI job (T021): compute the path sum from the latest measured p99 values of each component. Fail if `OTTO_ROUTER_TIMEOUT_SECONDS` < path_sum * 1.1. The CI job should also verify that no individual component timeout exceeds the router timeout.

---

### T024 — PGCONNECT_TIMEOUT=5s never measured against Postgres p99 under contention

**Class:** 5 — Semantic Timeouts  
**Priority:** P3  
**Phase:** 5  
**Status:** open  
**Blocked by:** T014  
**Description:** `PGCONNECT_TIMEOUT` is set to 5 seconds. This value was chosen without measurement. Under cluster contention (multiple pods competing for Postgres connections, estate-db Kustomization issues per T014), the actual p99 connection time may exceed 5s, causing spurious connection failures that appear as application errors rather than timeout signals.  
**Fix:** Measure Postgres connection p99 under realistic load (at least 10 concurrent connection attempts while the estate is at normal load). Document the measured value. If 5s provides less than 50% headroom over p99, increase it. Add to the weekly CI job (T021) as a lower-priority measurement.

---

## Class 6 — Failure Domain Isolation

> One node or link failure must never cascade to CoreDNS + OTel + DB + Otto simultaneously.

---

### T025 — VXLAN link failure cascaded to CoreDNS + OTel + LiteLLM + Otto simultaneously

**Class:** 6 — Failure Domain Isolation  
**Priority:** P1  
**Phase:** 6  
**Status:** open  
**Blocked by:** T026, T028, T029  
**Description:** On 2026-09-09, a single VXLAN link failure between two worker nodes simultaneously killed CoreDNS, the OTel collector, a LiteLLM replica, and Otto. This is the canonical failure domain violation: a single-link failure at the network layer produced a full-estate outage. The root cause is insufficient replica spread and missing anti-affinity rules for critical infrastructure components.  
**Fix:** Three concurrent topology changes required: (1) CoreDNS: minimum 2 replicas with `podAntiAffinity` hard rule across all nodes (T028). (2) OTel: DaemonSet mode so every node has a local collector, plus a separate Deployment for aggregation (T029). (3) LiteLLM: minimum 3 replicas with `topologySpreadConstraints` across all 3 nodes, `maxSkew: 1`. After T026 restores the third node, these changes ensure any single node loss leaves at least one replica of each component Running.

---

### T026 — 2/3 OKE nodes Ready; third node identity and root cause unknown

**Class:** 6 — Failure Domain Isolation  
**Priority:** P0  
**Phase:** immediate  
**Status:** open  
**Blocked by:** N/A  
**Description:** As of 2026-09-15, only 2 of 3 OKE worker nodes are in Ready state. The identity of the failing node and the reason for its failure are unknown. With only 2 nodes, anti-affinity rules for 3+ replicas cannot be satisfied, pod scheduling is constrained, and the estate is one additional node failure away from single-node operation (which would almost certainly cascade as in T025).  
**Fix:** (1) Identify the failing node: `kubectl get nodes -o wide`. (2) Describe the node: `kubectl describe node <name>` — look for taints, conditions, kubelet errors. (3) Check OCI/OKE console for the node pool and instance health. (4) If the node is fixable (disk pressure, kubelet crash): remediate and verify it rejoins. (5) If the instance is unhealthy: terminate and let the node pool auto-provision a replacement. (6) Verify all 3 nodes are Ready and schedulable before closing. Document root cause in an incident note.

---

### T027 — No VXLAN/CNI health monitor

**Class:** 6 — Failure Domain Isolation  
**Priority:** P1  
**Phase:** 6  
**Status:** open  
**Blocked by:** T026  
**Description:** The 2026-09-09 incident (T025) was discovered only when services went dark — there was no proactive signal that the VXLAN overlay was degraded. Without a VXLAN/CNI health monitor, the next link failure will again be discovered via user impact, not via alerting.  
**Fix:** Deploy a blackbox exporter as a DaemonSet. Each DaemonSet pod pings every other node's pod IP (using a ConfigMap-populated target list) every 30s. A Prometheus alert fires when any node-pair experiences >1% packet loss over a 5-minute window. Alert routes to the estate's existing Robusta/alertmanager setup. Also add a `kubectl get nodes` health check to Maestro's cycle (T037).

---

### T028 — CoreDNS: verify 2+ replicas with hard podAntiAffinity across all nodes

**Class:** 6 — Failure Domain Isolation  
**Priority:** P1  
**Phase:** 6  
**Status:** open  
**Blocked by:** T026  
**Description:** CoreDNS single-node placement was a contributing factor in the 2026-09-09 cascade (T025). Current replica count and anti-affinity configuration have not been verified since the incident.  
**Fix:** (1) Verify current state: `kubectl get deploy coredns -n kube-system -o yaml | grep -A 20 affinity`. (2) If replica count < 2 or anti-affinity is missing: patch the CoreDNS Deployment (via the estate's GitOps overlay, not via `kubectl apply` directly). Required config: `replicas: 2`, `podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution` with `topologyKey: kubernetes.io/hostname`. (3) After T026 restores 3 nodes, bump to 3 replicas for full single-node-loss tolerance.

---

### T029 — OTel collector: verify DaemonSet + Deployment topology

**Class:** 6 — Failure Domain Isolation  
**Priority:** P1  
**Phase:** 6  
**Status:** open  
**Blocked by:** T026, T011  
**Description:** The OTel collector is currently a single Deployment. A single-node failure takes out the entire telemetry pipeline (as in T025). Additionally, T011 shows that OTel unavailability causes otto.ingress to crash-loop, making OTel availability load-bearing for the serving path (until T011 is fixed).  
**Fix:** (1) Deploy OTel as a DaemonSet (one agent per node, receiving spans from pods on that node via localhost). (2) Add a separate OTel Deployment (2 replicas, anti-affinity) as a gateway/aggregator receiving from the DaemonSet agents. (3) Configure otto.ingress (and all other instrumented components) to export to the local DaemonSet agent (127.0.0.1:4317), not to the Deployment service. A single-node loss then only loses the agent on that node; the other agents continue exporting.

---

## Class 7 — Credential Provenance

> A pod cannot present a credential it was not issued for a specific service.

---

### T030 — otto-brain sidecar LiteLLM virtual key mismatch (fixed 2026-09-10); CI test missing

**Class:** 7 — Credential Provenance  
**Priority:** P1  
**Phase:** 2  
**Status:** open  
**Blocked by:** N/A  
**Description:** otto-brain sidecar was configured with a LiteLLM virtual key (issued by the estate router's Postgres database) but pointed at a loopback sidecar that has no Postgres and therefore cannot validate the virtual key. The sidecar was issuing its own local key, creating a mismatch. This was fixed on 2026-09-10. However, the fix is not regression-protected: no CI test verifies that the key the sidecar presents matches the key the sidecar expects. A future config change can silently re-introduce the mismatch.  
**Fix:** Create `bin/idp-otto-door-key-agrees`: a smoke test that (1) reads the LiteLLM API key from the otto-gateway ExternalSecret, (2) reads the key the otto-brain sidecar config expects, (3) asserts they agree. Run in `bin/idp-ci`. If the script does not exist, create it. Add to the estate's offline gate per the Memory entry for local pre-flight gates.

---

### T031 — GitHub App token becomes stale without Reloader (no checksum annotation)

**Class:** 7 — Credential Provenance  
**Priority:** P1  
**Phase:** 3  
**Status:** open  
**Blocked by:** T016  
**Description:** The ESO `GithubAccessToken` generator rotates the GitHub App installation token every 45 minutes. Stakater Reloader (T016) was supposed to trigger a pod restart when the Secret updates. With Reloader NOT READY, the pod holds the token that was current at its last start time. After 45 minutes, `gh auth` calls fail. The pod will not self-heal — it stays up (passes liveness) with a stale credential indefinitely.  
**Fix:** Add a pod-template annotation `checksum/github-token: <sha256 of GithubAccessToken Secret>` to the otto-gateway Deployment spec. When ESO updates the Secret, Flux re-applies the Kustomization, the checksum changes, the Deployment triggers a rolling restart, and the new pod picks up the fresh token. No external controller (Reloader) required. Verify the checksum annotation updates correctly in a staging deployment.

---

### T032 — ExternalSecret keys lack declared rotation metadata

**Class:** 7 — Credential Provenance  
**Priority:** P3  
**Phase:** 4  
**Status:** open  
**Blocked by:** N/A  
**Description:** otto-gateway's ExternalSecret manifest lists multiple secret keys (Telegram bot token, Postgres password, LiteLLM key, GitHub App key, etc.) without any comment or annotation declaring the rotation interval, the issuing system, or the escalation path for each key. An operator responding to a credential incident cannot quickly determine how fresh a key is, when it will next rotate, or who to contact.  
**Fix:** Add a structured comment block above each key in the ExternalSecret spec following the format:
```yaml
# key: TELEGRAM_BOT_TOKEN
# issuer: BotFather (manual)
# rotation: manual, no automatic rotation
# escalation: #otto-ops Slack channel
```
For programmatically rotated keys (GithubAccessToken), add the rotation interval as an annotation on the ExternalSecret resource. This is documentation, not code — but it is load-bearing for incident response time.

---

## Class 8 — Observability Gap

> Metrics must flow to dashboards; alerts must fire before users notice.

---

### T033 — channel_registration_ok metric exists but no dashboard receives it

**Class:** 8 — Observability Gap  
**Priority:** P1  
**Phase:** 6  
**Status:** open  
**Blocked by:** T007, T029  
**Description:** otto-gateway emits `channel_registration_ok`, `channel_pending_updates`, and `channel_registration_repaired` gauges. With OTel NOT READY (T007/T029), SigNoz is not receiving these metrics. Even when OTel is fixed, there is no Grafana or SigNoz dashboard visualizing Telegram channel health — an operator has no single pane to confirm the bot is registered and healthy.  
**Fix:** After T029 fixes OTel topology: (1) create a Grafana (or SigNoz) dashboard named "Telegram Channel Health" with panels for: `channel_registration_ok` (gauge, target=1), `channel_pending_updates` (time series), `channel_registration_repaired` (counter over time). (2) Dashboard should be committed as a ConfigMap in the monitoring namespace (GitOps, not manual). (3) Verify metrics are flowing with `kubectl exec -n otto-gateway <pod> -- curl localhost:9090/metrics | grep channel_`.

---

### T034 — No alert: channel_registration_ok == 0 for more than 5 minutes

**Class:** 8 — Observability Gap  
**Priority:** P0  
**Phase:** 6  
**Status:** open  
**Blocked by:** T033, T029  
**Description:** There is no alerting rule that fires when `channel_registration_ok` drops to 0. The estate can be Telegram-dark for an arbitrary duration without any automated signal reaching the operator. The 2026-09-15 state (1/100 functional) would not have generated a page. Empirical proof of this gap: the audit was triggered by user reports, not by an alert.  
**Fix:** After T033 confirms metrics are flowing: add a Prometheus alerting rule `TelegramChannelDark: channel_registration_ok == 0 for 5m` routed to Robusta/alertmanager. Severity: critical. The alert body should include the last known registration timestamp and the pod that holds the channel binding. Wire to the estate's on-call rotation (or owner's notification path). This alert must fire before any user reports the bot as unresponsive.

---

### T035 — No chaos drills in CI

**Class:** 8 — Observability Gap  
**Priority:** P1  
**Phase:** 5  
**Status:** open  
**Blocked by:** T005, T011, T013, T017  
**Description:** None of the failure scenarios uncovered in this audit have automated chaos coverage. The issues were discovered via production incidents or manual audit, not by failing CI. Without chaos drills, regressions to any of the remediations in this registry will be discovered in production.  
**Fix:** Implement the following Phase 5 chaos drills as CI jobs (can be gated to run on-demand or weekly):
1. Kill OTel collector → assert otto-gateway stays Ready within 60s (validates T011)
2. Kill LiteLLM home-1 → assert failover to otto-brain sidecar within 2s (validates T012)
3. Kill Postgres primary → assert otto-gateway degrades gracefully, /readyz returns degraded, no crash (validates T005/T017)
4. Break VXLAN between two nodes → assert CoreDNS + OTel + LiteLLM + Otto each retain at least one healthy replica (validates T025-T029)
5. Delete Telegram webhook via `curl` → assert reconciler restores it within 5 minutes (validates T001 ownership flow)
6. Rotate every ExternalSecret simultaneously → assert no ungraceful pod restarts (validates T031/T032)

---

### T036 — No weekly timeout-drift CI job measuring downstream p99s

**Class:** 8 — Observability Gap  
**Priority:** P2  
**Phase:** 5  
**Status:** open  
**Blocked by:** T021, T022, T023  
**Description:** T021, T022, and T023 each require a weekly CI job measuring p99 latencies. This ticket tracks the creation of that job as a single shared implementation artifact, since the individual tickets each describe only what the job must measure for their respective component.  
**Fix:** Create `bin/timeout-drift-check` (runs in CI): (1) measure hindsight recall p99 (50 requests), (2) measure embedding p99 (50 requests), (3) compute LLM router worst-case path sum from measured component p99s, (4) compare each against the configured timeout with 50% headroom, (5) if any timeout is within 10% of the headroom threshold, open a PR updating the env var and notify the #otto-ops channel. Schedule weekly via the estate's CI cron. Output a JSON artifact for the T033 dashboard.

---

## Cluster Infrastructure

> Tickets spanning multiple classes or requiring immediate ops action.

---

### T037 — Maestro (Mac-side work distributor) stale 3351 minutes

**Class:** Cluster Infra  
**Priority:** P1  
**Phase:** immediate  
**Status:** open  
**Blocked by:** N/A  
**Description:** As of 2026-09-15, Maestro (the Mac-side work distributor responsible for cycling agent tasks) is stale by 3351 minutes — approximately 56 hours. Its last successful cycle was 2026-09-13. Maestro being stopped means no agent tasks are being dispatched from the Mac-side coordinator, which may explain why some estate-level automation (ticket creation, report generation, routine diagnostics) has also stopped.  
**Fix:** (1) Inspect Maestro process state: `launchctl list | grep maestro` and check its log file. (2) Identify the failure reason (crash, hung task, auth expiry). (3) Restart the cycle manually: follow Maestro's documented restart procedure. (4) Add a launchd HealthCheck or a cron job that alerts if Maestro's last-cycle timestamp is more than 30 minutes old. (5) Add Maestro cycle status to the estate's `growmos context --brief` output as a monitored metric.

---

### T038 — openclaw gateway crash-looping since April 2026 (MODULE_NOT_FOUND)

**Class:** Cluster Infra  
**Priority:** P3  
**Phase:** —  
**Status:** open  
**Blocked by:** N/A  
**Description:** The `openclaw` gateway has been crash-looping since April 2026 with `MODULE_NOT_FOUND` for `dist/index.js`. openclaw has no Telegram credential configured and is not on the Telegram serving path. The crash-loop is benign to current functionality but consumes restart overhead, generates noise in cluster logs, and represents an unowned broken service.  
**Fix:** Decision required — either: (a) restore openclaw: run `npm run build` in the openclaw repo, push a fixed image via `bin/build-image`, let Flux reconcile; or (b) decommission openclaw: remove the Deployment from Flux, remove the launchd plist (if any), archive the repo. Given openclaw has no active Telegram configuration and the estate has higher-priority work, decommission is the recommended path unless openclaw serves another identified purpose.

---

### T039 — 46/86 Kustomizations NOT READY — systematic investigation and remediation

**Class:** Cluster Infra  
**Priority:** P0  
**Phase:** immediate  
**Status:** open  
**Blocked by:** T026  
**Description:** 46 of 86 Kustomizations are NOT READY as of 2026-09-15 13:04 UTC. This is the parent tracking ticket for the NOT READY cascade. Individual root causes include: the degraded cluster node (T026), failed ExternalSecrets (T002, T015), OTel crash-loops (T011), image-automation failures (T040), and dependency mis-wiring (T009). Each NOT READY Kustomization must be individually investigated, root-caused, and remediated. This ticket tracks the aggregate count and provides a common investigation checklist.  
**Fix:** For each NOT READY Kustomization, run this checklist:
1. `flux get kustomization <name>` → get failure message
2. `flux logs --kind=Kustomization --name=<name>` → get detailed error
3. Map failure to ticket class (secret missing → T015/T002; image → T040; dep → T009/T010; node → T026; OTel → T011)
4. Apply the appropriate fix from the linked ticket
5. `flux reconcile kustomization <name>` → verify it transitions to READY
6. Update count in this ticket

Target: 86/86 READY. Each Kustomization that remains NOT READY after its root cause is addressed must get its own child ticket if the fix is non-trivial.

---

### T040 — image-automation NOT READY — merged code may not be deployed

**Class:** Cluster Infra  
**Priority:** P0  
**Phase:** immediate  
**Status:** open  
**Blocked by:** T007  
**Description:** The `image-automation` Kustomization (Flux `ImageUpdateAutomation` controller) is NOT READY. When the ImageUpdateAutomation controller is down, `bin/build-image` pushes new multi-arch images to GHCR but the image tag is not bumped in the git repo, so Flux never rolls out the new image. Code changes that have been merged and built since image-automation went NOT READY may be silently absent from the running cluster. This is a critical gap in the GitOps delivery pipeline.  
**Fix:** (1) Determine when image-automation last successfully reconciled: `flux get imageupdateautomation -A`. (2) Compare the current image tags in Deployments against the latest GHCR digests: `kubectl get deploy otto-gateway -o yaml | grep image` vs `gh release list` or GHCR package list. (3) If there is a tag gap, manually bump the image tag in the git repo (commit + push, let Flux reconcile) to catch up. (4) Fix image-automation's root cause (likely a dependency or auth issue — check `flux logs --kind=ImageUpdateAutomation`). (5) After fix, verify the next `bin/build-image` push results in an automatic tag bump within 2 minutes.

---

## Phase Roadmap

| Phase | Focus | Key tickets | Exit criteria |
|-------|-------|-------------|---------------|
| **0 — Ownership** | Declare single writer in git | T001 | OWNER.yaml merged; CI lint rule green |
| **1 — Isolate writers** | Remove competing Telegram callers | T002, T003, T004 | Zero 409s in otto-gateway logs over 24h |
| **2 — Real readiness** | /readyz for gateway + golden; fix Flux healthChecks | T005, T006, T007, T008, T030 | Flux reports READY only when pod is functional |
| **3 — Dependency surgery** | Fix dep graph; OTel graceful degradation; credential rotation | T009, T010, T011, T012, T013, T014, T015, T016, T031 | No NOT READY Kustomization blocks the Telegram critical path |
| **4 — State durability** | Postgres conversation store; embedding atomicity; PVCs | T017, T018, T019, T020, T032 | Pod restart preserves all conversation history |
| **5 — Semantic timeouts + chaos** | CI measurement jobs; chaos drills | T021, T022, T023, T024, T035, T036 | Weekly CI job green; all 6 chaos drills pass |
| **6 — Failure domains + observability** | Topology fixes; dashboards; alerts | T025, T027, T028, T029, T033, T034 | Single-node failure produces no Telegram outage; alert fires within 5 min of channel dark |
| **Immediate** | Node recovery; NOT READY cascade; Maestro | T026, T037, T039, T040 | 3/3 nodes Ready; 86/86 Kustomizations READY; Maestro cycling |

---

## Correction: T017 Premise Is Wrong

> **T017 originally stated:** "SqliteConversationStore stores conversation threads in a SQLite file at /data/conversations.db."
>
> **Actual state (verified 2026-09-16 by reading source):** `otto.memory.conversation` is the **active** conversation store in the production answering path. `pipeline.py:843` calls `conversation.record()` and `pipeline.py:661` calls `conversation.recent_messages()`, both backed by `otto_turns` table in the estate's Postgres database (`OTTO_MEMORY_DATABASE_URL`). PR #99 ("a conversation that outlives the pod that held it") implemented this correctly.
>
> **`thread.py`'s `SqliteConversationStore` is not wired into the production answering path at all.** It is unused code — the `Worker` in `otto/ingress/worker.py` calls `answer_envelope()` which bypasses `thread.py` entirely. T017's migration prescription ("migrate SqliteConversationStore to Postgres") was implemented by PR #99 through a different abstraction.
>
> **T017 is demoted to T017b** (verify memory DB is configured and `otto_turns` has rows) and the conversation emptyDir risk is reclassified. The real risk is not emptyDir state but whether `OTTO_MEMORY_DATABASE_URL` is set and the schema is migrated.

---

## Feature Verification Tickets (T041–T058)

> These tickets cover features shipped in hermes-v2 PRs #63–#101 that are implemented in the codebase but have not been verified working end-to-end in production. Most depend on the cluster infrastructure fixes in T001–T040 before they can be verified.

---

### Summary additions to master table

| Ticket | Title | Class | Priority | Phase | Status |
|--------|-------|-------|----------|-------|--------|
| T041 | `otto_turns` Postgres conversation store: verify schema migrated and env configured | Feature Verification | P0 | 4 | open |
| T042 | `thread.py` SqliteConversationStore is dead code — remove or wire | Feature Verification | P2 | 4 | open |
| T043 | Voice STT (ADR22): verify `wants_voice_reply` flag set and speech transcribed | Feature Verification | P1 | feature | open |
| T044 | Voice TTS reply: verify `send_voice()` reaches founder for voice-in messages | Feature Verification | P1 | feature | open |
| T045 | `OTTO_TOOLSETS` unset: tool bridge is a noop — tools never reach the model | Feature Verification | P0 | feature | open |
| T046 | Human gate: verify fail-closed blocks T3 tools and approval path works | Feature Verification | P1 | feature | open |
| T047 | Verify lane: confirm `reply_judge` budget is configured and runs per turn | Feature Verification | P1 | feature | open |
| T048 | MCP estate server: verify estate toolset is wired and estate queries work | Feature Verification | P1 | feature | open |
| T049 | Multi-bot routing: verify staging + alerts bots answer through their own token | Feature Verification | P1 | feature | open |
| T050 | Fast recall: verify pgvector search returns relevant facts in production | Feature Verification | P1 | feature | open |
| T051 | Telegram inline buttons: verify `callback_query` events are processed | Feature Verification | P2 | feature | open |
| T052 | Explorer lane (crew#892 CP3): N-fold fan-out — verify implementation is present | Feature Verification | P1 | feature | open |
| T053 | Streaming/live edit (crew#892 CP2): verify `edit_message` wired in production | Feature Verification | P1 | feature | open |
| T054 | Reasoning lane (`/think`, `/kimi`): verify deep task class reaches the right model | Feature Verification | P1 | feature | open |
| T055 | Progress placeholder for long answers (PR #91 hands 7): verify sent and edited | Feature Verification | P2 | feature | open |
| T056 | Denied command user message (PR #95): verify human-readable denial reaches user | Feature Verification | P1 | feature | open |
| T057 | Conversation history window: verify 12-turn/12-hour defaults work under load | Feature Verification | P2 | feature | open |
| T058 | `reply_binding` envelope field: verify gateway stamps it on every inbound event | Feature Verification | P1 | feature | open |

---

### T041 — `otto_turns` conversation store: verify schema migrated and env configured

**Class:** Feature Verification  
**Priority:** P0  
**Phase:** 4  
**Status:** open  
**Supersedes:** T017 premise (see correction above)  
**PR:** #99 ("a conversation that outlives the pod that held it"), #101 ("Otto can see the conversation he is having")  
**Description:** PR #99 implemented `otto.memory.conversation` — an `otto_turns` table in the estate's Postgres DB. Every answered task writes one row (`pipeline.py:843`), and every subsequent question reads back the last 12 turns (`pipeline.py:661`). This is the correct architecture. However it depends on three conditions being true simultaneously:
1. `OTTO_MEMORY_DATABASE_URL` (or libpq `PG*` vars) is set in the otto-gateway Deployment env
2. The `otto_turns` migration has been applied to that database
3. The DB is reachable at serving time (already tracked via /readyz, T005)

When any condition fails, `recent_messages()` silently returns `[]` and Otto answers each message as if there is no prior conversation — the user sees the bot forget everything, indistinguishable from a pod restart. There is no log line or metric that distinguishes "memory DB unconfigured" from "memory DB unreachable" from "no history yet."  
**Fix:** (1) Verify `OTTO_MEMORY_DATABASE_URL` is in the otto-gateway ExternalSecret — `kubectl exec -n otto-gateway <pod> -- printenv OTTO_MEMORY_DATABASE_URL`. (2) Verify `otto_turns` table exists: `psql "$OTTO_MEMORY_DATABASE_URL" -c "\d otto_turns"`. (3) Verify rows are being written: `psql "$OTTO_MEMORY_DATABASE_URL" -c "SELECT COUNT(*) FROM otto_turns WHERE asked_at > now() - interval '1 hour'"`. (4) Add `OTTO_MEMORY_DATABASE_URL` to the /readyz critical checks (T005). (5) Add an `obs.memory.info("memory.record", ...)` log line when `record()` returns `False` to distinguish unconfigured from unreachable.

---

### T042 — `thread.py` SqliteConversationStore is dead code — remove or wire

**Class:** Feature Verification  
**Priority:** P2  
**Phase:** 4  
**Status:** open  
**Description:** `otto/ingress/thread.py` contains a complete `ConversationStore` protocol and `SqliteConversationStore` implementation with a 12-hour idle timeout, 24-turn cap, and per-principal thread logic. It is never instantiated in `__main__.py` or passed to `Worker`. The production answering path uses `otto.memory.conversation` (Postgres). `thread.py` is dead code.  
**Risk:** A future developer sees the protocol, wires `SqliteConversationStore` backed by `/data/conversations.db` (emptyDir), and introduces the exact problem T017 described. The dead code is a trap.  
**Fix:** Either (a) delete `thread.py` and the SQLite thread implementation entirely, since `otto.memory.conversation` covers the same function with better durability, or (b) wire a `PostgresConversationStore` backed by `otto_turns` to implement the `ConversationStore` protocol for the universal gateway path, replacing `otto.memory.conversation.recent_messages()` call in pipeline.py with a unified interface. Option (a) is the conservative choice.

---

### T043 — Voice STT (ADR22/PR #87): verify `wants_voice_reply` flag is set and speech is transcribed

**Class:** Feature Verification  
**Priority:** P1  
**Phase:** feature  
**Status:** open  
**PR:** #87 (ADR22 "voice ON by default and local-first STT in the image"), #91 (hands 3 & 4: "door senses voice and photos")  
**Description:** ADR22 specifies voice ON by default with local-first speech-to-text in the container image. The Worker (`worker.py:258`) checks `envelope.wants_voice_reply` to decide whether to send a voice reply after the text reply. This flag must be set by whatever processes the inbound Telegram voice note. The local STT model must be loaded in the image and reachable at the point the voice note is received.  
**Gaps to verify:** (1) Confirm the STT model binary/model file is present in the running image: `kubectl exec -n otto-gateway <pod> -- ls /opt/stt/` or equivalent. (2) Confirm a Telegram `voice` message type is correctly handled — the gateway must detect the media type, transcribe via STT, set `wants_voice_reply=True`, and publish the text to NATS. (3) Verify this path in logs: send a voice note to the bot and grep for `wants_voice_reply` in otto-gateway pod logs. (4) If STT is not in the image, identify what commit removed it and restore.  
**Fix:** Read the Dockerfile to confirm the STT model is included. If absent, restore per ADR22. If present but the code path is broken, trace from `otto.surface.bindings.telegram` through to the task envelope.

---

### T044 — Voice TTS reply: verify `send_voice()` reaches the founder for voice-in messages

**Class:** Feature Verification  
**Priority:** P1  
**Phase:** feature  
**Status:** open  
**PR:** #87, #91 ("hands & senses"), worker.py  
**Description:** `worker.py:254–268` calls `plugin.send_voice(secret, reply_to, answer.reply_text)` when `envelope.wants_voice_reply` is True. This is an ADR22 requirement: a voice message in should produce a voice message out. The `send_voice` method must synthesize speech from the reply text and upload it as a Telegram voice note.  
**Gaps to verify:** (1) Confirm the Telegram plugin has a `send_voice` method: `grep -rn "send_voice" otto/`. (2) Verify it is not a stub returning immediately. (3) Identify the TTS backend: is it local (same image as STT) or an API call (which provider)? (4) Send a voice note to the bot and verify a voice reply arrives. (5) If TTS is an API call, confirm the API key is in the ExternalSecret.  
**Fix:** If `send_voice` is missing or stubbed, implement it — TTS via the estate's LiteLLM router (which already handles audio generation) or a local model per ADR22's local-first principle.

---

### T045 — `OTTO_TOOLSETS` unset: tool bridge is a noop — tools never reach the model

**Class:** Feature Verification  
**Priority:** P0  
**Phase:** feature  
**Status:** open  
**PR:** #88 ("bridge the fork's tools into the tool gateway, step 1"), #89 ("provider tool loop and gateway executor, step 2"), #93 ("tool_choice, bridge proof, fail-closed human gate")  
**Description:** `pipeline.py:335` checks `os.environ.get("OTTO_TOOLSETS")`. When the env var is unset or empty, `register_fork_tools()` is never called and Otto has exactly one tool: `note` (which the model is never shown, per `pipeline.py:503`). Otto therefore operates with zero callable tools regardless of the 11 fork tool sets bridged in PRs #88–93 (terminal, web, search, skills, file, vision, TTS, memory, todo, cronjob, code_execution). Every question that requires a tool call returns a `NEEDS_HUMAN` or a hallucinated answer.  
**Verification:** `kubectl exec -n otto-gateway <pod> -- printenv OTTO_TOOLSETS` — if blank, the tool bridge is disabled in production.  
**Fix:** (1) Determine which toolsets are safe to enable for production use — `terminal` and `code_execution` require the most scrutiny (T3 tools behind the human gate). (2) Add `OTTO_TOOLSETS=terminal,web,search,skills,file,vision,memory,todo` (omitting T3 destructive tools until the human gate is verified per T046) to the otto-gateway Deployment env via ExternalSecret or ConfigMap. (3) Verify at boot: grep logs for `register_fork_tools` returning a non-zero count. (4) Send a question requiring a tool ("what is my estate's current CPU usage?") and verify the tool is called and the result is in the reply.

---

### T046 — Human gate: verify fail-closed approval blocks T3 tools in production

**Class:** Feature Verification  
**Priority:** P1  
**Phase:** feature  
**Status:** open  
**PR:** #93 ("tool_choice, bridge proof, fail-closed human gate")  
**Description:** `ToolGateway` is wired with `fail_closed_gate` as the human gate (`worker.py:300`). The gate is designed to block T3 (irreversible/destructive) tool calls until a human approves. The gate mechanism requires a human-facing approval channel — either a Telegram message back to the operator or a separate approval flow. Until T045 enables the tool bridge, this gate is never exercised in production.  
**Gaps to verify:** (1) After T045, send a request that would trigger a T3 tool (e.g., `rm` command through the terminal tool). (2) Verify the gate fires: `worker.answer_failed` should NOT appear; instead the worker should surface a "pending human approval" message. (3) Verify what happens when no approval comes — does the task time out? Does the bus redeliver? (4) Verify approval routing: where does the approval request go, and how does the founder approve? (5) If the gate is truly fail-closed (HUMAN_APPROVAL_REFUSED without an approval path), T3 tools are permanently inaccessible — that may be correct for now but must be documented.  
**Fix:** If the approval channel is not wired, document T3 tools as permanently denied (acceptable) or implement a Telegram-based approval flow.

---

### T047 — Verify lane (PR #92): confirm `reply_judge` budget and per-turn execution

**Class:** Feature Verification  
**Priority:** P1  
**Phase:** feature  
**Status:** open  
**PR:** #92 ("verify lane grades each reply line; a bad shape is asked again once"), #94 ("CP1: verify judge sees the turn's tool receipts")  
**Description:** `pipeline.py:765` calls `reply_judge.judge(statements, context=..., config=..., ledger=..., client=...)`. The verify lane grades each claim in the router's reply and marks it `[unverified]` or clean. PR #94 (CP1) added tool receipts to the judge's context so tool-backed claims can be verified. This is a real second model call per turn (additional LLM cost). Two conditions can silently disable it: (1) the `ledger.charged_usd` already exceeded today's budget before the judge runs, (2) `reply_judge.judge()` returns `None` on any exception.  
**Gaps to verify:** (1) Check `obs.router.info("verify.judged", ...)` in production logs — is `judged=True` for recent turns? (2) Check `clean` vs `total` in those log lines — are any claims being cleared? (3) Verify the judge's budget allocation: does it share the router's `litellm` budget, or does it have its own lane? A budget already consumed by the router's own calls may leave nothing for the judge.  
**Fix:** If verify.judged is always `judged=False`, investigate whether it's a budget exhaustion or a model-call failure. Add a dedicated budget line for the verify lane in `RouterConfig` so it does not compete with the primary router budget. Log explicitly when the judge is skipped due to budget.

---

### T048 — MCP estate server (PR #79): verify estate toolset is wired and estate queries work

**Class:** Feature Verification  
**Priority:** P1  
**Phase:** feature  
**Status:** open  
**PR:** #79 ("name the estate MCP server, so Otto can read state and ask Holmes")  
**Description:** PR #79 wired the estate's MCP server as a named tool so Otto can query estate state (services, deployments, knowledge graph) through a tool call. This depends on: (1) `OTTO_TOOLSETS` including the MCP toolset (blocked by T045), (2) the estate MCP server being reachable from the otto-gateway pod, (3) the `mcp_estate` toolset being registered by `register_fork_tools()`.  
**Gaps to verify:** (1) After T045, include `mcp_estate` in `OTTO_TOOLSETS`. (2) Verify the MCP server URL is reachable: `kubectl exec -n otto-gateway <pod> -- curl <mcp-server-url>/healthz`. (3) Ask Otto "what is the current status of the estate?" and verify the MCP tool is called. (4) Verify "Holmes" queries (estate knowledge graph) work — PR #79 specifically mentions Holmes integration.  
**Fix:** If the MCP server is not reachable from otto-gateway, add a NetworkPolicy allowing the connection or expose the MCP server via a ClusterIP Service in the otto-gateway namespace.

---

### T049 — Multi-bot routing (PR #85): verify staging and alerts bots answer through their own binding

**Class:** Feature Verification  
**Priority:** P1  
**Phase:** feature  
**Status:** open  
**PR:** #85 ("answer through the bot a message came in on")  
**Description:** `worker.py:189–193` uses `envelope.reply_binding` to look up the specific bot (`external_id`) that received the message, not just the tenant. This ensures the staging bot (@OttostageBot) replies through the staging token and the alerts bot replies through the alerts token, even though both serve the same tenant. The feature requires: (1) multiple `channel_binding` rows in Postgres — one per bot, each with its own `external_id` and `outbound_secret_ref`, (2) the gateway stamping `reply_binding` on every inbound envelope with the matched bot's `external_id`.  
**Gaps to verify:** (1) Query `channel_binding`: `psql -c "SELECT channel, external_id, status FROM channel_binding"` — verify rows for both production and staging bots. (2) Verify `reply_binding` is present on published NATS envelopes by checking the task envelope schema. (3) Send a message through the staging bot and verify the reply comes from the staging bot's username, not the production bot.  
**Fix:** If `reply_binding` is absent from envelopes, locate where the gateway mints the `TaskEnvelope` and add the field from the matched `channel_binding.external_id`. If only one channel_binding row exists, register the second bot via the seeding path.

---

### T050 — Fast recall (PR #76, #80): verify pgvector search returns relevant facts in production

**Class:** Feature Verification  
**Priority:** P1  
**Phase:** feature  
**Status:** open  
**PR:** #76 ("the one door remembers"), #80 ("synchronous read stops going through a cross-encoder")  
**Description:** `pipeline.py:645` calls `fast_recall.recall(asked)` — a pgvector dense search fused with full-text search by reciprocal rank fusion. PR #80 removed the slow cross-encoder rerank (31.87s measured p99) from the synchronous path. The feature requires: (1) `OTTO_MEMORY_DATABASE_URL` configured (same DB as T041), (2) the `otto_facts` table to have rows with non-null embedding vectors, (3) an embedding provider configured for the memory write path.  
**Gaps to verify:** (1) After T041 verifies the DB connection: `psql -c "SELECT COUNT(*) FROM otto_facts WHERE embedding IS NOT NULL"` — if zero, all stored facts have null vectors (the silent data-loss from T018). (2) Verify `memory.recalled chars=N` in pipeline logs has `N > 0` for recent turns. (3) Ask Otto something about a previously discussed topic and verify the recall influences the answer.  
**Fix:** If all vectors are null, identify the embedding provider: `kubectl exec <pod> -- printenv | grep EMBED`. If no embedding env var is set, configure one. If set but calls fail, check T018 (embedding timeout).

---

### T051 — Telegram inline buttons (PR #63): verify `callback_query` events are processed

**Class:** Feature Verification  
**Priority:** P2  
**Phase:** feature  
**Status:** open  
**PR:** #63 ("Telegram buttons and voice notes in")  
**Description:** PR #63 added support for Telegram inline keyboard buttons. When Otto sends a message with an inline keyboard, tapping a button generates a `callback_query` update — a different Telegram update type from a regular `message`. The gateway must handle `callback_query` events, extract the callback data, and route them through the same pipeline as text messages.  
**Gaps to verify:** (1) Search `grep -rn "callback_query" otto/` — verify the surface binding handles this update type. (2) Build a test: trigger Otto to send a message with buttons (find which pipeline path produces them) and tap a button. (3) Verify the callback appears in otto-gateway logs as a processed event, not a dropped unknown type.  
**Fix:** If `callback_query` is not handled, add it to `otto/surface/bindings/telegram.py`'s normalize path. The callback data should be surfaced as the message content of a synthetic user turn.

---

### T052 — Explorer lane (crew#892 CP3): verify N-fold fan-out is implemented in codebase

**Class:** Feature Verification  
**Priority:** P1  
**Phase:** feature  
**Status:** open  
**Description:** The git log references crew#892 with at least two checkpoints: CP1 (verify judge sees tool receipts, PR #94, confirmed in codebase) and CP3 (explorer lane for N-fold propose-fix fan-out — mentioned in commit messages but the specific commit was not in the first 80 lines of git log). The explorer lane proposes N parallel solutions and picks the best, used for complex reasoning tasks.  
**Investigation needed:** (1) `git log --oneline --grep="CP3\|explorer" --all` — find the commit. (2) If the commit exists, read the implementation and verify it's wired. (3) If no commit, the feature is on a branch or not yet implemented — create a ticket to implement it or identify what merge it's waiting for.  
**Fix:** After locating the implementation, verify it is reachable via a routing hint (e.g., `/explore <task>`) or automatically triggered for certain task classes.

---

### T053 — Streaming/live edit (crew#892 CP2): verify `transport.edit_message()` is wired

**Class:** Feature Verification  
**Priority:** P1  
**Phase:** feature  
**Status:** open  
**Description:** The git log references crew#892 CP2 as "placeholder edited in place as founder watches; `transport.edit_message()`; progress.edited obs events." This feature sends an initial placeholder message and edits it in-place as the answer streams, giving the founder live feedback during long reasoning tasks. It depends on the Telegram API's `editMessageText` endpoint.  
**Investigation needed:** (1) `grep -rn "edit_message" otto/` — find the implementation. (2) Verify it is called from the answering path for long-running tasks. (3) Verify the `message_id` of the placeholder is threaded through correctly (the placeholder must be sent, its `message_id` captured, and the edit call must have it).  
**Fix:** If not wired: the placeholder is sent via `send_reply()`, the `message_id` must be returned and stored on the context, and `edit_message()` called after each significant step. This requires the plugin to return `message_id` from `send_reply()` — a protocol change.

---

### T054 — Reasoning lane (`/think`, `/kimi`): verify deep task routes to the right model

**Class:** Feature Verification  
**Priority:** P1  
**Phase:** feature  
**Status:** open  
**PR:** #72 ("a reasoning lane you can reach, wait for and parse"), pipeline.py `route_hint()`  
**Description:** `pipeline.py:280–293` parses the `/think` and `/kimi` prefixes and returns `task_class="deep"`. The router's config maps "deep" to the estate's deep reasoning model (Kimi or equivalent). This is the operator's way to request long-form, careful reasoning vs. the fast default lane.  
**Gaps to verify:** (1) Verify `OTTO_ROUTER_TIMEOUT_SECONDS` is long enough for deep lane responses — deep models can take 90–120s. (2) Send `/think what is the meaning of life` and verify a longer, more considered response arrives. (3) Verify the response is not truncated by the Telegram 4096-character limit. (4) Verify `/kimi` routes to Kimi specifically (config: `RouterConfig` "deep" lane).  
**Fix:** If the deep lane times out: increase `OTTO_ROUTER_TIMEOUT_SECONDS` for the deep lane only (add a per-lane timeout config). If the response is truncated: split long replies across multiple Telegram messages.

---

### T055 — Progress placeholder for long answers (PR #91 hands 7): verify sent and edited

**Class:** Feature Verification  
**Priority:** P2  
**Phase:** feature  
**Status:** open  
**PR:** #91 commit c3f69a1 ("one progress line for a long answer, hands & senses 7")  
**Description:** For long-running answers (tool loops, deep reasoning), the spec requires sending one progress placeholder immediately so the founder knows the request was received, then editing it with the final answer. Without this, the bot appears silent for 30–90 seconds during deep reasoning, indistinguishable from being down.  
**Gaps to verify:** (1) `grep -rn "progress\|placeholder\|pending" otto/` — find where the progress message is sent. (2) Verify it is sent before the router call, not after. (3) For a long task (trigger with `/think`), measure the time between the founder's message and the first bot reply — if it exceeds 5s with no typing indicator and no placeholder, the feature is not active.  
**Fix:** If not active: the placeholder must be sent immediately on task receipt (before `answer_envelope`), the `message_id` stored, and the edit called with the final reply. This is tightly coupled to T053 (edit_message).

---

### T056 — Denied command user message (PR #95): verify human-readable denial reaches user

**Class:** Feature Verification  
**Priority:** P1  
**Phase:** feature  
**Status:** open  
**PR:** #95 ("a refused command is a denied turn, and the bus lane shows typing")  
**Description:** PR #95 specified that when the gateway denies a tool call (untrusted principal, wrong tier, human gate refused), the model should relay the denial to the user in plain English rather than going silent. `worker.py:235–240` handles the "no reply text" case by ack'ing silently — this is correct for an untrusted sender (they get silence by design). For a trusted sender whose command was denied by the human gate, the model should have received `"denied: human_gate"` and written a user-facing explanation.  
**Gaps to verify:** (1) After T045 enables tools: send a request requiring a T3 tool as the founder (trusted principal). (2) Verify the bot replies with a human-readable explanation of why the tool was not run. (3) Verify the typing indicator was shown while the model processed the denial and composed the explanation.  
**Fix:** If the denied response is empty: trace `answer_envelope` — the model receives `"denied: <reason>"` as the tool result and must respond. If the model is not generating a reply when all tools are denied, the system prompt may need to instruct it explicitly: "when a tool is denied, explain why in plain English."

---

### T057 — Conversation history window: verify 12-turn/12-hour defaults survive production load

**Class:** Feature Verification  
**Priority:** P2  
**Phase:** feature  
**Status:** open  
**PR:** #99, #101  
**Description:** `otto/memory/conversation.py:77–79` sets `DEFAULT_HISTORY_TURNS=12`, `DEFAULT_HISTORY_CHARS=24_000`, `DEFAULT_HISTORY_WINDOW="12 hours"`. Under production load with multiple principals and surfaces, the query `_RECENT` must remain fast. The `WHERE tenant_id = ... AND surface = ... AND asked_at > ...` clause must be indexed. If the index is missing on `otto_turns`, history reads become full table scans that grow unbounded.  
**Gaps to verify:** (1) Verify indexes exist on `otto_turns`: `psql -c "\d otto_turns"` — look for indexes on `(tenant_id, surface, asked_at)`. (2) Verify history reads complete in under 50ms: instrument with a timing log in `recent_messages()`. (3) After a week of operation, verify the table does not exceed 100MB without a retention policy.  
**Fix:** If indexes are missing: add `CREATE INDEX CONCURRENTLY otto_turns_history_idx ON otto_turns (tenant_id, surface, asked_at DESC)` to the migration chain. Add a `DELETE FROM otto_turns WHERE asked_at < now() - interval '30 days'` retention job scheduled weekly.

---

### T058 — `reply_binding` envelope field: verify gateway stamps it on every inbound event

**Class:** Feature Verification  
**Priority:** P1  
**Phase:** feature  
**Status:** open  
**PR:** #85 ("answer through the bot a message came in on")  
**Description:** `worker.py:190` checks `envelope.reply_binding` — if present, it looks up `find_by_external_id()` to get the specific bot's outbound credential. This field must be stamped by `otto/ingress/gateway.py` when it mints the `TaskEnvelope`, using the matched `ChannelBinding.external_id`. If the field is absent (None), the worker falls back to `find_by_tenant()` which picks whichever bot row comes first — breaking multi-bot routing when two bots serve the same tenant.  
**Gaps to verify:** (1) `grep -rn "reply_binding" otto/ingress/` — verify the gateway stamps it. (2) Check the `TaskEnvelope` Pydantic model: does `reply_binding` exist as a field? (3) Verify a NATS-published envelope has a non-None `reply_binding` field by adding a log line or checking OTel traces.  
**Fix:** If `reply_binding` is never set: find where `TaskEnvelope` is built in `gateway.py`, add `reply_binding=binding.external_id` to the constructor call. If the field doesn't exist in the schema, add it to `otto/spine/envelope.py`.

---

### T060 — `InMemoryNotifier` in production: operator never notified of NEEDS_HUMAN or QUEUED_BUDGET

**Class:** 8 — Observability Gap  
**Priority:** P0  
**Phase:** immediate  
**Status:** fixed (2026-09-16, branch `fix/otel-degraded-readyz`)  
**Root cause:** `otto/boot/pipeline.py:134` hardcoded `notifier=InMemoryNotifier()`. The `Notifier` protocol docstring says "tests use memory, the deployment wires Telegram" — but the wiring never happened. Every NEEDS_HUMAN and QUEUED_BUDGET event since launch was swallowed into a list object that is garbage-collected with the process.  
**Fix applied:** Created `otto/router/telegram_notifier.py` — a stdlib-only `TelegramNotifier` that POSTs to `api.telegram.org/bot{token}/sendMessage`. Updated `_router()` in `pipeline.py` to call `TelegramNotifier.from_env()` first; falls back to `InMemoryNotifier` with a `WARNING` log if `OTTO_TELEGRAM_BOT_TOKEN` or `OTTO_OPERATOR_CHAT_ID` is absent.  
**Remaining work:** (1) Add `OTTO_OPERATOR_CHAT_ID` to otto-gateway's ExternalSecret/Kustomization — the value is the founder's Telegram chat id. (2) After deploy, verify a deliberately-triggered NEEDS_HUMAN (kill LiteLLM mid-request) produces a Telegram message to the operator.

---

### T061 — Verify lane silent failure: `reply_judge` offline returns `None`

**Class:** 8 — Observability Gap  
**Priority:** P1  
**Phase:** feature  
**Status:** open  
**Root cause:** `otto/verify/reply_judge.py` catches all exceptions from `client.complete()` and returns `None`. The router's verify lane treats `None` identically to "lane not budgeted" and "lane offline" — three distinct situations produce identical silent non-verification. The founder sees an unverified response with no indication of which condition applies.  
**Gaps to verify:** (1) Read `reply_judge.py` and identify every `except` block that returns `None`. (2) Check whether the calling router lane logs the `None` outcome with a distinct reason code. (3) Verify whether the OTel span for a `None` outcome carries a `verify.outcome = "exception"` vs `"offline"` vs `"budget_exhausted"` attribute.  
**Fix:** Replace the bare `return None` on exception with a logged warning and a distinct sentinel value or raised exception so the router can distinguish "lane broken" from "lane unavailable". At minimum, log `logger.warning("verify lane failed: %s", exc)` before returning `None`.

---

### T062 — `fast_recall.configured()` silent schema gap

**Class:** 4 — State Durability  
**Priority:** P1  
**Phase:** 4  
**Status:** open  
**Root cause:** `otto/memory/fast_recall.py` `configured()` returns `""` (empty string, falsy) when the `otto_facts` table is missing — indistinguishable from "OTTO_MEMORY_DATABASE_URL not set". A Postgres migration failure or a fresh schema with the table not yet created silences recall entirely with no log and no metric.  
**Gaps to verify:** (1) Verify `otto_facts` table exists: `psql -c "\dt otto_facts"`. (2) Check whether `fast_recall.configured()` returns `""` when the table is absent vs when the env var is absent. (3) Confirm the caller in `pipeline.py` acts identically on both cases.  
**Fix:** In `configured()`: after verifying the env var is set and the Postgres connection succeeds, run `SELECT 1 FROM otto_facts LIMIT 0` and raise or log a distinct error if the table is absent. Return a non-empty string only when both the connection and the schema are confirmed. This turns a silent misconfiguration into an observable startup warning.

---

### T063 — otto-golden webhook still registered to a 404 endpoint

**Class:** 1 — Single Writer  
**Priority:** P1  
**Phase:** 1  
**Status:** open  
**Root cause:** `otto/boot/server.py` `do_POST` returns 404 for all requests — the `POST /telegram-webhook` route was intentionally removed (the module docstring at line 13-21 explains why). However, otto-golden has `OTTO_TELEGRAM_BOT_TOKEN` injected from `otto-staging-telegram` secret, and if a webhook was ever registered for that token pointing to otto-golden's service URL, Telegram is receiving 404s silently. Telegram retries failed webhooks with exponential backoff and eventually stops delivering.  
**Gaps to verify:** (1) Determine whether `OTTO_TELEGRAM_BOT_TOKEN` in `otto-staging-telegram` is a different bot from otto-gateway's token or the same. If the same: one of the two deployments is receiving all messages and the other gets nothing. If different: otto-golden is a separate staging bot that drops all messages. (2) Call `getWebhookInfo` for the otto-golden token: `curl "https://api.telegram.org/bot<token>/getWebhookInfo"`. (3) If a webhook is registered: call `deleteWebhook` to stop Telegram sending to a 404 endpoint.  
**Fix:** If staging bot (different token): deregister the webhook and decommission otto-golden's Telegram wiring (remove the secret mount, remove the `OTTO_TELEGRAM_BOT_TOKEN` env var from otto-golden's deployment). If same token as gateway: this is a two-writer violation — the token must be consolidated to otto-gateway only and the webhook re-registered there.

---

## Phase Roadmap (updated)

| Phase | Focus | Key tickets | Exit criteria |
|-------|-------|-------------|---------------|
| **0 — Ownership** | Declare single writer in git | T001 | OWNER.yaml merged; CI lint rule green |
| **1 — Isolate writers** | Remove competing Telegram callers | T002, T003, T004 | Zero 409s in otto-gateway logs over 24h |
| **2 — Real readiness** | /readyz for gateway + golden; fix Flux healthChecks | T005, T006, T007, T008, T030 | Flux reports READY only when pod is functional |
| **3 — Dependency surgery** | Fix dep graph; OTel graceful degradation; credential rotation | T009, T010, T011, T012, T013, T014, T015, T016, T031 | No NOT READY Kustomization blocks the Telegram critical path |
| **4 — State durability** | Verify otto_turns Postgres; clean up dead code | T017→T041, T042, T018, T019, T020, T032 | Pod restart preserves all conversation history; emptyDir has no conversation data |
| **5 — Semantic timeouts + chaos** | CI measurement jobs; chaos drills | T021, T022, T023, T024, T035, T036 | Weekly CI job green; all 6 chaos drills pass |
| **6 — Failure domains + observability** | Topology fixes; dashboards; alerts | T025, T027, T028, T029, T033, T034 | Single-node failure produces no Telegram outage; alert fires within 5 min of channel dark |
| **Immediate** | Node recovery; NOT READY cascade; Maestro; operator notifier | T026, T037, T039, T040, T060 | 3/3 nodes Ready; 86/86 Kustomizations READY; Maestro cycling; NEEDS_HUMAN fires Telegram alert |
| **Feature** | Unblock and verify implemented features | T043–T059, T061, T062, T063 | Each feature verified with a real production log line per the Empirical Proof Rule |

---

*This document is the live tracking registry for the Hermes estate remediation. Update ticket Status as work progresses. All deploys follow the Flux GitOps path — no `kubectl apply` by hand. Every image pushed via `bin/build-image` must be multi-arch (amd64 + arm64).*
