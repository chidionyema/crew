# Research capability, graded

Generated 2026-08-28 by `python3 science/research_grade.py`. Two directions, graded separately (R37): **Outward** is what the estate learned from the world, **Inward** is what it learned about itself. Every row re-runs; no number is typed by hand.

| Direction | Grade | One sentence |
|---|---|---|
| Outward | **ELITE** | 30 of 30 questions fed a decision; 0 stale, 0 with no source; intake fresh, 2 candidates (0 late). |
| Inward | **ELITE** | foresight trained; 2 of 16 predictions scored. |

## Outward — questions answered from the world

Source: `science/RESEARCH-LEDGER.jsonl`.

| What | Value | How it is counted |
|---|---|---|
| Questions asked | 30 | rows in `science/RESEARCH-LEDGER.jsonl` |
| Decisions fed | 30 (100%) | rows whose `decision_fed` carries text |
| Questions still open | 0 | rows with no `decision_fed` |
| Median question to decision | 0.0h | `decided_at` - `asked_at`, else day granularity |
| Sources cited | 339 total, median 9.5 per question (min 1, max 40) | `len(row['sources'])` |
| Questions with no source | 0 | `sources` empty |

30 of 30 fed rows record only a day, not a timestamp, so they count as 0h. The median is a floor, not a measurement, until the ledger carries `asked_at` and `decided_at`.

### Stale questions (>7 days, no decision fed)

None. Every open question is under 7 days old.

## Outward intake — releases the world shipped, and what the estate did with them

Source: `science/RESEARCH-INTAKE.jsonl`, watch list `science/research-sources.json`.

| What | Value | How it is counted |
|---|---|---|
| Last pull | 2026-08-28T05:12:06+00:00 (fresh, 0.5d ago) | `science/research-intake-state.json` `last_pull`, red past 2 days |
| Repos watched | 22 (0 unreachable on the last pull) | `research-sources.json` `watch` |
| Releases filed | 24 (22 baseline) | rows on the intake ledger; baseline = first release seen per repo |
| Candidates unanswered | 2 (0 RED, >7d) | `status == candidate` |
| Adopted / declined | 0 / 0 | `status` with a ticket |

| Seen | Row | Release | Status |
|---|---|---|---|
| 2026-08-28 | Scheduling | [dagster-io/dagster 1.13.20](https://github.com/dagster-io/dagster/releases/tag/1.13.20) | candidate |
| 2026-08-28 | Code quality | [astral-sh/ruff 0.16.5](https://github.com/astral-sh/ruff/releases/tag/0.16.5) | candidate |
| 2026-08-27 | GitOps (at k8s time) | [fluxcd/flux2 v2.9.4](https://github.com/fluxcd/flux2/releases/tag/v2.9.4) | baseline |
| 2026-08-27 | Admission policy | [kyverno/kyverno v1.19.0](https://github.com/kyverno/kyverno/releases/tag/v1.19.0) | baseline |
| 2026-08-27 | Data | [duckdb/duckdb v1.5.5](https://github.com/duckdb/duckdb/releases/tag/v1.5.5) | baseline |
| 2026-08-27 | Data | [dbt-labs/dbt-core v1.12.3](https://github.com/dbt-labs/dbt-core/releases/tag/v1.12.3) | baseline |
| 2026-08-27 | Job monitoring | [healthchecks/healthchecks v4.3](https://github.com/healthchecks/healthchecks/releases/tag/v4.3) | baseline |
| 2026-08-27 | Notifications | [caronc/apprise v1.13.0](https://github.com/caronc/apprise/releases/tag/v1.13.0) | baseline |
| 2026-08-27 | Backups | [restic/restic v0.19.1](https://github.com/restic/restic/releases/tag/v0.19.1) | baseline |
| 2026-08-27 | Secrets | [getsops/sops v3.13.3](https://github.com/getsops/sops/releases/tag/v3.13.3) | baseline |


## Inward — what the estate knows about itself

| What | Value | Evidence |
|---|---|---|
| Foresight model | TRAINED on 1570 labelled PRs; holdout accuracy 0.726 vs base rate 0.723 (model beats the base rate on unseen PRs) | `science/foresight-state.json` |
| Predictions recorded | 16 | `science/predictions.jsonl`, `model == foresight` |
| Predictions scored | 2 | rows carrying `scored_at` |
| Hit rate | 50% | 1 correct of 2 scored |

## Re-run this page

```
python3 science/research_grade.py --print   # the page, written nowhere
python3 science/research_grade.py --check   # exit 1 when a question is stale
```
