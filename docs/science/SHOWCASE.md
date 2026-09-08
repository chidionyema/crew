# Science lane showcase

Generated 2026-09-08T19:04Z by `python3 science/showcase.py`. Every number is read at generation
time; the command under each heading reproduces it. A section that cannot see its source says BLIND.

## Progress since the previous run

Previous run: 2026-09-08T13:04Z.

- foresight labelled PRs: 2151 -> 2147
- foresight holdout accuracy: 0.868 -> 0.884
- warehouse rows: 247387 -> 251311
- commits, 7d: 106 -> 107
- complaints, 7d: 285 -> 287
- spend USD, 7d: 2655.98 -> 2680.4
- USD per commit: 25.06 -> 25.05
- lane code facts 24h: 51095 -> 52208
- lane crew facts 24h: 82568 -> 84227
- lane data-ml facts 24h: 53664 -> 54719
- lane hermes-v2 facts 24h: 9930 -> 9943
- lane portal facts 24h: 26669 -> 26694
- lane science facts 24h: 23338 -> 23397

## Capabilities

`python3 science/showcase.py  (reads science/*.py, scripts/science-collect, scripts/verify.d, launchd)`

| Capability | What it answers | Run | Scheduled by |
|---|---|---|---|
| capa | Did the fix actually stop him having to say it again | `python3 science/capa.py` | hand-run |
| collect | Collect every estate data store into one queryable table | `python3 science/collect.py` | launchd com.founder.sciencecollect via scripts/science-collect |
| datamap | The estate's data dictionary, generated rather than written | `python3 science/datamap.py` | CI: scripts/verify.d/26-datamap-register.sh |
| dbt_build | Generate the dbt project's `facts` model from the one registry | `python3 science/dbt_build.py` | hand-run |
| docsmap | Inventory every document this estate owns, and say which ones fail the standard | `python3 science/docsmap.py` | CI: scripts/verify.d/95-docs.sh |
| dora | DORA four keys for the estate, measured from GitHub, never from memory (crew#495 CP9) | `python3 science/dora.py` | hand-run |
| duckdb_differential | Does DuckDB's `read_json_auto` read this estate's stores the same way collect.py does? | `python3 science/duckdb_differential.py` | hand-run |
| emit | Emit every collected science row to the estate collector as an OTLP log (LAW 50) | `python3 science/emit.py` | hand-run |
| export_drill | crew#74 row 1: the warehouse exit drill | `python3 science/export_drill.py` | hand-run |
| foresight | Foresight: predict a red CI run before the push, and score the prediction after (crew#405) | `python3 science/foresight.py` | launchd com.founder.sciencecollect via scripts/science-collect |
| friction | What the founder has had to say twice, measured over every transcript on this machine | `python3 science/friction.py` | hand-run |
| law_enforcement | Law enforcement coverage: which laws are machine-enforced, which are prose | `python3 science/law_enforcement.py` | launchd com.founder.lawenforcement |
| ledger | Writer for the research ledger (crew#72 row 1) | `python3 science/ledger.py` | hand-run |
| map_covers_laws | Every law in AGENTS.md has a check written for it in enforcement-map.json | `python3 science/map_covers_laws.py` | hand-run |
| outcomes | Collect what the estate produced, so spend can be divided by something | `python3 science/outcomes.py` | launchd com.founder.sciencecollect via scripts/science-collect |
| producers | Every producer of data in the estate, discovered by class rather than typed by hand | `python3 science/producers.py` | hand-run |
| research_grade | Grade the general-purpose research capability from its own ledger (crew#508) | `python3 science/research_grade.py` | hand-run |
| research_intake | Scheduled outward research intake (crew#508 CP8) | `python3 science/research_intake.py` | hand-run |
| research_worker | The research worker: GPT Researcher through the router, every report graded by Inspect, every | `python3 science/research_worker.py` | hand-run |
| self_grade | Weekly self-grade of the research loop (LAW 35, crew#72 row 4) | `python3 science/self_grade.py` | hand-run |
| transcripts | Read Claude Code session transcripts incrementally, by byte offset (crew#319, crew#74 row 4) | `python3 science/transcripts.py` | launchd com.founder.sciencecollect via scripts/science-collect |
| velocity | Velocity per lane, measured from the board, never felt (crew#527 CP1) | `python3 science/velocity.py` | hand-run |


## Lanes

`sqlite3 science/warehouse.db "select source, count(*) from facts where ingested_at >= datetime('now','-24 hours') group by source"`

Every lane graded on what it emitted in the last 24h. BLIND rows first:
a lane that emitted no fact is not healthy, it is unobserved (crew#508).

| Lane | Facts, 24h | Checkpoints, 24h | Grade | Sources counted |
|---|---:|---:|---|---|
| code | 52,208 | 0 | GAP | ships, ci_runs, ci_reach, bundle_push, estate_push, worktree_cleanup, hook_outcomes, close_guard |
| crew | 84,227 | 0 | GAP | board, ledger, decisions, directives, tickets, goal_net, attention, founder_actions, board_deadletter, prompt_ledger |
| data-ml | 54,719 | 0 | GAP | dagster-ticks, dagster-runs, temporal_dev_executions, job_timelines |
| hermes-v2 | 9,943 | 0 | GAP | alerts_inbox, sovereign_receipts, sovereign_budget, revenue, agent_cert, runaway-reaper, stuck_detector, aiden_ticks |
| portal | 26,694 | 0 | GAP | estate_registry, capability_receipts, enforcement_map, drills, drills_scripts |
| science | 23,397 | 0 | GAP | research_ledger, predictions, method_metrics, history, spend |
| unmapped | 89 | 0 | GAP | hindsight_recall, pi_bridge_runs |

- BLIND: none
- sources in no lane: hindsight_recall (80), pi_bridge_runs (9) — add them to LANE_SOURCES in science/showcase.py
- checkpoints 0 for every lane: no `- [x]` line in a ledger written in the last 24h (searched science/RESEARCH-LEDGER.jsonl, science/ships.jsonl, science/attention.jsonl, science/predictions.jsonl; fresh: science/ships.jsonl, science/attention.jsonl, science/predictions.jsonl)

## Warehouse

`sqlite3 science/warehouse.db "select count(*), count(distinct source), max(ingested_at) from facts"`

- 251,311 rows across 43 sources; last ingest 2026-09-08T18:37:16+00:00
- 0 of 42 declared sources carry owner, method, retention and sensitivity
- stale past their SLA: aiden_ticks (289h), stuck_detector (300h), job_timelines (234h), estate_push (268h), drills_scripts (301h), sovereign_receipts (327h), board_deadletter (315h), estate_registry (337h), ci_runs (304h), lane.code.pr-hygiene (293h), runaway-reaper (304h), hindsight_recall (274h)

## Data map (LAW 50)

`python3 science/datamap.py --check`

- 59 register entries (COLLECTED 29, EXCLUDED 9, NEVER_EMITTED 9, WIRED_NEVER 11, WRITER_DEAD 1); 8206 producers discovered at the last census
- shape walk: BLIND (science/shapes.json empty or absent; no walk has landed)
- domains blind at the last census: cluster_live, warehouse
- contract violations now: BLIND (crew#71 not merged)

## Research ledger

`python3 -c "import json; print(sum(1 for l in open('science/RESEARCH-LEDGER.jsonl')))"`

- 26 entries, 2026-08-23 to 2026-09-05; 26 record the decision they fed

- **2026-08-27** Is there a mature open-source tool that predicts a red CI run / selects tests from repository history, and which learner and prediction-trac
  - decision: Foresight uses scikit-learn LogisticRegression (requirements-dev floor >=1.5) trained on the estate's own run history; no test-selection product is bought or bu
  - metric: no prediction existed (1 hand prediction ever scored) -> 1078 labelled PRs; holdout 216: accuracy 0.676 vs base 0.634, red precision 0.846, Brier 0.209; 11 open PRs predicted before CI
- **2026-08-27** What is the mature standard for each identity population (cloud machines, workloads, humans), and what number grades it?
  - decision: docs/STANDARDS.md Identity row (crew#482); crew#227 CP3/CP4/CP5 graded against it
  - metric: 0 of 3 (no Identity row); static-secret-gate 25 -> 3 of 3 written; static-secret-gate 25 (the number the row now grades)
- **2026-09-05** Where does a refusal that grades the agent's own reply belong, now that the estate is migrating hand-rolled Python guards to Rego, when the 
  - decision: THE EMPIRICAL PROOF RULE is enforced from policy/reply.rego, not dod-guard.py. opa-hook.py gained reply_evidence(), which measures reply_has_quote and reply_ass
  - metric: dod-guard.py 236 lines against a 202 ceiling; hand-rolled-policy FAIL (7 tests, 1 failure); the rule unreachable from Rego -> dod-guard.py back to 202; hand-rolled-policy pass; opa test policy/reply.rego policy/reply_test.rego 40/40; end-to-end through opa-hook.py 3 of 3 correct (probe-only BLOCK, quoted log PASS, backticked mention PASS)

## Delivery outcomes

`python3 science/outcomes.py ship --days 7; python3 science/outcomes.py attention --days 7`

- last 7 days: 107 commits across 3 repos
- founder messages 4538, complaints 287 (6.3%)
- spend USD 2680.4, USD per commit 25.05
- machine learning: none. Nothing here trains a model; every number is a count or a ratio.

## Predictions

`python3 science/outcomes.py rate`

- 15 recorded before a repair, 6 scored after, hit rate 50%

## Foresight: will this PR go red?

`python3 science/foresight.py report`

- trained 2026-09-08T19:04Z on 2147 labelled PRs; 25% of first runs were red
- unseen newest 430 PRs: accuracy 88% against a base rate of 85%; Brier 0.086
- model beats the base rate on unseen PRs
- strongest signals: r_crew (+0.73), log_add (+0.58), r_idp (-0.44), r_prospector (-0.36), r_claude-guards (+0.34)
- live: 13 open PRs predicted before their CI finished, 4 scored, hit rate 50%
