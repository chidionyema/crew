# R37: research is a crew that looks outward; science/ML is an embedded layer that looks inward

Founder, 2026-08-25, framing: "so that the expectations are clear, ignore the actual implementation,
you don't need to follow exactly unless I say so but the principle and architecture is key."

The directive follows verbatim (table cells were flattened by the paste; the wording is his).

## Verbatim

THE SPLIT

| | Research | Science / ML |
|---|---|---|
| Direction | Outward — discovers the world | Inward — understands itself |
| Feeds | Products, crews, capabilities | Guards, jobs, predictions, baselines |
| Question | "What should we build?" | "When will it be ready? Is it broken? Is it improving?" |
| Data source | Dossiers, markets, competitors | Transcripts, CI runs, agent sessions, guard triggers, job latencies |
| Output | Hypotheses, experiments, verdicts | Predictions, grades, alerts, self-healing triggers |
| Adoption rule | Experiment team decides, founder has last call | Embedded everywhere, always on, no opt-out |

Research is a crew. Science/ML is a layer.

WHAT DATA IS BEING THROWN AWAY RIGHT NOW

Every component in your estate is screaming and nobody is listening:

| Source | Data produced | Currently | Should be |
|---|---|---|---|
| Agent sessions | Transcripts, token burn, latency, halt reasons | Ephemeral, lost when session dies | Feeds prediction model: "this session pattern usually fails at step 5" |
| CI runs | Duration, failure mode, retry count, queue depth | GitHub logs, deleted after 90 days | Feeds baseline: "builds are 20% slower than last week, investigate" |
| Guard triggers | goal-guard, dod-guard, idle-guard blocks | Terminal output, ephemeral | Feeds behavior model: "this agent type triggers idle-guard 3x more" |
| Oracle sign-ins | Time to sign-in, failure reason, retry count | Manual debugging only | Feeds prediction: "founder sign-in usually takes 2 min, it's been 10, something is wrong" |
| Budget burns | Token consumption per step, per model, per agent | Manual inspection | Feeds forecast: "at current burn, budget exhausts in 4 hours" |
| Merkle commits | State diff sizes, branch frequency, merge conflicts | Storage only | Feeds pattern: "this agent produces 3x larger diffs than others, likely hallucinating" |
| Telegram receipts | Response time, action type, founder interruption rate | Chat history | Feeds presence model: "founder usually approves in 30s, it's been 5 min, escalate" |
| Crew PRs | Review time, rework count, qa failures, merge time | GitHub metrics | Feeds team health: "crew#241 has 3 reworks, predict 2 more days" |

You are flying blind. Every prediction you want — "when will infra be ready?" — requires this data.
It is being produced and discarded.

THE EMBEDDED SCIENCE LAYER (No New Infrastructure)

We do not need a Kubernetes science plane to start. We need a data parasite — a thin layer that
attaches to everything already running and exfiltrates metrics.

Phase 0: The Telemetry Tapeworm (This Week)

One script: ~/.estate/science/ingest.py

    # Runs every 60 seconds. Attaches to everything.
    # Writes to ~/.estate/science/metrics.db (SQLite, local, free)
    tables:
    - agent_sessions (session_id, start_time, end_time, tokens_burned, halt_reason, final_state)
    - ci_runs (pr_number, job_name, duration_sec, result, retry_count)
    - guard_triggers (guard_name, agent_name, timestamp, reason, resolution)
    - founder_actions (action_type, response_time_sec, device, timestamp)
    - budget_events (session_id, event_type, amount, remaining, timestamp)
    - merkle_commits (session_id, commit_hash, diff_size_bytes, parent_hash, timestamp)
    - crew_prs (pr_number, review_time_hours, rework_count, qa_failures, merge_time_hours)

How it captures: reads ~/.estate/dag/ for Merkle data; reads ~/.claude/ transcripts for session
data; polls GitHub API for CI/PR data; reads ~/.estate/interventions/ for founder action data;
reads Langfuse traces for agent behavior data.

No new services. No new cloud bills. One SQLite file on your Mac.

Phase 1: The Living Oracle (Week 2-3)

Queries on the telemetry database:

