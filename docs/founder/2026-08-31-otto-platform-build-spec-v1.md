---
captured: 2026-08-31T19:14:36+00:00
session: 90c3f0b9-6972-448c-a8b0-3024ed280a8e
cwd: /Users/chidionyema/dev/code
chars: 22314
source: founder prompt, verbatim (founder-doc-capture.py)
---

chidi onyema <chidionyema@gmail.com>
8:11 PM (1 minute ago)
to me

# Otto Agent Platform — Engineering Build Specification v1.0

**Date:** 31 August 2026
**Owner:** Chidi (product + final authority on all T3 actions)
**Audience:** One senior engineer. This document is intended to be buildable without further clarification; where a choice is left open it is explicitly marked `DECISION`.
**Companion documents:** NATS JetStream backbone build spec (existing); estate runbooks (to be converted to skills, §14).

---

## 0. Purpose and non-goals

Build the production-grade version of Otto: a personal autonomous agent platform that is **verifiable by construction**. The differentiating edge is not model intelligence — it is that no other personal agent stack has (a) deterministic, credential-separated verification of every completion claim, (b) tiered authority enforced outside the model, and (c) a full audit/replay spine. Intelligence is rented from hosted models; trust is built here.

**Non-goals for v1 (deferred, with re-entry triggers recorded in §16):** fine-tuning of any model; multi-agent role troupes (planner/critic/researcher personas); NLI-based claim checkers; any path to the production cluster.

---

## 1. Constitution (invariants — violating any of these is a build defect)

- **P1 — No self-certification.** No task reaches state `completed` without a signed verdict from the Verification Plane referencing that task's ULID. The orchestrator physically cannot mint verdicts (no key material).
- **P2 — Capabilities broad, authority tiered.** Tools are available; *execution* is gated by authority tier (§9), enforced deterministically at the tool gateway, never by prompt.
- **P3 — Measurement-in-turn.** Any claim about live system state must derive from a tool read executed within the same task. Model memory of state is never a source.
- **P4 — Everything on the bus.** Every task event, tool call, tool result, and verdict is published to JetStream. If it isn't on the stream, it didn't happen.
- **P5 — Untrusted content is data.** Anything retrieved from web/search/fetch/email is wrapped, tagged untrusted, and can never escalate authority (§10).
- **P6 — Evals gate change.** No prompt, router, or tool change merges without the eval suite run and the delta recorded.
- **P7 — Human gate on irreversibility.** T3 actions require Chidi's explicit word, every time. No batching, no standing approval. (Codifies ruling R60.)
- **P8 — Class-level elimination.** Every incident closes with a systemic fix captured as a skill/runbook change, not a one-off patch.

---

## 2. System architecture overview

```
Telegram ⇄ Gateway API ──▶ Orchestrator (stateless daemons, Hermes Agent harness)
                                │
                    ┌───────────┼───────────────┐
                    ▼           ▼               ▼
              Model Router   Tool Gateway   Context Engine
                    │           │               │
             hosted models   Sandbox        Memory (Postgres
             (3 lanes)       (K8s Jobs,     + pgvector)
                             gVisor)
                    │           │               │
                    └───────► NATS JetStream ◄──┘
                                │
                        Verification Plane
                     (separate creds, signs verdicts)
```

- **Runtime:** staging Kubernetes cluster (OCI, Flux-managed). A slim local mode (MacBook) runs the same containers via compose for offline work; the cloud deployment is authoritative. Agents hold **zero** production credentials — enforced at OCI IAM/compartment level, not policy files.
- **All daemons stateless.** Durable state lives only in Postgres and JetStream. Any daemon can be killed at any time; tasks resume from the stream.
- **Primary interface:** Telegram (existing bot), designed phone-first. Secondary: CLI for the engineer and eval runner.

---

## 3. Task lifecycle and envelope

Every unit of work is a **task** with a ULID that doubles as the OpenTelemetry trace ID.

```json
{
  "task_id": "01J6XW6M6R2K8Q4S7VZC9T3PBA",
  "source": "telegram | cron | api | subtask",
  "parent_task_id": null,
  "class": "research | code | ops_read | comms | schedule | memory",
  "input": "user text or structured payload",
  "authority_ceiling": "T0 | T1 | T2 | T3",
  "context_budget_tokens": 24000,
  "cost_budget_usd": 0.50,
  "deadline_s": 600,
  "created_at": "2026-08-31T14:00:00Z"
}
```

