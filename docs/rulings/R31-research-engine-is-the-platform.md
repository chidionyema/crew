# R31: the research engine is the platform, prospector is a user

Founder, 2026-08-25, verbatim, attached to crew #221.

What the crew thinks: "Replace prospector's scheduler with Argo, its queue with Postgres, its evals with MLflow."

What you are building: "A research capability that any product, prospector, hermes-v2, a future customer, can call to answer questions autonomously."

| Level | What it is | Who uses it |
|---|---|---|
| Platform | Autonomous research engine | Every product |
| Product | Prospector | One use case (due diligence) |
| Product | Hermes-v2 | One use case (founder ops) |
| Product | [Future customer] | Their use case |

The five behaviours the crew must prove, before touching Argo or MLflow:

1. Question generation. Feed it 100 dossiers. It outputs 10 hypotheses you did not ask for.
2. Experiment design. Give it one hypothesis. It designs the test, picks the data, chooses the method.
3. Execution. It runs the experiment and records results without human intervention.
4. Calibration. It scores its own predictions against outcomes and publishes a Brier score.
5. Explanation. It tells you what it learned and why it changed its mind, in one sentence.

The crew's job is not to port prospector. It is to build the engine that makes prospector obsolete as a hand-written system.

"Stop thinking about prospector. Prospector is one customer. I want the research engine that prospector calls. If prospector needs a due diligence check, it asks the research engine. If hermes needs a market analysis, it asks the same engine. The engine is the platform. Prospector is just a user."

The cost question is real but secondary. Argo vs Temporal vs Dagster matters for the bill. But the behaviour must exist first. Pick the cheapest tool that lets the five behaviours run. Optimise cost after the behaviours work.
