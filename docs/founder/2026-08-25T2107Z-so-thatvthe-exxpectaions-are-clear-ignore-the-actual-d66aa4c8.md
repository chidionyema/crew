---
captured: 2026-08-25T21:07:09+00:00
session: 9f8f4f5f-1e12-4c54-b7a9-6fca2b737991
cwd: /Users/chidionyema/dev/code/crew
chars: 7512
source: founder prompt, verbatim (founder-doc-capture.py)
---

so thatvthe exxpectaions are clear,  ignore the actual inplenenntatino, you dont need to follow eactly uless i say so but the priciple and archtecure is key .

THE SPLIT

Table





ResearchScience / MLDirectionOutward — discovers the worldInward — understands itselfFeedsProducts, crews, capabilitiesGuards, jobs, predictions, baselinesQuestion"What should we build?""When will it be ready? Is it broken? Is it improving?"Data sourceDossiers, markets, competitorsTranscripts, CI runs, agent sessions, guard triggers, job latenciesOutputHypotheses, experiments, verdictsPredictions, grades, alerts, self-healing triggersAdoption ruleExperiment team decides, founder has last callEmbedded everywhere, always on, no opt-out

Research is a crew. Science/ML is a layer.

WHAT DATA IS BEING THROWN AWAY RIGHT NOW

Every component in your estate is screaming and nobody is listening:

Table





SourceData ProducedCurrentlyShould BeAgent sessionsTranscripts, token burn, latency, halt reasonsEphemeral, lost when session diesFeeds prediction model: "this session pattern usually fails at step 5"CI runsDuration, failure mode, retry count, queue depthGitHub logs, deleted after 90 daysFeeds baseline: "builds are 20% slower than last week, investigate"Guard triggersgoal-guard, dod-guard, idle-guard blocksTerminal output, ephemeralFeeds behavior model: "this agent type triggers idle-guard 3x more"Oracle sign-insTime to sign-in, failure reason, retry countManual debugging onlyFeeds prediction: "founder sign-in usually takes 2 min, it's been 10, something is wrong"Budget burnsToken consumption per step, per model, per agentManual inspectionFeeds forecast: "at current burn, budget exhausts in 4 hours"Merkle commitsState diff sizes, branch frequency, merge conflictsStorage onlyFeeds pattern: "this agent produces 3x larger diffs than others, likely hallucinating"Telegram receiptsResponse time, action type, founder interruption rateChat historyFeeds presence model: "founder usually approves in 30s, it's been 5 min, escalate"Crew PRsReview time, rework count, qa failures, merge timeGitHub metricsFeeds team health: "crew#241 has 3 reworks, predict 2 more days"

You are flying blind. Every prediction you want — "when will infra be ready?" — requires this data. It is being produced and discarded.

THE EMBEDDED SCIENCE LAYER (No New Infrastructure)

We do not need a Kubernetes science plane to start. We need a data parasite — a thin layer that attaches to everything already running and exfiltrates metrics.

Phase 0: The Telemetry Tapeworm (This Week)

One script: ~/.estate/science/ingest.py

Python



# Runs every 60 seconds. Attaches to everything.# Writes to ~/.estate/science/metrics.db (SQLite, local, free)



tables:- agent_sessions (session_id, start_time, end_time, tokens_burned, halt_reason, final_state)- ci_runs (pr_number, job_name, duration_sec, result, retry_count)- guard_triggers (guard_name, agent_name, timestamp, reason, resolution)- founder_actions (action_type, response_time_sec, device, timestamp)- budget_events (session_id, event_type, amount, remaining, timestamp)- merkle_commits (session_id, commit_hash, diff_size_bytes, parent_hash, timestamp)- crew_prs (pr_number, review_time_hours, rework_count, qa_failures, merge_time_hours)

How it captures:

Reads ~/.estate/dag/ for Merkle data

Reads ~/.claude/ transcripts for session data

Polls GitHub API for CI/PR data

Reads ~/.estate/interventions/ for founder action data

Reads Langfuse traces for agent behavior data

No new services. No new cloud bills. One SQLite file on your Mac.

Phase 1: The Living Oracle (Week 2-3)

Queries on the telemetry database:

Table





