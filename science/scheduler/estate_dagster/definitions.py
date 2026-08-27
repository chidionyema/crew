"""The fact assets plus the dbt warehouse, for an interpreter that carries dagster-dbt.

The registered code location is facts.py (idp/scheduler/workspace.yaml, name
`estate-facts`); this module adds the dbt half on top of it and is NOT
registered anywhere yet, because the scheduler's interpreter (Python 3.14)
resolves dagster-dbt back to 0.22.6 / dagster 1.6.6 (see facts.py).

  estate/<name>   every source in sources.json, from facts.py.
  facts           the dbt model that unions them into DuckDB.

NOT YET WIRED: `facts` reads the same files but is not declared as depending
on them, so the two halves are separate graphs in the UI. Joining them means
emitting a dbt sources.yml from science/sources.json alongside the generated
facts.sql, which is a change to dbt_build.py and is not in this step.

WHAT THIS REPLACES
------------------
The prediction the founder asked for is not a model. A source going quiet is
observable hours before the report built on it is wrong, and the window that
says how long is already written down per source. Dagster turns "this file is
older than its declared window" into a failed check on a named asset with a
lineage graph attached, which is the thing three separate hand-rolled watchers
were each approximating into three separate logs.

Python 3.12 or 3.13. Not 3.14: pip resolves dagster-dbt backwards there
(measured 2026-08-27 on the idp venv: dagster-dbt 0.22.6, dagster 1.6.6), and
the install looks like it succeeded.
"""

# No `from __future__ import annotations` in this module. It turns every
# annotation into a string, and @dbt_assets inspects the real type object of the
# `context` parameter, so the import makes the decorator reject a correct
# signature with "Cannot annotate context parameter with type
# AssetExecutionContext" -- naming the exact type it just refused.

import os
import shutil
import sys
from pathlib import Path

import dagster as dg
from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets

from estate_dagster.facts import observe_job, observe_schedule
from estate_dagster.sources import SCIENCE, observe

DBT_DIR = SCIENCE / "dbt"

# profiles.yml resolves the warehouse through SCIENCE_DUCKDB, so the code
# location does not decide where the database lives; the environment does.
os.environ.setdefault("DBT_PROJECT_DIR", str(DBT_DIR))

# dbt is installed beside the interpreter running this module, not on PATH. The
# webserver, the daemon and every run worker are separate processes, and under
# launchd none of them inherit a PATH containing the venv, so a bare "dbt" fails
# at definition load with an error about the executable rather than about the
# environment.
#
# Setting DbtCliResource(dbt_executable=...) is not enough on its own:
# DbtProject.prepare_if_dev() builds its own resource internally and cannot be
# told where dbt is, so it fails first. Putting the venv's bin directory on PATH
# for this process fixes every caller at once, including that one.
BIN = Path(sys.executable).parent
os.environ["PATH"] = f"{BIN}{os.pathsep}{os.environ.get('PATH', '')}"
DBT_EXE = str(BIN / "dbt") if (BIN / "dbt").exists() else (shutil.which("dbt") or "dbt")

dbt_project = DbtProject(project_dir=DBT_DIR, profiles_dir=DBT_DIR)
dbt_project.prepare_if_dev()


@dbt_assets(manifest=dbt_project.manifest_path)
def dbt_estate_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


build_job = dg.define_asset_job("build_warehouse", selection=dg.AssetSelection.all())
build_schedule = dg.ScheduleDefinition(
    job=build_job, cron_schedule="17 * * * *", name="build_warehouse_hourly"
)

# No sensor. Freshness policies attached to the specs are evaluated by the
# daemon itself; build_sensor_for_freshness_checks is superseded in 1.13.
defs = dg.Definitions(
    assets=[observe, dbt_estate_assets],
    jobs=[observe_job, build_job],
    schedules=[observe_schedule, build_schedule],
    resources={"dbt": DbtCliResource(project_dir=dbt_project, dbt_executable=DBT_EXE)},
)
