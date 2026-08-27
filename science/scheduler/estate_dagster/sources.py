"""The estate's fact files (every source in sources.json), as Dagster assets that go stale when their
producer dies.

WHY THIS IS NOT A SCRIPT
------------------------
science/sources.json has carried `stale_after_hours` per source since it was
written. Nothing read it, and two other files answered "has this producer died?"
with their own numbers instead:

  ~/.claude/scripts/estate/estate_watch.py:46   STALE_H, default 3 hours, one
                                                threshold for every source
  ~/.claude/scripts/estate/estate_audit.py:1024 its own `stale` list, its own
                                                report

Neither reads sources.json, so a per-source window declared in one place was
enforced against a global constant in another, and each reported into a
different log.

Dagster already has that mechanism, so this module declares the data and stops.
`FreshnessPolicy.time_window` is Dagster's own; nothing here re-implements it.

THE PART THAT IS EASY TO GET WRONG
----------------------------------
Dagster's freshness evaluator reads `latest_materialization_event.timestamp` --
the time Dagster recorded the event, not any timestamp the event carries
(dagster/_core/definitions/freshness_evaluator.py:65). So the obvious wiring,
polling every 15 minutes and recording what it saw, marks every asset fresh
forever no matter what the file underneath is doing. It looks like monitoring
and reports nothing.

The fix is to make the event mean what the policy already assumes it means.
`observe()` below records a materialization only when the file's mtime has
actually MOVED since the last recorded one. An unchanged file produces no event,
its last event keeps ageing, and it crosses its declared window on time.

The cost of that shape is resolution: the event lands up to one poll interval
after the file changed, so every verdict here is accurate to 15 minutes. The
shortest declared window on the estate is 6 hours, so the lag does not matter.
The gain is that this runs on Dagster's supported API with no sensor.

THE SAME TRAP, AT SEEDING
-------------------------
"Record when the mtime moved" is not enough on its own. On the first run no mtime
has been recorded for any source, so every mtime counts as moved, and a producer
that died three days ago gets an event stamped NOW and reads PASS for its whole
window. That is the false-green failure again, moved to the one run where nobody
is watching for it.

So `observe()` records only when the file is BOTH changed and currently inside
its own declared window. A file older than its window produces no event, which
leaves the asset UNKNOWN rather than PASS, and UNKNOWN is the honest verdict: no
evidence of health, not evidence of health. When the producer starts writing
again the mtime moves to the present, the clause passes, and the asset becomes
PASS on the next poll.

The clause also covers a case that is not seeding: a file restored from backup
with an old mtime. It changed, but it is not evidence that anything is alive.

The rejected alternative was `build_last_update_freshness_checks`, which does
read a `dagster/last_updated_timestamp` from the event's metadata
(asset_check_factories/utils.py:164) and would need no comparison at all. It is
marked superseded in 1.13 and removed in 2.0, and it requires a sensor to
evaluate. Trading five lines of mtime comparison for an API with a stated
removal date was the wrong way round.

A file that does not exist produces no event ever, so its freshness state is
UNKNOWN rather than PASS or FAIL. That is the honest reading: a declared source
with nothing on disk is an absence of evidence, not evidence of health. Sources
the estate decided not to collect are in the `declined` list in sources.json and
never reach this module.
"""

# No `from __future__ import annotations` here, for the same reason as
# definitions.py: it stringifies annotations, and @multi_asset resolves the real
# type of the `context` parameter. Python 3.12 needs no future import for
# `list[Path]` or `float | None`.

import glob
import json
import time
from datetime import timedelta
from pathlib import Path

import dagster as dg
from dagster import AssetExecutionContext
from dagster.preview.freshness import FreshnessPolicy

#: .../science/scheduler/estate_dagster/sources.py -> .../science
SCIENCE = Path(__file__).resolve().parents[2]
SOURCES_JSON = SCIENCE / "sources.json"

GROUP = "estate_facts"

#: Where observe() stores the mtime it recorded, so the next run can tell
#: whether the file moved. Read back off the asset's own last event, which means
#: the state lives in Dagster's event log and not in a file of ours.
MTIME_KEY = "source_mtime"


def _base(root: str) -> Path:
    """sources.json names two roots. 'science' is this repo; 'home' is $HOME."""
    return SCIENCE if root == "science" else Path.home()


def _matches(spec: dict) -> list[Path]:
    """Every real file a source points at. A source may be a glob."""
    p = str(_base(spec["root"]) / spec["path"])
    if "*" in p:
        return [Path(m) for m in glob.glob(p, recursive=True)]
    f = Path(p)
    return [f] if f.exists() else []


def _mtime(spec: dict) -> tuple[float, int]:
    """(newest mtime across the source's files, how many files matched).

    Newest rather than oldest: a directory of daily shards is still being
    written to as long as any shard is, and the old ones are meant to stop.
    """
    files = _matches(spec)
    if not files:
        return 0.0, 0
    return max(f.stat().st_mtime for f in files), len(files)


