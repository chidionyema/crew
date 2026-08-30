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
| Open-web research worker | GPT Researcher, via the router | Apache-2.0; the step that actually reads the web. Added 2026-08-30, see below |
| Durable business workflows | Temporal (already in idp) | Stays; Argo is the batch scheduler, not a second Temporal |

Not chosen, and why (full table with licence, release, stars and URL in the research agent's
output, attached to #221):

- **Full Kubeflow distro.** Graduated 2026-08-17 and credible, but 26.03 brings Istio, Dex, Katib and
  Notebooks. That day-2 surface is what a buyer's engineer takes apart, and KFP compiles to Argo anyway.
- **Prefect / Dagster.** Prefect is acquiring Dagster (combined company from Aug 2026); OSS scope is in
  flux during our diligence window, and either is a second scheduler beside Temporal and Argo.
- **Arize Phoenix.** Elastic 2.0 licence forbids offering it as a service. A resale flag.
- **W&B Server.** Production features sit behind a vendor licence key.
- **AI-Scientist-v2.** Non-OSI licence. Not platform material.
- **STORM (stanford-oval/storm).** MIT, 31,165 stars -- but last pushed 2025-09-30, eleven months
  cold (GitHub API, read 2026-08-30). It is knowledge curation into an article, not a report
  answering a brief, and GPT Researcher already cites its paper as an influence. Read it for the
  method; do not take a cold repository as a platform dependency.
- **GPT-Researcher. THIS ROW WAS WRONG AND IS WITHDRAWN (2026-08-30).** It was rejected here on
  2026-08-25 as "non-OSI licence, or report generators with no eval loop and no state", which
  merged three tools into one sentence and got this one wrong on both halves. Measured from the
  GitHub API on 2026-08-30: licence Apache-2.0 (OSI-approved), 29,201 stars, `pushed_at`
  2026-08-27 -- three days ago, not abandoned. The second half is true and is not a reason to
  reject it: it has no eval loop, because it is not an eval harness. It is the WORKER. See "The
  research worker" below.

## The research worker (added 2026-08-30)

Source: the founder's own note, `~/.claude/docs/founder/2026-08-30T0055Z-the-honest-answer-is-that-gpt-researcher-is-cd422c25.md`, committed to the claude-estate repo. Read that file, not this summary of it.

**The decision: GPT Researcher is the research worker, and it runs against frontier models through
the router. Never a local model.**

The plane above had a hole nobody named on 2026-08-25. Argo schedules, MLflow records, Inspect
scores, Langfuse traces, pgvector retrieves -- and *nothing in the table actually reads the web and
writes an answer*. That is the one job the estate has been doing with hand-written Python since,
which is what LAW 43 exists to stop. The reason the hole was invisible is that the only tool that
fills it had been struck off the list in the same sentence as a non-OSI project, so the list looked
complete.

Why this one, checked rather than recalled (GitHub API, 2026-08-30):

- Apache-2.0. OSI-approved, no resale flag, unlike Arize Phoenix's Elastic 2.0.
- 29,201 stars; `pushed_at` 2026-08-27. Live, not a snapshot.
- It predates the vendor deep-research modes it now gets compared against, so it is a library we
  own the shape of rather than a feature of somebody's product.
- The architecture is a three-role split we can schedule: a planner turns the brief into research
  questions, execution agents crawl in parallel, one per question, and a publisher aggregates. One
  Argo step per role, and the fan-out is the thing Argo is for.
- `report_type="deep"` is recursive tree exploration with configurable breadth and depth;
  `report_source="hybrid"` mixes the open web with our own documents. The founder's note is blunt
  about why it gets a bad reputation: "Most people run it in its shallow default and conclude it's
  weak." A grade of the shallow default is not a grade of the tool.

**The control that makes it safe, and it is not optional.** From the note: the 2026 "Cited but Not
Verified" benchmark found open-source models scored lower on fact-check accuracy than frontier
models, so self-hosting moves the citation-quality risk onto us. "If you point any of these at a
local model to save cost, you get a well-structured report with worse-verified claims, which is
precisely the failure mode you spent tonight building a spec against." That is the same failure
this document already measured from the other end: 3,608 dossiers and 166,000 ledger rows of
verdicts, none ever scored against what happened. A faster way to produce unscored claims is not
an improvement.

So the worker is wired with two hard edges:

1. **Frontier only, enforced by the router, not by a config file.** LAW 34 already says no consumer
   holds a vendor key; the worker gets a router virtual key whose allowed models are frontier. It
   cannot reach a local model by editing an env var, because it never had the key to one.
2. **No report leaves the worker unscored.** The publisher's output is an Inspect eval sample and a
   Langfuse score in the same Argo run that produced it. A run that writes a report and no score is
   a failed run. This is the eval loop the 2026-08-25 rejection said it lacked -- which was true,
   and is now the plane's job rather than the worker's.

Not switched to, and the specific reason each was raised:

- **Stanford STORM** -- for structured article-style synthesis rather than a report answering a
  brief. Different output, and the repository is eleven months cold. Method, not dependency.
- **Local Deep Research** -- only if external API calls become the constraint. They are not; the
  constraint is citation quality, and this option makes that worse by construction.
- **Open Deep Research** -- a smaller codebase to modify rather than a framework to configure. We
  do not want a codebase to modify. LAW 43.

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
