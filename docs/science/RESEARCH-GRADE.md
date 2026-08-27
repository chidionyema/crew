# Research capability, graded

Generated 2026-08-27 by `python3 science/research_grade.py`. Two directions, graded separately (R37): **Outward** is what the estate learned from the world, **Inward** is what it learned about itself. Every row re-runs; no number is typed by hand.

| Direction | Grade | One sentence |
|---|---|---|
| Outward | **ELITE** | 25 of 25 questions fed a decision; 0 stale, 0 with no source; intake fresh, 0 candidates (0 late). |
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

## Outward intake — releases the world shipped, and what the estate did with them

Source: `science/RESEARCH-INTAKE.jsonl`, watch list `science/research-sources.json`.

| What | Value | How it is counted |
|---|---|---|
| Last pull | 2026-08-27T14:51:47+00:00 (fresh, 0.0d ago) | `science/research-intake-state.json` `last_pull`, red past 2 days |
| Repos watched | 22 (0 unreachable on the last pull) | `research-sources.json` `watch` |
| Releases filed | 22 (22 baseline) | rows on the intake ledger; baseline = first release seen per repo |
| Candidates unanswered | 0 (0 RED, >7d) | `status == candidate` |
| Adopted / declined | 0 / 0 | `status` with a ticket |

| Seen | Row | Release | Status |
|---|---|---|---|
| 2026-08-27 | GitOps (at k8s time) | [fluxcd/flux2 v2.9.4](https://github.com/fluxcd/flux2/releases/tag/v2.9.4) | baseline |
| 2026-08-27 | Admission policy | [kyverno/kyverno v1.19.0](https://github.com/kyverno/kyverno/releases/tag/v1.19.0) | baseline |
| 2026-08-27 | Data | [duckdb/duckdb v1.5.5](https://github.com/duckdb/duckdb/releases/tag/v1.5.5) | baseline |
| 2026-08-27 | Data | [dbt-labs/dbt-core v1.12.3](https://github.com/dbt-labs/dbt-core/releases/tag/v1.12.3) | baseline |
| 2026-08-27 | Job monitoring | [healthchecks/healthchecks v4.3](https://github.com/healthchecks/healthchecks/releases/tag/v4.3) | baseline |
| 2026-08-27 | Notifications | [caronc/apprise v1.13.0](https://github.com/caronc/apprise/releases/tag/v1.13.0) | baseline |
| 2026-08-27 | Backups | [restic/restic v0.19.1](https://github.com/restic/restic/releases/tag/v0.19.1) | baseline |
| 2026-08-27 | Secrets | [getsops/sops v3.13.3](https://github.com/getsops/sops/releases/tag/v3.13.3) | baseline |
| 2026-08-27 | Secrets | [FiloSottile/age v1.3.1](https://github.com/FiloSottile/age/releases/tag/v1.3.1) | baseline |
| 2026-08-27 | Identity | [spiffe/spire v1.15.3](https://github.com/spiffe/spire/releases/tag/v1.15.3) | baseline |


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
