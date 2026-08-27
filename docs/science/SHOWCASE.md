# Science lane showcase

Generated 2026-08-27T08:59Z by `python3 science/showcase.py`. Every number is read at generation
time; the command under each heading reproduces it. A section that cannot see its source says BLIND.

## Progress since the previous run

First run: nothing to diff yet.

## Capabilities

`python3 science/showcase.py  (reads science/*.py, scripts/science-collect, scripts/verify.d, launchd)`

| Capability | What it answers | Run | Scheduled by |
|---|---|---|---|
| capa | Did the fix actually stop him having to say it again | `python3 science/capa.py` | hand-run |
| collect | Collect every estate data store into one queryable table | `python3 science/collect.py` | launchd com.founder.sciencecollect via scripts/science-collect |
| datamap | The estate's data dictionary, generated rather than written | `python3 science/datamap.py` | CI: scripts/verify.d/26-datamap-register.sh |
| dbt_build | Generate the dbt project's `facts` model from the one registry | `python3 science/dbt_build.py` | hand-run |
| docsmap | Inventory every document this estate owns, and say which ones fail the standard | `python3 science/docsmap.py` | CI: scripts/verify.d/95-docs.sh |
| duckdb_differential | Does DuckDB's `read_json_auto` read this estate's stores the same way collect.py does? | `python3 science/duckdb_differential.py` | hand-run |
| export_drill | crew#74 row 1: the warehouse exit drill | `python3 science/export_drill.py` | hand-run |
| foresight | Foresight: predict a red CI run before the push, and score the prediction after (crew#405) | `python3 science/foresight.py` | launchd com.founder.sciencecollect via scripts/science-collect |
| friction | What the founder has had to say twice, measured over every transcript on this machine | `python3 science/friction.py` | hand-run |
| law_enforcement | Law enforcement coverage: which laws are machine-enforced, which are prose | `python3 science/law_enforcement.py` | launchd com.founder.lawenforcement |
| ledger | Writer for the research ledger (crew#72 row 1) | `python3 science/ledger.py` | hand-run |
| map_covers_laws | Every law in AGENTS.md has a check written for it in enforcement-map.json | `python3 science/map_covers_laws.py` | hand-run |
| outcomes | Collect what the estate produced, so spend can be divided by something | `python3 science/outcomes.py` | launchd com.founder.sciencecollect via scripts/science-collect |
| producers | Every producer of data in the estate, discovered by class rather than typed by hand | `python3 science/producers.py` | hand-run |
| self_grade | Weekly self-grade of the research loop (LAW 35, crew#72 row 4) | `python3 science/self_grade.py` | hand-run |
| transcripts | Read Claude Code session transcripts incrementally, by byte offset (crew#319, crew#74 row 4) | `python3 science/transcripts.py` | launchd com.founder.sciencecollect via scripts/science-collect |


## Warehouse

`sqlite3 science/warehouse.db "select count(*), count(distinct source), max(ingested_at) from facts"`

BLIND: /private/tmp/claude-501/-Users-chidionyema-dev-code/09cd04a6-12cd-4d9b-84af-10b1620739d1/scratchpad/wt-403b/science/warehouse.db absent

## Data map (LAW 50)

`python3 science/datamap.py --check`

- 58 register entries (COLLECTED 29, EXCLUDED 9, NEVER_EMITTED 9, WIRED_NEVER 11); 8206 producers discovered at the last census
- 0 field paths in the last shape walk
- domains blind at the last census: cluster_live, warehouse
- contract violations now: BLIND (crew#71 not merged)

## Research ledger

`python3 -c "import json; print(sum(1 for l in open('science/RESEARCH-LEDGER.jsonl')))"`

- 24 entries, 2026-08-23 to 2026-08-27; 24 record the decision they fed

- **2026-08-24** What replaces a hand-written ephemeral self-hosted GitHub Actions runner on Kubernetes, and does this estate still need one at all?
  - decision: Do NOT write deploy/k8s/base/runner.yaml, and do not port entrypoint.sh. The fifth compose service gets NO Kubernetes representation, and that is the finished a
  - metric: 4 of 5 (the runner had no manifest and no recorded reason) -> 5 of 5 (four declared, the runner deliberately absent with the measurement that says why, deploy/k8s/base/kustomization.yaml)
- **2026-08-25** What is the one front-end platform for every Bytesync public surface (parent site plus each company's brand and store), so that a new brand 
  - decision: STANDARDS.md gains a Front end row: Next.js + Payload 3 + one design system with per-brand tokens + Medusa 2 under selling brands; brand = config + collection +
  - metric: 0 of 3 (Store.Web, look-engine, mumchimp-medusa storefront; no row existed) -> row exists; still 0 of 3 until crew#235 CP2 lands, then 1 of 3
- **2026-08-27** Is there a mature open-source tool that predicts a red CI run / selects tests from repository history, and which learner and prediction-trac
  - decision: Foresight uses scikit-learn LogisticRegression (requirements-dev floor >=1.5) trained on the estate's own run history; no test-selection product is bought or bu
  - metric: no prediction existed (1 hand prediction ever scored) -> 1078 labelled PRs; holdout 216: accuracy 0.676 vs base 0.634, red precision 0.846, Brier 0.209; 11 open PRs predicted before CI

## Delivery outcomes

`python3 science/outcomes.py ship --days 7; python3 science/outcomes.py attention --days 7`

- last 7 days: 795 commits across 6 repos
- founder messages 2005, complaints 103 (5.1%)
- spend: BLIND (warehouse absent)
- machine learning: none. Nothing here trains a model; every number is a count or a ratio.

## Predictions

`python3 science/outcomes.py rate`

- 13 recorded before a repair, 1 scored after, hit rate 100%

## Foresight: will this PR go red?

`python3 science/foresight.py report`

BLIND: /private/tmp/claude-501/-Users-chidionyema-dev-code/09cd04a6-12cd-4d9b-84af-10b1620739d1/scratchpad/wt-403b/science/foresight-state.json absent (python3 science/foresight.py train)
