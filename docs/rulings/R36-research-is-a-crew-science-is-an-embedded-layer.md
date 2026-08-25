# R36: research is a crew that looks outward; science/ML is an embedded layer that looks inward

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
steps in `docs/research-engine/CHARTER.md`, and every guard, job and product on the estate.
