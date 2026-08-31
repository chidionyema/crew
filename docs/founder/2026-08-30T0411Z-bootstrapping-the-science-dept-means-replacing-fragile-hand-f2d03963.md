---
captured: 2026-08-30T04:11:04+00:00
session: 41fd24d8-96a0-417e-bc3f-b7b15aceb026
cwd: /Users/chidionyema/dev/code/idp
chars: 2096
source: founder prompt, verbatim (founder-doc-capture.py)
---

Bootstrapping the "Science Dept" means replacing fragile, hand-written Python with an automated, research-grade pipeline.

To answer your question directly: **GPT Researcher is the worker, not the manager.** It is the execution engine that plans the query, parallelizes the web scrapers, and writes the final report with hard-linked citations.

It was previously rejected from your stack because it lacks an internal evaluation loop. You cannot trust unsupervised agents to do science without grading their work. Here is how you bootstrap the complete pipeline to fix that constraint.

## The Science Department Blueprint

Right now, your `idp` repo has Temporal (14 files) and Langfuse (30 files) successfully wired, but Argo, MLflow, Inspect, and pgvector are at zero. Here is the exact architecture to build:

* **1. The Orchestrator (Argo / Temporal):** You trigger a research job on a schedule using Argo, or wrap it in a durable execution using Temporal (which you already have deployed).
* **2. The Execution (GPT Researcher):** The job spins up GPT Researcher. It must hit a frontier model through your router key—do not use local models here, as their claim verification and citation structuring are inferior for this level of rigorous work.
* **3. The Evaluator (Inspect):** This is the critical missing link. The moment GPT Researcher finishes, Inspect scores the answer. If a run produces a report but fails the Inspect score, the run is marked as a failure and dropped.
* **4. The Memory Vault:** The final report, the original question, and the Inspect score are saved to MLflow. The token usage and API traces are caught by Langfuse. If the agent needs to read your internal estate docs alongside the public web, it queries pgvector.

By wrapping GPT Researcher in Inspect's grading loop and Temporal's durability, you get the massive web-scraping power of the tool without sacrificing reliability.

Since Prospector main is finally green again (front-end fixes #785 and #786 just landed), the deck is clear to start building this backend. Where do you want to lay the first brick?
