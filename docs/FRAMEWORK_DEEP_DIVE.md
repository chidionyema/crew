# Framework deep dive for the science plane

Written 2026-08-25 for crew #221, after the founder's ruling: "the grounded checks will not be
necessary if we do our job correctly, we need to deeply understand the frameworks we are proposing."

Five research agents each read one framework's official docs online and reported with a URL per
claim. Versions and dates are what the docs and PyPI/GitHub showed on 2026-08-25. This document
answers one question per framework: which of the six behaviours prospector hand-rolls in
`verify.py` does the framework provide, and what is the one design constraint the team must
understand before building on it.

The six behaviours, lettered so the tables can refer to them:

- (a) a verdict grounded only in retrieved evidence, never model memory
- (b) every claim carries a source reference minted by the fetch path
- (c) checks run in kill-fast order, stopping at the first fail
- (d) typed check kinds with a per-check verdict and confidence
- (e) a golden corpus replayed for regression
- (f) per-check calibration against later outcomes

## The finding that matters

No framework provides (a), (b) or (f). Two provide (e). Two provide the plumbing for (d). Argo
provides (c) at the DAG level and nothing else on the list, because it is a scheduler.

So the ruling has a precise consequence. If the six behaviours are still wanted after the rebuild,
they are product code that runs *on* these frameworks; the frameworks supply runs, traces, scores,
datasets, logs and scheduling. If they are not wanted, nothing is lost by dropping `verify.py`.
Either way, none of the five tools is a verification engine and none should be presented to a
buyer as one.

## Per-framework

### Argo Workflows + Hera (scheduler)

Apache-2.0. Argo v4.1.2, 2026-08-21. CNCF Graduated. ~16.9k stars. Hera v7.1.0, 2026-08-18.

| Prospector behaviour today | Argo primitive | Provided |
|---|---|---|
| 2h cadence daemon | `CronWorkflow`, cron syntax, timezone, `startingDeadlineSeconds` | yes |
| overlap control | `concurrencyPolicy: Allow / Replace / Forbid` | yes |
| PAUSE switch | `suspend: true` on the CronWorkflow, `argo suspend / resume` | yes |
| Postgres queue with `FOR UPDATE SKIP LOCKED` leases | none; `synchronization` semaphores and mutexes limit concurrency, they do not lease work items | no |
| (c) kill-fast | DAG `failFast: true` (default) plus `depends:` expressions | yes |
| retries and provider failover | `retryStrategy` with backoff, limit, expression-gated | yes |
| audit row per check | Workflow Archive to Postgres/MySQL; pod logs need a separate artifact repo | partly |
| alerts | `onExit` exit handlers reading `{{workflow.status}}` | yes |
| skip repeated work | memoization keyed on inputs, ConfigMap-backed, 1 MB cap | yes |

Sources: argo-workflows.readthedocs.io pages `cron-workflows`, `synchronization`, `walk-through/dag`,
`enhanced-depends-logic`, `retries`, `workflow-archive`, `walk-through/exit-handlers`,
`memoization`, `installation`; github.com/argoproj-labs/hera/releases;
github.com/cnoe-io/plugin-argo-workflows.

Operational surface: workflow-controller, argo-server, one artifact store (S3 or MinIO). Helm chart
`argoproj/argo-helm/charts/argo-workflows`. Backstage plugin `cnoe-io/plugin-argo-workflows` shows
workflows on the entity page by label selector.

**Understand deeply:** every step is a pod. There is no in-process queue and no lease table. Each
step pays a Kubernetes scheduling round trip in seconds. The `SKIP LOCKED` queue does not lift
one-to-one; it becomes N parallel DAG tasks under a semaphore, which is a redesign, not a port.

### MLflow 3 (runs, datasets, scorers, prompt registry)

Apache-2.0. 3.15.1, 2026-08-03. ~27.7k stars. Linux Foundation.

| Behaviour | MLflow primitive | Provided |
|---|---|---|
| (a) grounded verdict | `RetrievalGroundedness` LLM judge scores a response against retrieved context at evaluation time | evaluation-time only; not a generation-time constraint |
| (b) source per claim | `RETRIEVER` spans carry `doc_uri` per document; no claim-to-source binding | no |
| (c) kill-fast | scorers run independently and concurrently; no early stop | no |
| (d) typed checks, verdict + confidence | `Scorer` (Pydantic, named) returning `Feedback(value, rationale)`; you write the six | plumbing yes, checks no |
| (e) golden replay | `EvaluationDataset` with inputs and expectations, replayed by `mlflow.genai.evaluate()` | yes |
| (f) calibration to outcomes | `log_expectation` / `log_feedback` on traces; SIMBA alignment tunes a judge to human labels | judge-to-human only, not verdict-to-outcome |

Sources: mlflow.org/docs/latest/genai/eval-monitor/scorers/llm-judge/rag/groundedness,
.../scorers/custom, .../scorers/llm-judge/alignment, mlflow.org/docs/3.4.0/genai/concepts/evaluation-datasets,
mlflow.org/docs/3.2.0/genai/tracing/concepts/span, mlflow.org/docs/latest/self-hosting/architecture/backend-store,
docs.databricks.com/gcp/en/mlflow3/genai/overview/oss-managed-diff, pypi.org/project/mlflow.

