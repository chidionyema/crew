#!/usr/bin/env python3
"""Collect every estate data store into one queryable table.

The estate has 18 append-only stores. Each is written by one script and read by
that same script. Nothing reads across them, so every cross-store question costs
a throwaway script -- measured 2026-08-23, twice in one session.

This is not a second ledger (LAW 30). It holds no original data. Every row is a
copy of a row that still lives in its source file, and the whole database can be
deleted and rebuilt from those files by running this command again. If a source
and the warehouse disagree, the source is right.

    python3 science/collect.py            # rebuild, print what landed
    python3 science/collect.py --reconcile  # what the crawl found that this does not collect
    python3 science/collect.py --check    # exit 1 if a source is stale, broken or undeclared

Readers, named before it was built (LAW 28):
  - science/law_enforcement.py, which today opens four stores by hand
  - scripts/estate-snapshot, which writes the row the founder reads in STATE.md

WHY THE SOURCE LIST IS NO LONGER TRUSTED ON ITS OWN
---------------------------------------------------
Founder, 2026-08-24: "we need unification of dta pipeline ... one nodel".

The warehouse was already one model. `facts(source, at, ingested_at, payload)` is the
right shape and it stays. The defect was upstream: this list was typed by hand, 19
entries, while ~/.estate/scripts/inventory.py CRAWLS the machine and finds 88 data and
ledger stores. The two instruments never met. So a store nobody remembered to add looked
exactly like a store somebody deliberately left out, and 72 of them accumulated in that
gap without a single thing going red.

The practice this now follows, read rather than assumed:

  dbt makes you declare every source, and makes exclusion explicit rather than silent:
  a table you deliberately do not check carries `freshness: null` in the same file. There
  is no way to leave a source unmentioned and have the project still look complete.

  DataHub does not trust a typed list at all. Its connectors "crawl your data systems on
  a schedule" and the catalogue is the crawl's output, not a document somebody maintains.

  Fowler, on the data monolith: "the whole pipeline i.e. the monolithic platform, is the
  smallest unit that must change to cater for a new functionality". So the writers stay
  where they are. One model and one registry, not one program that owns every store.

Applied here: the inventory's crawl is the oracle. Every store it finds must appear in
SOURCES or in DECLINED with a stated reason, and a store in neither fails --check. The
registry can now only be wrong in a way that is visible.

Sharded stores are one source, not many. The crawl already groups 46 shard files under
two logical parents via its `member_of` field, and this collects a directory as a single
source for the same reason dbt names a table rather than a file.
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
import time
from datetime import UTC, datetime
from pathlib import Path


#: Every path this program uses is overridable from the environment, and none of the
#: three defaults is baked into the registry file. code-84, on the estate's kubernetes
#: work, 2026-08-24: read config from a file and the rest from the environment, never a
#: path under $HOME, so porting this is a manifest and not a rewrite. The immediate
#: payoff is smaller and arrives today: the paired controls below can point all three at
#: a scratch directory and exercise the real gate without touching the real warehouse.
def _env_path(var: str, default: Path) -> Path:
    raw = os.environ.get(var)
    return Path(os.path.expanduser(raw)) if raw else default


HOME = _env_path("ESTATE_HOME", Path.home())
WAREHOUSE = _env_path("SCIENCE_WAREHOUSE", Path(__file__).parent / "warehouse.db")

# THE REGISTRY IS A FILE, NOT A PYTHON DICT
# ------------------------------------------
# It used to be three dicts in this module. code-84, on the estate's kubernetes work,
# 2026-08-24: "make the registry a plain declarative file that `kubectl apply -k` could
# carry unchanged. Not a Python dict. Then when a cluster does exist, adopting it is an
# overlay entry." That is the same reason dbt keeps sources in yml rather than in the
# code that reads them: whoever owns a store has to be able to declare it without
# editing the collector, or they will not declare it at all, and 72 undeclared stores is
# what that looks like after a few months.
#
# Paths are declared under a NAMED ROOT rather than absolutely, so nothing in the file
# hardcodes /Users/chidionyema. Moving this to a container is then a roots mapping and
# not a rewrite.
REGISTRY = _env_path("SCIENCE_REGISTRY", Path(__file__).parent / "sources.json")


def _default_collector_config() -> Path:
    """idp's collector config, found beside this repo's main checkout, never under a
    typed home path (LAW 46). A worktree resolves through its git common dir."""
    import subprocess
    try:
        common = subprocess.run(["git", "rev-parse", "--git-common-dir"], cwd=Path(__file__).parent,
                                capture_output=True, text=True, check=True).stdout.strip()
        main_checkout = Path(common).resolve().parent
    except (subprocess.CalledProcessError, OSError):
        main_checkout = Path(__file__).resolve().parents[1]
    return main_checkout.parent / "idp" / "observability" / "otel-collector.yaml"


#: The one pipeline every source lands in (crew#258, idp#128). Each source names the
#: receiver key it arrives through; a name the collector does not declare is refused.
COLLECTOR_CONFIG = _env_path("OTEL_COLLECTOR_CONFIG", _default_collector_config())


def collector_receivers(path: Path = COLLECTOR_CONFIG) -> set[str] | None:
    """Receiver keys the collector declares, or None when the file cannot be read."""
    try:
        import yaml
        doc = yaml.safe_load(path.read_text()) or {}
    except (OSError, ImportError, ValueError):
        return None
    rec = doc.get("receivers") or {}
    return set(rec) if isinstance(rec, dict) else set()


def receiver_verdict() -> tuple[list[str], str]:
    """Sources naming a receiver the collector lacks, and a one-line note.

    BLIND when the collector config is unreadable: no verdict, never a pass."""
    keys = collector_receivers()
    if keys is None:
        return [], f"receivers: BLIND (no collector config at {COLLECTOR_CONFIG})"
    bad = sorted(f"{n} -> {r}" for n, r in RECEIVERS.items() if r not in keys)
    if bad:
        return bad, (f"receivers: {len(bad)} source(s) name a receiver the collector does not "
                     f"declare ({', '.join(sorted(keys))}): {', '.join(bad)}")
    return [], f"receivers: every source lands in a declared receiver ({', '.join(sorted(keys))})"


def load_registry(path: Path = REGISTRY) -> dict:
    """Read the registry, or fail loudly. There is no built-in default on purpose.

    A collector that silently falls back to an empty or hardcoded source list when its
    registry is missing reports a healthy run over nothing, which is the exact failure
    this whole change exists to remove.
    """
    try:
        reg = json.loads(path.read_text())
    except FileNotFoundError:
        sys.exit(f"registry missing: {path}. This collects nothing without it.")
    except json.JSONDecodeError as exc:
        sys.exit(f"registry will not parse: {path}: {exc}")

    roots = {"home": HOME, "science": Path(__file__).parent}
    for name, raw in (reg.get("roots") or {}).items():
        if name not in roots:
            roots[name] = Path(os.path.expanduser(raw))

    sources: dict[str, tuple[Path, str, str | None]] = {}
    stale: dict[str, int] = {}
    receivers: dict[str, str] = {}
    for s in reg.get("sources", []):
        root = roots.get(s.get("root", "home"))
        if root is None:
            sys.exit(f"registry names an unknown root {s.get('root')!r} for {s.get('name')!r}")
        #: A source with no receiver has no way into the one pipeline (R37 req 8).
        if not (s.get("receiver") or "").strip():
            sys.exit(f"registry source {s.get('name')!r} names no receiver. Every source "
                     f"says which collector receiver it arrives through.")
        receivers[s["name"]] = s["receiver"]
        sources[s["name"]] = (root / s["path"], s.get("kind", "jsonl"), s.get("time_field"))
        if s.get("stale_after_hours"):
            stale[s["name"]] = int(s["stale_after_hours"])

    declined: dict[str, str] = {}
    declined_dirs: dict[str, Path] = {}
    for d in reg.get("declined", []):
        #: A reason is not decoration. An exclusion with no stated reason is
        #: indistinguishable from a store somebody forgot, which is the thing being
        #: fixed, so it is refused here rather than accepted quietly.
        if not (d.get("reason") or "").strip():
            sys.exit(f"registry declines {d.get('id')!r} with no reason. "
                     f"Every exclusion states why, or it is not an exclusion.")
        declined[d["id"]] = d["reason"]
        #: An exclusion may name a directory instead of matching one crawl id, using the
        #: same root/path pair a source uses. Without this, a tool that writes one file
        #: per run -- Dagster's run store writes `<uuid>.db` -- has to be re-declined by
        #: hand every time it runs, and the reconcile goes red on the next run whatever
        #: anyone typed today. An exclusion that must be restated per run is not an
        #: exclusion, it is a chore, and a chore in front of a gate is how the gate gets
        #: switched off.
        if d.get("path"):
            root = roots.get(d.get("root", "home"))
            if root is None:
                sys.exit(f"registry declines {d.get('id')!r} against an unknown root "
                         f"{d.get('root')!r}")
            declined_dirs[d["id"]] = root / d["path"]

    return {"sources": sources, "declined": declined, "declined_dirs": declined_dirs,
            "stale": stale, "receivers": receivers,
            "default_stale": int(reg.get("default_stale_after_hours", 48))}


_REG = load_registry()
SOURCES: dict[str, tuple[Path, str, str | None]] = _REG["sources"]
DECLINED: dict[str, str] = _REG["declined"]
RECEIVERS: dict[str, str] = _REG["receivers"]
#: The subset of DECLINED that excludes a whole directory rather than one crawl id.
DECLINED_DIRS: dict[str, Path] = _REG["declined_dirs"]

# A source that has not been written inside this many hours is reported STALE. The
# number is the source's own cadence times three, not a guess, and it lives beside the
# source in the registry now rather than in a second table here.
STALE_HOURS: dict[str, int] = _REG["stale"]
DEFAULT_STALE_HOURS: int = _REG["default_stale"]

#: The crawl this reconciles against. Written hourly by com.estate.inventory.
INVENTORY = _env_path("ESTATE_INVENTORY", HOME / ".estate/state/inventory.json")

SCHEMA = """
CREATE TABLE IF NOT EXISTS facts (
    source     TEXT NOT NULL,
    at         TEXT,           -- the row's own timestamp, ISO, NULL if it carries none
    ingested_at TEXT NOT NULL,
    payload    TEXT NOT NULL   -- the source row, verbatim JSON
);
CREATE INDEX IF NOT EXISTS idx_facts_source ON facts(source);
CREATE INDEX IF NOT EXISTS idx_facts_at     ON facts(at);

