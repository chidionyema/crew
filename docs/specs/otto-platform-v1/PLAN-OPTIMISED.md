# Otto Platform v1.0 — the optimised execution plan (LAW 51)

Spec of record: the founder's emailed "Otto Agent Platform — Engineering Build Specification v1.0",
captured verbatim at `~/.claude/docs/founder/2026-08-31T1914Z-chidi-onyema-chidionyema-gmail-com-21d0aaa8.md`.
His words after sending it, all binding: new build, new branch, new Telegram channel, current Otto
untouched; BDD; strong verification of every requirement; end-to-end proof automated; tests; edge
cases; network and bandwidth failure coverage; everything is a commercial product — **this one is
the golden goose**; be smart and use MiniMax for raw execution because it is fast, but verify it
strongly, with a final careful verification; needs clever planning; feed progress every 15 minutes.

## Decisions the spec left open — now settled (no menu; each names its receipt)

1. **Bulk lane provider = MiniMax.** His word this evening ("use MiniMax but verify strongly
   because MiniMax is fast... MiniMax can do raw execution"). The spec's own §5 design absorbs the
   risk: bulk-lane output is never self-certified (P1) and the verify lane is a different model
   family, so MiniMax's speed is bought with the Verification Plane, not with trust.
2. **Secrets backend = OCI Vault via ExternalSecrets.** Measured, not chosen: the estate's one
   `ClusterSecretStore` (`idp/platform/secret-store/store.yaml`) is OCI Vault, 34 ExternalSecrets
   ride it, SOPS is absent from the repo, and the provider-independence policy refuses any other
   store. Spec §6's only requirement — secret material never in model context or streams — is met
   with gateway-side handle resolution against that store.
3. **Trace backend = SigNoz (+ Langfuse for model calls).** Both already run in the observability
   namespace (`idp/platform/observability/`); the spec's requirement is trace search by task_id
   and a cost-by-lane panel, which SigNoz serves. Tempo/Phoenix would be a second collector —
   the stitching the headline forbids.
4. **gVisor: decide by measurement in Phase 1.** No RuntimeClass exists today (the estate decided
   "the sandbox is the pod", `idp/tests/test_incident_crew524_sandbox_is_the_pod.py`). The spec
   already names the fallback (tainted pool + restricted PSS + no SA token + default-deny egress);
   Phase 1 probes the OKE version for gVisor and takes it only if it is there.

## What already exists (inventory, so nothing is built twice — LAW 39)

- **NATS JetStream + transactional outbox: EXISTS in production idp** (`platform/event-bus/nats.yaml`,
  `platform/messaging/outbox/`, ADR-0011/0012). Phase 0 adds Otto's subjects and streams — no new bus.
  (A parallel copy sits in the crew repo; the idp one is the platform layer, the crew copy is a
  candidate for deletion under LAW 43 — flagged, not in this plan's path.)
- **Harness: hermes-agent adapter has webhook mode built** (`plugins/platforms/telegram/adapter.py`),
  boot-contract work green (hermes-v2#61), image lane exists.
- **Postgres+pgvector pattern: EXISTS** (`platform/hindsight/postgres.yaml`, pgvector 0.8.6-pg17
  StatefulSet). The memory stack stamps this pattern into the staging namespace; no new invention.
- **Kyverno admission, catalogue-entity enforcement, secrets-never-env: EXIST** and will grade the
  new services from day 0.
- **Eval prior art: partial** (`hermes-v2/estate-evals/`, `hermes-agent/evals/`); DSPy runs nowhere
  yet (crew#513 is its first build) — the spec's eval harness (§11) is new work that subsumes it.
- **Verification Plane: ABSENT** (closest prior art is the verdict-HMAC key wall,
  `platform/verification/verdict-key-wall.yaml`) — this is the genuinely new build, and the moat.
- **Staging namespace EXISTS** (`platform/staging/`) but has no hermes-agent overlay — the new Otto
  lands there, which is exactly what keeps the current Otto untouched.

## Isolation guarantee (his "leave current as is")

New branch in hermes-v2 (`otto-platform-v1`), separate image tag lane, separate namespace
(`otto-staging`) under `platform/staging/`, its own PVC, its own NATS subjects (`otto.*.v1.>`), its
own **new Telegram bot** — a fresh token minted into the vault as a new entry, never printed, held
by one process (the new gateway), so the running Otto's token, PVC, deployment and channel are
untouched by construction. The current Otto's manifests are not edited by any phase.

## Verification spine (his BDD / strong verification / E2E / edge / network words, made concrete)

- One BDD feature per checkpoint (Gherkin, `docs/specs/otto-platform-v1/features/`), each with the
  happy path, at least one edge case, and network/bandwidth scenarios where I/O is touched: NATS
  partition, Telegram API flap, slow provider, egress denial, budget exhaustion.
- The spec's own falsification set is mandatory and automated: forged verdict, replayed verdict,
  absent verdict each leave a task un-completable (§7 acceptance); untrusted-context tier cap (§10);
  false-success eval set with 0 leakage (§11).
- **Final careful verification** = the Verification Plane itself plus the Phase-gate rule: every
  phase's acceptance is a command CI runs, and MiniMax-built work merges only after the judgment
  lane's review AND the BDD suite for that checkpoint is green. No self-scoring (his standing ban):
  the verdict always comes from outside the lane that built the work.

## Optimised (naive → optimised)

Naive: 6 spec phases × (build + review + PR + approval) serially ≈ 40 steps, ~24 PR waves, every
phase waiting on the previous. Bottlenecks: founder approval round trips (R60), CI waves, and the
one cluster.

Optimised:
- **Reuse over build:** Phase 0's bus, outbox, Postgres pattern, admission policies and both trace
  backends already exist — Phase 0 shrinks to subjects + replay CLI + eval corpus + inventory
  generator (4 deliverables, one PR wave each in idp and hermes-v2).
- **Parallel lanes (his "use parallel agents"):** three independent build lanes run concurrently —
  (A) Phase 1 tool gateway + sandbox (idp+hermes-v2), (B) Phase 2 Verification Plane (new service,
  touches nothing A touches), (C) Phase 3 memory stack (stamps the pgvector pattern). Phases 4–5
  are integration and ride after A+B land. MiniMax-lane agents do the raw build inside each lane;
  verification of each lane's output is by a different session/model plus the BDD suite (his
  MiniMax ruling, applied to the build process itself).
- **Batched approvals:** R60 words batched to 3 gates — after Phase 0 (spine live), after Phases
  1+2+3 (the trust core), after Phases 4+5 (the product). Each gate is one founder word on a set
  of green PRs, not a word per PR.
- **Count:** ~40 steps → 19; ~24 PR waves → 8; approval round trips → 3.

## Not doing (spec non-goals, restated so nobody drifts)

No fine-tuning, no persona troupes, no NLI checkers, no path to production, no second bus, no
second scheduler, no touching the running Otto.
