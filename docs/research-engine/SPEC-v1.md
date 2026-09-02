---
captured: 2026-09-02T21:16:23+00:00
session: a14fc078-4cf4-4882-8041-20d70d995c89
cwd: /Users/chidionyema/dev/code/crew
chars: 16878
source: founder prompt, verbatim (founder-doc-capture.py)
---

tis is tha spec # Research Engine — Engineering Specification v1.0

**Status:** FINAL pending the rulings in §15. Build starts when §15 lands; nothing else blocks.
**Supersedes:** CHARTER.md R34/R35 stack and scope language; the crew#659 reset ticket (its checkpoints
become §14 of this document); all prior verbal designs.
**Audience:** the engineer or session building it. §§4–13 are the build; §14 is the order; §15 is what
waits on the founder.

---

## 1. What this is

The estate's research department, as a service. It answers questions with evidence: any requester —
the founder, a product lane, an estate/infra lane, a future department — submits a research request
through one contract and receives back an artifact composed exclusively of provenance-gated claims.
The engine knows nothing about business ideas, verdicts, packs, incidents, or any other consumer
domain. Consumers translate their domain into questions on their own side of the boundary and
translate claims back into their own decisions. That boundary is the product.

**Not in scope:** prospector's internals (parked 2026-08-30 until first paying customer), the
mumchimp renderer (follow-on; §5's artifact manifest is what makes it possible later), any UI,
MLflow, Windmill, Argo (deferral trigger in §13).

## 2. Invariants

These hold at every checkpoint. Each is enforced by a mechanism that cannot read English (§11); a
rule enforced only by prose is treated as unenforced.

- **I1 — Provenance gate.** No claim is admitted without a resolvable source, a stored snapshot, a
  locator, and an independent verifier verdict of `supported`. Full algorithm in §7.
- **I2 — Domain isolation.** No consumer-domain identifier appears in the engine's schema, code
  namespaces, or prompts. Enforced as an architectural dependency lint on identifiers and schema
  (docs and comments exempt — the check targets structure, not prose, per founder ruling 2026-09-01
  on context-sensitive wording).
- **I3 — Honest gaps.** `not_found` beats filler. Every factual sentence in an artifact maps to at
  least one admitted claim id; unanswered questions are listed, never papered over.
- **I4 — Cap-and-stop.** Budget exhaustion halts the pipeline cleanly with status `BUDGET_STOP`. The
  engine never downgrades models or quality to keep producing (class elimination of the 2026-08-30
  sourceless-report incident).
- **I5 — No self-certification.** Producers cannot verify their own claims; workers have no write
  path to grades; no checkpoint exits on its own testimony (verification-plane pattern).
- **I6 — Same-turn evidence.** Any status claim about live state ships with the measurement that
  produced it, taken in the same turn.

## 3. Actors and trust boundaries

| Actor | Holds | Never holds |
|---|---|---|
| Requesters (founder, prospector adapter, estate lane, science lane) | contract client, own router key | engine internals, ledger write access |
| Engine workers (compile/retrieve/extract/verify/synthesize) | ledger write via gate, snapshot write, router keys | grade write, cluster API, merge rights, any production credential |
| Grader session | ledger read, grades write, signing key | ledger write, pipeline control |
| Founder | everything above plus rulings | — |

Machine credentials come from the estate vault by OCID via workload identity — no console steps, no
human-held machine secrets (per the 2026-09-02 vault ruling: agents do not hand the founder chores a
credential can perform).

## 4. The contract (v1 — freeze before any CP1 code)

Versioned schemas, committed under `contract/v1/`. Transport: CP1 = CLI + Postgres rows; CP2+ =
JetStream subjects `research.request.v1` / `research.delivery.v1` / `research.event.v1` with the
platform's Postgres-outbox + JetStream-dedupe pattern. Idempotency key =
`sha256(requester, subject, questions|profile_id, date)`; duplicate submissions return the existing
request (today's repeated-payload lesson, applied).

**ResearchRequest**
```
id, requester_id, subject {kind: catalogue|external|freeform, ref},
questions[]? (raw text, founder path) | profile_id? (everyone else),
priority (0 founder · 1 estate/incident · 2 standing sweep · 3 bulk),
budget_tokens?, deadline?, created_at
```

**ResearchDelivery**
```
request_id, artifact_id, claim_manifest[] (admitted claim ids),
confidence_summary {corroborated, single_source, contested: counts},
unanswered[] {question_id, coverage_note},
status: complete|partial|budget_stop|not_found, delivered_at
```

**DeliveryEvent** — emitted by the *consumer* when research is used: `{request_id, claim_ids[],
use: verdict|sale|decision|report, requester_id, at}`. Consumer SDK makes this one call; the founder
path accepts `used <claim-id>` over CLI/Telegram. Outward grade is computed from these events and
nothing else.

**PredictionScore** — `{claim_id, resolve_by, oracle_question_id, outcome: true|false|void, scored_at,
scored_by}`. Every predictive claim carries `resolve_by` and an oracle question at admission; the
scheduler reopens it at deadline; only the grader writes outcomes. (Directly closes the "0 of 11
predictions scored" gap.)

**Engine guarantees:** every manifest claim passed I1 · snapshots retained per §5 · I3 and I4 hold.
**Consumer obligations:** emit DeliveryEvents on use · score predictions they acted on · keep domain
translation in their own adapter (§8).

## 5. Data model

Postgres is the system of record; R2 holds bytes; ClickHouse holds metrics. All three already run on
the platform (idp main: Postgres ×47 manifests, ClickHouse ×25, R2 ×5, JetStream ×7) — the engine
adds no new infrastructure tool.

**claims** — `id` PK = content hash(statement+sources+retrieved_at) · `statement` (one sentence,
falsifiable) · `question_id` FK · `target_ref` · `sources jsonb[]` {url, retrieved_at, snapshot_ref,
locator} · `producer` {model, provider, run_id} · `verification` {verifier_model, verifier_provider,
verdict: supported|contradicted|not_found, checked_at} · `confidence` derived ∈ {single_source,
corroborated, contested} — corroborated requires ≥2 independent registrable domains; contested when
any `contradicted` exists; never model-asserted · `status` admitted|rejected ·
`rejection_reason?` (enum, §7) · CHECK `producer.provider <> verification.verifier_provider`.

**questions** — `id` · `request_id` FK · `text` · `posture` (default **disproof**: phrased as a
hypothesis to kill — prospector's methodology, generalized) · `status`
open|answered|not_found|budget_stop · `answered_by[]`.

**artifacts** — `id` · `request_id` · `synthesis_ref` (R2) · `manifest[]` admitted claim ids only ·
`renderer_profile` · grade columns writable **only** by the grader role (Postgres grant, not
convention).

**snapshots** (R2) — key `sha256(bytes)`; raw bytes + extracted-text sidecar; metadata {url,
retrieved_at, content_type}. Retention: indefinite where any admitted claim references it; 90 days
otherwise (parameter).

**requesters / budget_ledger** — requester_id, router_key_ref, daily_cap, spent_today, priority
floor. **delivery_events**, **prediction_scores** as in §4.

**ClickHouse** — `claims_admitted_daily`, `rejections_by_reason`, `time_to_artifact`,
`delivery_events_weekly`, `budget_burn` — written by the pipeline, read by the grade page. The
grade page computes from these tables and delivery_events; it accepts no testimony.

## 6. Pipeline

`compile → retrieve → extract → verify → synthesize → grade`

CP1 runs this as one Python 3.12 process with stages as functions (default per §15; the router and
search tiers already have Python clients). Stage boundaries are the schemas above, so the CP2+ split
onto JetStream consumers — or a later port of any single stage to .NET — is mechanical.

- **compile** — profile × subject → question set; founder raw questions pass through untouched. The
  catalogue is one subject adapter; external subjects another; ClickHouse/estate telemetry is a
  *source adapter* available to retrieval, not a lane (science-facts folds in here).
- **retrieve** — three-tier search (SearXNG → DDG → metered), per-domain politeness and robots
  respected; every kept document snapshotted to R2 before use.
- **extract** — producer model turns snapshots into candidate claims with locators. Fetched page
  content is **untrusted data**: it is quoted into prompts as material to extract from, never
  executed as instruction, and can trigger no tool call (prompt-injection boundary).
- **verify** — cross-model entailment: does the snapshot at the locator actually support the
  statement? Verifier provider ≠ producer provider, enforced by the DB CHECK and asserted in code;
  verdict and models logged per claim.
- **synthesize** — admitted claims → artifact; a checker pass rejects any synthesis sentence lacking
  a claim-id citation (I3 enforcement); unanswered questions compiled into `unanswered[]`.
- **grade** — separate credentialed session signs the inward verdict; §10.

## 7. Admission gate

```
admit(claim):
  every source URL resolved at retrieval time            else reject(url_unresolved)
  every source has snapshot_ref in R2                    else reject(snapshot_missing)
  every source has locator into its snapshot             else reject(locator_missing)
  verifier(provider ≠ producer).verdict == supported     else reject(entailment_failed
                                                               | contradicted → status contested path)
  budget check passed                                    else halt(BUDGET_STOP)  # I4, not a rejection
→ admitted; derive confidence per §5
```
Rejected claims are **kept and counted** with reasons. Model degradation therefore surfaces as a
rejection-rate spike on the grade page, never as silent bad output. Model choice is a cost dial; the
gate is the quality floor. No model or lexical ban-lists anywhere in the engine.

## 8. Profiles and adapters (the isolation mechanism)

**Profiles are data, never code**: YAML under `profiles/` — question templates, retrieval hints,
renderer parameters, budget defaults. A profile can parameterize the engine; it cannot inject
behaviour.

**Adapters live in the consumer's repo**, never the engine's. The prospector adapter (in
`prospector/`) compiles "is this idea worth pursuing?" into disproof questions, submits a
ResearchRequest, receives claims, and computes its verdict in prospector's own code — the engine
never sees the words. Physical repo separation makes I2 auditable: CP3's deliverable lands in the
prospector repo or it has failed.

**Standing profiles at v1:** `estate-guards` (guard architectures and best practice for multi-agent
estates — also trace #1 per §14), `incident-postmortem` (input: an incident record; output: root-cause
hypotheses to kill, best-practice comparison — the merge breach and the vault circle are case files
#1 and #2), `prospector-vet` (CP3, via adapter). The estate is a standing client, not an
afterthought: incidents, guard logs, and agent-behaviour history are its request stream, and the
scored-claim corpus this produces is the science lane's first real ML dataset.

**Founder path:** priority 0, raw questions, no profile required, budget default generous —
priority and access, never gate exemption: an ungated founder answer would just be bespoke slop.
Entry via CLI now, Telegram once Otto's door is open.

## 9. Scheduling and budgets

Per-requester router keys with fixed daily caps in `budget_ledger`; the platform router makes the
producer/verifier pairing a setting, not code. Priority queue 0–3 with aging so bulk work cannot
starve and product volume cannot crowd out an estate request (the demand-leak failure, closed on the
capacity side as I2 closes it on the semantic side). Cap hit ⇒ I4 clean stop, `BUDGET_STOP` delivery
status, notification — visible stop, never silent degradation.

## 10. Verification and grading plane

The grader is a separate session with its own credential: ledger read, grades write, signing key —
nothing else. Workers cannot reach the grades tables (Postgres grants). Inward grade = grader's
signed re-resolution of sampled claims (id → snapshot → locator → entailment re-check). Outward
grade = DeliveryEvents only. Prediction scoring per §4. Nothing in the grading path accepts a
worker's word for anything — the grade page reads measurements or it reads nothing.

## 11. Security and governance

- Engine workers hold read-only web egress, router keys, ledger-gate write, snapshot write. **Zero**
  cluster API, zero merge rights, zero production credentials — a bad day here is a bad document,
  caught by the grader; that bounded blast radius is why this lane can run autonomously under full
  estate lockdown and is the template for other lanes re-earning autonomy.
- Secrets: vault-by-OCID via workload identity; no human-held machine tokens; no console procedures
  in any runbook.
- Merges: R60 — PR through gates, founder word, Flux applies. No agent merge path.
- Guards for this lane follow the review criteria: out-of-band effect (a guard blocks, halts, or
  pages — it does not advise), no self-satisfiable gates (the actor that produced the output cannot
  operate the gate that judges it), and **guard error ⇒ halt + page** — a fail-closed guard that
  errors into silence is a hole in a uniform.
- Every rule in this spec maps to a mechanism: DB grants (I5), CHECK constraints (verifier ≠
  producer), lint (I2), scheduler (I4), signatures (§10). A rule that exists only as prose gets
  flagged unenforced within 24h.

## 12. Observability

Grade page and feed read from ClickHouse + delivery_events. Paging: standing sweep misses its
schedule ⇒ page; pipeline stalled > N hours with queue non-empty ⇒ page; guard error ⇒ page.
Budget stop ⇒ notify (expected behaviour, not an incident). Metrics that count as progress:
`claims_admitted/day · rejection_rate (by reason) · time_to_artifact · delivery_events/week ·
predictions_scored/outstanding`. Charter edits, checkpoint edits, and grade-scaffolding do not
count. Admitted claims do.

## 13. Runtime plan

CP1: one process, invoked by `make skeleton SUBJECT=<ref>`, state in Postgres/R2/ClickHouse. CP2:
staging cluster via idp as a scheduled job, same evidence re-signed from cluster reads. CP3+:
stages split onto JetStream consumers (`research.*` subjects), outbox+dedupe per the backbone spec —
the engine becomes the backbone's second serious tenant. **Argo deferral trigger:** adopt only when
sweep fan-out measurably exceeds a JetStream consumer group; until then it is out.

## 14. Build order and acceptance (absorbs the reset ticket's CP0–CP5)

- **CP0 — Trace.** Founder runs one subject by hand, session scribes to
  `docs/research-engine/TRACE-<subject>.md`. Trace #1 subject: **estate-guards** (the research the
  founder would do by hand this week anyway; dogfoods the inward profile and stress-tests I2 against
  the exact leak it exists to stop). Trace #2: a prospector target. Exit: founder receipt.
- **CP1 — Contract freeze + skeleton.** Entry: `contract/v1/` schemas committed. Exit: `make
  skeleton` reproduces trace #1 end-to-end through the §7 gate; a second session independently
  resolves every manifest claim id → snapshot → locator → verifier log and signs; founder word to
  merge. Target: one week from CP0 receipt.
- **CP2 — Staging.** Scheduled job on the staging cluster; identical evidence from cluster reads.
- **CP3 — Prospector adapter**, in the prospector repo, verdicts consuming claims, DeliveryEvents on
  use. Revenue becomes the built-in outward signal. (Contingent on ruling 15.2.)
- **CP4 — Unattended volume.** Catalogue sweep live, N subjects/week untouched; grade page fed by
  ClickHouse measurements only.
- **CP5 — Outward reality.** First external consumption recorded through DeliveryEvents; outward
  grade computed from events alone.

Every CP handoff: `Built:/Use:/Expect:/Not done:/Evidence:`; DONE adds `Founder receipt:` (DoD
v2.1). No CP self-certifies (I5).

## 15. Rulings that gate the start (everything else is decided above)

- **15.1** Stack as §5/§13 (Postgres+ClickHouse+R2, JetStream from CP2/3; MLflow, Windmill out;
  Argo deferred). Rides with it: the standards page's Experiments row is rewritten in the same
  change.
- **15.2** Prospector integrates as client #1 **through the §4 contract via a repo-separated
  adapter** — honouring the parked rewrite; if the adapter ever requires prospector-internal
  changes, that is the rewrite by another name and returns to the founder.
- **15.3** Model pairing producer=minimax / verifier=claude via the platform router (different
  providers, DB-enforced), and the founder sets the daily cap number per requester.
- **15.4** CP0 mode: founder-run trace with a session scribing (default), trace #1 = estate-guards.

Reply `APPROVE: spec-v1 15.1 15.2 15.3 15.4` — or strike any number with the change — and CP0
schedules.