CREATE TABLE IF NOT EXISTS ingest_log (
    source      TEXT NOT NULL,
    ingested_at TEXT NOT NULL,
    rows        INTEGER NOT NULL,
    bad_rows    INTEGER NOT NULL,
    source_mtime TEXT,
    status      TEXT NOT NULL   -- OK | ABSENT | UNREADABLE
);
"""

# Spend is the estate's only money series, so it gets a typed view rather than
# living as opaque JSON. Every other source stays generic until something asks.
SPEND_VIEW = """
DROP VIEW IF EXISTS spend_daily;
CREATE VIEW spend_daily AS
SELECT
    json_extract(payload, '$.day')      AS day,
    MAX(json_extract(payload, '$.total'))    AS usd,
    MAX(json_extract(payload, '$.requests')) AS requests
FROM facts
WHERE source = 'spend'
  AND json_extract(payload, '$.day') >= '2020-01-01'   -- drops the epoch-zero rows
GROUP BY day
ORDER BY day;

-- What the money bought. Crude on purpose: a commit is not value, and this view
-- says nothing about whether any of it was worth doing. It is the estate's first
-- denominator of any kind, and the point of it is that dividing by SOMETHING makes
-- the question askable. Read usd_per_commit as an upper bound on cost, never as a
-- measure of merit -- the cheapest way to move it is to commit more often.
DROP VIEW IF EXISTS value_daily;
CREATE VIEW value_daily AS
SELECT
    s.day,
    s.usd,
    COALESCE(c.commits, 0) AS commits,
    COALESCE(p.prs, 0)     AS prs_merged,
    ROUND(s.usd / NULLIF(c.commits, 0), 2) AS usd_per_commit
