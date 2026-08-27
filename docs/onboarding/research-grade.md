# Onboarding: the research grade page

## What it is

`science/research_grade.py` grades the estate's research capability in two directions and writes
`docs/science/RESEARCH-GRADE.md`. **Outward** is counted from `science/RESEARCH-LEDGER.jsonl`:
questions asked, decisions fed, median question-to-decision, sources per question, and a `RED`
row for any question over 7 days old with no decision. **Inward** is read from what the estate
learned about itself: `science/foresight-model.json` (committed) or `science/foresight-state.json`
(gitignored working file), plus scored rows in `science/predictions.jsonl`.

Each block is graded ELITE / GAP / BLIND, and a BLIND block puts itself on the page's first line.

## Use it

```
python3 science/research_grade.py            # write docs/science/RESEARCH-GRADE.md
python3 science/research_grade.py --print    # write nothing, show the page
python3 science/research_grade.py --check    # exit 1 when a question is stale
python3 -m pytest -q tests/test_crew508_research_grade.py
```

## Add a question so it counts

Append one JSON object per line to `science/RESEARCH-LEDGER.jsonl`:

```json
{"date": "2026-08-27", "ticket": "crew#508", "owner": "science",
 "question": "...", "decision_fed": "...", "sources": ["https://..."],
 "findings": ["..."], "metric": "...", "metric_before": "...", "metric_after": null}
```

`decision_fed` empty or absent means the question is still open; after 7 days it becomes a RED
row on the page with your ticket and name on it. Add `asked_at` and `decided_at` (ISO
timestamps) and the median stops being a floor and becomes a measurement — without them a
same-day decision counts as 0h and the page says so.

## Retrain the inward half

```
python3 science/foresight.py pull            # GitHub API -> science/ci/ (gitignored)
python3 science/foresight.py train           # needs scikit-learn; the estate venv has it
```

`train` exits 2 BLIND when `science/ci/` is empty, and the system python3 has no sklearn — use
the estate venv interpreter. Both were the measured blockers on 2026-08-27 (crew#508 CP3), and
both are recorded in `science/foresight-model.json`.
