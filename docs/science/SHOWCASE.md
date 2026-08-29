# Science lane showcase

Generated 2026-08-29T18:53Z by `python3 science/showcase.py`. Every number is read at generation
time; the command under each heading reproduces it. A section that cannot see its source says BLIND.

## Progress since the previous run

Previous run: 2026-08-29T00:49Z.

- foresight labelled PRs: 1682 -> 1882
- foresight holdout accuracy: 0.721 -> 0.74
- foresight predictions scored: 4 -> 5
- foresight hit rate %: 50 -> 40
- warehouse rows: 350377 -> 460854
- warehouse sources: 42 -> 43
- stale sources: 6 -> 10
- commits, 7d: 649 -> 665
- complaints, 7d: 142 -> 267
- spend USD, 7d: 7373.66 -> 9045.2
- USD per commit: 11.36 -> 13.6
- predictions recorded: 20 -> 22
- predictions scored: 6 -> 7
- lane code facts 24h: 227778 -> 324071
- lane crew facts 24h: 36996 -> 44025
- lane data-ml facts 24h: 34295 -> 38985
- lane hermes-v2 facts 24h: 8612 -> 9544
- lane portal facts 24h: 25642 -> 25721
- lane science facts 24h: 16974 -> 18426
- lane unmapped facts 24h: 80 -> 82

## Capabilities

`python3 science/showcase.py  (reads science/*.py, scripts/science-collect, scripts/verify.d, launchd)`

