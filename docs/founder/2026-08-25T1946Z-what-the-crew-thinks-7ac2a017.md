---
captured: 2026-08-25T19:46:42+00:00
session: 9f8f4f5f-1e12-4c54-b7a9-6fca2b737991
cwd: /Users/chidionyema/dev/code/crew
chars: 1716
source: founder prompt, verbatim (founder-doc-capture.py)
---

What the crew thinks:
"Replace prospector's scheduler with Argo, its queue with Postgres, its evals with MLflow."
What you are building:
"A research capability that any product — prospector, hermes-v2, a future customer — can call to answer questions autonomously."
The reframe:
Table
Level    What It Is    Who Uses It
Platform    Autonomous Research Engine    Every product
Product    Prospector    One use case (due diligence)
Product    Hermes-v2    One use case (founder ops)
Product    [Future customer]    Their use case
The five behaviors the crew must prove (before touching Argo or MLflow):
Question generation. Feed it 100 dossiers. It outputs 10 hypotheses you did not ask for.
Experiment design. Give it one hypothesis. It designs the test, picks the data, chooses the method.
Execution. It runs the experiment and records results without human intervention.
Calibration. It scores its own predictions against outcomes and publishes a Brier score.
Explanation. It tells you what it learned and why it changed its mind — in one sentence.
The crew's job is not to port prospector. It is to build the engine that makes prospector obsolete as a hand-written system.
What you tell them:
"Stop thinking about prospector. Propector is one customer. I want the research engine that prospector calls. If prospector needs a due diligence check, it asks the research engine. If hermes needs a market analysis, it asks the same engine. The engine is the platform. Propector is just a user."
The cost question is real but secondary. Argo vs. Temporal vs. Dagster matters for the bill. But the behavior must exist first. Pick the cheapest tool that lets the five behaviors run. Optimize cost after the behaviors work.
