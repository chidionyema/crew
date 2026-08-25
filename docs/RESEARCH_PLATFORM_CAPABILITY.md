# Research, data science and ML as a platform capability

Written 2026-08-25 for crew #221. Founder's ask, verbatim: "i think we need to rip most of it out ...
id rather have research, data science/or science, machine learning as a platform capability that
can enable any part of the platform. i think we under-researched open source tooling."

Three agents produced this: an engine map with file:line, an online survey of 35 open-source tools
with sources, and a brainstorm of framings. Everything below is a claim with its receipt.

## The one answer

**Build a science plane in `idp`. Prospector keeps its moat as a client library and loses its
plumbing to the platform.**

The science plane, all Apache/BSD/MIT and foundation-governed, on the Kubernetes, Postgres,
ClickHouse, Langfuse and R2 that already exist:

| Layer | Tool | Why this one |
|---|---|---|
| Batch / DAG runs | Argo Workflows 4.0 via the Hera Python SDK | CNCF Graduated; the only ML-adjacent tool with a maintained Backstage plugin (cnoe-io/plugin-argo-workflows) |
| Experiments, runs, artifacts, prompt registry, GenAI eval API | MLflow 3.14 | Linux Foundation; 27k stars; replaces `diagnostics.py`, `adaptive.py`, `golden.py` bookkeeping |
| Research workbench | JupyterHub (z2jh chart) with the marimo extension | Project Jupyter; multi-user on K8s; marimo for reactive notebooks |
| Deterministic eval harness | Inspect (UK AI Security Institute) | MIT; logs are files, so it survives any rewrite; test-ladder rung 5 |
| Traces and scores | Langfuse (already in idp) | Scores API with numeric/categorical/boolean types; datasets and dataset runs |
| Retrieval | pgvector in the existing Postgres | No new stateful service |
| Durable business workflows | Temporal (already in idp) | Stays; Argo is the batch scheduler, not a second Temporal |

