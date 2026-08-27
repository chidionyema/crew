# Science lane showcase

Generated 2026-08-27T00:25Z by `python3 science/showcase.py`. Every number is read at generation
time; the command under each heading reproduces it. A section that cannot see its source says BLIND.

## Progress since the previous run

Previous run: 2026-08-27T00:20Z.

No number changed.

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
| friction | What the founder has had to say twice, measured over every transcript on this machine | `python3 science/friction.py` | hand-run |
| law_enforcement | Law enforcement coverage: which laws are machine-enforced, which are prose | `python3 science/law_enforcement.py` | launchd com.founder.lawenforcement |
| map_covers_laws | Every law in AGENTS.md has a check written for it in enforcement-map.json | `python3 science/map_covers_laws.py` | hand-run |
| outcomes | Collect what the estate produced, so spend can be divided by something | `python3 science/outcomes.py` | launchd com.founder.sciencecollect via scripts/science-collect |
| producers | Every producer of data in the estate, discovered by class rather than typed by hand | `python3 science/producers.py` | hand-run |


## Warehouse

`sqlite3 science/warehouse.db "select count(*), count(distinct source), max(ingested_at) from facts"`

- 47,399 rows across 27 sources; last ingest 2026-08-26T18:52:52+00:00
- 0 of 28 declared sources carry owner, method, retention and sensitivity
- stale past their SLA: predictions (72h)

## Data map (LAW 50)

`python3 science/datamap.py --check`

- 51 register entries (COLLECTED 10, EXCLUDED 5, NEVER_EMITTED 13, WIRED_NEVER 23); 8152 producers discovered at the last census
- 755 field paths in the last shape walk
- domains blind at the last census: cluster_live
- contract violations now: BLIND (crew#71 not merged)

## Research ledger

`python3 -c "import json; print(sum(1 for l in open('science/RESEARCH-LEDGER.jsonl')))"`

- 23 entries, 2026-08-23 to 2026-08-25; 23 record the decision they fed

- **2026-08-24** Founder table 2026-08-24 (custom code is a last resort): does each proposed open-source replacement hold up online — pre-commit, ruff, pyrig
  - decision: docs/STANDARDS.md founder-table section (PR #124): pre-commit ADOPT (crew#130), ruff ADOPT, pyright kept, Gotify rejected, Apprise kept as the standard, Dagster
  - metric: 0 of 7 -> 7 of 7
- **2026-08-24** What replaces a hand-written ephemeral self-hosted GitHub Actions runner on Kubernetes, and does this estate still need one at all?
  - decision: Do NOT write deploy/k8s/base/runner.yaml, and do not port entrypoint.sh. The fifth compose service gets NO Kubernetes representation, and that is the finished a
  - metric: 4 of 5 (the runner had no manifest and no recorded reason) -> 5 of 5 (four declared, the runner deliberately absent with the measurement that says why, deploy/k8s/base/kustomization.yaml)
- **2026-08-25** What is the one front-end platform for every Bytesync public surface (parent site plus each company's brand and store), so that a new brand 
  - decision: STANDARDS.md gains a Front end row: Next.js + Payload 3 + one design system with per-brand tokens + Medusa 2 under selling brands; brand = config + collection +
  - metric: 0 of 3 (Store.Web, look-engine, mumchimp-medusa storefront; no row existed) -> row exists; still 0 of 3 until crew#235 CP2 lands, then 1 of 3

## Delivery outcomes

`python3 science/outcomes.py ship --days 7; python3 science/outcomes.py attention --days 7`

- last 7 days: 795 commits across 6 repos
- founder messages 2005, complaints 103 (5.1%)
- spend USD 6602.54, USD per commit 8.31
- machine learning: none. Nothing here trains a model; every number is a count or a ratio.

## Predictions

`python3 science/outcomes.py rate`

- 1 recorded before a repair, 1 scored after, hit rate 100%
