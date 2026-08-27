#!/usr/bin/env python3
"""The warehouse exit drill (crew#74 row 1, LAW 19): prove the data leaves DuckDB.

WHY. A warehouse a buyer cannot walk out of is a liability on the balance sheet, and
"DuckDB can export to Parquet" is a claim until a run does it. DuckDB's own `EXPORT
DATABASE` writes every table as Parquet plus the DDL to rebuild it; `IMPORT DATABASE`
rebuilds it in a fresh database. This runs both and compares per-table row counts.
It writes nothing into the warehouse it reads.

    python3 science/exit_drill.py                      # the real warehouse, science/dbt/warehouse.duckdb
    python3 science/exit_drill.py --db other.duckdb
    python3 science/exit_drill.py --fixture            # a tiny built-in database (CI has no warehouse)

Exit 0 when every table round-trips with the same count; 1 otherwise; 2 when there is no
database to drill, printed as BLIND. Two lines of receipt, then one row appended to the
drills store the estate snapshot already reads (`drills` in science/sources.json).
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
import time
from pathlib import Path

try:
    import duckdb  # pyright: ignore[reportMissingImports]
except ImportError:  # pragma: no cover
    sys.exit("duckdb is not installed in this interpreter (requirements-dev.txt names it).")

HERE = Path(__file__).resolve().parent
DEFAULT_DB = HERE / "dbt" / "warehouse.duckdb"
DRILL_ID = "warehouse-exit-export-database"


def counts(con: duckdb.DuckDBPyConnection) -> dict[str, int]:
    tables = [r[0] for r in con.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main' "
        "AND table_type = 'BASE TABLE' ORDER BY 1").fetchall()]
    return {t: con.execute(f'SELECT count(*) FROM "{t}"').fetchone()[0] for t in tables}


def fixture_db(path: Path) -> None:
    con = duckdb.connect(str(path))
    con.execute('CREATE TABLE facts(source VARCHAR, "at" TIMESTAMP, payload JSON)')
    con.execute("INSERT INTO facts SELECT 'fixture', now(), to_json({'i': i}) FROM range(1000) t(i)")
    con.execute("CREATE TABLE quality_checks(run INTEGER, rows BIGINT)")
    con.execute("INSERT INTO quality_checks VALUES (1, 1000), (2, 1000)")
    con.close()


def drill(db: Path, out: Path, damage: str | None = None) -> tuple[bool, dict]:
    """Export `db` to `out`, import it into a fresh database, compare counts.
    `damage` names a table whose Parquet file is removed after export: the failing case."""
    src = duckdb.connect(str(db), read_only=True)
    before = counts(src)
    src.execute(f"EXPORT DATABASE '{out.as_posix()}' (FORMAT PARQUET)")
    src.close()
    if damage:
        for p in out.glob(f"{damage}.parquet"):
            p.unlink()
    fresh = duckdb.connect()
    try:
        fresh.execute(f"IMPORT DATABASE '{out.as_posix()}'")
        after = counts(fresh)
        err = None
    except duckdb.Error as exc:
        after, err = {}, str(exc).splitlines()[0]
    fresh.close()
    diff = {t: (before.get(t), after.get(t)) for t in sorted(set(before) | set(after))
            if before.get(t) != after.get(t)}
    ok = not diff and not err and bool(before)
    return ok, {"tables": len(before), "rows": sum(before.values()), "diff": diff, "error": err,
                "parquet_bytes": sum(p.stat().st_size for p in out.glob("*.parquet"))}


def record(status: str, rc: int, seconds: float, note: str) -> Path | None:
    sys.path.insert(0, str(HERE))
    from collect import SOURCES
    entry = SOURCES.get("drills")
    if not entry:
        return None
    path = Path(entry[0])
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {"id": DRILL_ID, "ts": int(time.time()), "iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "status": status, "rc": rc, "seconds": round(seconds, 2), "note": note, "log": "science/exit_drill.py"}
    with open(path, "a") as fh:
        fh.write(json.dumps(row) + "\n")
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", type=Path, default=DEFAULT_DB)
    ap.add_argument("--fixture", action="store_true", help="drill a built-in 1000-row database instead")
    ap.add_argument("--no-record", action="store_true", help="do not append to the drills store")
    args = ap.parse_args()
    t0 = time.time()
    tmp = Path(tempfile.mkdtemp(prefix="exit-drill-"))
    try:
        db = args.db
        if args.fixture:
            db = tmp / "fixture.duckdb"
            fixture_db(db)
        if not db.exists():
            print(f"BLIND  no database at {db}; run science/dbt_build.py then dbt run, or pass --fixture")
            return 2
        ok, r = drill(db, tmp / "export")
        status = "PASS" if ok else "FAIL"
        note = (f"{r['tables']} table(s), {r['rows']} row(s) exported as Parquet ({r['parquet_bytes']} bytes) "
                f"and imported into a fresh database" + (f"; diff {r['diff']}" if r["diff"] else "")
                + (f"; error {r['error']}" if r["error"] else ""))
        print(f"{status}  {DRILL_ID}  {db.name}: {note}")
        rc = 0 if ok else 1
        if not args.no_record:
            where = record(status, rc, time.time() - t0, note)
            print(f"recorded in {where}" if where else "not recorded: no `drills` entry in science/sources.json")
        return rc
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
