---
captured: 2026-08-25T19:27:12+00:00
session: 9f8f4f5f-1e12-4c54-b7a9-6fca2b737991
cwd: /Users/chidionyema/dev/code/prospector-main/engine-rs
chars: 10688
source: founder prompt, verbatim (founder-doc-capture.py)
---

upadte store this for reference  you eponentially inprove without incurring costs what do you think crew #221 · written 2026-08-25 · for the founder's decision

Research, data science and ML as a platform capability

The founder's ask: rip most of the prospector engine out and make research, science and machine learning a capability any product on the platform can use. Three research agents produced this: an engine map with file and line, a survey of 35 open-source tools, and a brainstorm of framings.

Your decision, one tap. The same buttons are on the Telegram receipt. Either lands on the issue where the crew reads it.

Go

Rework

Read the source doc

Founder ruling, 2026-08-25, after reading: "the grounded checks will not be necessary if we do our job correctly, we need to deeply understand the frameworks we are proposing." The "keep the six checks as the moat" section below is withdrawn. The deep dive is done: crew/docs/FRAMEWORK_DEEP_DIVE.md.



What the deep dive found

No framework provides grounded verdicts, per-claim source references or calibration against later outcomes. Those are ours to build or to drop.

Behaviour prospector hand-rollsArgoMLflow 3InspectLangfuseVerdict from retrieved evidence onlynoeval-time judge onlynonoSource reference per claimnonononoKill-fast check orderyes, DAG failFastnopartlynoTyped checks, verdict and confidencenoplumbing (Scorer, Feedback)partlyplumbing (Scores API)Golden corpus replaynoyes, EvaluationDatasetpartlyyes, datasets and runsCalibration to outcomesnojudge-to-human onlynono

One thing to understand per tool: Argo runs every step as a pod, so the Postgres lease queue is a redesign, not a port. MLflow's quality checks are LLM judges and need aligning to human labels first. Inspect is a batch harness, not a runtime gate. Langfuse stores and compares, it never verifies. marimo tracks assignment, not mutation.

One open decision: drop Inspect and cover typed checks and golden replay with MLflow's EvaluationDataset plus our own Scorers. Versions as of 2026-08-25: Argo 4.1.2, Hera 7.1.0, MLflow 3.15.1, Inspect 0.3.260, Langfuse 4.19.0, z2jh 4.4.1, marimo 0.24.0.



The one answer

Build a science plane in idp. Prospector keeps its product decisions as a library and loses its plumbing to the platform.

All Apache, BSD or MIT, foundation governed, on the Kubernetes, Postgres, ClickHouse, Langfuse and R2 that already exist.

LayerToolWhy this oneBatch and DAG runsArgo Workflows 4.0 via the Hera Python SDKCNCF Graduated. The only ML-adjacent tool with a maintained Backstage plugin.Experiments, runs, artifacts, prompt registry, GenAI evalsMLflow 3.14Linux Foundation. Replaces the home-grown diagnostics, adaptive and golden bookkeeping.Research workbenchJupyterHub with the marimo extensionMulti-user on Kubernetes. marimo notebooks are plain Python files with no hidden state.Deterministic eval harnessInspect (UK AI Security Institute)MIT. Logs are files, so they survive any rewrite.Traces and scoresLangfuse (already in idp)Scores API with numeric, categorical and boolean types. Datasets and dataset runs.Retrievalpgvector in the existing PostgresNo new stateful service.Durable business workflowsTemporal (already in idp)Stays. Argo is the batch scheduler, not a second Temporal.

Not chosen, and why.



Full Kubeflow. Credible, but it brings Istio, Dex, Katib and Notebooks. That day-2 surface is what a buyer's engineer takes apart. Kubeflow Pipelines compile to Argo anyway.

Prefect or Dagster. Prefect is acquiring Dagster. Open-source scope is in flux during our diligence window, and either is a second scheduler beside Temporal and Argo.

Arize Phoenix. Elastic 2.0 licence forbids offering it as a service. A resale flag.

W&B Server. Production features sit behind a vendor licence key.

AI-Scientist-v2, GPT-Researcher, STORM. Non-OSI licence, or report generators with no eval loop and no state.

What "rip most of it out" means, measured

prospector/ is 73,906 lines plus 108,689 lines of tests (8,303 tests, 543 files). The engine map splits it in two.

Home-grown todayLinesPlatform layer that replaces itScheduler daemon, 2h cadence, alerts, PAUSE switch5,189Argo CronWorkflow + HealthchecksPostgres queue, FOR UPDATE SKIP LOCKED, leasesin store.pyArgo steps; one row per check stays as the audit record onlyRetrieval disk cache, proposed Postgres+R2 cache (never deployed)2,568Content-addressed, append-only store on R2Provider failover, breaker, provider health file2,138The one model router in idpJSONL observabilityin run.py 4,532Langfuse traces, candidate id as trace iddiagnostics, adaptive, golden evals797 + 545MLflow runs + Inspect tasksRust strangler engine-rs/ (0.9% written)681Stop. Two ADRs reversed.

