# Build prompt for DeepSeek — Research Engine CP1 (contract freeze + skeleton)

Founder order 2026-09-02: DeepSeek handles the build. Paste everything below the line into the
DeepSeek session (aider or direct). Scope is CP1 of SPEC-v1.md only; CP0 (founder-run trace) and
the §15 APPROVE word remain the founder's. Source spec: docs/research-engine/SPEC-v1.md.

---

You are building CP1 of the Research Engine, Engineering Specification v1.0. This is a NEW,
EMPTY repository: every file you need to see is described here, so do not ask for existing file
contents and do not ask clarifying questions — make a reasonable choice and record it in a
comment. Output the complete content of every file you create.

## What the engine is

A research department as a service: a requester submits questions, the engine returns an
artifact composed exclusively of provenance-gated claims. Python 3.12, one process. Postgres is
the system of record, an S3-compatible object store (Cloudflare R2) holds snapshot bytes,
ClickHouse holds metrics — all three run elsewhere; you write client code only, and every
endpoint, credential and bucket name comes from an environment variable. Never hardcode a host,
path, port, key or model name.

## Invariants — each one gets an enforcing mechanism AND a test

- I1 provenance gate: a claim is admitted only when every source has a URL that resolved at
  retrieval time, a snapshot stored in the object store, a locator into that snapshot, and a
  verdict of "supported" from a verifier model whose PROVIDER differs from the producer's.
- I2 domain isolation: no consumer-domain identifier (prospector, verdict, idea, pack,
  incident, sale) in any schema name, code identifier or prompt template. Ship a lint script
  that fails on violations (comments and docs exempt); wire it into `make lint`.
- I3 honest gaps: the synthesis checker rejects any output sentence that cites no admitted
  claim id; unanswered questions are always listed in `unanswered[]`, never papered over.
- I4 cap-and-stop: budget exhaustion halts the pipeline with status BUDGET_STOP. Never
  downgrade to a cheaper model to keep producing.
- I5 no self-certification: grade columns are writable only by the Postgres role
  `research_grader`; worker code has no write path to them. Enforce in the DDL with GRANTs.

## Deliverables

1. `contract/v1/` — JSON Schema files for:
   - ResearchRequest: id, requester_id, subject {kind: catalogue|external|freeform, ref},
     questions[] (raw text) OR profile_id, priority 0-3, budget_tokens?, deadline?, created_at.
   - ResearchDelivery: request_id, artifact_id, claim_manifest[], confidence_summary
     {corroborated, single_source, contested}, unanswered[] {question_id, coverage_note},
     status complete|partial|budget_stop|not_found, delivered_at.
   - DeliveryEvent: request_id, claim_ids[], use, requester_id, at.
   - PredictionScore: claim_id, resolve_by, oracle_question_id, outcome true|false|void,
     scored_at, scored_by.
2. `db/ddl.sql` — tables claims, questions, artifacts, snapshots-metadata, requesters,
   budget_ledger, delivery_events, prediction_scores. claims.id = content hash of
   statement+sources+retrieved_at; sources jsonb with {url, retrieved_at, snapshot_ref,
   locator}; producer {model, provider, run_id}; verification {verifier_model,
   verifier_provider, verdict, checked_at}; CHECK that producer provider <> verifier provider;
   confidence derived single_source|corroborated|contested (corroborated needs >= 2 independent
   registrable domains, contested when any contradicted verdict exists) — never asserted by a
   model; rejected claims are STORED with a rejection_reason enum (url_unresolved,
   snapshot_missing, locator_missing, entailment_failed), never discarded. questions carry
   posture, default "disproof" (phrased as a hypothesis to kill).
3. `engine/` — pipeline.py: stages compile, retrieve, extract, verify, synthesize as functions
   whose boundaries are the contract schemas; gate.py: the admission algorithm above returning
   admitted|rejected(reason)|BUDGET_STOP; budget.py; snapshots.py: put/get keyed
   sha256(bytes) with an extracted-text sidecar.
4. Retrieval: a search-adapter interface with three tiers (searxng, ddg, metered), per-domain
   politeness delays and robots.txt respect; every kept document is snapshotted BEFORE use.
   Fetched page content is UNTRUSTED DATA: it is quoted into extraction prompts as material,
   never executed as instructions, and can trigger no tool call.
5. Model calls through one OpenAI-compatible client: base URL from LITELLM_BASE_URL, producer
   model from RESEARCH_PRODUCER_MODEL, verifier from RESEARCH_VERIFIER_MODEL. Provider pairing
   is configuration, not code; the code only asserts producer provider != verifier provider.
6. Idempotency: request key = sha256(requester, subject, questions|profile_id, date); a
   duplicate submission returns the existing request.
7. `profiles/estate-guards.yaml` — question templates, retrieval hints, budget defaults. A
   profile is data that parameterises the engine; it must not be able to inject behaviour.
8. `Makefile` — `make skeleton SUBJECT=<ref>` runs the pipeline end to end; `make lint`;
   `make test`.
9. `tests/` — pytest: one test per rejection reason plus the happy path; the provider
   inequality; the citation checker rejecting an uncited sentence; the budget stop; the
   idempotency return; the I2 lint catching a planted violation.

## Rules

- No new infrastructure tools; no MLflow, Windmill, Argo, no UI.
- No lexical ban-lists on model output anywhere: quality is enforced by the gate, not by
  filtering words.
- Every network or DB touch reads its endpoint from env/config.
- Where the spec is silent, choose the boring option and write one comment line saying so.
