# Science lane showcase

Generated 2026-08-30T21:05Z by `python3 science/showcase.py`. Every number is read at generation
time; the command under each heading reproduces it. A section that cannot see its source says BLIND.

## Progress since the previous run

Previous run: 2026-08-30T19:04Z.

- producers discovered: 5224 -> 5247

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
| false_success | False-success rate: how often an agent's "resolved" claim on the board was rejected by the prover (crew#631 CP | `python3 science/false_success.py` | hand-run |
| foresight | Foresight: predict a red CI run before the push, and score the prediction after (crew#405) | `python3 science/foresight.py` | launchd com.founder.sciencecollect via scripts/science-collect |
| friction | What the founder has had to say twice, measured over every transcript on this machine | `python3 science/friction.py` | hand-run |
| law_enforcement | Law enforcement coverage: which laws are machine-enforced, which are prose | `python3 science/law_enforcement.py` | launchd com.founder.lawenforcement |
| ledger | Writer for the research ledger (crew#72 row 1) | `python3 science/ledger.py` | hand-run |
| map_covers_laws | Every law in AGENTS.md has a check written for it in enforcement-map.json | `python3 science/map_covers_laws.py` | hand-run |
| outcomes | Collect what the estate produced, so spend can be divided by something | `python3 science/outcomes.py` | launchd com.founder.sciencecollect via scripts/science-collect |
| producers | Every producer of data in the estate, discovered by class rather than typed by hand | `python3 science/producers.py` | hand-run |
| research_grade | Grade the general-purpose research capability from its own ledger (crew#508) | `python3 science/research_grade.py` | hand-run |
| research_inspect_grade | crew#701 CP1: the Inspect grader, run by science/research_run.py in its own interpreter | `python3 science/research_inspect_grade.py` | hand-run |
| research_intake | Scheduled outward research intake (crew#508 CP8) | `python3 science/research_intake.py` | hand-run |
| research_run | crew#701 CP1: one graded research report, end to end, on a GitHub runner | `python3 science/research_run.py` | hand-run |
| research_worker | The research worker: GPT Researcher through the router, every report graded by Inspect, every | `python3 science/research_worker.py` | hand-run |
| self_grade | Weekly self-grade of the research loop (LAW 35, crew#72 row 4) | `python3 science/self_grade.py` | hand-run |
| transcripts | Read Claude Code session transcripts incrementally, by byte offset (crew#319, crew#74 row 4) | `python3 science/transcripts.py` | launchd com.founder.sciencecollect via scripts/science-collect |
| velocity | Velocity per lane, measured from the board, never felt (crew#527 CP1) | `python3 science/velocity.py` | hand-run |


## Lanes

`sqlite3 science/warehouse.db "select source, count(*) from facts where ingested_at >= datetime('now','-24 hours') group by source"`

BLIND: science/warehouse.db has no readable facts table (no such table: facts)

## Warehouse

`sqlite3 science/warehouse.db "select count(*), count(distinct source), max(ingested_at) from facts"`

BLIND: science/warehouse.db has no readable facts table (no such table: facts)

## Data map (LAW 50)

`python3 science/datamap.py --check`

- 60 register entries (COLLECTED 35, EXCLUDED 9, NEVER_EMITTED 4, WIRED_NEVER 11, WRITER_DEAD 1); 5247 producers discovered at the last census
- shape walk: BLIND (science/shapes.json empty or absent; no walk has landed)
- domains blind at the last census: cluster_live
- contract violations now: 1

## Research ledger

`python3 -c "import json; print(sum(1 for l in open('science/RESEARCH-LEDGER.jsonl')))"`

- 31 entries, 2026-08-23 to 2026-08-28; 31 record the decision they fed

- **2026-08-24** Which of the estate's hand-written Claude Code guard hooks (rule-guard, goal-guard, tracked, jargon-guard, context-guard-hook) can be expres
  - decision: Replace one, split one, delete half of one, keep two. (1) jargon-guard.py -> Vale 3.17.1, already installed, already configured in 10+ repos: highest-value swap
  - metric: 269 lines (jargon-guard.py) duplicating Vale 3.17.1, which is installed and used in 10+ repos and referenced 0 times by the guard; plus an unmeasured share of rule-guard.py's 1362 lines duplicating 41 existing permissions.deny rules. -> None
- **2026-08-24** Is there a proven tool for 'prove this system can be rebuilt from nothing', to replace the hand-written nightly drill runner at ~/.claude/sc
  - decision: KEEP ~/.claude/scripts/drills/run.py. It is a drill REGISTER - 13 entries, 5 named as not yet written, with an orphan check - and no product on the market is th
  - metric: 13 registered, 8 with a command, 5 NOT WRITTEN; ai.estate.drills last exit = 1; its plist is in no git repo. -> None
- **2026-08-28** Would this market pay at least twice the price of an idea dossier for a five-year survival probability conditioned on industry code and regi
  - decision: Whether prospector's next price test sells a survival rating beside the dossier (SCALE_market hypothesis 7 test: two checkout pages, 200 visitors each, pass if 
  - metric: 0 ideas on the ledger; three contract rows FAIL (no data) -> None

## Delivery outcomes

`python3 science/outcomes.py ship --days 7; python3 science/outcomes.py attention --days 7`

- last 7 days: 488 commits across 6 repos
- founder messages 1990, complaints 92 (4.6%)
- spend: BLIND (warehouse absent)
- machine learning: none. Nothing here trains a model; every number is a count or a ratio.

## Predictions

`python3 science/outcomes.py rate`

- 13 recorded before a repair, 2 scored after, hit rate 50%

## Ideas: the prospector contract (crew#537)

`python3 -c "import json; print(sum(1 for l in open('science/RESEARCH-LEDGER.jsonl') if json.loads(l).get('kind')=='idea'))"`

| Row | Value | Grade |
|---|---|---|
| ideas generated per week | 1 | ok |
| ideas graded (forecast with source) | 1 | ok |
| ideas resolved with Brier | 0 | FAIL (no data) |

- 1 idea rows in the ledger (`kind: idea`, written by `python3 science/ledger.py add --kind idea --forecast P`); resolved with `--outcome 0|1`. Red until the first business idea lands (CP5).

## Foresight: will this PR go red?

`python3 science/foresight.py report`

BLIND: science/foresight-state.json absent (python3 science/foresight.py train)

## False success: claims the prover rejected

`python3 science/false_success.py --days 30`

- false-success rate n/a (no claim decided yet): 0 rejected of 0 decided claims, 1 pending, last 30d
- a claim is an agent labelling a ticket RESOLVED_PENDING_VERIFICATION; the verdict of the moment is the prover App's next move on it (idp ticket-verification.yml)
  - pending #636 ticket-verify canary (crew#631 CP5): an agent-set VERIFIED must be rev