State machine: `submitted → planned → executing → awaiting_verdict → completed | failed | needs_human`. The `awaiting_verdict → completed` transition is the only path to `completed` and requires a valid signed verdict (§7). `needs_human` pushes a Telegram approval card.

---

## 4. Event substrate — NATS JetStream

Reuses the company backbone (existing spec). Otto-specific additions:

**Subject taxonomy (versioned):**

| Subject | Payload | Stream | Retention |
|---|---|---|---|
| `otto.task.v1.<state>` | task envelope + state | OTTO_TASKS (WorkQueue for `submitted`, Limits for the rest) | 90d |
| `otto.tool.v1.req.<tool>` | tool call args (secrets redacted to handles) | OTTO_AUDIT | 180d |
| `otto.tool.v1.res.<tool>` | tool result + exit metadata | OTTO_AUDIT | 180d |
| `otto.verdict.v1.<pass\|fail>` | signed verdict (§7) | OTTO_VERDICTS | 365d |
| `otto.mem.v1.<write\|read>` | memory mutation/query record | OTTO_AUDIT | 180d |
| `otto.metric.v1.>` | cost/latency/tokens per span | OTTO_METRICS | 30d |

- **Dedupe:** `Nats-Msg-Id` = `<task_id>:<seq>`; aligns with the Postgres transactional-outbox + JetStream dedupe pattern already chosen for the backbone. Task submission goes through the outbox table; a relay publishes.
- **Replay is a feature:** the engineer must deliver a `otto replay <task_id>` CLI that reconstructs the full task from streams. This is the debugging story and the audit story.
- Streams: file storage, R1 acceptable on staging; nightly snapshot to OCI Object Storage.

---

## 5. Model router

Three lanes, policy in versioned YAML, hot-reloadable. Hosted inference only (no local weights). Provider selection honors: flat-rate preferred, single stable provider per lane, no provider-specific workflow coupling.

```yaml
lanes:
  judgment:   # planning, ambiguity, final synthesis, anything user-facing
    provider: anthropic
    max_cost_per_task_usd: 0.80
  bulk:       # cron, background, drafts, extraction, summarisation
    provider: DECISION   # DeepSeek vs. the model chosen for the Hermes Agent cron lane — settle before Phase 4
    max_cost_per_task_usd: 0.10
  verify:     # cross-model check lane, used by Verification Plane for text-only claims
    provider: google     # deliberately a different family from judgment lane to break error correlation
routes:
  - match: {source: cron}                       -> bulk
  - match: {class: code}                        -> judgment
  - match: {class: research, complexity: low}   -> bulk
  - default:                                    -> judgment
guards:
  daily_budget_usd: {judgment: 15, bulk: 5, verify: 3}
  on_budget_exhausted: queue_and_notify   # never silent degradation
```

Every model call is a traced span with tokens, cost, latency, lane, and model version recorded to `otto.metric.v1.llm`.

**Structured outputs everywhere.** Every model call uses the provider's schema-constrained/tool-call mode. Universal response contract for answer-producing calls:

```json
{
  "answer": "string",
  "claims": [
    {"text": "string", "evidence_refs": ["tool_call_id | mem_id | url"], "confidence": "high|med|low"}
  ],
  "proposed_actions": [{"tool": "string", "args": {}, "tier": "T0-T3"}],
  "unknowns": ["string"]
}
```

Claims with empty `evidence_refs` are rendered in Telegram prefixed `⚠ unverified:`. This is a rendering rule, not a model instruction — enforced in the gateway.

---

## 6. Tool plane

**Hard cap: 12 core tools in v1.** Tool sprawl degrades selection accuracy; additions require removing or consolidating and an eval run (P6).

| Tool | Tier | Notes |
|---|---|---|
| `web_search` | T0 | existing 3-tier stack: SearXNG → DuckDuckGo keyless → metered fallback; provider recorded per call |
| `web_fetch` | T0 | output always wrapped as untrusted (§10) |
| `fs_read` | T0 | workspace-scoped, path-allowlisted |
| `mem_search` | T0 | §8 |
| `k8s_read` | T0 | staging cluster only, read-only ServiceAccount |
| `code_exec` | T1 | sandbox Jobs (§ below) |
| `fs_write` | T1 | workspace-scoped only |
| `git_ops` | T1 | commit/push to non-default branches only; PR creation is T2; merge is T3 |
| `mem_write` | T1 | provenance mandatory (§8) |
| `telegram_send` | T1 to Chidi / **T2 to anyone else** | |
| `calendar_ops` | T2 | writes only |
| `email_draft` | T2 | drafts only in v1; sending is T3 |

