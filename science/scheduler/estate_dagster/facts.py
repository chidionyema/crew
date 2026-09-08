# Standard: scheduling row, docs/STANDARDS.md -- one scheduler, idp/scheduler; this is a code location it loads
# Rejected: a cron or a standalone `dagster dev` -- a second scheduler; the freshness policies must live where the one daemon evaluates them
"""The estate's fact files as one Dagster code location, registered in the one
scheduler: ``idp/scheduler/workspace.yaml`` names this file as location
``estate-facts`` and ``idp/bin/scheduler-up`` loads it beside the schedule.yml
jobs. Nothing here is started by hand and there is no second daemon (crew#140,
headline: one platform).

What is declared:

  estate/<name>   every source in science/sources.json, polled every 15
                  minutes, each carrying the freshness window sources.json
                  already declares for it (sources.py has the two traps).

What is NOT here: the dbt model that unions the files into DuckDB. It needs
dagster-dbt, and on the scheduler's interpreter (Python 3.14) pip resolves
dagster-dbt back to 0.22.6 / dagster 1.6.6, a downgrade of the running
scheduler. definitions.py keeps that half for an interpreter that can carry it;
it is not registered anywhere until one exists.
"""

# No `from __future__ import annotations` (see sources.py).

import dagster as dg

from estate_dagster.sources import GROUP, SPECS, observe

# Observation is cheap -- one stat() per source -- so it runs far more often
# than the shortest declared window (6h). The check is only ever as current as
# the last observation, so the observation cadence is the resolution of every
# prediction this code location makes.
observe_job = dg.define_asset_job(
    "observe_estate_facts",
    selection=dg.AssetSelection.groups(GROUP),
)
observe_schedule = dg.ScheduleDefinition(
    job=observe_job,
    cron_schedule="*/15 * * * *",
    name="observe_estate_facts_every_15m",
    default_status=dg.DefaultScheduleStatus.RUNNING,
)

# No sensor. Freshness policies attached to the specs are evaluated by the
# daemon itself; build_sensor_for_freshness_checks is superseded in 1.13.
defs = dg.Definitions(
    assets=[observe],
    jobs=[observe_job],
    schedules=[observe_schedule],
)

__all__ = ["SPECS", "defs", "observe_job", "observe_schedule"]