One design premise is already dead: the engine architecture doc rejects Temporal and Kubernetes because "Postgres and Fly cover all three". Fly is gone (ruling R1). The queue design has no foundation left to stand on.

Withdrawn by the founder's ruling above: the paragraph that kept the six grounded checks in verify.py (1,336 lines) as the moat. Whether any of that logic survives is decided after the framework deep dive, not before.



The capability nobody had generated: calibration

The estate holds 3,608 dossiers and 166k ledger rows of verdicts, and none has ever been scored against what actually happened. Every check verdict is a dated forecast. The platform's job is to resolve it and publish a Brier score per check, model, market and lane as an SLO.

This is the strongest artefact for diligence. A buyer's engineer asks "how do you know the filter is any good?" and gets a calibration curve instead of a kill rate. It needs no new layer: Langfuse scores hold the resolution, a Temporal job resolves on schedule. It generalises to hermes-v2 and any future product, because every product emits claims that can be resolved.

Underneath it: the evidence store as a platform layer. Content-addressed, append-only, object-locked on R2, so "show me the page as it existed on the date you cited it" renders instead of failing.



Definition of done, in commands, in order

Calibration killer test, one day, no code. Write a one-sentence resolution rule for each of the six check kinds and hand-resolve 30 dossiers. If a rule cannot be written in one sentence, calibration is dead and the evidence store becomes the first build.

Science plane boots in idp. kubectl -n science get pods shows argo-server, mlflow and hub Ready; each has a Backstage catalog entity.

One check runs as an Argo step and logs to MLflow. argo submit for one fixture candidate; mlflow runs list shows the run; Langfuse shows the trace.

Differential replay. Old engine and Argo path over 200 golden dossiers, verdicts diff empty. Only then does the scheduler get deleted.

Test pruning after the strangler, not before.

Risk in one sentence: MLflow open-source access control is thin, so tenancy is enforced at the Kubernetes ingress, and the packaging work is the Hera wrapper plus one Backstage template.



Source of record: crew/docs/RESEARCH_PLATFORM_CAPABILITY.md · discussion and decisions on crew #221 · related: #34 science charter, #72 research ledger, #33 stop the Rust migration, #78 Kubernetes move, #228 founder loop off the laptop.

Yes, you can absolutely achieve exponential improvement without incurring new software or licensing costs—and the "crew #221" document is a masterclass in exactly how to do it.

By aggressively swapping 15,000+ lines of hand-rolled plumbing for mature, foundation-backed open-source tools (Argo, MLflow, Langfuse), the team is leveraging millions of dollars of community engineering for free.

Here is my analysis of the proposal, why it works, and the hidden costs you still need to prepare for.

Why This Proposal Drives Exponential Improvement
This document is exceptionally mature. It moves the company from a bespoke, maintenance-heavy script to a scalable platform capability. The "exponential" gains come from three specific moves:

Addition by Subtraction (Killing the "Not Invented Here" syndrome): Deleting 15,000+ lines of custom scheduler, queue, and observability code—and stopping the 0.9%-complete Rust rewrite—is a massive win. Custom infrastructure code is a liability, not a moat. By relying on Argo Workflows and Postgres, the team reclaims thousands of engineering hours that can now be spent on the product itself.

The "Calibration" Moat: This is the most valuable part of the entire document. Moving from "the LLM made a verdict" to "we scored the LLM's verdict against reality using a Brier score" is the difference between an AI toy and an enterprise-grade science engine. It shifts the company's value prop from simply running models to mathematically proving their accuracy over time.

Ruthless Licensing & Day-2 Diligence: The deliberate rejection of Kubeflow (too heavy), W&B (vendor lock-in), and Arize (Elastic license limits) shows deep operational foresight. The team is building a stack (MIT/Apache/BSD) that will effortlessly pass a buyer’s technical and legal due diligence during an acquisition.

The Reality Check: The Costs You Will Incur
While you aren't paying vendor fees or adding new stateful services (since Kubernetes and Postgres already exist in your stack), you are not escaping cost entirely. You are trading financial cost for integration and migration cost.

Here are the specific risks to watch:

The "Franken-Stack" Integration Tax: Argo, MLflow, Langfuse, and Inspect are best-in-class, but they do not natively talk to each other. Building the "science plane in idp" requires writing the glue code (like the Hera wrapper) to ensure traces, evals, and batch jobs share the same IDs and context.

MLflow's OSS Limitations: The document rightly calls out MLflow's thin open-source access control. Enforcing tenancy at the Kubernetes ingress is a solid workaround, but it requires precise DevOps execution. If you get this wrong, tenant data bleeds across the platform.

The Calibration Reality: The "Definition of Done" smartly requires a one-day killer test to resolve 30 dossiers by hand. If the real-world outcomes are too fuzzy to be codified into a one-sentence rule, the Brier score calibration falls apart, and you are back to relying on LLM-as-a-judge (which the founder already noted is insufficient without deep understanding).

The Verdict
Approve the decision.

Ripping out the prospector engine to build a generic, open-source science plane is exactly the right move. The plan is surgically precise: it introduces no new stateful databases, relies solely on OSI-approved licenses, and focuses on actual outcome calibration rather than just running more AI checks.