**Tool contract (uniform, JSON Schema published in repo, example):**

```yaml
name: code_exec
tier: T1
idempotent: false
timeout_s: 300
input_schema:  {language: [python, node, bash], code: str, files: [ {path, content_b64} ], allow_network: false}
output_schema: {exit_code: int, stdout: str, stderr: str, artifacts: [{path, sha256, url}]}
errors: [SANDBOX_TIMEOUT, EGRESS_BLOCKED, OOM_KILLED, INVALID_INPUT]
```

The **tool gateway** is a single service that: validates args against schema, checks tier against the task's `authority_ceiling` and the escalation rules (§10), resolves secret handles, executes, publishes req/res to the audit stream, and returns. Models never receive raw credentials — only opaque handles like `secret://github/pat-otto` resolved gateway-side from OCI Vault (or SOPS+age already in the Flux setup — `DECISION`, either acceptable; requirement is only that secret material never enters model context or the audit stream).

**Sandbox execution (`code_exec`):**
- Ephemeral Kubernetes Job per execution on the staging cluster, dedicated node pool.
- RuntimeClass gVisor if available on the OCI Kubernetes version in use; fallback: dedicated tainted node pool + Pod Security `restricted` + seccomp `RuntimeDefault` + no SA token mount + read-only root FS.
- NetworkPolicy default-deny egress. When `allow_network: true` (T2, requires escalation), egress only via an allowlisting proxy (Envoy or Squid) — package registries and explicitly approved domains only.
- Limits: 1 CPU / 2Gi / `activeDeadlineSeconds: 330`. Artifacts out via OCI Object Storage presigned PUT; no shared volumes with the orchestrator.

---

## 7. Verification Plane (Otto edition)

Separate deployment, separate namespace, **separate OCI credentials and its own read-only ServiceAccounts**. The orchestrator and the prover share nothing but the bus.

**Flow:** on reaching `awaiting_verdict`, the orchestrator publishes a claim package: `{task_id, claims[], evidence_spec}`. The prover verifies each claim by the cheapest **deterministic** method available:

| Claim type | Method |
|---|---|
| "code passes tests" | re-run tests in a *fresh* sandbox from the pushed ref; compare exit code + JUnit hash |
| "file written / artifact produced" | independent fetch + sha256 compare |
| "live system state is X" | direct read with the prover's own read-only creds (never trusts the orchestrator's tool output) |
| "source says X" | fetch source, string/semantic containment check |
| text-only judgment claims | cross-model check on the `verify` lane; result marked `soft` — soft verdicts satisfy P1 only for T0/T1 tasks |

**Verdict record (Ed25519-signed):**

```json
{
  "verdict_id": "01J6XX...",
  "task_id": "01J6XW6M...",
  "claim_hash": "sha256:...",
  "method": "rerun_tests",
  "evidence": {"junit_sha256": "...", "exit_code": 0, "ref": "otto/wip-142@a1b2c3"},
  "result": "pass",
  "hardness": "hard | soft",
  "prover_key_id": "vp-ed25519-2026-08",
  "sig": "base64..."
}
```

Public keys ship in orchestrator config; rotation is a documented runbook. **Acceptance test (Phase 2):** a forged verdict, a replayed verdict for a different task, and an absent verdict must each leave the task un-completable; prover credentials must demonstrably fail any write operation against every system they can read.

---

## 8. Memory stack

Single Postgres instance (staging cluster, backed up nightly to Object Storage) with `pgvector`.

**Tables:**
- `facts` — entity store. Columns: `id, entity, attribute, value, provenance (tool_call_id | url | 'chidi_stated'), confidence, created_at, last_verified_at, stale_after, superseded_by`. **Provenance is NOT NULL** — a fact without a source cannot be written; the gateway rejects it.
- `episodes` — compacted task summaries (what was tried, what worked), written at task close.
- `procedures` — successful action sequences, promoted to skills (§14) when repeated.
- `task_history` — envelope + outcome + verdict ref per task.

**Retrieval:** hybrid — pgvector dense (hosted embedding API on the bulk lane) + Postgres FTS as the lexical arm + a hosted reranker over the merged top-40 → top-8. One `mem_search` tool; the fusion is internal.

