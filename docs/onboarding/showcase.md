# Onboarding — science/showcase.py

## What it is for

The science lane had eleven scripts, four JSONL stores, a warehouse and a research ledger,
and no single place that said what they do or whether they are moving. Every status
request was answered from memory. The showcase answers it from disk (crew#403).

## What it reads

| Section | Source |
|---|---|
| Capabilities | the first docstring line of every `science/*.py`; scheduling from `scripts/science-collect`, `scripts/verify.d/*.sh` and `~/.claude/scripts/launchagents/*.plist` |
| Warehouse | `science/warehouse.db` `facts`, staleness from `science/sources.json` |
| Data map | `science/verdicts.json`, `science/census.json`, `science/shapes.json`, `datamap.contract_violations()` |
| Research ledger | `science/RESEARCH-LEDGER.jsonl` |
| Delivery outcomes | `science/ships.jsonl`, `science/attention.jsonl`, spend facts in the warehouse, 7-day window |
| Predictions | `science/predictions.jsonl`, newest row per id |

## Progress

`science/showcase-state.json` (gitignored, per machine) holds the previous run's scalars.
The progress section is the diff. A first run says so instead of inventing a baseline.

## Rules it keeps

- A missing source is `BLIND:` plus the path (LAW 45). It is never an empty section.
- Every section shows the command that reproduces it (LAW 15).
- The page says plainly that no machine learning runs here: every number is a count or a ratio.

## Adding a section

Add a function raising `Blind` when its source is absent, a row in `SECTIONS` with its
reproducing command, its scalars in `numbers()`, and a branch in `render()`.