Storage: SQL backend (Postgres) for metadata, S3-compatible store for artifacts including trace
spans. Trace query is `mlflow.search_traces()`. Open issue mlflow/mlflow#20782 reports a
self-hosted Postgres+S3 setup where the session processor reads traces from SQL only while spans
are written to the artifact store. Test this on our stack before any design relies on SQL trace
queries.

OSS versus Databricks-only: evaluate, tracing and the prompt registry are OSS. The `Safety` and
`RetrievalRelevance` judges, the human-labelling Review App, production monitoring and Unity
Catalog governance are Databricks-managed only.

**Understand deeply:** MLflow's quality checks are LLM judges scoring LLM output. They are
probabilistic. Using them without first running the alignment workflow against human labels swaps
one unaudited model for another.

### Inspect (eval harness, UK AI Security Institute)

MIT. 0.3.260, 2026-08-21. ~2.6k stars.

| Behaviour | Inspect primitive | Provided |
|---|---|---|
| (a) grounded verdict | `Solver` transforms `TaskState` freely; `web_search` tool exists; nothing forces the scorer to use only retrieved output | no |
| (b) source per claim | no forced citation mechanism | no |
| (c) kill-fast | `TaskState.completed`, `message_limit`; per-sample, not an ordered check pipeline | partly |
| (d) typed checks | multiple `Scorer`s per task, each a `Score`, reduced together; confidence needs a custom metadata field | partly |
| (e) golden replay | eval-sets reuse completed samples by id across reruns; no cross-run diff of verdicts | partly |
| (f) calibration | none | no |

Sources: inspect.aisi.org.uk/solvers.html, tools.html, scorers.html, eval-sets.html, eval-logs.html;
mlflow.org/blog/inspect-mlflow-integration; pypi.org/project/inspect-ai.

Storage: `.eval` binary logs (default since 0.3.46) or JSON, in `./logs` or S3/Azure/HF buckets.
Read with `read_eval_log()`, `inspect log list/dump`, `inspect view`. No Langfuse integration. MLflow
integration is the third-party `inspect-mlflow` package (hooks merged upstream), two env vars.

**Understand deeply:** Inspect is a batch eval harness that scores an answer against a known
target. It is not a runtime gate. It gives the harness and the log format; grounding, citation and
calibration would all be custom `Solver` and `Scorer` code.

### Langfuse (traces and scores, already in idp)

MIT core (some enterprise-licensed modules). v4.19.0. ~33.7k stars.

| Behaviour | Langfuse primitive | Provided |
|---|---|---|
| (a) grounded verdict | none | no |
| (b) source per claim | none; spans hold arbitrary input/output | no |
| (c) kill-fast | none | no |
| (d) typed checks, verdict + confidence | Scores API: numeric, categorical, boolean, with comment, attached to trace or observation | plumbing yes |
| (e) golden replay | Datasets and dataset runs, scores per run item | yes |
| (f) calibration | none; a score is a row, the resolution job is yours | no |

**Understand deeply:** Langfuse is observability primitives. It stores what you tell it and lets
you compare runs. It does not verify anything.

### JupyterHub (z2jh) with marimo (research workbench)

BSD (Jupyter), Apache-2.0 (marimo). z2jh chart 4.4.1, 2026-08-10. marimo 0.24.0, 2026-08-17.

Not an eval tool, so the (a)–(f) table does not apply. What it gives: multi-user hub on Kubernetes
with OAuth/OIDC, one PVC per user; marimo notebooks are plain `.py` files with a reactive DAG built
from variable names, so no hidden execution order. No official MLflow or Langfuse integration in
marimo; Argo runs a notebook as a container or papermill step.

**Understand deeply:** marimo's DAG tracks variable *assignment*, not *mutation*. A cell that
mutates a list defined elsewhere does not re-run its dependants. The team writes cells that
reassign, never mutate, or the reactivity promise is false.

## What this changes in the proposal

1. The proposal's table row "Deterministic eval harness: Inspect" is overstated. Inspect is a
   harness with file logs; the determinism is in the scorers we write.
2. The "calibration" capability in the proposal is confirmed as something no framework has. If it
   is built, it is a Temporal job writing Langfuse or MLflow scores, and it is ours to sell.
3. The tool list stands: Argo+Hera, MLflow 3, Langfuse, JupyterHub+marimo. Inspect stays only if
   we want a second eval harness beside MLflow's `evaluate()`; the honest position is that MLflow's
   `EvaluationDataset` plus custom `Scorer`s covers (d) and (e) alone, and Inspect is dropped
   unless a specific need appears. That is the one open decision for #221.

## Definition of done for this document

- Every version and date above matches the source on the day a reviewer checks it, or the row is
  corrected with the new date.
- The mlflow/mlflow#20782 trace-storage gap is reproduced or refuted on our Postgres+R2 stack
  before step 3 of the proposal's DoD (one check logs to MLflow).
