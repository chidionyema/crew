#!/usr/bin/env python3
"""Generate the dbt project's `facts` model from the one registry.

WHY THIS IS GENERATED AND NOT WRITTEN BY HAND. `science/sources.json` is the registry, and
the reconcile gate fails a run when the machine's own crawl finds a store the registry does
not mention. A second copy of that list, in dbt's own YAML or in SQL, would drift from it
inside a week, and the gate would keep passing while the warehouse quietly stopped loading
something. So what dbt reads is a build artefact: generated here, gitignored, rebuilt before
every dbt run. There is one registry and it is the JSON.

WHAT IS DELIBERATELY NOT HERE YET. A dbt `sources:` block. The obvious shape for it,
`meta.external_location` per table, did not render on dbt-duckdb 1.11.0 and nothing in this
model needs it: `facts.sql` names each `read_json_auto` call directly. Registering the
stores as dbt sources buys `dbt docs` and per-source lineage, which are worth having and
are not worth a half-working YAML block that parses today and silently resolves to nothing.
Tracked on crew#74.

WHY THE MODEL SQL IS GENERATED TOO, WHICH IS THE LESS OBVIOUS HALF. `facts` is a union of
29 append-only JSONL stores written by a dozen producers, and they do not share a schema.
Referring to a column that a given store does not have is a SQL error, not a null, so a
hand-written union would break the moment a producer changed shape. This asks DuckDB what
columns each store actually has, then writes only the expressions that can compile.

WHAT THIS PORTS, AND THE ONE RULE IT KEEPS VERBATIM. `row_time()` in collect.py exists
because producers on this estate name a row's timestamp three ways and encode it two ways,
and because a field called `t` holding something that was not a time silently landed rows
in 1970. That epoch sanity window is reproduced here rather than reinvented: a number
outside it is not a timestamp and the row keeps a NULL, on the same reasoning the original
gives, which is that a missing date shows up as a gap and a wrong one shows up as a trend.

    python3 science/dbt_build.py            # write the artefacts
    python3 science/dbt_build.py --print     # write nothing, show what it would write

Then, from `science/dbt`:

    dbt run --profiles-dir .

This writes nothing to the SQLite warehouse and reads nothing from it. It is additive until
crew#74 decides to switch, at which point collect.py's loader and the differential both go.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from collect import (  # noqa: E402  the registry has one reader, and this is not a second
    EPOCH_HI,
    EPOCH_LO,
    EPOCH_MS_HI,
    EPOCH_MS_LO,
    SOURCES,
    TIME_KEYS,
    shard_files,
)

try:
    import duckdb
except ImportError:                                              # pragma: no cover
    sys.exit("duckdb is not installed in this interpreter.\n"
             "  /Users/chidionyema/dev/code/crew/.venv/bin/python science/dbt_build.py")

HERE = Path(__file__).parent
PROJECT = HERE / "dbt"
STAGING = PROJECT / "models" / "staging"

#: The read is identical to the one the differential proved against collect.py's reader,
#: and it stays identical on purpose. If these two ever disagree the differential's green
#: run stops meaning anything.
READ_OPTS = ("format='newline_delimited', union_by_name=true, sample_size=-1, "
             "ignore_errors=true, maximum_object_size=67108864")

#: DuckDB types that can hold a unix timestamp. A BOOLEAN or a STRUCT called `t` is not a
#: candidate and must not be coerced into one.
NUMERIC = {"BIGINT", "DOUBLE", "FLOAT", "HUGEINT", "INTEGER", "SMALLINT", "TINYINT",
           "UBIGINT", "UINTEGER", "USMALLINT", "UTINYINT", "DECIMAL"}

#: read_json_auto parses an ISO-8601 string into a TIMESTAMP by itself, so the column never
#: arrives as VARCHAR and a check that only looked for VARCHAR and numbers found nothing.
#: Measured 2026-08-24: that mistake reported 16 of 27 sources as having no time column at
#: all, including spend, ships, attention and prompt_ledger, every one of which collect.py
#: timestamps correctly. The lesson is the estate's own: ask the data what type it is.
TEMPORAL = ("TIMESTAMP", "DATE")


def scan_target(path: Path, kind: str) -> str | None:
    """The DuckDB read expression for one store, or None when there is nothing to read."""
    if kind == "jsonl-dir":
        if not shard_files(path):
            return None
        #: `**/*.jsonl` because shard_files uses rglob: ~/.claude/jobs keeps its timelines
        #: one directory deeper than every other sharded store.
        return f"read_json_auto('{path}/**/*.jsonl', {READ_OPTS})"
    if kind == "jsonl":
        return f"read_json_auto('{path}', {READ_OPTS})"
    #: A single JSON document is one row to collect.py. `records='false'` stops DuckDB
    #: reading a top-level array as N rows, which would silently change the row count that
    #: the differential just proved.
    #:
    #: unnest() because records='false' hands back ONE column called `json` holding the
    #: whole document as a STRUCT, so the document's own keys are not columns and nothing
    #: can find its timestamp. Measured 2026-08-24: method_metrics carries `generated_at`
    #: and the model gave it no time at all until this line existed, while collect.py
    #: timestamped it correctly. unnest lifts the struct's fields to columns, which is the
    #: shape the rest of this file assumes.
    return (f"(SELECT unnest(json) FROM read_json_auto('{path}', records='false', "
            f"maximum_object_size=67108864))")


def columns(con, scan: str) -> dict[str, str]:
    """What columns this store actually has, asked of the data rather than assumed."""
    try:
        return {r[0]: str(r[1]).upper() for r in
                con.execute(f"DESCRIBE SELECT * FROM {scan}").fetchall()}
    except duckdb.Error:
        return {}


def time_expr(cols: dict[str, str], field: str | None) -> str:
    """collect.py's row_time(), as SQL that only names columns this store has.

    The configured field wins and the rest of TIME_KEYS follow it, so a new source is
    timestamped without anyone remembering to declare which key it uses. That ordering is
    collect.py's and it is kept.
    """
    keys = ([field] if field else []) + [k for k in TIME_KEYS if k != field]
    parts = []
    for key in keys:
        typ = cols.get(key)
        if typ is None:
            continue
        if typ.startswith("TIMESTAMP WITH TIME ZONE"):
            parts.append(f"timezone('UTC', \"{key}\")")
        elif typ.startswith(TEMPORAL):
            #: Left exactly as DuckDB parsed it, offset and all already dropped. This is
            #: the faithful port and it is deliberately not a timezone fix: collect.py
            #: stores the producer's own string and the SQLite views read its wall clock,
            #: so shifting anything here would make the warehouse disagree with itself
            #: while the differential was still using it as the oracle.
            #:
            #: The ambiguity underneath is real and is not this file's to settle. Some
            #: producers write UTC with an offset and some write bare local time, and
            #: nothing on this estate records which. That is a producer defect; it gets a
            #: ticket, not a silent +1h here.
            parts.append(f'"{key}"')
        elif typ.startswith("VARCHAR"):
            #: try_cast, not cast: a string that is not a time yields NULL and the next
            #: candidate key gets its turn, instead of failing the whole model.
            parts.append(f'try_cast("{key}" AS TIMESTAMP)')
        elif any(typ.startswith(n) for n in NUMERIC):
            #: UTC, because that is what collect.py's iso() does with an epoch:
            #: datetime.fromtimestamp(ts, tz=timezone.utc). Then stripped back to a naive
            #: wall clock so every row in the column means the same kind of thing.
            parts.append(
                f'CASE WHEN "{key}" BETWEEN {EPOCH_LO} AND {EPOCH_HI} '
                f'THEN timezone(\'UTC\', to_timestamp(CAST("{key}" AS DOUBLE))) '
                #: Milliseconds, because `history` writes them and the two windows are a
                #: thousand apart so nothing is ambiguous. Kept in step with row_time()
                #: by importing the same constants rather than repeating the numbers.
                f'WHEN "{key}" BETWEEN {EPOCH_MS_LO} AND {EPOCH_MS_HI} '
                f'THEN timezone(\'UTC\', to_timestamp(CAST("{key}" AS DOUBLE) / 1000)) END')
    if not parts:
        #: Typed so the UNION ALL still lines up. A store with no time column is a real
        #: state, not an error: eight of nineteen sources were in it before the time keys
        #: were widened, and the fix was to widen them, not to invent a date.
        return "CAST(NULL AS TIMESTAMP)"
    return "COALESCE(" + ", ".join(parts) + ")" if len(parts) > 1 else parts[0]


def build() -> tuple[str, list[dict]]:
    con = duckdb.connect()
    selects, report = [], []
    for name, (path, kind, tfield) in sorted(SOURCES.items()):
        if not path.exists():
            report.append({"source": name, "status": "path absent", "at": None})
            continue
        scan = scan_target(path, kind)
        if scan is None:
            report.append({"source": name, "status": "no shards", "at": None})
            continue
        cols = columns(con, scan)
        if not cols:
            report.append({"source": name, "status": "DuckDB cannot describe it", "at": None})
            continue
        at = time_expr(cols, tfield)
        report.append({"source": name, "status": "ok", "at": at,
                       "timed": at != "CAST(NULL AS TIMESTAMP)"})
        #: to_json(t) reproduces collect.py's `payload`: the whole row as it was written,
        #: so nothing downstream depends on a schema this loader guessed.
        selects.append(
            f"SELECT '{name}' AS source, {at} AS at, to_json(t) AS payload\n"
            f"FROM {scan} AS t"
        )

    facts_sql = "\n".join([
        "-- GENERATED by science/dbt_build.py. Do not edit; edit science/sources.json.",
        "--",
        "-- This is collect.py's `facts(source, at, ingested_at, payload)` table, built by",
        "-- DuckDB's JSON reader instead of ~300 lines of hand-rolled parsing (crew#74).",
        "-- `ingested_at` is the run time rather than a stored column, because a rebuilt",
        "-- table has one ingest time and storing it per row was always a copy of that.",
        "{{ config(materialized='table') }}",
        "",
        "SELECT *, now() AS ingested_at FROM (",
        "\nUNION ALL BY NAME\n".join(selects),
        ")",
        "",
    ])
    return facts_sql, report


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--print", action="store_true", dest="dry",
                    help="write nothing, show what would be written")
    args = ap.parse_args()

    facts_sql, report = build()
    ok = [r for r in report if r["status"] == "ok"]
    timed = [r for r in ok if r["timed"]]

    if args.dry:
        print(facts_sql)
    else:
        STAGING.mkdir(parents=True, exist_ok=True)
        (STAGING / "facts.sql").write_text(facts_sql)
        print(f"wrote {STAGING / 'facts.sql'}")

    print(f"\nsources in the registry : {len(SOURCES)}")
    print(f"readable now            : {len(ok)}")
    print(f"  of those, timestamped : {len(timed)}")
    skipped = [r for r in report if r["status"] != "ok"]
    for r in skipped:
        print(f"  skipped {r['source']}: {r['status']}")
    untimed = [r["source"] for r in ok if not r["timed"]]
    if untimed:
        #: Named rather than counted, because "3 sources have no timestamp" is a number
        #: nobody can act on and "these three" is a list somebody can go and fix.
        print(f"  no time column at all   : {', '.join(untimed)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