**Hygiene (this is the actual work):** nightly job flags facts past `stale_after`, detects contradiction pairs (same entity/attribute, different value, no supersession), and posts a weekly review card to Telegram. Memory writes are T1 — automatic but fully audited and reviewable via replay.

---

## 9. Authority tiers (enforced in the tool gateway, deterministically)

| Tier | Meaning | Examples | Gate |
|---|---|---|---|
| T0 | Read-only | search, fetch, fs_read, k8s_read, mem_search | none, audited |
| T1 | Reversible writes inside the workspace | fs_write, code_exec, git branch push, mem_write, telegram→Chidi | none, audited |
| T2 | External side effects, recoverable | PR creation, calendar writes, messages to third parties, sandbox egress | approval card to Telegram; may proceed after explicit tap. Batching allowed |
| T3 | Irreversible / spend / prod-adjacent | merge, deploy, send email, spend > cap, delete outside workspace | Chidi's explicit word, per action, no standing approvals (R60) |

Escalation is impossible from inside a task: `authority_ceiling` is set at submission and only Chidi can raise it (which itself creates a new task).

---

## 10. Injection defense (lethal-trifecta mitigations)

Otto has private data, reads untrusted content, and can act — the classic confused-deputy setup. Mitigations are structural, not prompt-level:

1. **Taint tracking.** Every context block carries a `trust` tag (`chidi | system | tool_trusted | untrusted`). `web_fetch`, `web_search` results, and any inbound third-party text are `untrusted`, wrapped in delimiters, and rendered to the model with an immovable header stating they are data.
2. **The two-source rule.** A task whose context contains any `untrusted` block has its effective authority capped at T1 for the remainder of the task, regardless of `authority_ceiling`. Proposed T2/T3 actions are queued as approval cards showing the untrusted sources that were in context. Enforced in the gateway by inspecting the task's taint set — the model cannot talk its way past it.
3. **Egress control.** Sandbox and orchestrator egress via allowlisting proxy. New domains are a config PR, not a runtime decision.
4. **Secrets never in context** (§6). Audit streams store handles, never material.
5. **Canary red-team suite** (part of the eval harness): ≥10 canned attacks — instructions embedded in a fetched page, in a "search result", in a filename, in an email body, a data-exfil attempt via URL construction, an escalation attempt via mem_write. All must fail; suite runs in CI on every gateway change.

---

## 11. Eval harness — **built first, Phase 0**

Nothing else can be gauged without it, and it operationalises measurement-in-turn for the platform itself.

