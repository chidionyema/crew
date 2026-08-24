# Moving a scheduled job onto Dagster

crew#126 says what we migrate to and in what order. This says how one job moves,
so slices can run in parallel without each session rediscovering the same two
traps. Step 1 of that ticket, Dagster, is the one in progress.

Scope: `science/dagster/` in this repo, code location `estate`, Python 3.12.

## What the first slice proved

28 fact files declared in `science/sources.json` are now Dagster assets, each
carrying the `stale_after_hours` window that file has always declared. Branch
`platform/dagster-migration`, `science/dagster/estate_dagster/sources.py`.

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
`tests/test_incident_false_green_at_seeding.py` asserts all three outcomes
including the permit case, because a guard only ever seen refusing has never
been shown to permit.

## Traps that only cost time

- **Python 3.14 has no Dagster wheel.** pip resolves `dagster-dbt` backwards to
  `0.11.14`, a 2021 release, the install reports success and `import dagster`
  then fails. Use `/usr/local/bin/python3.12`.
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

    export DAGSTER_HOME=~/.estate/dagster
    cd science/dagster
    ~/.estate/venvs/dagster/bin/dagster dev -m estate_dagster.definitions -p 3070

Freshness state, which is the answer to "is anything about to fail":

    curl -s http://127.0.0.1:3070/graphql -H 'Content-Type: application/json' \
      -d '{"query":"{ assetNodes { assetKey { path } freshnessStatusInfo { freshnessStatus } } }"}'

`DAGSTER_HOME` is `~/.estate/dagster`, not a vendor-named directory, per R8.

## What is not done

- The code location runs under `dagster dev`, which dies with the terminal. It
  is not yet a declared service, so it does not survive a reboot. That lands
  with nix-darwin, crew#126 step 3, rather than as another plist.
- `facts`, the dbt model, reads the same 28 files but is not declared as
  depending on them, so the two halves are separate graphs. Joining them means
  emitting a dbt `sources.yml` from `science/sources.json` next to the generated
  `facts.sql`.
- Nothing routes a FAIL anywhere yet. A stale asset is visible in the UI and
  over GraphQL and alerts nobody, which is an instrument nobody reads (LAW 28).
- The 25 other scheduled jobs are still launchd's.
