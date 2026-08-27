# Research capability, graded

Generated 2026-08-27 by `python3 science/research_grade.py`. Two directions, graded separately (R37): **Outward** is what the estate learned from the world, **Inward** is what it learned about itself. Every row re-runs; no number is typed by hand.

| Direction | Grade | One sentence |
|---|---|---|
| Outward | **ELITE** | 25 of 25 questions fed a decision; 0 stale, 0 with no source. |
| Inward | **GAP** | foresight trained; 0 of 11 predictions scored. |

## Outward — questions answered from the world

Source: `science/RESEARCH-LEDGER.jsonl`.

| What | Value | How it is counted |
|---|---|---|
| Questions asked | 25 | rows in `science/RESEARCH-LEDGER.jsonl` |
| Decisions fed | 25 (100%) | rows whose `decision_fed` carries text |
| Questions still open | 0 | rows with no `decision_fed` |
| Median question to decision | 0.0h | `decided_at` - `asked_at`, else day granularity |
| Sources cited | 245 total, median 8 per question (min 1, max 40) | `len(row['sources'])` |
| Questions with no source | 0 | `sources` empty |

25 of 25 fed rows record only a day, not a timestamp, so they count as 0h. The median is a floor, not a measurement, until the ledger carries `asked_at` and `decided_at`.

### Stale questions (>7 days, no decision fed)

None. Every open question is under 7 days old.

## Inward — what the estate knows about itself

| What | Value | Evidence |
|---|---|---|
| Foresight model | TRAINED on 565 labelled PRs; holdout accuracy 0.602 vs base rate 0.593 (model beats the base rate on unseen PRs) | `science/foresight-state.json` |
| Predictions recorded | 11 | `science/predictions.jsonl`, `model == foresight` |
| Predictions scored | 0 | rows carrying `scored_at` |
| Hit rate | n/a, nothing scored | 0 correct of 0 scored |

## Re-run this page

```
python3 science/research_grade.py --print   # the page, written nowhere
python3 science/research_grade.py --check   # exit 1 when a question is stale
```
