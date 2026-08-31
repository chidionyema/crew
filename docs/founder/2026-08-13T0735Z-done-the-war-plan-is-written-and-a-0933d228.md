---
captured: 2026-08-13T07:35:05+00:00
session: efb69fce-3bd0-47be-bbc8-cc743c95d5c5
cwd: /Users/chidionyema/Documents/code/prospector
chars: 3531
source: founder prompt, verbatim (founder-doc-capture.py)
---

DONE: the war plan is written — and a third research workflow landed mid-session whose adversarial critique overturned my own headline. I verified the correction on disk before rewriting anything.

⧉ https://claude.ai/code/artifact/e3bda52e-84ce-4758-8e47-f535a60c105e · docs/ENGINE_WAR_PLAN_2026-08-13.md

The audit's economics were wrong. Across 50 batches since 2026-07-22: 447 vetted → 38 PASS (8.5%), $0.0145/candidate, unverifiable median 43.1% — not zero passes at $0.051 with 66%. Cost is bimodal; 22 of 50 batches cost $0.00. So k=100 is ~$1.45/wave against a $20 cap, and the premise under any scorer-replacement is gone.

Six proposals are cut before they cost an hour — including one I had ranked as the biggest lever.

Next step is W0.1: AUC of a free proxy against the 447 already-labelled outcomes. Zero tokens, local CPU, and it decides which architecture gets funded at all.

---
What the critique changed, with the check that changed it

┌───────────────────────────────┬──────────────────────┬──────────────────────────────────────────────────────────────────────┐
│              Was              │         Now          │                               Because                                │
├───────────────────────────────┼──────────────────────┼──────────────────────────────────────────────────────────────────────┤
│ Local NLI = biggest cost      │ Router only, $0      │ Under its own fence both outcomes still end in a trusted call — the  │
│ lever                         │ booked               │ saving and the doctrine can't both be true                           │
├───────────────────────────────┼──────────────────────┼──────────────────────────────────────────────────────────────────────┤
│ Rerank justified by           │ Keep it, behind its  │ Reranking's step is 2.9→1.9 (1.0pp); contextual embeddings' is       │
│ Anthropic's 67%               │ own A/B              │ 5.7→3.7 (2.0pp)                                                      │
├───────────────────────────────┼──────────────────────┼──────────────────────────────────────────────────────────────────────┤
│ Pairwise scorer swap          │ Post-hoc calibration │ The cited paper's ablations covered prompts, not scoring             │
│                               │                      │ methodologies                                                        │
├───────────────────────────────┼──────────────────────┼──────────────────────────────────────────────────────────────────────┤
│ Chain reorder / G8 removal /  │ Cut                  │ Already the config · already enabled: false · already measured at    │
│ template revert               │                      │ 93% unverifiable here                                                │
└───────────────────────────────┴──────────────────────┴──────────────────────────────────────────────────────────────────────┘

Three of five citation spot-checks changed a recommendation. New free levers found: verbalized-sampling typicality is generated and discarded (config.yaml:868-873), and prescreen_ are built but inert (:1349, :1401).

Two things I did not do: the audit's artifact still (its markdown is corrected), and the merge is stillunlanded — 79aa357 is a fast-forward sitting in ../prospector-latest, and Wave 0 branches from it.

Handoff written. Execution is per-wave, and a war room is Fable 5 chosen at process start — so relaunch on it rather than clearing.

Safe point — type /clear (state saved, nothing will be lost). ok lets get to work, get latest changes