QueryPredictionAction"Average CI duration last 7 days vs. today""Build will finish in 45 min ± 10 min"Surface to founder if >2x normal"Guard trigger rate per agent type""Agent X has 3x idle-guard blocks, likely stuck"Auto-halt, alert founder"Founder response time trend""Founder usually responds in 30s, currently 10 min, may be away"Escalate to haptic, do not spam"Budget burn rate vs. allocation""Budget exhausts in 4 hours at current rate"Pre-authorization request"Session failure pattern""Sessions with >5 state transitions fail 80% of the time"Auto-halt at transition 4"Crew velocity trend""PR rework rate up 40%, predict 2 more days for crew#241"Surface to founder, adjust expectations

Phase 2: Self-Improving Predictions (Month 2)

Every prediction gets a Brier score:

plain



prediction: "CI will finish in 45 min"

actual: 52 min

Brier: (0.75 - 0)^2 = 0.5625 (if 75% confidence)



prediction: "Budget exhausts in 4 hours"

actual: 3.5 hours

Brier: (0.80 - 0)^2 = 0.64 (if 80% confidence)

The model adjusts its confidence based on historical accuracy. If it is consistently over-confident on CI times, it widens the interval. The oracle learns its own mistakes.

HOW RESEARCH AND SCIENCE INTERACT

plain



┌─────────────────────────────────────────────────────────────┐

│ FOUNDER │

│ (Last call on adoption) │

└───────────────────────┬───────────────────────────────────────┘

│

┌───────────────┴───────────────┐

▼ ▼

┌───────────────┐ ┌───────────────┐

│ RESEARCH │ │ SCIENCE / ML │

│ (Outward) │◄─────────────►│ (Inward) │

│ │ "Research │ │

│ Discovers: │ says X │ Predicts: │

│ - New markets │ improves │ - When infra │

│ - Competitor │ estate; │ will be ready│

│ moves │ Science │ - Which agents │

│ - Capabilities│ says it │ will fail │

│ to adopt │ will take │ - Founder │

│ │ 3 days" │ availability │

└───────┬───────┘ └───────┬───────┘

│ │

▼ ▼

┌───────────────┐ ┌───────────────┐

│ EXPERIMENT │ │ EMBEDDED │

│ TEAM │ │ LAYER │

│ │ │ │

│ Decides: │ │ Embedded in: │

│ - Run test? │ │ - Agents │

│ - Adopt? │ │ - CI │

│ - Timeline? │ │ - Guards │

│ │ │ - Budget │

│ Founder has │ │ - Founder UI │

│ last call │ │ │

└───────────────┘ └───────────────┘

The loop:

Research discovers a capability that could improve estate

Science predicts: "adoption will take 3 days, CI will slow 20%, 80% confidence"

Experiment team decides: "worth it" or "not now"

Founder has last call

If adopted, Science measures actual vs. predicted, improves next prediction

WHAT YOU BUILD FIRST (This Week)

Day 1-2: Telemetry Tapeworm

ingest.py running every 60s

SQLite schema for the 7 tables above

Backfill from existing logs (transcripts, CI history, Merkle DAG)

Day 3-4: First Predictions

"CI duration forecast" (simple linear regression on historical data)

"Budget exhaustion forecast" (token burn rate projection)

"Guard trigger alert" (anomaly detection on guard frequency)

Day 5-7: Founder Dashboard

One web page: localhost:8080/science

Shows: predictions, baselines, anomalies, Brier scores

Updates every 5 minutes from SQLite

No Kubernetes. No Argo. No MLflow. Python + SQLite + cron.

YOUR ROLE IN THE DESIGN

Table





DecisionYour CallWhich predictions matter most?You pick: CI time? Budget? Founder availability?What is "good enough" accuracy?70%? 80%? You set the thresholdWhen does Science escalate to you?Anomaly >2x baseline? Prediction failed? You defineWhich data is sensitive?Transcripts? Founder actions? You gate access

My role: Architecture the tapeworm, the schema, the prediction queries. Validate with you. Hand to crew.

Crew's role: Build ingest.py, run backfill, wire to dashboard.

THE ONE SENTENCE

Research discovers what to build. Science predicts when it will be ready, if it will break, and whether the founder can be interrupted. Both are mandatory. Neither can wai
