# Moving a scheduled job onto Dagster

crew#126 says what we migrate to and in what order. This says how one job moves,
so slices can run in parallel without each session rediscovering the same two
traps. Step 1 of that ticket, Dagster, is the one in progress.

Scope: `science/scheduler/` in this repo, registered as code location
`estate-facts` in `idp/scheduler/workspace.yaml`. It runs on the idp venv, under
the one daemon `idp/bin/scheduler-up` starts; there is no second Dagster.

## What the first slice proved

Every source declared in `science/sources.json` (43 at the time of writing; the
test asserts the count against the file) is a Dagster asset carrying the
`stale_after_hours` window that file has always declared.
`science/scheduler/estate_dagster/sources.py` declares them, `facts.py` is the
registered location.

Before, nothing read `stale_after_hours`. `estate_watch.py:46` used one 3-hour
constant for every source and `estate_audit.py:1024` kept its own stale list.
The window was declared in one file and enforced against a different number in
two others, into two more logs.

## The recipe, per job

1. **Find the thing the job produces.** A file, a table, a report. That is the
   asset. The job is not the asset; the job is how the asset gets made. If a
   script produces nothing you can name, it is a guard, not a job, and it
   belongs in step 2 of crew#126 (OPA), not here.

2. **Find where its schedule is already declared.** Most of ours are declared
   twice: an interval in `jobs.json` and a threshold hardcoded in the script
   that checks it. Pick the declaration, delete the constant.

3. **Declare the asset with a `FreshnessPolicy.time_window`.** Warn at half the
   window so a producer slowing down is visible before it fails. This is the
   whole reason to be here: a stale asset is a failure predicted rather than
   reported.

4. **Prove it goes red.** Not "it loaded". A migrated job that can only report
   green is worse than the script it replaced, because it answers the question
   wrongly instead of not answering it. See both traps below.

5. **Delete the script.** Nothing is migrated until the old code is gone. A PR
   that adds Dagster code without deleting more than it adds is REWORK under
   crew#126's own rule, and AC6 wants the number printed.

## The two traps

Both produce a system that reports permanent health. Both were hit on slice 1.

**The evaluator ignores your timestamps.** `FreshnessPolicy` compares now
against the timestamp *Dagster* wrote on the last materialization event, not any
timestamp the event carries
(`dagster/_core/definitions/freshness_evaluator.py:65`, read at 1.13.19). So the
obvious wiring — poll every 15 minutes, record what you saw — marks every asset
fresh forever no matter what the file underneath is doing.

The fix is to make the event mean what the policy already assumes: record a
materialization only when the thing actually changed. Do not reach for
`build_last_update_freshness_checks`, which does read
`dagster/last_updated_timestamp` from metadata; it is superseded in 1.13,
removed in 2.0, and needs a sensor.

**Seeding is the same trap wearing a hat.** On the first run nothing has been
recorded, so everything counts as changed, and a producer that died three days
ago gets an event stamped NOW and reads healthy for the length of its own
window. Refuse to record a change that is already older than the window it is
measured against. The asset stays UNKNOWN, which is the honest reading: no
evidence of health is not evidence of health.

`decide()` in `sources.py` holds both refusals, and
`science/scheduler/tests/test_incident_false_green_at_seeding.py` asserts all three outcomes
including the permit case, because a guard only ever seen refusing has never
been shown to permit.

## Traps that only cost time

- **Python 3.14 has no `dagster-dbt` wheel.** `dagster` itself installs (1.13.19
  on the idp venv), but pip resolves `dagster-dbt` backwards to 0.22.6 and drags
  dagster down to 1.6.6, and the install reports success. The dbt half needs
  3.12 or 3.13.
- **`from __future__ import annotations` breaks the decorators.** It stringifies
  annotations, and `@dbt_assets` and `@multi_asset` resolve the real type object
  of the `context` parameter, so the decorator rejects a correct signature with
  an error naming the exact type it just refused.
- **`dbt` must be on PATH, not just in the resource.**
  `DbtProject.prepare_if_dev()` builds its own `DbtCliResource` with a bare
  `"dbt"` and cannot be told otherwise, so setting `dbt_executable` on the
  resource you pass to `Definitions` is not enough. Put the venv's `bin` on PATH
  in the module.
- **Observable source assets are not schedulable in 1.13.**
  `AssetSelection.groups(...)` resolves to zero keys, there is no
  `dagster asset observe` command, and the job then succeeds having done
  nothing. Use `@multi_asset` with `can_subset=True`.

## Running it

Nothing to start. `idp/scheduler/workspace.yaml` names
`../../crew/science/scheduler/estate_dagster/facts.py` as location `estate-facts`
(relative to the idp checkout, so no file names where a checkout lives, LAW 46),
and `idp/bin/scheduler-up` loads it with the schedule.yml jobs and refuses to
report "up" if it does not import. The dashboard is the scheduler's own,
the address `idp/bin/scheduler-up` prints on its `ui` line (`$DAGSTER_URL` below).

Freshness state, which is the answer to "is anything about to fail":

    curl -s "$DAGSTER_URL/graphql" -H 'Content-Type: application/json' \
      -d '{"query":"{ assetNodes { assetKey { path } freshnessStatusInfo { freshnessStatus } } }"}'

Tests, from the repo root, on any interpreter that has `dagster`
(`requirements-dev.txt` carries it):

    python -m pytest -q science/scheduler/tests

## What is not done

- `facts`, the dbt model (`definitions.py`), is not registered: the scheduler's
  interpreter is Python 3.14 and pip resolves `dagster-dbt` there back to
  0.22.6 with dagster 1.6.6, a downgrade of the running scheduler (measured
  2026-08-27). It waits for an interpreter that carries it, and it still reads
  the same files without declaring the dependency, so the two halves would be
  separate graphs even then.
- Nothing routes a FAIL anywhere yet. A stale asset is visible in the UI and
  over GraphQL and alerts nobody, which is an instrument nobody reads (LAW 28).
- The 25 other scheduled jobs are still launchd's.