| Query | Prediction | Action |
|---|---|---|
| Average CI duration last 7 days vs. today | "Build will finish in 45 min ± 10 min" | Surface to founder if >2x normal |
| Guard trigger rate per agent type | "Agent X has 3x idle-guard blocks, likely stuck" | Auto-halt, alert founder |
| Founder response time trend | "Founder usually responds in 30s, currently 10 min, may be away" | Escalate to haptic, do not spam |
| Budget burn rate vs. allocation | "Budget exhausts in 4 hours at current rate" | Pre-authorization request |
| Session failure pattern | "Sessions with >5 state transitions fail 80% of the time" | Auto-halt at transition 4 |
| Crew velocity trend | "PR rework rate up 40%, predict 2 more days for crew#241" | Surface to founder, adjust expectations |

Phase 2: Self-Improving Predictions (Month 2)

Every prediction gets a Brier score:

    prediction: "CI will finish in 45 min"       actual: 52 min    Brier: (0.75 - 0)^2 = 0.5625 (if 75% confidence)
    prediction: "Budget exhausts in 4 hours"     actual: 3.5 hours Brier: (0.80 - 0)^2 = 0.64 (if 80% confidence)

The model adjusts its confidence based on historical accuracy. If it is consistently over-confident
on CI times, it widens the interval. The oracle learns its own mistakes.

HOW RESEARCH AND SCIENCE INTERACT

Founder (last call on adoption) sits above both. Research (outward) discovers new markets,
competitor moves, capabilities to adopt. Science/ML (inward) predicts when infra will be ready,
which agents will fail, founder availability. Between them: "Research says X improves estate;
Science says it will take 3 days." Research feeds the Experiment Team (run test? adopt? timeline?
founder has last call). Science feeds the Embedded Layer (embedded in agents, CI, guards, budget,
founder UI).

The loop:
1. Research discovers a capability that could improve estate
2. Science predicts: "adoption will take 3 days, CI will slow 20%, 80% confidence"
3. Experiment team decides: "worth it" or "not now"
4. Founder has last call
5. If adopted, Science measures actual vs. predicted, improves next prediction

WHAT YOU BUILD FIRST (This Week)

Day 1-2: Telemetry Tapeworm — ingest.py running every 60s; SQLite schema for the 7 tables above;
backfill from existing logs (transcripts, CI history, Merkle DAG).
Day 3-4: First Predictions — "CI duration forecast" (simple linear regression on historical data);
"Budget exhaustion forecast" (token burn rate projection); "Guard trigger alert" (anomaly detection
on guard frequency).
Day 5-7: Founder Dashboard — one web page: localhost:8080/science; shows predictions, baselines,
anomalies, Brier scores; updates every 5 minutes from SQLite.

No Kubernetes. No Argo. No MLflow. Python + SQLite + cron.

YOUR ROLE IN THE DESIGN

| Decision | Your call |
|---|---|
| Which predictions matter most? | You pick: CI time? Budget? Founder availability? |
| What is "good enough" accuracy? | 70%? 80%? You set the threshold |
| When does Science escalate to you? | Anomaly >2x baseline? Prediction failed? You define |
| Which data is sensitive? | Transcripts? Founder actions? You gate access |

My role: Architecture the tapeworm, the schema, the prediction queries. Validate with you. Hand to crew.
Crew's role: Build ingest.py, run backfill, wire to dashboard.

THE ONE SENTENCE

Research discovers what to build. Science predicts when it will be ready, if it will break, and
whether the founder can be interrupted. Both are mandatory. Neither can wait.

## Second message, same day, verbatim — the implementation is cloud-native (R36, crew#250), not a Mac script

"this is crucial. The conceptual split you just defined is brilliant. It perfectly categorizes the
chaos. Research is the scout (Outward). Science is the central nervous system (Inward). However,
the implementation plan in that pasted text — a Python 'tapeworm' script writing to a local SQLite
database on your Mac — is completely incompatible with the elite, cloud-agnostic standard we just
established. If we build a local SQLite script, we violate the 'Disposable Compute' rule. If your
Mac goes to sleep or gets stolen, the Oracle dies. Here is how we take your exact conceptual split
and build it natively into the idp platform so it is bulletproof, scalable, and truly embedded.