FROM spend_daily s
LEFT JOIN (
    SELECT json_extract(payload, '$.day') AS day,
           SUM(json_extract(payload, '$.commits')) AS commits
    FROM facts WHERE source = 'ships'
      AND json_extract(payload, '$.commits') IS NOT NULL
    GROUP BY day
) c ON c.day = s.day
LEFT JOIN (
    SELECT json_extract(payload, '$.day') AS day, COUNT(*) AS prs
    FROM facts WHERE source = 'ships'
      AND json_extract(payload, '$.pr') IS NOT NULL
    GROUP BY day
) p ON p.day = s.day
ORDER BY s.day;

-- What it cost HIM. The estate measured its own money and its own output and never
-- once measured the founder, who is one of the platform's two customers (LAW 36).
-- His messages are the effort the estate asked of him; his complaints are the
-- platform telling on itself. Joined to spend and commits so the three move together
-- on one row: a day that shipped more, cost less and needed fewer of his words is the
-- only shape of "better" that means anything here.
DROP VIEW IF EXISTS attention_daily;
CREATE VIEW attention_daily AS
SELECT
    a.day,
    a.messages,
    a.complaints,
    a.complaint_rate,
    v.usd,
    v.commits,
    ROUND(v.commits * 1.0 / NULLIF(a.messages, 0), 2) AS commits_per_message
