# Onboarding: research grade, hourly

- Generator: `science/research_grade.py` (reads `science/RESEARCH-LEDGER.jsonl`, `science/predictions.jsonl`, `science/foresight-model.json`).
- Publisher: `scripts/estate-snapshot` step "regenerate the research grade", then the page is copied to the snapshot branch with the science page (`RESEARCH_PAGE`).
- Gate: `python3 science/research_grade.py --check` exits 1 when a question is older than 7 days with no decision fed.
- Test: `python3 -m pytest -q tests/test_incident_crew508_research_grade_published_hourly.py`.