- **Corpus:** 40–60 tasks extracted from real Otto/Telegram history, classes matching §3. Each has either a golden answer, a programmatic check, or a rubric.
- **Graded dimensions per task:** correctness; groundedness (every claim's `evidence_refs` resolve and actually support it — checked mechanically where possible); tool-path validity (right tools, no flailing); latency; cost; and for the false-success set (≥10 tasks engineered to tempt premature completion claims): leakage rate, target 0.
- **Runner:** CLI (`otto eval run --suite core`) + CI job on staging. Results to Postgres; Grafana dashboard: score by class over time, cost/task, ungrounded-claim rate.
- **Gate:** every change to prompts, router policy, tools, or context engine runs the suite; regressions block (subject to P7 — merges are Chidi's word anyway, but he sees the delta before saying it).
- **Rule:** every future proposal ("add a critic pass", "fine-tune", "add tool X") is admitted or rejected on its measured eval delta, nothing else.

---

## 12. Context engine

- Per-task token budget from the envelope; just-in-time retrieval (mem_search / fetch on demand) over pre-loading.
- Compaction: at 70% budget, summarise-and-swap; the summary is written as an `episode` so nothing is silently lost.
- Subtasks get **fresh, isolated context** with an explicit contract (input, expected output schema, ceiling ≤ parent) — never the parent's transcript.
- Trust tags (§10) survive compaction: a summary of untrusted content is still untrusted.

---

## 13. Observability

- OpenTelemetry throughout; `task_id` = trace id. Spans: model calls (lane, model, tokens, cost), tool calls, verdicts, context compactions.
- Backend: Tempo + Grafana on the estate (or Phoenix if the engineer prefers — `DECISION`; requirement is trace search by task_id and a cost/day-by-lane panel).
- The JetStream audit stream remains the source of truth; traces are for ergonomics.
- Weekly digest to Telegram: tasks by class, verdict pass rate, ungrounded-claim rate, cost by lane, incidents + their class-level fixes (P8).

---

## 14. Skills and runbooks

Estate runbooks are converted into **skills**: versioned markdown procedures in a repo, loaded just-in-time by name. When a task matches a skill, the orchestrator must follow it exactly; deviation requires marking the task `needs_human`. `procedures` rows that recur ≥3 times with pass verdicts are candidates for promotion to skills (a weekly card proposes them; Chidi approves).

---

## 15. Capability inventory

A generated (never hand-maintained) registry answering: every tool Otto has, every credential handle it can resolve, every ServiceAccount and its RBAC, every egress domain, every lane budget. Emitted by CI from the actual config, published as a signed artifact, diffed on every deploy, and viewable via `otto inventory`. **A capability not in the inventory does not exist; a diff without an approved PR is an incident.** This is the platform analog of the estate's inventory-first ruling and ships in Phase 0.

---

## 16. Deferred items and their re-entry triggers

| Deferred | Trigger to revisit |
|---|---|
| Fine-tuning / DPO / RLVR | one task class flatlined on evals for 4+ weeks despite prompt/retrieval iterations, AND that class is high-volume with programmatic reward |
| Multi-agent role troupes | a measured eval failure attributable to single-context limits, not fixable by subtask isolation |
| Parallel research fan-out | allowed now via subtask dispatch (read-only, T0) — not deferred, just scoped |
| NLI claim checkers | ungrounded-claim rate stuck >5% after mechanical evidence checking is exhausted |
| Email send, payments, prod access | email send: after 30 days of clean T2 drafts. Payments/prod: not in scope for this platform at all |

---

## 17. Delivery plan (one senior engineer; durations are estimates, acceptance criteria are not)

**Phase 0 — Spine + measurement (wk 1–2).** JetStream subjects live; existing Otto tool calls published; outbox relay; eval corpus v1 + runner + baseline recorded; capability inventory generator; `otto replay` CLI.
*Accept:* any task replayable end-to-end from streams; baseline eval report exists; inventory artifact generated in CI.

**Phase 1 — Tool gateway, tiers, sandbox (wk 2–4).** Gateway with schema validation, tier enforcement, taint tracking, secret handles; sandbox Jobs + egress proxy; red-team suite v1.
*Accept:* all 10+ canary attacks fail; sandbox cannot reach a non-allowlisted domain (tested); no secret material appears in any stream (scanned); untrusted-context task provably capped at T1.

**Phase 2 — Verification Plane (wk 4–6).** Prover service, separate creds, signed verdicts, completion coupling.
*Accept:* forged/replayed/absent verdicts each block completion; prover creds fail all writes (tested per system); false-success eval set: 0 leakage.

**Phase 3 — Memory + context engine (wk 6–8).** pgvector hybrid + reranker; provenance enforcement; hygiene job; budgets, compaction, subtask isolation.
*Accept:* retrieval precision@8 ≥ 0.8 on the retrieval eval slice; zero facts without provenance (constraint-enforced); stale/contradiction cards demonstrably fire.

**Phase 4 — Router + structured outputs (wk 8–10).** Lane policy, budget guards, universal response contract, unverified-claim rendering, cross-model verify lane.
*Accept:* eval delta per lane recorded; daily budget guard demonstrably queues rather than degrades; ungrounded-claim rate on evals < 5%.

**Phase 5 — Hardening + phone-first polish (wk 10–12).** Approval cards UX, weekly digests, skill promotion flow, chaos pass (kill daemons mid-task, partition NATS), runbook for key rotation.
*Accept:* daemon kill mid-task loses nothing; full platform operable from Telegram alone for a normal week.

---

## 18. Assumptions and open decisions

**Assumed:** staging OKE cluster with Flux exists and has capacity for two small node pools (platform, sandbox); the NATS backbone deploys per its own spec; Postgres available on the estate; Telegram bot identity carries over; all inference hosted (no local weights); Hermes Agent harness remains the orchestrator base — the gateway, verifier, router, and memory are built *around* it as services, so the harness stays swappable.

**Open `DECISION`s for the engineer to bring options on:** bulk-lane model/provider (flat-rate constraint applies); secrets backend (OCI Vault vs SOPS+age); trace backend (Tempo vs Phoenix); gVisor availability on the current OKE version.

---

*End of specification.*

 plan carefully, optinse to go faster, use parallel agents if necessary
