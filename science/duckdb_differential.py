#!/usr/bin/env python3
"""Does DuckDB's `read_json_auto` read this estate's stores the same way collect.py does?

WHY THIS EXISTS. crew#74 and the wheel audit (crew#104, two lanes independently) both say
the same thing about `science/collect.py`: the ~300 lines of hand-rolled JSONL parsing in
`read_rows` are a wheel, and `duckdb.read_json_auto` is the mature tool that does it. The
audit's words: "REPLACE (parsing/load half) ... deletes ~300 lines of read_rows/row_time".

That verdict is almost certainly right, and it is still a claim. Before ~300 lines are
deleted, something has to show that the replacement reads the SAME ROWS out of the SAME
FILES. This is that something.

WHAT RUNG THIS IS. Rung 3, differential replay, straight out of the estate's testing
doctrine: "For any rewrite, the oracle is the current implementation. Run both over the
recorded corpus and diff. One assertion, thousands of cases." And the doctrine's other
half applies too -- "A differential test is a migration tool, not a permanent test: delete
it when the old implementation goes." When `collect.py`'s loader is gone, delete this file
with it. It has no reason to outlive the thing it is checking.

WHAT IT COMPARES, AND WHAT IT DELIBERATELY DOES NOT. Row counts per declared source, both
directions, against the `facts` table `collect.py` last wrote. Row counts are the whole
question for the loader: a parser that drops rows or invents them is the failure mode that
matters, and it is the one no amount of reading the code will rule out on 29 real stores
with real broken lines in them.

It does NOT compare timestamps. `row_time()` is a separate ~20-line function with its own
rules (three key names, two encodings, an epoch sanity window that exists because a field
called "t" was silently landing rows in 1970). Porting that to SQL is a second migration
with a second differential, and mixing the two would mean a red result here could be
either. One question per run.

    python3 science/duckdb_differential.py            # the table and the verdict
    python3 science/duckdb_differential.py --json     # for a reader that is not a person

Exit 1 if any declared source disagrees. That is the point: a green run is the evidence
crew#74 needs before the loader is replaced, and a red one names the file to go and look at.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from collect import SOURCES, WAREHOUSE, shard_files  # noqa: E402  the registry has one reader

try:
    import duckdb
except ImportError:                                              # pragma: no cover
    sys.exit("duckdb is not installed in this interpreter.\n"
             "  /Users/chidionyema/dev/code/crew/.venv/bin/python science/duckdb_differential.py")


def duckdb_count(con, path: Path, kind: str) -> tuple[int | None, str]:
    """How many rows DuckDB reads out of one store, and why if it cannot.

    `ignore_errors=true` is the deliberate match for collect.py's behaviour: it counts an
    unparseable line and moves on rather than failing the store. `union_by_name=true` and
    `sample_size=-1` matter because these stores are append-only JSONL written by a dozen
    different producers over months -- the fields at the end of a file are not the fields
    at the start, and a schema guessed from the first 20 lines drops the rest.
    """
    if kind == "jsonl-dir":
        #: `**/*.jsonl`, not `*.jsonl`, because collect.py's shard_files uses rglob --
        #: ~/.claude/jobs keeps its timelines one directory deeper than the other sharded
        #: stores. The first run of this differential reported job_timelines as a DIFFERS
        #: with 316 rows against nothing, and the defect was here, not in DuckDB.
        target = str(path / "**" / "*.jsonl")
        if not shard_files(path):
            return 0, "no shards"
    elif kind == "jsonl":
        target = str(path)
    else:
        #: A single JSON document is one row to collect.py. read_json_auto on a top-level
        #: array would report its length instead, so this asks the question collect.py
        #: asks: does the file parse, yes or no.
        try:
            json.loads(path.read_text(errors="ignore"))
            return 1, "single json document"
        except (json.JSONDecodeError, OSError) as exc:
            return 0, f"will not parse: {type(exc).__name__}"

    sql = (f"SELECT count(*) FROM read_json_auto('{target}', "
           f"format='newline_delimited', union_by_name=true, sample_size=-1, "
           f"ignore_errors=true, maximum_object_size=67108864)")
    try:
        return con.execute(sql).fetchone()[0], ""
    except duckdb.Error as exc:
        return None, str(exc).splitlines()[0][:120]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", help="machine output")
    args = ap.parse_args()

    if not WAREHOUSE.exists():
        sys.exit(f"no warehouse at {WAREHOUSE}. Run `python3 science/collect.py` first -- "
                 f"there is nothing to be differential against.")

    sq = sqlite3.connect(f"file:{WAREHOUSE}?mode=ro", uri=True)
    oracle = dict(sq.execute("SELECT source, count(*) FROM facts GROUP BY source").fetchall())
    sq.close()
    con = duckdb.connect()

    rows = []
    for name, (path, kind, _tf) in sorted(SOURCES.items()):
        if not path.exists():
            #: A declared source whose file is absent is a registry question, not a loader
            #: question. collect.py reports it separately and so does this.
            rows.append({"source": name, "kind": kind, "sqlite": oracle.get(name, 0),
                         "duckdb": None, "note": "path absent", "agree": None})
            continue
        got, note = duckdb_count(con, path, kind)
        want = oracle.get(name, 0)
        rows.append({"source": name, "kind": kind, "sqlite": want, "duckdb": got,
                     "note": note, "agree": got == want})

    #: A source sitting in the warehouse that the registry no longer declares is a real
    #: finding -- it means collect.py wrote it under a name nobody maintains any more.
    for name in sorted(set(oracle) - set(SOURCES)):
        rows.append({"source": name, "kind": "-", "sqlite": oracle[name], "duckdb": None,
                     "note": "in the warehouse, not in the registry", "agree": None})

    agree = [r for r in rows if r["agree"] is True]
    differ = [r for r in rows if r["agree"] is False]
    unknown = [r for r in rows if r["agree"] is None]

    if args.json:
        print(json.dumps({"warehouse": str(WAREHOUSE), "duckdb": duckdb.__version__,
                          "agree": len(agree), "differ": len(differ),
                          "unmeasurable": len(unknown), "rows": rows}, indent=2))
        return 1 if differ else 0

    print(f"oracle    : {WAREHOUSE}")
    print(f"challenger: duckdb {duckdb.__version__} read_json_auto")
    print()
    print(f"  {'source':<22} {'kind':<10} {'sqlite':>9} {'duckdb':>9}  verdict")
    for r in rows:
        d = "-" if r["duckdb"] is None else f"{r['duckdb']:,}"
        v = "same" if r["agree"] else ("DIFFERS" if r["agree"] is False else "-")
        note = f"  {r['note']}" if r["note"] else ""
        print(f"  {r['source']:<22} {r['kind']:<10} {r['sqlite']:>9,} {d:>9}  {v}{note}")

    print()
    print(f"agree        : {len(agree)}")
    print(f"DIFFER       : {len(differ)}")
    print(f"unmeasurable : {len(unknown)}")
    if differ:
        print("\nThe loader is not a drop-in replacement yet. Each DIFFERS row is a file to open:")
        for r in differ:
            print(f"  {r['source']}: sqlite {r['sqlite']:,} vs duckdb {r['duckdb']}")
        print("Do not delete read_rows() until this is empty.")
    else:
        print("\nEvery declared and present source reads the same both ways. This is the "
              "evidence crew#74 needs to replace the loader; timestamps are a separate run.")
    return 1 if differ else 0


if __name__ == "__main__":
    sys.exit(main())
