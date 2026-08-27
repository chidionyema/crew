# Architecture gap: the four laws against what runs

Measured 2026-08-25 by session fable-4e5b5e8f (haiku Explore agent af3e8f4d, 55 commands over
crew, idp, prospector-main, hermes-v2). Every value below came from the command in its receipt
column, run that day. Not a generator yet: crew#260 replaces this table with a scheduled run.
Laws: `docs/ARCHITECTURE_LAWS.md`.

## LAW 1: zero-gravity compute

| Fact | Measured | Receipt |
|---|---|---|
| Cloud-specific strings in idp platform manifests outside the provisioner | 0 | `idp/bin/cloud-agnostic-gate` -> 0 (idp#124, merged 4f83383) |
| Residual: Traefik LB annotations | 4 OCI annotations, injected by the cluster row patch, not by the manifest | `kubectl -n edge get svc traefik -o jsonpath='{.metadata.annotations}'` -> 4; `idp/clusters/oke/edge.yaml` patches block |
| Provider-only services in application code (dynamodb, pubsub, oci.object_storage) | 0 uses | `grep -ril` over *.py *.ts *.cs in prospector-main, hermes-v2, excluding node_modules/.venv/.terraform: comments and venv only |
| State that lives inside the cluster instead of a Postgres URL or S3 endpoint | 1 StatefulSet (postgres, ns backstage), 3 PVCs (healthchecks-data, prospector-store-api-data, prospector-data) | `idp/platform/backstage/base/postgres.yaml:20-22,42`; `prospector-main/deploy/k8s/estate/healthchecks.yaml`; `prospector-main/deploy/k8s/base/api.yaml`, `engine.yaml` |

Gap: state. Four workloads keep their data on cluster disks, so the DR scenario (tear down,
rehydrate in 15 minutes) loses them. Close by moving each to the Postgres row and an S3 bucket
(crew#250 pillar 3).

## LAW 2: the fractal primitive

| Fact | Measured | Receipt |
|---|---|---|
| Deployable services (Dockerfile + manifest) | 8: prospector-main 5 (engine, runner, searxng, Store.Web, Store.Api), hermes-v2 2 (hermes-agent, deploy/fly), idp 1 (backstage) | `find` Dockerfiles; `prospector-main/deploy/k8s/base/` |
| Services sharing one DATABASE_URL | 0 | `grep DATABASE_URL\|POSTGRES_URL` across k8s manifests and compose files |
| Event bus or broker manifest (nats, kafka, rabbitmq, redis streams, temporal) | 0 | `grep -ril` over idp/platform, prospector-main/deploy, compose files |
| Services with a Backstage catalog entity | not measured this run | `idp/catalog/` |

Gap: no bus. Every service is isolated by storage already, but they talk by HTTP or not at all,
so a service cannot be replaced behind an event contract. Choose the bus row in STANDARDS.md
first (one, mature), then onboard the 8.

## LAW 3: the default nervous system

| Fact | Measured | Receipt |
|---|---|---|
| OTel Collector / ClickHouse / Langfuse on the cluster | 0 manifests (only Flux in gotk-components) | `grep -ril` over idp/platform/**; k8s |
| The same three as docker-compose on the Mac | 3 files | `idp/observability/langfuse.yml`, `clickhouse-low-memory.xml`, `otel-fallback.yaml` |
| Services that emit OTel | prospector-main 1 (`prospector/otlp.py`); hermes-v2 5+ (`agent/monitoring/otlp_exporter.py`, langfuse plugin, lazy_deps.py, gateway_health_export.py) | file paths as named |
| Emitters not yet collected | 37 | `crew/scripts/estate-snapshot` `uncollected` row (session 9f8f4f5f, 2026-08-25) |
| Alert on a broken workload within 10 minutes | in review: idp#127 | Flux Provider + Alert -> Telegram |

Gap: the nervous system exists only as a laptop compose stack (Mac-bound, crew#247). Close by
deploying the collector pipeline from idp manifests on OKE (blocked on nothing since the cluster
exists; crew#253 is the emitter-registry gate).

## LAW 4: the calibration loop

| Fact | Measured | Receipt |
|---|---|---|
| Brier score computed anywhere in application code | 0 | `grep -r brier --include=*.py --include=*.md` over crew, idp, excluding .venv: library builtins only |
| MLflow deployed | 0 | no manifest or compose file names mlflow |
| Langfuse scoring files | present, Mac compose only | `idp/observability/langfuse.yml`; `idp/sovereign/engine/tracing.py` |
| STANDARDS.md rows | Agent traces (row 27) partially live; Experiments (row 28) MLflow, not deployed | `crew/docs/STANDARDS.md:27-28` |
| Forecast ledger | 30 priors in `crew/science/predictions.jsonl`, 0 scored | `docs/research-engine/CHARTER.md` bootstrap step 3 (crew#256) |

Gap: no prediction is graded. Close in the order CHARTER.md gives: MLflow + Langfuse on OKE
behind the collector, then the ledger writes to the collector and the first three forecasts
are scored.

## The one number

Four laws, zero fully met. LAW 1 is closest (0 cloud strings, 4 stateful workloads left).
LAW 3 and LAW 4 have nothing on the cluster. A buyer's engineer opening this file sees the
measured state, and the next commit to each row is a command in its receipt column.
