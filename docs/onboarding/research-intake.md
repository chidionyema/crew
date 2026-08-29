# Onboarding: research intake

- **Watch list:** `science/research-sources.json` — one entry per STANDARDS.md row and GitHub
  repo. Add a row when a standard names a new tool; `tests/test_crew508_research_intake.py`
  refuses an entry whose `row` is not on `docs/STANDARDS.md`.
- **Ledger:** `science/RESEARCH-INTAKE.jsonl` — `seen`, `row`, `repo`, `tag`, `published_at`,
  `url`, `status` (`baseline` | `candidate` | `adopted` | `declined`), `ticket`.
- **State:** `science/research-intake-state.json` — `last_pull`, `watched`, `unreachable`, `new`.
- **Answering a candidate:** edit its row's `status` and `ticket`. Unanswered past 7 days it
  is a RED row on `docs/science/RESEARCH-GRADE.md` and Outward drops to GAP.
- **Source of truth for releases:** the GitHub Releases API via `gh api` (tags as fallback).
  Renovate/Dependabot were rejected (LAW 43): they watch dependency manifests and open PRs;
  the estate needs a graded ledger against a standards page.
- **Schedule:** idp `idp/scheduler/schedule.yml` `com.estate.research-intake`, daily.
