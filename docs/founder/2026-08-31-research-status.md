# Research function: status, 2026-08-31 ~22:4xZ

Asked by the founder: "the stack for the research team and update on where they are with their objectives, the research engine, prospector etc". Measured from origin/main @ 65b7e760 (crew), generated pages, gh issue/run state — never memory. Full receipts inline.

## Headline

The research function is built but parked. All of its code, ledgers and graded pages exist; nothing runs on a schedule, the ledger has had no new row for 3 days, and every open research objective sits at 0 checkpoints ticked. The grade page is now honest: both directions read GAP, floored there until someone outside the lane records a delivery — the ELITE rows were removed on 2026-08-31 (PR crew#731) under the self-scoring ban.

## 1. The stack (what actually exists)

- Python pipeline in crew `science/`: `research_worker.py`, `research_run.py`, `research_intake.py` (22 repos watched), `ledger.py` → `science/RESEARCH-LEDGER.jsonl` (31 rows, newest 2026-08-28), graded by Inspect (UK AISI) via `research_inspect_grade.py`, pages generated hourly by `scripts/estate-snapshot` → `docs/science/SHOWCASE.md`, `docs/science/RESEARCH-GRADE.md`.
- One CI research engine: `.github/workflows/science-research.yml` (GPT Researcher through the router, Inspect grades, MLflow records) — dispatch-only, no cron. Last ran 2026-08-30 (burst of 5, 4 success / 1 failure). Idle since.
- NOT running: the launchd collector (`com.founder.sciencecollect`) exists in git only, never installed — confirmed by `launchctl list` and the 2026-08-29 research-department audit. The DuckDB warehouse is BLIND (`no such table: facts`). Foresight state file absent.
- Scheduler question is unsettled three ways: charter says Dagster (RED), RESEARCH_PLATFORM_CAPABILITY.md says Argo, crew#701 rules Windmill. One answer is needed; Windmill is the standing ruling.

## 2. Objectives standing

| Item | State |
|---|---|
| crew#474 investor showcase | OPEN, 0/5 checkpoints, all expected dates passed |
| crew#475 charter into roles/science.md | DELIVERED (merged 2026-08-27) — the only delivered item |
| crew#508 science across lanes | OPEN, 0/5, overdue |
| crew#513 DSPy Fable-teacher/MiniMax-student | OPEN, 0/6, stuck 4 days at CP1 = founder confirms requirements |
| crew#659 ideas scoreboard | OPEN, 0/5 (1 idea ever on the ledger, 0 scored) |
| crew#701 research engine CP0–CP5 | OPEN, 0/6, CP0 = founder confirmation pending |
| crew#596 ROAD-TO-9D | OPEN, 0/2; research appears in one row of the whole road |

## 3. The research engine

Worker code and workflow exist and have run; no schedule anywhere (only cron in the family is weekly self-grade). Ledger silent 3 days. Intake last pulled 2026-08-30 03:29Z; 4 candidates (age, langfuse, dagster, ruff) sit unanswered, 0 adopted. Six unmerged research branches on origin. Output all-time: 31 ledger rows of which 1 is an idea; the rest are estate plumbing questions — the exact gap crew#659 opened ("we dropped the ball major on that one").

## 4. Prospector

- Shop live on mumchimp.com (storefront merged onto OKE, PR #792, 2026-08-30). Last merge #793 2026-08-30 20:57Z; nothing merged 2026-08-31.
- Storefront smoke is flapping: latest run FAILED 2026-08-31 14:58Z and correctly opened prospector#798 — the shop is serving code older than main; fix is the image `newTag` bump in `deploy/k8s/overlays/oke/kustomization.yaml`, permanent fix tracked idp#925.
- Money path: last proven 69+ days ago (2026-06-20); price rungs are marked HYPOTHESIS in config; no willingness-to-pay evidence since.
- Stale open P1s: #679 claims the engine is blocked on a PAST_DUE Fly invoice (unedited since 2026-08-23) — this predates the OKE move and contradicts the no-Fly ruling (R1) and the "Fly has zero apps" measurement; the ticket needs reconciling with where the engine actually deploys now, not paying. #661, #695 similarly stale. Escape-hatch drill has failed on every recorded run, 8 days stale.

## 5. Grade honesty

RESEARCH-GRADE.md now reads GAP/GAP with the self-scoring ban quoted in its own body; the lift path is `science/DELIVERY-RECEIPTS.jsonl`, which does not exist yet — "None. Nothing this lane produced has a receipt from anyone who used it." That is the honest floor working as ruled.

One live defect found this sweep, same silent-green class one page over: SHOWCASE.md still advertises 6 capabilities as "Scheduled by launchd com.founder.sciencecollect" while no such job is loaded and no plist installed — a green-looking column for something that has never run unattended. Ticketed.
