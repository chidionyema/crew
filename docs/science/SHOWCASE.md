# Science lane showcase

Generated 2026-09-03T07:01Z by `python3 science/showcase.py`. Every number is read at generation
time; the command under each heading reproduces it. A section that cannot see its source says BLIND.

## Progress since the previous run

Previous run: 2026-09-02T19:03Z.

- foresight labelled PRs: 2130 -> 2136
- foresight holdout accuracy: 0.69 -> 0.682
- foresight predictions scored: 7 -> 2
- foresight hit rate %: 43 -> 50
- warehouse rows: 693616 -> 728694
- stale sources: 12 -> 14
- sources with a contract: 44 -> 0
- register entries: 60 -> 59
- producers discovered: 6999 -> 8206
- field paths: 1045 -> 0
- research entries: 30 -> 25
- research entries with a decision: 30 -> 25
- commits, 7d: 254 -> 204
- complaints, 7d: 342 -> 378
- spend USD, 7d: 9250.05 -> 8382.9
- USD per commit: 36.42 -> 41.09
- predictions recorded: 23 -> 13
- predictions scored: 9 -> 4
- lane code facts 24h: 510988 -> 539500
- lane crew facts 24h: 67234 -> 70862
- lane data-ml facts 24h: 58454 -> 60962
- lane hermes-v2 facts 24h: 9835 -> 9845
- lane portal facts 24h: 26141 -> 26194
- lane science facts 24h: 20875 -> 21208
- lane unmapped facts 24h: 89 -> 123
- capabilities: 23 -> 22
- capabilities scheduled: 9 -> 7

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
| code | 539,500 | 0 | GAP | ships, ci_runs, ci_reach, bundle_push, estate_push, worktree_cleanup, hook_outcomes, close_guard |
| crew | 70,862 | 0 | GAP | board, ledger, decisions, directives, tickets, goal_net, attention, founder_actions, board_deadletter, prompt_ledger |
| data-ml | 60,962 | 0 | GAP | dagster-ticks, dagster-runs, temporal_dev_executions, job_timelines |
| hermes-v2 | 9,845 | 0 | GAP | alerts_inbox, sovereign_receipts, sovereign_budget, revenue, agent_cert, runaway-reaper, stuck_detector, aiden_ticks |
| portal | 26,194 | 0 | GAP | estate_registry, capability_receipts, enforcement_map, drills, drills_scripts |
| science | 21,208 | 0 | GAP | research_ledger, predictions, method_metrics, history, spend |
| unmapped | 123 | 0 | GAP | dora, hindsight_recall, pi_bridge_runs |

- BLIND: none
- sources in no lane: dora (34), hindsight_recall (80), pi_bridge_runs (9) — add them to LANE_SOURCES in science/showcase.py
- checkpoints 0 for every lane: no `- [x]` line in a ledger written in the last 24h (searched science/RESEARCH-LEDGER.jsonl, science/ships.jsonl, science/attention.jsonl, science/predictions.jsonl; fresh: science/RESEARCH-LEDGER.jsonl, science/ships.jsonl, science/attention.jsonl, science/predictions.jsonl)

## Warehouse

`sqlite3 science/warehouse.db "select count(*), count(distinct source), max(ingested_at) from facts"`

- 728,694 rows across 43 sources; last ingest 2026-09-03T06:37:10+00:00
- 0 of 42 declared sources carry owner, method, retention and sensitivity
- stale past their SLA: aiden_ticks (157h), stuck_detector (168h), predictions (167h), job_timelines (102h), estate_push (136h), drills_scripts (169h), sovereign_receipts (195h), board_deadletter (182h), estate_registry (205h), research_ledger (175h), ci_runs (172h), lane.code.pr-hygiene (161h), runaway-reaper (172h), hindsight_recall (142h)

## Data map (LAW 50)

`python3 science/datamap.py --check`

- 59 register entries (COLLECTED 29, EXCLUDED 9, NEVER_EMITTED 9, WIRED_NEVER 11, WRITER_DEAD 1); 8206 producers discovered at the last census
- shape walk: BLIND (science/shapes.json empty or absent; no walk has landed)
- domains blind at the last census: cluster_live, warehouse
- contract violations now: BLIND (crew#71 not merged)

## Research ledger

`python3 -c "import json; print(sum(1 for l in open('science/RESEARCH-LEDGER.jsonl')))"`

- 25 entries, 2026-08-23 to 2026-08-27; 25 record the decision they fed

- **2026-08-25** What is the one front-end platform for every Bytesync public surface (parent site plus each company's brand and store), so that a new brand 
  - decision: STANDARDS.md gains a Front end row: Next.js + Payload 3 + one design system with per-brand tokens + Medusa 2 under selling brands; brand = config + collection +
  - metric: 0 of 3 (Store.Web, look-engine, mumchimp-medusa storefront; no row existed) -> row exists; still 0 of 3 until crew#235 CP2 lands, then 1 of 3
- **2026-08-27** Is there a mature open-source tool that predicts a red CI run / selects tests from repository history, and which learner and prediction-trac
  - decision: Foresight uses scikit-learn LogisticRegression (requirements-dev floor >=1.5) trained on the estate's own run history; no test-selection product is bought or bu
  - metric: no prediction existed (1 hand prediction ever scored) -> 1078 labelled PRs; holdout 216: accuracy 0.676 vs base 0.634, red precision 0.846, Brier 0.209; 11 open PRs predicted before CI
- **2026-08-27** What is the mature standard for each identity population (cloud machines, workloads, humans), and what number grades it?
  - decision: docs/STANDARDS.md Identity row (crew#482); crew#227 CP3/CP4/CP5 graded against it
  - metric: 0 of 3 (no Identity row); static-secret-gate 25 -> 3 of 3 written; static-secret-gate 25 (the number the row now grades)

## Delivery outcomes

`python3 science/outcomes.py ship --days 7; python3 science/outcomes.py attention --days 7`

- last 7 days: 204 commits across 4 repos
- founder messages 6336, complaints 378 (6.0%)
- spend USD 8382.9, USD per commit 41.09
- machine learning: none. Nothing here trains a model; every number is a count or a ratio.

## Predictions

`python3 science/outcomes.py rate`

- 13 recorded before a repair, 4 scored after, hit rate 50%

## Foresight: will this PR go red?

`python3 science/foresight.py report`

- trained 2026-09-03T07:00Z on 2136 labelled PRs; 35% of first runs were red
- unseen newest 428 PRs: accuracy 68% against a base rate of 58%; Brier 0.184
- model beats the base rate on unseen PRs
- strongest signals: r_crew (+0.50), log_files (+0.48), r_prospector (-0.39), log_add (+0.30), f_test (+0.26)
- live: 11 open PRs predicted before their CI finished, 2 scored, hit rate 50%