def load_sources() -> tuple[list[dict], int]:
    """The declared sources and the fallback window, from sources.json."""
    doc = json.loads(SOURCES_JSON.read_text(encoding="utf-8"))
    return doc["sources"], int(doc.get("default_stale_after_hours", 48))


SOURCES, DEFAULT_HOURS = load_sources()


def window_hours(spec: dict) -> int:
    return int(spec.get("stale_after_hours", DEFAULT_HOURS))


def key_for(name: str) -> dg.AssetKey:
    return dg.AssetKey(["estate", name])


def _spec(s: dict) -> dg.AssetSpec:
    hours = window_hours(s)
    return dg.AssetSpec(
        key=key_for(s["name"]),
        group_name=GROUP,
        description=(
            f"{s['root']}/{s['path']}. Expected to be written at least every "
            f"{hours}h. {s.get('note', '')}".strip()
        ),
        # The window the estate declared for this source, enforced by Dagster.
        # warn at half of it, so a producer slowing down is visible before it is
        # a failure -- which is the whole point of predicting rather than
        # reporting.
        freshness_policy=FreshnessPolicy.time_window(
            fail_window=timedelta(hours=hours),
            warn_window=timedelta(hours=max(1, hours // 2)),
        ),
        metadata={
            "path": str(_base(s["root"]) / s["path"]),
            "kind": s["kind"],
            "stale_after_hours": hours,
            "time_field": s.get("time_field") or "none",
        },
    )


SPECS = [_spec(s) for s in SOURCES]


#: What observe() decided about one source, and why. The reason is what gets
#: logged, so a reader sees which sources were refused and on what grounds
#: rather than a count (LAW 28).
RECORD = "record"
UNCHANGED = "unchanged"
ALREADY_STALE = "already_stale"


def decide(mtime: float, recorded: float | None, hours: int, now: float) -> str:
    """Whether this source's mtime should be recorded as a materialization.

    Both refusals exist to stop the same failure, which is an event stamped NOW
    that reports a dead producer as healthy:

      UNCHANGED      the file has not moved since the last recorded event, so
                     recording again would reset its clock and it would never
                     cross its window.
      ALREADY_STALE  the file moved, but the change is older than the window it
                     is measured against, so it is not evidence anything is
                     alive. Fires on the first run for a producer that was
                     already dead, and on a file restored from backup.
    """
    if recorded is not None and recorded == mtime:
        return UNCHANGED
    if (now - mtime) / 3600 >= hours:
        return ALREADY_STALE
    return RECORD


def _recorded_mtime(context: AssetExecutionContext, key: dg.AssetKey) -> float | None:
    """The mtime the last run recorded for this asset, or None if never run."""
    event = context.instance.get_latest_materialization_event(key)
    if event is None:
        return None
    mat = event.asset_materialization
    if mat is None:
        return None
    entry = (mat.metadata or {}).get(MTIME_KEY)
    return float(entry.value) if entry is not None and entry.value is not None else None


@dg.multi_asset(specs=SPECS, name="estate_fact_files", can_subset=True)
def observe(context: AssetExecutionContext):
    """Record a materialization for every source file whose mtime moved.

    One run covers every source -- one stat() each -- rather than one run per source.
    """
    selected = set(context.selected_asset_keys)
    now = time.time()
    moved: list[str] = []
    unchanged: list[str] = []
    missing: list[str] = []
    already_stale: list[str] = []
    for s in SOURCES:
        key = key_for(s["name"])
        if key not in selected:
            continue
        mtime, n = _mtime(s)
        if n == 0:
            missing.append(s["name"])
            continue
        hours = window_hours(s)
        verdict = decide(mtime, _recorded_mtime(context, key), hours, now)
        if verdict == UNCHANGED:
            unchanged.append(s["name"])
            continue
        if verdict == ALREADY_STALE:
            age = (now - mtime) / 3600
            already_stale.append(f"{s['name']} ({age:.0f}h old, window {hours}h)")
            continue
        moved.append(s["name"])
        yield dg.MaterializeResult(
            asset_key=key,
            metadata={
                MTIME_KEY: mtime,
                "files_matched": n,
                "stale_after_hours": window_hours(s),
            },
        )
    # Named, not counted. "23 unchanged" tells a reader nothing they can act on;
    # the names are what says which producer to go and look at (LAW 28).
    context.log.info(
        f"written since last run ({len(moved)}): {', '.join(moved) or 'none'}\n"
        f"unchanged ({len(unchanged)}): {', '.join(unchanged) or 'none'}\n"
        f"already older than their own window, left UNKNOWN ({len(already_stale)}): "
        f"{', '.join(already_stale) or 'none'}\n"
        f"no file on disk ({len(missing)}): {', '.join(missing) or 'none'}"
    )