The 'Living Oracle' Architecture (Cloud-Native). To make predictions like 'When will the
infrastructure be ready?' based on transcripts and PRs, the Science layer cannot be a script that
polls for data. It must be an event-driven nervous system built directly into the Kubernetes cluster.

1. The Nerve Endings: OpenTelemetry (OTel). Instead of a script scraping your laptop, we deploy an
OpenTelemetry Collector as a DaemonSet in your cluster. Every time an agent writes a transcript, it
pushes a trace to OTel. Every time a CI run starts, GitHub Actions pushes a webhook to OTel. Every
time a budget guard is triggered, it emits an OTel metric. Why this is elite: OTel is the industry
standard. It is cloud-agnostic. No matter where the platform runs, the telemetry flows instantly
without polling.

2. The Universal Memory: ClickHouse (or TimescaleDB). Time-series data (metrics, logs, traces)
destroys standard Postgres databases at scale. OTel streams all this raw data into a columnar
analytical database like ClickHouse (which is open-source and cloud-agnostic). Why this is elite:
ClickHouse can run aggregations on 100 million rows in milliseconds. When your Oracle needs to
calculate the average CI duration over the last 90 days to predict today's build, it happens instantly.

3. The Oracle Engine: MLflow + Langfuse. This is where the 'Science' layer actually lives. We deploy
a lightweight ML inference pod that subscribes to the OTel data. The Readiness Predictor: It looks
at the current agent transcript (e.g., 'Agent is stuck on step 4'), compares it to the ClickHouse
history of similar tasks, and outputs: 'Prediction: idp#121 will merge in 45 minutes (80%
confidence).' The Auto-Grader (Brier Scores): Langfuse logs the Oracle's prediction. When the PR
actually merges 52 minutes later, Langfuse calculates the Brier score and feeds it back to MLflow to
tune the model for next time.

How It Changes the Platform Experience. When Science is truly embedded, you don't look at dashboards
to find out what went wrong. The platform tells you what is about to go wrong.

| Capability | What it does today (Amateur) | What the Oracle does (Elite) |
|---|---|---|
| Infra readiness | You wait for a Telegram ping from the crew. | Oracle analyzes agent transcript velocity + CI queue and pushes to Telegram: 'idp#110 deploy is 80% complete. Estimated live in 12 mins.' |
| Agent health | Agent spins in a loop until it hits a hard timeout. | Oracle detects token-burn vs state-change anomalies and halts the agent early: 'Agent X halted. 95% probability of hallucination loop.' |
| Budgeting | You check the Stripe/OpenAI dashboard at the end of the month. | Oracle forecasts burn continuously: 'Current PR rework rate is up 40%. Predicting budget exhaustion 3 days early. Pre-auth required.' |

