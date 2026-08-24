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
    python3 science/collect.py --check    # exit 1 if a source is stale or broken

Readers, named before it was built (LAW 28):
  - science/law_enforcement.py, which today opens four stores by hand
  - scripts/estate-snapshot, which writes the row the founder reads in STATE.md
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
WAREHOUSE = Path(__file__).parent / "warehouse.db"

# source name -> (path, kind, the field holding the row's own timestamp)
SOURCES: dict[str, tuple[Path, str, str | None]] = {
    "spend":          (HOME / ".claude/estate-spend-history.jsonl",          "jsonl", "at"),
    "board":          (HOME / ".claude/ESTATE_BOARD.jsonl",                  "jsonl", "at"),
    "ledger":         (HOME / ".claude/state/ledger.jsonl",                  "jsonl", "at"),
    "close_guard":    (HOME / ".claude/state/close-guard-observe.jsonl",     "jsonl", "at"),
    "toolguard":      (HOME / ".claude/state/toolguard/events.jsonl",        "jsonl", "at"),
    "would_have_fired": (HOME / ".claude/state/one-branch/would-have-fired.jsonl", "jsonl", "at"),
    "drills":         (HOME / ".claude/state/drills.jsonl",                  "jsonl", "at"),
    "ci_reach":       (HOME / ".claude/state/ci-reach.jsonl",                "jsonl", "at"),
    "aiden_ticks":    (HOME / ".claude/state/aiden-ticks.jsonl",             "jsonl", "at"),
    "stuck_detector": (HOME / ".claude/state/logs/stuck-detector.jsonl",     "jsonl", "at"),
    "bundle_push":    (HOME / ".claude/state/estate-bundle-push.jsonl",      "jsonl", "at"),
    "agent_cert":     (HOME / ".claude/agent-cert/history.jsonl",            "jsonl", "at"),
    "decisions":      (HOME / ".claude/DECISIONS.jsonl",                     "jsonl", "at"),
    "consult":        (HOME / ".claude/logs/consult.jsonl",                  "jsonl", "at"),
    "method_metrics": (HOME / "Documents/code/prospector/store/ops/method_metrics.json",
                       "json", "generated_at"),
    "enforcement_map": (Path(__file__).parent / "enforcement-map.json",      "json", None),
    # Outcome collections, written by science/outcomes.py. These are the only two
    # sources on this list that record what the estate produced rather than what it
    # did to itself. Everything above is telemetry; these are the denominator.
    "ships":          (Path(__file__).parent / "ships.jsonl",                "jsonl", "at"),
    "predictions":    (Path(__file__).parent / "predictions.jsonl",          "jsonl", "at"),
    # The founder himself. His messages and complaints per day, derived from the
    # directives ledger, which had 6,917 rows and no reader (LAW 28).
    "attention":      (Path(__file__).parent / "attention.jsonl",            "jsonl", "at"),
}

# A source that has not been written inside this many hours is reported STALE.
# The number is the source's own cadence times three, not a guess: reflect runs
# every 4 hours, the spend collector every 10 minutes, the rest are event-driven
# and only report stale after a full day of silence.
STALE_HOURS = {"spend": 6, "method_metrics": 12, "ships": 26, "attention": 26}
DEFAULT_STALE_HOURS = 48

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
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat(timespec="seconds")


def read_rows(path: Path, kind: str) -> tuple[list[dict], int]:
    """Return (rows, bad_row_count). A row that will not parse is counted, never guessed at."""
    rows: list[dict] = []
    bad = 0
    if kind == "jsonl":
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


def row_time(obj: dict, field: str | None) -> str | None:
    if not field:
        return None
    v = obj.get(field)
    return v if isinstance(v, str) else None


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
    return report


def staleness(entry: dict) -> str:
    """How old the SOURCE file is, against its own declared cadence."""
    if entry["status"] != "OK" or not entry["mtime"]:
        return entry["status"]
    age_h = (time.time() - datetime.fromisoformat(entry["mtime"]).timestamp()) / 3600
    limit = STALE_HOURS.get(entry["source"], DEFAULT_STALE_HOURS)
    return f"STALE {age_h:.0f}h" if age_h > limit else f"fresh {age_h:.0f}h"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if any source is absent, unreadable or stale")
    args = ap.parse_args()

    conn = sqlite3.connect(WAREHOUSE)
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
    print(f"spend_daily view:  {days} days, ${spend} total")

    if failures:
        print("\nneeds attention:")
        for f in failures:
            print(f"  - {f}")

    conn.close()
    return 1 if (args.check and failures) else 0


if __name__ == "__main__":
    sys.exit(main())