| Capability | What it answers | Run | Scheduled by |
|---|---|---|---|
| capa | Did the fix actually stop him having to say it again | `python3 science/capa.py` | hand-run |
| collect | Collect every estate data store into one queryable table | `python3 science/collect.py` | launchd com.founder.sciencecollect via scripts/science-collect |
| datamap | The estate's data dictionary, generated rather than written | `python3 science/datamap.py` | CI: scripts/verify.d/26-datamap-register.sh |
| dbt_build | Generate the dbt project's `facts` model from the one registry | `python3 science/dbt_build.py` | hand-run |
| decisions_intake | Decision intake from merged pull requests (crew#366, act/agent_decisions) | `python3 science/decisions_intake.py` | launchd com.founder.sciencecollect via scripts/science-collect |
| docsmap | Inventory every document this estate owns, and say which ones fail the standard | `python3 science/docsmap.py` | CI: scripts/verify.d/95-docs.sh |
| dora | DORA four keys for the estate, measured from GitHub, never from memory (crew#495 CP9) | `python3 science/dora.py` | launchd com.founder.sciencecollect via scripts/science-collect |
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
| self_grade | Weekly self-grade of the research loop (LAW 35, crew#72 row 4) | `python3 science/self_grade.py` | hand-run |
| transcripts | Read Claude Code session transcripts incrementally, by byte offset (crew#319, crew#74 row 4) | `python3 science/transcripts.py` | launchd com.founder.sciencecollect via scripts/science-collect |
| velocity | Velocity per lane, measured from the board, never felt (crew#527 CP1) | `python3 science/velocity.py` | hand-run |


## Lanes

`sqlite3 science/warehouse.db "select source, count(*) from facts where ingested_at >= datetime('now','-24 hours') group by source"`

Every lane graded on what it emitted in the last 24h. BLIND rows first:
a lane that emitted no fact is not healthy, it is unobserved (crew#508).

| Lane | Facts, 24h | Checkpoints, 24h | Grade | Sources counted |
|---|---:|---:|---|---|
| code | 324,071 | 0 | GAP | ships, ci_runs, ci_reach, bundle_push, estate_push, worktree_cleanup, hook_outcomes, close_guard, dora |
| crew | 44,025 | 0 | GAP | board, ledger, decisions, directives, tickets, goal_net, attention, founder_actions, board_deadletter, prompt_ledger |
| data-ml | 38,985 | 0 | GAP | dagster-ticks, dagster-runs, temporal_dev_executions, job_timelines |
| hermes-v2 | 9,544 | 0 | GAP | alerts_inbox, sovereign_receipts, sovereign_budget, revenue, agent_cert, runaway-reaper, stuck_detector, aiden_ticks |
| portal | 25,721 | 0 | GAP | estate_registry, capability_receipts, enforcement_map, drills, drills_scripts |
| science | 18,426 | 0 | GAP | research_ledger, predictions, method_metrics, history, spend |
| unmapped | 82 | 0 | GAP | hindsight_recall, pi_bridge_runs |

- BLIND: none
- sources in no lane: hindsight_recall (80), pi_bridge_runs (2) — add them to LANE_SOURCES in science/showcase.py
- checkpoints 0 for every lane: no `- [x]` line in a ledger written in the last 24h (searched science/RESEARCH-LEDGER.jsonl, science/ships.jsonl, science/attention.jsonl, science/predictions.jsonl; fresh: science/ships.jsonl, science/attention.jsonl, science/predictions.jsonl)

## Warehouse

`sqlite3 science/warehouse.db "select count(*), count(distinct source), max(ingested_at) from facts"`

- 460,854 rows across 43 sources; last ingest 2026-08-29T18:38:06+00:00
- 44 of 44 declared sources carry owner, method, retention and sensitivity
- stale past their SLA: aiden_ticks (49h), stuck_detector (60h), drills_scripts (61h), sovereign_receipts (87h), board_deadletter (74h), estate_registry (96h), ci_runs (63h), lane.code.pr-hygiene (53h), temporal_dev_executions (87h), hindsight_recall (34h)

## Data map (LAW 50)

`python3 science/datamap.py --check`

- 60 register entries (COLLECTED 35, EXCLUDED 9, NEVER_EMITTED 4, WIRED_NEVER 11, WRITER_DEAD 1); 6999 producers discovered at the last census
- 1045 field paths in the shape walk of 2026-08-28 17:17Z
- domains blind at the last census: cluster_live
- contract violations now: 0

## Research ledger

`python3 -c "import json; print(sum(1 for l in open('science/RESEARCH-LEDGER.jsonl')))"`

- 30 entries, 2026-08-23 to 2026-08-27; 30 record the decision they fed

- **2026-08-24** What replaces launchd for a single-Mac estate that must survive the Mac dying, weighed on: does it run when the laptop is shut, does a moved
  - decision: Three-part split, not a product, and it FITS docs/STANDARDS.md rather than deviating from it (the standard already names Healthchecks self-hosted as the job-mon
  - metric: 32 estate plists: 9 hc-wrapped but the receiver is down so 0 effectively monitored; 4 of 32 in git, of which 3 have drifted; 0 drift checks running. -> None
- **2026-08-24** Which of the estate's hand-written Claude Code guard hooks (rule-guard, goal-guard, tracked, jargon-guard, context-guard-hook) can be expres
  - decision: Replace one, split one, delete half of one, keep two. (1) jargon-guard.py -> Vale 3.17.1, already installed, already configured in 10+ repos: highest-value swap
  - metric: 269 lines (jargon-guard.py) duplicating Vale 3.17.1, which is installed and used in 10+ repos and referenced 0 times by the guard; plus an unmeasured share of rule-guard.py's 1362 lines duplicating 41 existing permissions.deny rules. -> None
- **2026-08-24** Is there a proven tool for 'prove this system can be rebuilt from nothing', to replace the hand-written nightly drill runner at ~/.claude/sc
  - decision: KEEP ~/.claude/scripts/drills/run.py. It is a drill REGISTER - 13 entries, 5 named as not yet written, with an orphan check - and no product on the market is th
  - metric: 13 registered, 8 with a command, 5 NOT WRITTEN; ai.estate.drills last exit = 1; its plist is in no git repo. -> None

## Delivery outcomes

`python3 science/outcomes.py ship --days 7; python3 science/outcomes.py attention --days 7`

- last 7 days: 665 commits across 6 repos
- founder messages 4246, complaints 267 (6.3%)
- spend USD 9045.2, USD per commit 13.6
- machine learning: none. Nothing here trains a model; every number is a count or a ratio.

## Predictions

`python3 science/outcomes.py rate`

- 22 recorded before a repair, 7 scored after, hit rate 43%

## Foresight: will this PR go red?

`python3 science/foresight.py report`

- trained 2026-08-29T18:53Z on 1882 labelled PRs; 32% of first runs were red
- unseen newest 377 PRs: accuracy 74% against a base rate of 72%; Brier 0.175
- model beats the base rate on unseen PRs
- strongest signals: r_crew (+0.49), log_files (+0.43), r_prospector (-0.32), log_add (+0.31), log_del (-0.26)
- live: 20 open PRs predicted before their CI finished, 5 scored, hit rate 40%