The Founder's Role in the Loop. You do not need to write the ML models. Your job in this
architecture is the Calibration Authority: Set the Thresholds: tell the Oracle when to bother you
(e.g., 'Only alert me if predicted CI time deviates by >2x the baseline, or budget burn spikes by
15%'). Define the Brier Targets: determine what constitutes a 'good' prediction. The Final Call:
Research proposes a new capability. Science predicts it will cost $400 and take 3 days to integrate.
You look at those numbers and say 'Yes' or 'Kill it.'

We already have MLflow and Langfuse approved for the cluster. We just need to wire them to an
OpenTelemetry collector instead of a local script."

## What the second message changes in the requirements

- Requirement 3 (Phase 0) is replaced. The "cloud-agnostic standard we just established" is R36 (crew#250, idp#124). There is no local ingest script and no SQLite file on the
  Mac. The nerve endings are an OpenTelemetry Collector on the OKE cluster (`idp`); sources push
  (agent traces via OTel GenAI semconv, GitHub Actions webhook, guards emitting OTel metrics); the
  store is ClickHouse (TimescaleDB is the named alternative); the oracle is an inference pod with
  MLflow for runs and models and Langfuse for prediction logging and Brier grading.
- The seven tables of the first message are the schema the OTel data must be able to answer, not a
  SQLite DDL. They become ClickHouse tables or views fed by the collector.
- Requirement 7 (this week: ingest, three forecasts, a dashboard) stands, delivered on the cluster.
- The friction point "the tapeworm extends crew/science/" is withdrawn as the Phase 0 path.
  `crew/science/` (DuckDB + dbt on the laptop) is the interim baseline and the backfill source for
  history the cluster has never seen; it is not the live nervous system, and it is retired once the
  ClickHouse store carries the same rows. That matches R-infra-never-Mac-bound (2026-08-25).
- "MLflow approved for the cluster": approved is the word on this page; on disk today MLflow is
  `absent` (STANDARDS.md Experiments row, crew#251) and Langfuse is `partially live` (Agent traces
  row). The Oracle's first PR deploys both to OKE; until then the calibration column is empty.
- What stays exactly as held: the split, the six predictions with actions, Brier scoring, the loop
  with the founder's last call, and the founder as calibration authority (thresholds, Brier
  targets, sensitive data).

## Requirements, as held (founder to confirm or correct each line)

1. Two functions split by direction. Research looks outward and is a crew. Science/ML looks inward
   and is a layer: embedded in agents, CI, guards, budget and the founder UI, always on, no opt-out.
2. Science answers "when will it be ready, is it broken, is it improving" with predictions that
   carry a confidence, are Brier-scored against the outcome, and widen when over-confident.
3. Phase 0 is telemetry ingest over what already runs: the seven tables above, backfilled from
   existing logs, no new service and no new bill.
4. Phase 1 is the six predictions above, each paired with an action. Phase 2 is calibration.
5. The loop is research proposes → science predicts cost and time → experiment team decides →
   founder has last call → science grades actual against predicted.
6. The founder sets which predictions come first, the accuracy threshold, the escalation rule and
   which data is sensitive.
7. This week's deliverable: ingest, three forecasts (CI duration, budget exhaustion, guard-trigger
   anomaly), one dashboard page.
8. Every data point is mapped, and no data point — including one that does not exist yet — can be
   missed. Founder, 2026-08-25, verbatim: "save docs, we need to map all data points and ensure
   nothing even new data points can be ingested seamlessly it must be impossible for any potential
   data point to be missed." Held as: (a) a single registry of every emitter on the estate (today
   `crew/science/sources.json`, 28 stores; the estate-inventory run of 2026-08-25T20:59Z reports
   `uncollected=37`, so the map is already behind); (b) a new file, job, hook, guard, service or
   log that writes anything is registered or it fails to land — a CI/pre-commit gate refuses an
   unregistered writer (LAW 45, guarded at estate width, proved both ways); (c) the OTel Collector
   is the one ingestion path, so a registered emitter is collected by construction with no
   per-source wiring; (d) the snapshot prints the count of unregistered and uncollected emitters
   every hour and any number above zero is an open P1.

## Friction points (resolved unless the founder says otherwise)

- R34 named MLflow and Argo; this directive says "No MLflow, no Argo" for Phase 0. Held as: R34's
  tooling is the Phase 2+ target; Phase 0 is Python + SQLite. STANDARDS.md (crew#251) already
  records MLflow as `absent`, so nothing on disk contradicts either ruling.
- `crew/science/` already holds the Phase 0 skeleton: `collect.py`, `warehouse.db` (DuckDB + dbt),
  `outcomes.py` with a forecast ledger (`predictions.jsonl`), and the hourly
  `com.founder.sciencecollect` job. The headline forbids a second collector, so the tapeworm is
  built by extending `crew/science/` to the seven tables, not by a new `~/.estate/science/ingest.py`.
  Principle kept, path changed; the founder said the implementation is ours unless he says so.
- "Every 60 seconds, reads transcripts" on the 16 GB Mac: incremental reads keyed on file offset,
  never a full rescan; a bounded run that prints how many rows it added.

## Applies to

crew#221 (research capability), crew#242 (step 1), crew#244 (science-plane rows), the bootstrap
steps in `docs/explanation/research-engine/CHARTER.md`, and every guard, job and product on the estate.
