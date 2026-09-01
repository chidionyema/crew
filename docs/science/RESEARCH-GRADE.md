# Research capability, graded

Generated 2026-09-01 by `python3 science/research_grade.py`. Two directions, graded separately (R37): **Outward** is what the estate learned from the world, **Inward** is what it learned about itself. Every row re-runs; no number is typed by hand.

| Direction | Grade | One sentence |
|---|---|---|
| Outward | **GAP** | 31 of 31 questions fed a decision; 0 stale, 0 with no source; intake RED, 4 candidates (0 late); ideas: 0 scored in 1d of 1 ever. |
| Inward | **GAP** | foresight trained; 0 of 11 predictions scored. |

## Delivered — receipts authored outside this lane

Self scoring is banned (founder, 2026-08-31, verbatim: "the research ledger should never score itself SELF SCORING IS BANNED FOREVER"). Every count above comes from the lane's own ledger, so none of it can raise the grade past GAP. Only a receipt written by the consumer of a research output — pointing at the merged PR or commit where it changed what shipped (`used_in`) — counts as delivery. Source: `science/DELIVERY-RECEIPTS.jsonl`.

None. Nothing this lane produced has a receipt from anyone who used it; the grade floors at GAP whatever the self-authored numbers say.

## Outward — questions answered from the world

Source: `science/RESEARCH-LEDGER.jsonl`.

| What | Value | How it is counted |
|---|---|---|
| Questions asked | 31 | rows in `science/RESEARCH-LEDGER.jsonl` |
| Decisions fed | 31 (100%) | rows whose `decision_fed` carries text |
| Questions still open | 0 | rows with no `decision_fed` |
| Median question to decision | 0.0h | `decided_at` - `asked_at`, else day granularity |
| Sources cited | 342 total, median 9 per question (min 1, max 40) | `len(row['sources'])` |
| Questions with no source | 0 | `sources` empty |

31 of 31 fed rows record only a day, not a timestamp, so they count as 0h. The median is a floor, not a measurement, until the ledger carries `asked_at` and `decided_at`.

## Outward — ideas for the store front (crew#659)

Source: rows with `kind: idea` on the ledger, written only by `science/research_worker.py`, each graded by Inspect before it is written. The founder's measure (2026-08-30): scored ideas per day above zero, or the lane is GAP whatever else it says.

| What | Value | How it is counted |
|---|---|---|
| Ideas on the ledger | 1 | rows with `kind == idea` |
| Ideas with a score | 0 | rows carrying a numeric `score` (Inspect model_graded_qa) |
| Scored in the last 1d | 0 (RED: no progress) | `decided_at` inside the window |
| Mean score | n/a | C=1, P=0.5, I=0 |

### Stale questions (>7 days, no decision fed)

None. Every open question is under 7 days old.

## Outward intake — releases the world shipped, and what the estate did with them

Source: `science/RESEARCH-INTAKE.jsonl`, watch list `science/research-sources.json`.

| What | Value | How it is counted |
|---|---|---|
| Last pull | 2026-08-30T03:29:58+00:00 (RED, 2.6d ago) | `science/research-intake-state.json` `last_pull`, red past 2 days |
| Repos watched | 22 (0 unreachable on the last pull) | `research-sources.json` `watch` |
| Releases filed | 26 (22 baseline) | rows on the intake ledger; baseline = first release seen per repo |
| Candidates unanswered | 4 (0 RED, >7d) | `status == candidate` |
| Adopted / declined | 0 / 0 | `status` with a ticket |

| Seen | Row | Release | Status |
|---|---|---|---|
| 2026-08-30 | Secrets | [FiloSottile/age v1.3.2](https://github.com/FiloSottile/age/releases/tag/v1.3.2) | candidate |
| 2026-08-30 | Agent traces | [langfuse/langfuse v4.24.0](https://github.com/langfuse/langfuse/releases/tag/v4.24.0) | candidate |
| 2026-08-30 | Scheduling | [dagster-io/dagster 1.13.20](https://github.com/dagster-io/dagster/releases/tag/1.13.20) | candidate |
| 2026-08-30 | Code quality | [astral-sh/ruff 0.16.5](https://github.com/astral-sh/ruff/releases/tag/0.16.5) | candidate |
| 2026-08-27 | GitOps (at k8s time) | [fluxcd/flux2 v2.9.4](https://github.com/fluxcd/flux2/releases/tag/v2.9.4) | baseline |
| 2026-08-27 | Admission policy | [kyverno/kyverno v1.19.0](https://github.com/kyverno/kyverno/releases/tag/v1.19.0) | baseline |
| 2026-08-27 | Data | [duckdb/duckdb v1.5.5](https://github.com/duckdb/duckdb/releases/tag/v1.5.5) | baseline |
| 2026-08-27 | Data | [dbt-labs/dbt-core v1.12.3](https://github.com/dbt-labs/dbt-core/releases/tag/v1.12.3) | baseline |
| 2026-08-27 | Job monitoring | [healthchecks/healthchecks v4.3](https://github.com/healthchecks/healthchecks/releases/tag/v4.3) | baseline |
| 2026-08-27 | Notifications | [caronc/apprise v1.13.0](https://github.com/caronc/apprise/releases/tag/v1.13.0) | baseline |


## Inward — what the estate knows about itself

| What | Value | Evidence |
|---|---|---|
| Foresight model | TRAINED on 565 labelled PRs; holdout accuracy 0.602 vs base rate 0.593 (beats the base rate on unseen PRs by 0.9 points (0.602 vs 0.593) - a thin edge, not a claim) | `science/foresight-model.json` |
| Predictions recorded | 11 | `science/predictions.jsonl`, `model == foresight` |
| Predictions scored | 0 | rows carrying `scored_at` |
| Hit rate | n/a, nothing scored | 0 correct of 0 scored |

## Re-run this page

```
python3 science/research_grade.py --print   # the page, written nowhere
python3 science/research_grade.py --check   # exit 1 when a question is stale
```
