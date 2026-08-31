# Onboarding — the audit register and roadmap sections of the showcase

## What it is for

Auditing. A buyer's engineer, or the founder, asks: exactly which datasets does the
science lane copy out of the estate, who writes each one, how sensitive is it, how long
is it kept, and what did the lane decide *not* to collect and why. Before this, the
answer lived in `science/sources.json` — complete, but a JSON file nobody is shown is
not transparency (LAW 28). The showcase page now renders it, plus the lane's roadmap
from `science/PLAN.md`, on every collector run.

## What it costs

Nothing new. `science/showcase.py` already ran on every `scripts/science-collect` cycle;
these are two more sections on the same page, one read of `sources.json`, one read-only
query of `warehouse.db`, one read of `PLAN.md` and one `git log -1` for its date.

## What it reads, and what it does not change

Reads `science/sources.json`, `science/warehouse.db` (read-only URI), `science/PLAN.md`.
Writes only `docs/science/SHOWCASE.md`, like every other section. Nothing here edits the
register: the register stays owned by `collect.py --check`, which fails when the machine
crawl finds a store that is neither collected nor declined — that gate is what makes the
page trustworthy rather than decorative.

## How it stays living rather than drifting

- The page is generated; hand edits are overwritten on the next run.
- The dataset rows come from the same file the collector enforces, so the page cannot
  claim a dataset the pipeline does not check.
- The roadmap section re-reads `PLAN.md` each run and prints its last-changed date, so a
  stale plan is visible as an old date, not hidden by a fresh page timestamp.
- If `sources.json` or `PLAN.md` is missing, the section renders `BLIND:` with the path
  it looked for, never an empty table (LAW 45).