FROM (
    SELECT json_extract(payload, '$.day')            AS day,
           MAX(json_extract(payload, '$.messages'))  AS messages,
           MAX(json_extract(payload, '$.complaints')) AS complaints,
           MAX(json_extract(payload, '$.complaint_rate')) AS complaint_rate
    FROM facts WHERE source = 'attention'
    GROUP BY day
) a
LEFT JOIN value_daily v ON v.day = a.day
ORDER BY a.day;
"""


def iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=UTC).isoformat(timespec="seconds")


def shard_files(path: Path) -> list[Path]:
    """Every .jsonl under a sharded store, in a stable order.

    Sorted so two runs over an unchanged directory produce the same row order and a
    diff of the warehouse means something. rglob, because ~/.claude/jobs holds its
    timelines one directory deeper than the others.
    """
    return sorted(p for p in path.rglob("*.jsonl") if p.is_file())


def read_rows(path: Path, kind: str) -> tuple[list[dict], int]:
    """Return (rows, bad_row_count). A row that will not parse is counted, never guessed at."""
    rows: list[dict] = []
    bad = 0
    if kind == "jsonl-dir":
        #: Every shard keeps its own name on the row. Without it the shards melt into
        #: one undifferentiated source and "which project was he talking about" stops
        #: being answerable, which is most of what the directives store is for.
        for shard in shard_files(path):
            shard_rows, shard_bad = read_rows(shard, "jsonl")
            bad += shard_bad
            name = shard.stem
            for r in shard_rows:
                r.setdefault("_shard", name)
                rows.append(r)
    elif kind == "jsonl":
        with open(path, errors="ignore") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    bad += 1
                    continue
                rows.append(obj if isinstance(obj, dict) else {"value": obj})
    else:
        try:
            obj = json.loads(path.read_text(errors="ignore"))
        except json.JSONDecodeError:
            return [], 1
        rows.append(obj if isinstance(obj, dict) else {"value": obj})
    return rows, bad


#: Producers on this estate name the row's own timestamp three different ways and
#: encode it two different ways. Measured 2026-08-24: 4,261 of 5,548 rows landed with
#: at=NULL because this function looked only for a field literally called "at" and
#: only accepted strings. Eight of nineteen sources had every row untimestamped,
#: including the two largest, which makes any time series over them impossible.
TIME_KEYS = ("at", "ts", "t", "timestamp", "generated_at")

#: 2001-09-09 to 2033-05-18. A number outside this range is not a unix timestamp, so a
#: field that happens to be called "t" and holds something else is dropped rather than
#: silently recorded as a date in 1970.
EPOCH_LO, EPOCH_HI = 1_000_000_000, 2_000_000_000

#: The same window three orders of magnitude up. Producers on this estate disagree about
#: the unit as well as the key name: `history` writes milliseconds, and its 13,142 rows --
#: the largest store here -- landed with at=NULL for as long as this file has existed,
#: because a millisecond epoch is a thousand times too big to be a second one and was
#: therefore dropped as "not a timestamp". Found 2026-08-24 by the DuckDB differential,
#: which reported the store as untimed on both sides and made it obvious that both sides
#: were wrong in the same way. The two windows do not overlap, so nothing is ambiguous.
EPOCH_MS_LO, EPOCH_MS_HI = EPOCH_LO * 1000, EPOCH_HI * 1000


def row_time(obj: dict, field: str | None) -> str | None:
    """The row's own timestamp as ISO-8601, or None when it genuinely carries none.

    The configured field wins; the rest of TIME_KEYS are tried after it so a new source
    is timestamped without anyone remembering to declare which key it uses. Anything
    that will not validate as a time returns None, because a wrong date is worse than a
    missing one: a missing one shows up as a gap and a wrong one shows up as a trend.
    """
    for key in ((field,) if field else ()) + TIME_KEYS:
        v = obj.get(key)
        if isinstance(v, str) and v.strip():
            try:
                datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError:
                continue
            return v
        if isinstance(v, (int, float)) and EPOCH_LO <= v <= EPOCH_HI:
            return iso(float(v))
        if isinstance(v, (int, float)) and EPOCH_MS_LO <= v <= EPOCH_MS_HI:
            return iso(float(v) / 1000)
    return None


def collect(conn: sqlite3.Connection) -> list[dict]:
    now = iso(time.time())
    report = []
    for name, (path, kind, tfield) in SOURCES.items():
        if not path.exists():
            report.append({"source": name, "status": "ABSENT", "rows": 0, "bad": 0, "mtime": None})
            conn.execute(
                "INSERT INTO ingest_log VALUES (?,?,?,?,?,?)",
                (name, now, 0, 0, None, "ABSENT"),
            )
            continue

        #: A directory's own mtime moves when a shard is ADDED and not when one is
        #: appended to, so it would report a store fresh that has been silent for a
        #: week. The freshest shard is the store's real age.
        if kind == "jsonl-dir":
            shards = shard_files(path)
            mtime = iso(max((s.stat().st_mtime for s in shards), default=path.stat().st_mtime))
        else:
            mtime = iso(path.stat().st_mtime)
        try:
            rows, bad = read_rows(path, kind)
        except OSError as exc:
            report.append({"source": name, "status": f"UNREADABLE: {exc}",
                           "rows": 0, "bad": 0, "mtime": mtime})
            conn.execute("INSERT INTO ingest_log VALUES (?,?,?,?,?,?)",
                         (name, now, 0, 0, mtime, "UNREADABLE"))
            continue

        conn.execute("DELETE FROM facts WHERE source = ?", (name,))
        conn.executemany(
            "INSERT INTO facts (source, at, ingested_at, payload) VALUES (?,?,?,?)",
            [(name, row_time(r, tfield), now, json.dumps(r, separators=(",", ":")))
             for r in rows],
        )
        conn.execute("INSERT INTO ingest_log VALUES (?,?,?,?,?,?)",
                     (name, now, len(rows), bad, mtime, "OK"))
        report.append({"source": name, "status": "OK", "rows": len(rows),
                       "bad": bad, "mtime": mtime})

    #: A source that moves from collected to declined leaves its old rows behind, because
    #: nothing in this loop visits a name the registry no longer mentions. Found 2026-08-24
    #: by the DuckDB differential: `would_have_fired` was declined with a reason and still
    #: had 162 rows in `facts`, which the freshness check then reported STALE. An alarm
    #: about a store the estate deliberately stopped collecting is an alarm that trains
    #: people to ignore alarms (LAW 28).
    #:
    #: Dropping them is safe in the way rebuilding a derived table is safe: `facts` is
    #: built entirely from the JSONL on disk, this loop already DELETEs and rewrites every
    #: declared source on every run, and a registry that will not parse exits before
    #: reaching here. The registry is the truth about what is collected; the warehouse is
    #: made to match it rather than accumulating whatever it was told years ago.
    orphans = [r[0] for r in conn.execute(
        "SELECT DISTINCT source FROM facts").fetchall() if r[0] not in SOURCES]
    for name in sorted(orphans):
        n = conn.execute("SELECT count(*) FROM facts WHERE source = ?", (name,)).fetchone()[0]
        conn.execute("DELETE FROM facts WHERE source = ?", (name,))
        report.append({"source": name, "status": "DROPPED", "rows": n, "bad": 0,
                       "mtime": None})
    return report


def staleness(entry: dict) -> str:
    """How old the SOURCE file is, against its own declared cadence."""
    if entry["status"] != "OK" or not entry["mtime"]:
        return entry["status"]
    age_h = (time.time() - datetime.fromisoformat(entry["mtime"]).timestamp()) / 3600
    limit = STALE_HOURS.get(entry["source"], DEFAULT_STALE_HOURS)
    return f"STALE {age_h:.0f}h" if age_h > limit else f"fresh {age_h:.0f}h"


def reconcile() -> tuple[list[dict], list[str], list[str], str]:
    """Compare the machine's crawl against this registry.

    Returns (undeclared, stale_declines, blind_declines, note). `undeclared` is the
    finding that matters: a store that exists, that the crawler found, and that this file
    has never heard of. `stale_declines` is the other direction, an exclusion for
    something that is no longer there, which is how a DECLINED map rots into a list of
    ghosts. `blind_declines` is neither: an exclusion whose directory could not be read,
    so this run has no opinion about it and says so instead of guessing.

    A shard is covered by its parent. The crawl already groups shard files under a
    logical store in its `member_of` field, so `directives/-Users-...jsonl` is answered
    by the `directives` declaration and is not 40 separate omissions.

    No inventory means no verdict, and that is said out loud rather than passing. A
    reconciliation that silently succeeds when its oracle is missing is worse than none,
    because it reads as proof of coverage.
    """
    if not INVENTORY.exists():
        return [], [], [], (f"NO CRAWL TO RECONCILE AGAINST: {INVENTORY} is missing, so this "
                        f"cannot tell a complete registry from an empty one. Run "
                        f"com.estate.inventory, or ~/.estate/scripts/inventory.py.")
    try:
        crawl = json.loads(INVENTORY.read_text())
    except (json.JSONDecodeError, OSError) as exc:
        return [], [], [], f"CRAWL UNREADABLE: {INVENTORY}: {exc}"

    declared_paths = {str(p.resolve()) if p.exists() else str(p)
                      for p, _k, _t in SOURCES.values()}
    #: A file inside a declared directory source is already collected by it. The crawl
    #: lists ~/.claude/jobs/<id>/timeline.jsonl as six separate stores and sets no
    #: member_of on them, so without containment the registry is told to declare six
    #: things it is already reading. Containment is by resolved path, not by string
    #: prefix, so a sibling directory whose name merely starts the same is not swallowed.
    declared_dirs = [p.resolve() for p, k, _t in SOURCES.values()
                     if k == "jsonl-dir" and p.exists()]
    known_ids = set(DECLINED) | set(SOURCES)

    def inside_declared_dir(p: Path) -> bool:
        try:
            rp = p.resolve()
        except OSError:
            return False
        return any(d == rp or d in rp.parents for d in declared_dirs)

    def presence_of(d: Path) -> str:
        """"there", "gone" or "blind" -- and never "gone" because we could not look.

        `Path.exists()` answers False for two different facts: the directory is not
        there, and the directory could not be read. A permission error, a dead mount, a
        network filesystem that timed out all come back as False, so an exclusion whose
        directory is merely unreachable reports as a ghost, gets deleted as dead wood,
        and the registry then goes red on a morning nobody typed anything wrong -- which
        is the exact failure this directory exclusion exists to stop.

        Three checks on this estate collapsed the same two facts on 2026-08-24: an escrow
        check printed NOT PRESENT for a permission error, a database drill printed
        corruption for SQLITE_CANTOPEN on a locked file, and a research pass reported a
        file unmerged after looking at one branch. Attributed by session chidionyema-7e
        reviewing this change, before it merged.

        FileNotFoundError is on both sides, which is why the parent is asked. An
        unmounted volume raises FileNotFoundError for everything beneath its mountpoint,
        so a decline on an external disk or a dead network mount arrives looking exactly
        like a deleted directory -- and the data is provably still there when it comes
        back. Demonstrated by session chidionyema-73 on a real disk image: detach the
        volume and this said "gone"; reattach it and the file was untouched. So an
        absence only counts when it is an absence inside a filesystem we can still see:
        if the parent is reachable the directory really is missing, and if the parent is
        unreachable too we are looking at a hole rather than an absence.

        RESIDUAL, stated rather than hidden: deleting a whole tree removes the parent as
        well, so that reads "blind" from then on and the exclusion is never called stale.
        That is the safe direction -- an exclusion nobody deletes costs a printed line,
        where an exclusion wrongly deleted turns the registry red on the next run -- but
        it is a real limit and the "COULD NOT LOOK" line is the only thing that surfaces
        it.
        """
        try:
            d.stat()
        except NotADirectoryError:
            return "gone"
        except FileNotFoundError:
            try:
                d.parent.stat()
            except OSError:
                return "blind"
            return "gone"
        except OSError:
            return "blind"
        return "there"

    #: Resolved once, outside the row loop, because resolve() hits the filesystem and the
    #: crawl has thousands of rows.
    presence = {i: presence_of(d) for i, d in DECLINED_DIRS.items()}
    declined_dirs = {i: (d.resolve() if presence[i] == "there" else d)
                     for i, d in DECLINED_DIRS.items()}

    def covering_decline(p: Path) -> str:
        """The id of the directory exclusion that covers this path, or ""."""
        try:
            rp = p.resolve()
        except OSError:
            rp = p
        for i, d in declined_dirs.items():
            if d == rp or d in rp.parents:
                return i
        return ""

    undeclared, seen_ids = [], set()
    for row in crawl.get("rows", []):
        if row.get("kind") not in ("data", "ledger"):
            continue
        ident = row.get("member_of") or row.get("id") or ""
        seen_ids.add(ident)
        seen_ids.add(row.get("id") or "")
        if ident in known_ids or (row.get("id") or "") in known_ids:
            continue
        p = Path(row.get("path") or "")
        covered = covering_decline(p)
        if covered:
            seen_ids.add(covered)
            continue
        if (str(p.resolve()) if p.exists() else str(p)) in declared_paths:
            continue
        if p.exists() and inside_declared_dir(p):
            continue
        #: A shard is only covered when its parent is. member_of is the crawl's own
        #: grouping, so this trusts it rather than re-deriving the grouping from paths.
        if row.get("member_of"):
            continue
        undeclared.append({"id": row.get("id"), "path": row.get("path"),
                           "rows": row.get("rows"), "mb": row.get("mb")})

    #: A directory exclusion is stale when the directory is gone, not when this hour's
    #: crawl happened to find nothing inside it. Judging it by crawl rows would report
    #: `dagster-run-store` as a ghost on any morning Dagster had not run overnight, and an
    #: instrument that cries ghost on a quiet night gets ignored on the night it means it.
    #: An exclusion with no directory is not in `presence` at all, and defaults to "gone"
    #: so that an id-only decline is judged exactly as it was before directories existed.
    stale = sorted(i for i in DECLINED
                   if i not in seen_ids and presence.get(i, "gone") == "gone")
    #: Reported separately rather than folded into either answer. A directory that could
    #: not be read is not evidence of anything, and a checker that quietly picks one of
    #: the two verdicts it cannot distinguish is the defect, whichever one it picks.
    blind = sorted(i for i, v in presence.items() if v == "blind")
    return undeclared, stale, blind, ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if any source is absent, unreadable, stale or undeclared")
    ap.add_argument("--reconcile", action="store_true",
                    help="print what the machine's crawl found that this registry does "
                         "not mention, and exit without rebuilding")
    args = ap.parse_args()

    if args.reconcile:
        undeclared, stale, blind, note = reconcile()
        print(f"registry : {len(SOURCES)} collected, {len(DECLINED)} declined with a reason")
        print(f"crawl    : {INVENTORY}")
        bad_receivers, rnote = receiver_verdict()
        print(rnote)
        if bad_receivers:
            return 1
        if note:
            print(note)
            return 1
        if undeclared:
            print(f"\nUNDECLARED, {len(undeclared)} store(s) the crawl found and this "
                  f"registry has never heard of:")
            for u in sorted(undeclared, key=lambda r: -((r["rows"] or 0) + (r["mb"] or 0))):
                size = f"{u['rows']} rows" if u["rows"] else f"{u['mb']} MB"
                print(f"  {str(u['id'])[:58]:58} {size}")
            print("\nAdd each to SOURCES to collect it, or to DECLINED with the reason it "
                  "is left out. Silence is not one of the options.")
        else:
            print("\nUNDECLARED: none. Every store the crawl found is either collected or "
                  "declined with a stated reason.")
        if stale:
            print(f"\nDECLINED FOR SOMETHING THAT IS GONE, {len(stale)}: {', '.join(stale)}")
        if blind:
            print(f"\nCOULD NOT LOOK, {len(blind)}: {', '.join(blind)}. These exclusions "
                  f"name a directory this run could not read -- a permission error, an "
                  f"unmounted volume, a filesystem that timed out. They are not stale and "
                  f"they are not confirmed; nobody should delete them on this evidence.")
        return 1 if undeclared else 0

    # Two writers meet here routinely: com.founder.sciencecollect runs hourly and an
    # agent runs the same script by hand. Without a busy timeout the second one dies on
    # "database is locked" mid-DELETE, which reads as a broken collector rather than as
    # two collectors queueing. Measured 2026-08-24: exactly that, on collect.py:221.
    # WAL additionally lets estate-snapshot read the views while a collection is writing.
    conn = sqlite3.connect(WAREHOUSE, timeout=60)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=60000")
    conn.executescript(SCHEMA)
    report = collect(conn)
    conn.executescript(SPEND_VIEW)
    conn.commit()

    print(f"warehouse: {WAREHOUSE}")
    print(f"{'source':18} {'rows':>7} {'bad':>4}  age")
    print("-" * 56)
    failures = []
    for e in sorted(report, key=lambda r: -r["rows"]):
        age = staleness(e)
        if e["status"] != "OK" or age.startswith("STALE") or e["bad"]:
            failures.append(f"{e['source']}: {age}" + (f", {e['bad']} unparseable rows" if e["bad"] else ""))
        print(f"{e['source']:18} {e['rows']:>7} {e['bad']:>4}  {age}")

    total = conn.execute("SELECT count(*) FROM facts").fetchone()[0]
    sources = conn.execute("SELECT count(DISTINCT source) FROM facts").fetchone()[0]
    print("-" * 56)
    print(f"{'TOTAL':18} {total:>7}       across {sources} sources")

    days = conn.execute("SELECT count(*) FROM spend_daily").fetchone()[0]
    spend = conn.execute("SELECT round(sum(usd),2) FROM spend_daily").fetchone()[0]
    #: `$None` is what SUM over an empty view prints, and a money line reading `$None`
    #: is a money line nobody trusts. Say there is nothing there instead.
    print(f"spend_daily view:  {days} days, "
          + (f"${spend} total" if spend is not None else "no spend rows"))

    #: The registry checks itself against the machine on every run, not only when asked.
    #: A gap that is only visible behind a flag nobody types is the same shape as the
    #: defect this closes (LAW 28).
    undeclared, stale_declines, blind_declines, note = reconcile()
    if note:
        print(f"\n{note}")
        failures.append("no crawl to reconcile against")
    elif undeclared:
        print(f"\nundeclared stores, {len(undeclared)} the crawl found and this does not "
              f"mention: {', '.join(str(u['id'])[:40] for u in undeclared[:6])}"
              f"{' ...' if len(undeclared) > 6 else ''}")
        failures.append(f"{len(undeclared)} store(s) in neither SOURCES nor DECLINED "
                        f"(run --reconcile)")
    if stale_declines:
        print(f"declined for something that is gone: {', '.join(stale_declines)}")
    #: Printed, never counted as a failure. A directory this run could not read is a
    #: blind spot, and failing the check on a blind spot is how a check that refuses
    #: correct work gets switched off (LAW 38).
    if blind_declines:
        print(f"declined for a directory this run could not read, so no verdict on it: "
              f"{', '.join(blind_declines)}")
    #: Every source names the collector receiver it lands in; a receiver the collector
    #: does not declare is a source with no way into the pipeline. BLIND when the
    #: collector config is not on this host: printed, never a pass, never a failure.
    bad_receivers, rnote = receiver_verdict()
    print(rnote)
    if bad_receivers:
        failures.append(f"{len(bad_receivers)} source(s) name an undeclared receiver")

    if failures:
        print("\nneeds attention:")
        for f in failures:
            print(f"  - {f}")

    conn.close()
    return 1 if (args.check and failures) else 0


if __name__ == "__main__":
    sys.exit(main())
