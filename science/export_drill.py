#!/usr/bin/env python3
"""crew#74 row 1: the warehouse exit drill.

LAW 19 grades every dependency by its exit. The science warehouse is one SQLite
file (`science/warehouse.db`); its exit is DuckDB's `EXPORT DATABASE`, which
writes every table as plain Parquet plus the `schema.sql`/`load.sql` pair that
`IMPORT DATABASE` reads back. An exit that has never been taken is a hope, so
this takes it on every run and then proves the copy is whole: a fresh DuckDB
imports the directory and every table's row count must equal the source's.

    python3 science/export_drill.py             # export to a temp dir, verify, delete
    python3 science/export_drill.py --keep DIR  # export into DIR and leave it there

Exit 0 when every table round-trips, 1 otherwise, one line per table either way.
Registered as drill `export-database` in the estate drill register
(`drills/register.json`, run daily by `ai.estate.drills`), whose `--check` goes
red when this fails or its last green is older than the bar.
"""
from __future__ import annotations

import argparse
import os
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

WAREHOUSE = Path(os.environ.get("SCIENCE_WAREHOUSE") or Path(__file__).parent / "warehouse.db")


def tables_in(warehouse: Path) -> list[str]:
    """Table names as SQLite lists them. Views are not exported: they are SQL
    over these tables and DuckDB cannot always run SQLite's dialect of them."""
    con = sqlite3.connect(f"file:{warehouse}?mode=ro", uri=True)
    try:
        rows = con.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        ).fetchall()
    finally:
        con.close()
    return [r[0] for r in rows]


def export(warehouse: Path, out: Path) -> dict[str, int]:
    """EXPORT DATABASE every table of `warehouse` into `out`; return source counts."""
    import duckdb

    con = duckdb.connect()
    con.execute(f"ATTACH '{warehouse}' AS w (TYPE sqlite, READ_ONLY)")
    counts: dict[str, int] = {}
    for tb in tables_in(warehouse):
        con.execute(f'CREATE TABLE "{tb}" AS SELECT * FROM w."{tb}"')
        counts[tb] = con.execute(f'SELECT count(*) FROM "{tb}"').fetchone()[0]
    con.execute(f"EXPORT DATABASE '{out}' (FORMAT PARQUET)")
    con.close()
    return counts


def verify(out: Path, counts: dict[str, int]) -> list[str]:
    """IMPORT DATABASE into a fresh DuckDB and compare row counts. Failures are
    sentences naming the table; an empty list is a whole copy."""
    import duckdb

    failures: list[str] = []
    con = duckdb.connect()
    try:
        con.execute(f"IMPORT DATABASE '{out}'")
    except duckdb.Error as exc:
        return [f"import of {out} failed: {str(exc).splitlines()[0]}"]
    for tb, n in counts.items():
        try:
            got = con.execute(f'SELECT count(*) FROM "{tb}"').fetchone()[0]
        except duckdb.Error as exc:
            failures.append(f"{tb}: not in the export ({str(exc).splitlines()[0]})")
            continue
        if got != n:
            failures.append(f"{tb}: exported {got} rows, warehouse has {n}")
    con.close()
    return failures


def drill(warehouse: Path, out: Path) -> tuple[dict[str, int], list[str]]:
    if not warehouse.exists():
        return {}, [f"warehouse {warehouse} does not exist"]
    counts = export(warehouse, out)
    if not counts:
        return counts, [f"warehouse {warehouse} has no tables"]
    return counts, verify(out, counts)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--keep", metavar="DIR", help="export into DIR and leave it there")
    args = ap.parse_args()
    out = Path(args.keep) if args.keep else Path(tempfile.mkdtemp(prefix="export-database-"))
    try:
        counts, failures = drill(WAREHOUSE, out)
        for tb, n in counts.items():
            print(f"{tb:18} {n:>8} rows -> {out / (tb + '.parquet')}")
        for f in failures:
            print(f"FAIL {f}")
        print(f"{'FAIL' if failures else 'PASS'}    export-database: {len(counts)} table(s) round-tripped through "
              f"EXPORT DATABASE/IMPORT DATABASE from {WAREHOUSE}" + ("" if failures else "; every count matches"))
        return 1 if failures else 0
    finally:
        if not args.keep:
            shutil.rmtree(out, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
