# Research, data science and ML crew: charge, expectations, what exists, bootstrap

Founder, 2026-08-25: "how is this capability going to improve our platform, lanes science
(data), machine learning, research. we have data pipeline set up or not? so we need to be clear
about the charge and expectations for this crew, get up to speed and bootstrap."

Rulings that bind this file: R31, R32, R34, R35. Role file: `roles/science.md`. Method:
`docs/explanation/EXPERIMENTS.md`. Goals ledger: `science/PLAN.md`.

## The charge, one sentence

Make every product on the platform provably right and measurably improving, by generating the
questions nobody asked, running the experiments without a human, and keeping one calibration
ledger that any buyer can read.

## Three lanes, one ledger

| lane | owns | first deliverable | measured by |
|---|---|---|---|
| Research | behaviours 1, 2, 5: hypotheses nobody asked for, experiment design, one-sentence explanation, for any catalog target | done for 3 targets: `STEP1_2026-08-25.md` | hypotheses per target whose test was run inside 14 days |
| Data science | behaviours 3, 4: run the test unattended; every check is a forecast; Brier per source; the calibration curve | forecast ledger with resolved outcomes | `science/predictions.jsonl` scored rows > 0; Brier per prompt/model in MLflow |
| ML | the models under both: routing, evaluation, fine-tunes when a grader shows a gain; provider-agnostic (LAW 34) | second model over the same 3 targets, same prompt, ledgered | Brier of model A vs model B on the same forecasts |

One ledger. `roles/science.md` refuses a second one; MLflow is where the ledger's scores are
tracked, not a replacement for it.

## How it improves each product (R35: a target is a catalog entity)

- prospector: every check in a dossier becomes a forecast with a source locked in R2 and a
  Brier score when reality resolves it. The buyer gets a calibration curve (R34).
- hermes-v2: same contract; its outputs are targets, its claims are forecasts.
- the estate: `SCALE_estate_2026-08-25.md` is the first run; hypothesis 1 there was
  measured true inside the run.
- a new product: add a catalog entity in `idp/catalog/catalog-info.yaml`. The sweep picks it up.

## What exists today (measured 2026-08-25, `scripts/estate-snapshot` science-plane rows)

| asset | state | path |
|---|---|---|
| warehouse | GREEN, DuckDB+dbt, 1 dbt model, rebuilt 2h ago | `crew/science/warehouse.db`, `crew/science/dbt/` |
| scheduler | RED, Dagster installed, 0 processes running | `idp/scheduler/`, `idp/run/dagster/` (44 run dbs) |
| experiment tracker | ABSENT | MLflow named by R34, not installed anywhere |
| forecast ledger | RED, 2 forecasts, 0 scored | `crew/science/predictions.jsonl` |
| declared stores | 28 | `crew/science/sources.json` |
| collectors | hourly `com.founder.sciencecollect` (was not running at 17:24 UTC) | `crew/scripts/science-collect` |
| source lock (R2 object-lock) | ABSENT | nothing fetches-and-freezes a page today |
| prospector outcomes | none: `dossiers` table, 3,608 rows, no outcome column | `prospector/store/prospector.db` |

So: a data pipeline exists (DuckDB + dbt + hourly collectors). A science plane does not: no
experiment tracker, no scored forecasts, no locked sources, no running scheduler.

## R34 tooling against what runs, reconciled (amended by R37, 2026-08-25)

R34 names Argo Workflows + MLflow + Kubernetes. R37 fixes where they run: the Oracle is
cloud-native. Founder, 2026-08-25, verbatim: "a Python 'tapeworm' script writing to a local
SQLite database on your Mac is completely incompatible with the elite, cloud-agnostic standard".
So the data path is one pipeline and it lives in `idp`: every emitter → the OpenTelemetry
Collector on the cluster → ClickHouse → the MLflow + Langfuse inference pod. The Mac holds
nothing load-bearing. `crew/science/` is the backfill and the baseline until the pipeline
receives its first row, then it is read-only history. Dagster on launchd stays the scheduler
only until #78 lands; Argo Workflows replaces it in the PR that brings the cluster. Risk: while
#78 is open the pipeline has no cluster to run on, so steps 1 to 3 below wait on it; steps 4 to
6 do not. Standards rows Scheduling, Experiments and Agent traces (docs/reference/STANDARDS.md) are the
single source for what is live.

## Bootstrap, in commands, in order

1. Emitter registry and gate (#253): one entry per source in the Collector pipeline config in
   `idp`; a writer with no entry cannot land; `scripts/estate-snapshot` prints
   `unregistered emitters` and `uncollected` and either above 0 is a P1. Measured today:
   uncollected=37.
2. MLflow and Langfuse on OKE (blocked by #78): OTel Collector → ClickHouse → MLflow + Langfuse
   pod, deployed from `idp` manifests, backed by the cluster's object store, never a local
   SQLite file. Snapshot row `experiment tracker` goes ABSENT → GREEN.
3. Forecast ledger in the pipeline: `science/outcomes.py predict` gains `resolve <id>
   <outcome>` and writes to the Collector, not to a file; the 30 step-1 priors are backfilled
   from `science/predictions.jsonl`; row `forecast ledger` shows 30, 0 scored. Then run the
   cheapest test per scale unattended (estate H1 is measured; company H1 needs a CDR sample;
   market H5 is a Google Trends pull, £0, 1 hour). Row shows 3 scored, Brier per source.
4. Source lock: every fetched URL is written once to an object-locked bucket in the cluster's
   object store with its hash; a claim carries the object key. Row `source lock` goes GREEN.
5. Second model over the same 3 targets; Brier per model in MLflow. LAW 34 proof.
6. Golden Corpus: the crew researches the first 10 online from the 10 most recent dossier titles
   (topics only), two models per item, locked sources, agreement required. No founder hand.

Each step is a crew issue with the snapshot row as its done-probe.
