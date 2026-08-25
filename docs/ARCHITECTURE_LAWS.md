# The Living Estate: four architecture laws

Founder, 2026-08-25 (crew#250), verbatim in the quoted lines. These four laws govern every
line of code the crew writes, in every repository. Proposed rank: the top of the WHAT axis of
`~/AGENTS.md`, above LAW 19; that ranking lands in `~/AGENTS.md` only by the founder's own PR,
this file cannot rank itself into it. A pull request that breaks one
does not merge; the checklist at the end is copied into every PR body and each line is a
command, not a sentence.

The standard stack that implements each law is one row per layer in `docs/STANDARDS.md`;
the acceptance scenarios are in idp `features/cloud-agnostic/` and `features/estate-rebuild/`.
The measured gap between these laws and what runs today is `docs/ARCHITECTURE_GAP.md`,
measured by hand on 2026-08-25; the generator that re-measures it on a schedule is crew#260.

## LAW 1: Zero-gravity compute (extreme portability)

> Compute has no soul. It is entirely disposable. The platform must never know or care whose
> metal it runs on. It must be capable of surviving the instantaneous destruction of its host
> environment.

Mechanism: everything is declared in git and the platform pulls itself into existence (Flux).
State lives only behind universal protocols: S3-compatible storage for objects, the Postgres
wire protocol for relations. Secrets reach a pod through ExternalSecrets and the one
ClusterSecretStore, never a literal. A cloud may be named in three places only: the compute
provisioner, the secret store, the per-cluster row.

The reality: point a blank Kubernetes cluster on any provider at the repository and the estate
reconstitutes itself in ten minutes.

You are breaking it when: a manifest under `platform/` carries a provider annotation; a
StatefulSet or PersistentVolumeClaim holds data the business needs; a service calls a
provider-only API (DynamoDB, Pub/Sub, a vendor object-storage SDK); a human or a CI job runs
`kubectl apply` or `helm install`.

## LAW 2: The fractal primitive (extreme pluggability)

> The whole exists in the part. Any capability must stand alone. Every feature must be built as
> a headless, containerized primitive with an exposed API. There are no monolithic dependencies.

Mechanism: services talk only through declared API contracts and event streams, never by
reading each other's databases. The web UI is a thin shell over those APIs.

The reality, the new-startup test: fork the repository, delete one product module, keep auth,
billing and telemetry, deploy. A secured, enterprise-grade foundation for a new company in
five minutes.

You are breaking it when: two services share a database or a connection string; a module
imports another module's internals instead of its client; a feature has no container image or
no API contract; the UI holds business logic.

## LAW 3: The default nervous system (self-awareness)

> A system that cannot feel its own pain is dead. Nothing goes into the platform without a
> sensor attached to it. Telemetry is not an afterthought; it is a strict admission requirement.

Mechanism: the OpenTelemetry Collector is the spinal cord. Every API request, every agent token
burned, every CI run and every database query fires a trace into one time-series store
(ClickHouse). Alerts are derived from what the platform feels, not from a human looking.

The reality: the platform knows it is sick before a person does: a hallucinating agent, a
slowing checkout, a failing external provider, all felt as latency and error rate.

You are breaking it when: a Deployment ships without an OTLP exporter endpoint; an agent call
produces no trace; a CI run leaves no span; an alert exists only as a log line nobody reads.

## LAW 4: The calibration loop (extreme intelligence)

> Every action is a hypothesis. Every result is a grade. The system must relentlessly grade its
> own performance and adjust its future behaviour based on mathematical reality (Brier scores).
> It does not just alert; it predicts and self-tunes.

Mechanism: the science layer reads the nervous system, predicts outcomes ("this deploy takes
four minutes", "this agent fails this task"), Langfuse grades the prediction when reality
lands, and the model weights adjust. Every prediction is recorded before the outcome, every
outcome is scored, and the score changes future routing.

The reality: the platform gets better every day without new code: it learns which deploys run
slow, which model fails at which reasoning, and routes around the damage.

You are breaking it when: a run produces something worth knowing and nothing records it; a
prediction is made in prose and never scored; a score is computed and nothing reads it.

## The vision: all in all in all

It breathes (pulls its DNA from git and spins up compute on demand), it feels (OpenTelemetry),
it learns (the prediction layer grading itself against reality), it reproduces (modular and
portable enough to spawn child estates for new companies with zero technical debt).

## The pull-request checklist

Copied into every PR body under `## Architecture laws`. Each line is the command that proves
the law for THIS change, or `n/a:` with the reason. A line that is a sentence fails review.

```
## Architecture laws
- LAW 1 zero-gravity: <command, e.g. bin/cloud-agnostic-gate -> 0; no new StatefulSet/PVC>
- LAW 2 fractal: <command, e.g. the service's container builds and its API contract file>
- LAW 3 nervous system: <command, e.g. the Deployment carries OTEL_EXPORTER_OTLP_ENDPOINT>
- LAW 4 calibration: <command, e.g. the prediction row written before the run, the score after>
```

Enforcement, in order of landing: idp `bin/cloud-agnostic-gate` (LAW 1, live); the estate
merge gate refusing a PR body without the four lines (all repos, crew#254); a per-law gate for
each mechanical check as the layer lands (LAW 3 when the collector is on the cluster, LAW 4
when the prediction ledger is).