Not chosen, and why (full table with licence, release, stars and URL in the research agent's
output, attached to #221):

- **Full Kubeflow distro.** Graduated 2026-08-17 and credible, but 26.03 brings Istio, Dex, Katib and
  Notebooks. That day-2 surface is what a buyer's engineer takes apart, and KFP compiles to Argo anyway.
- **Prefect / Dagster.** Prefect is acquiring Dagster (combined company from Aug 2026); OSS scope is in
  flux during our diligence window, and either is a second scheduler beside Temporal and Argo.
- **Arize Phoenix.** Elastic 2.0 licence forbids offering it as a service. A resale flag.
- **W&B Server.** Production features sit behind a vendor licence key.
- **AI-Scientist-v2, GPT-Researcher, STORM.** Non-OSI licence, or report generators with no eval
  loop and no state. Not platform material.

## What "rip most of it out" means, measured

`prospector/` is 73,906 lines plus 108,689 lines of tests (8,303 tests, 543 files). The engine map
splits it in two.

**Plumbing that moves to the platform (delete from prospector):**

| Home-grown today | Lines | Platform layer |
|---|---|---|
| `scheduler/run_scheduled.py` daemon, 2h cadence, alerts, PAUSE switch | 5,189 | Argo CronWorkflow + Healthchecks |
| Postgres queue, `FOR UPDATE SKIP LOCKED`, leases (ADR 0005) | in `store.py` | Argo steps; one row per check stays as the audit record only |
| Retrieval disk cache, proposed Postgres+R2 cache (ADR 0008, never deployed) | in `retrieval.py` 2,568 | Content-addressed WORM store on R2 (see calibration below) |
| Provider failover, breaker, `provider_health.json` | `errors.py`, `health.py`, `operator.py` 2,138 | The one model router in idp (LAW 34) |
| `store/prospector.jsonl` observability | in `run.py` 4,532 | Langfuse traces, candidate id as trace id (already the shape) |
| `diagnostics.py`, `adaptive.py`, `golden.py` evals | 797 + 545 + corpus | MLflow runs + Inspect tasks |
| Rust strangler for the kernel, queue and scheduler (ADR 0006 step 3-4, crew #33: 0.9% written) | 681 | Stop for the plumbing only. The platform now owns queue and scheduling. |

**The moat that stays, as a library any product can import:** the six grounded checks in
`verify.py` (1,336 lines), kill-fast order, source-or-die, verdict-from-retrieval-only, the pack as
a typed IR with two arms (ADR 0010), SourceRef minted only by the fetch path (ADR 0011), the four
lanes, and the prompt templates as `.md` files. These are product decisions, not infrastructure.
ADR 0004 (unit of work is one check for one candidate) also stays: it maps one-to-one onto an Argo
step.

**The pack stays Rust, by founder ruling 2026-08-25 ("still keen on this").** ADR 0010 (the pack is
a typed IR, `Support { Cited(SourceRef), Unverifiable }`, two arms only) and `ENGINE_ARCHITECTURE.md:78`
(packs: Typst + Askama, Rust) and `ENGINE_RUST_REWRITE_SPEC.md:28` (pack gen: Typst + pulldown-cmark
replacing fpdf2 + mistune) stand. Nothing of the pack generator is written in Rust yet; crew #33
measured only `decision.rs` (193 lines) and the retrieval crate. Under R28 the pack generator is
prospector's "pick, package, publish" step, so it is product code, not platform, and it is the one
Rust build that continues.

One design premise is already dead: `docs/ENGINE_ARCHITECTURE.md:85,379` rejects Temporal and
Kubernetes because "Postgres and Fly cover all three". Fly is gone (ruling R1). ADR 0005 has no
foundation left to stand on.

## The capability nobody had generated: calibration

The brainstorm's bet, and mine. The estate holds 3,608 dossiers and 166k ledger rows of verdicts,
and none has ever been scored against what actually happened. Every check verdict is a dated
forecast; the platform's job is to resolve it. Output: a Brier score per (check, model, market,
lane), published as an SLO.

This is the strongest artefact for diligence. A buyer's engineer asks "how do you know the filter
is any good?" and gets a calibration curve instead of a kill rate. It needs no new layer: Langfuse
scores hold the resolution, a Temporal job resolves on schedule. It generalises to hermes-v2 and any
future product, because every product emits claims that can be resolved.

Underneath it: the evidence store as a platform layer. Content-addressed, append-only, object-locked
on R2 (lakeFS or MinIO object lock), so "show me the page as it existed on the date you cited it"
renders instead of 404ing.

## Founder ruling R31 (2026-08-25): the engine is the platform, prospector is a user

Verbatim: "Stop thinking about prospector. Prospector is one customer. I want the research engine
that prospector calls. If prospector needs a due diligence check, it asks the research engine. If
hermes needs a market analysis, it asks the same engine. The engine is the platform."

| Level | What it is | Who uses it |
|---|---|---|
| Platform | Autonomous research engine | Every product |
| Product | Prospector | Due diligence |
| Product | hermes-v2 | Founder ops |
| Product | a future customer | Their use case |

**Five behaviours, proved in this order, before Argo, MLflow or any other tool is touched:**

1. Question generation. From scratch, at any scale (one company, one market, the estate): 10 hypotheses out that nobody asked for. Not fed the old dossiers (R32).
2. Experiment design. One hypothesis in; the test, the data and the method out.
3. Execution. Runs the experiment and records the result with no human in the loop.
4. Calibration. Scores its own predictions against outcomes and publishes a Brier score.
5. Explanation. Says what it learned and why it changed its mind, in one sentence.

The tool table above is now the second question, not the first: pick the cheapest tool that lets
the five behaviours run, and optimise cost after they work. The "Definition of done" below is
reordered by this ruling (R31): step 1 (calibration killer test) stays first because it is behaviour 4
with no code; the science plane boot moves behind a working demonstration of behaviours 1 to 3.
The crew's job is not to port prospector. It is to build the engine that makes prospector obsolete
as a hand-written system.

**Founder ruling R32 (2026-08-25), verbatim:** "why are we concerned with the old dossiers when we
want to exponentially improve things, old dossiers were duck taped together, our new capabilities
should be sneering at this and want to prove they can generate much better ideas for all scales."
So: the 3,608 dossiers and 166k ledger rows are not the engine's input, its training set, or its
yardstick. Their one use is a baseline the engine beats side by side: same company, old dossier
next to new ideas. The calibration section below is read the same way: the Brier score is on the
engine's own forecasts, resolved forward from the day it makes them, not backfilled from the old
ledger. Step 1 of the DoD becomes: pick 5 targets at three scales, let the engine generate, and put
the old dossier beside it.

## Founder ruling R35 (2026-08-25): the research crew is a platform layer for every product

Founder: "they are here to exponentially improve all parts of the estate including prospector,
the capabilities need to be world class on their own and can be purposed to any part of platform
and beyond as we add new product and capabilities." Full text and the drift guard:
`docs/rulings/R35-research-crew-is-a-platform-layer-for-every-product.md`.

How it engages the rest of the platform: in through a `research` issue, a `research generate
<target>` call, or a scheduled sweep over the Backstage catalog; out as a doc in the owning repo,
a ticket on the owner's board, traces in the estate collector, and every prior in one estate-wide
forecast ledger. A new product joins by adding a catalog entity. Step 1 proof at three scales:
`docs/research-engine/STEP1_2026-08-25.md`.

## Definition of done, in commands, in order

1. **Calibration killer test, one day, no code.** Write a one-sentence resolution rule for each of
   the six `check_kind` values and hand-resolve 30 dossiers from the corpus. If a rule cannot be
   written in one sentence, calibration is dead and the evidence store becomes the first build.
2. **Science plane boots in idp.** `kubectl -n science get pods` shows argo-server, mlflow, hub
   Ready; `helm list -n science` shows the three charts; each has a Backstage catalog entity.
3. **One check runs as an Argo step and logs to MLflow.** `argo submit` of `payer_solvency` for one
   fixture candidate, `mlflow runs list` shows the run with the verdict and SourceRefs as artifacts,
   Langfuse shows the trace.
4. **Differential replay.** Old engine and Argo path over 200 golden dossiers, verdicts diff empty.
   Only then does `scheduler/` get deleted.
5. **Test pruning after the strangler, not before** (ADR 0012:559-590).

Risk in one sentence: MLflow OSS RBAC is thin, so tenancy is enforced at the Kubernetes ingress,
and the packaging work is the Hera wrapper plus one Backstage template.

Founder ruling R28 (2026-08-25): this capability is a provider with its own crew; prospector is
one customer, every other part of the estate can be one, each with a signed contract, and the
capability works ahead of demand so prospector already holds hundreds of vetted ranked ideas.

Related: #34 (science function charter), #72 (research ledger has no writer; MLflow runs become the
writer), #33 (stop the Rust migration), #78 (Kubernetes move).
