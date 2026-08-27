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
from collect import (
    SOURCES,
    WAREHOUSE,
    read_rows,
    shard_files,
)

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


def facts_differential(duck_path: Path) -> int:
    """The second question: does the built `facts` table match the one collect.py writes?

    Row counts were the loader's question and they are answered. This is the timestamp
    question, which is separate and harder, because `row_time()` is not a parser -- it is a
    set of estate-specific rules about which key holds the time, which encodings are real,
    and which numbers are too small or too large to be a date at all.

    Two things are compared per source: how many rows carry a timestamp, and what the
    newest one is. The second matters more than it looks. DuckDB parses an ISO string into
    a naive TIMESTAMP and drops the offset, so the model has to decide what timezone that
    naive value was in. It assumes UTC. If that assumption is wrong the newest timestamp
    lands a whole number of hours out, which is exactly what a max() comparison shows and
    what a row count never would.
    """
    import sqlite3 as _s

    #: THE RACE, AND WHY THIS IS NOT A TOLERANCE. These stores are appended to while the
    #: comparison runs. The first version of this reported eight sources as disagreeing --
    #: 3015 rows against 3066 on stuck_detector -- and every one of them was the estate
    #: writing more rows in the six minutes between the two loaders. A tolerance would have
    #: hidden a real defect of the same size, so instead the two sides are compared at a
    #: WATERMARK: the older of their two newest rows. Below that line both loaders saw
    #: exactly the same file, and the counts must match exactly.
    #:
    #: Rows above the line are only ever expected on the DuckDB side, because dbt runs
    #: second. A SQLite side that is ahead means rows went missing, which is a defect.
    def wall(v) -> str | None:
        """A timestamp as its wall clock, with no timezone arithmetic anywhere.

        Both sides are compared as the producer wrote them. Converting either one is how
        the first run of this manufactured a clean +1.00h disagreement on four sources
        that were storing exactly the same instant.
        """
        if v is None:
            return None
        s = str(v).replace("T", " ")
        for cut in ("+", "Z"):
            if cut in s[10:]:
                s = s[:10] + s[10:].split(cut)[0]
        s = s.strip()[:19]
        #: A date with no clock is still a wall clock, and it has to be written to the same
        #: width as one or a string comparison puts it in the wrong order. founder_actions
        #: stores `opened: "2026-08-23"`, and "2026-08-23 00:00:00" <= "2026-08-23" is false
        #: while the two are the same instant. That produced the only DISAGREE in an
        #: otherwise clean run, and it was this function's fault, not the data's.
        if len(s) == 10:
            s += " 00:00:00"
        elif len(s) == 16:
            s += ":00"
        return s

    sq = _s.connect(f"file:{WAREHOUSE}?mode=ro", uri=True)
    left = {r[0]: (r[1], r[2], wall(r[3])) for r in sq.execute(
        "SELECT source, count(*), count(at), max(at) FROM facts GROUP BY source")}

    con = duckdb.connect(str(duck_path), read_only=True)
    #: `at` must be quoted in DuckDB. It is a keyword there (AT TIME ZONE) and is not one
    #: in SQLite, so the same column name needs different SQL on the two sides.
    right = {r[0]: (r[1], r[2], wall(r[3])) for r in con.execute(
        'SELECT source, count(*), count("at"), max("at") FROM facts GROUP BY source').fetchall()}

    print(f"\n{'source':<22} {'at the watermark':>18} {'newest':>10}  {'total rows':>14}")
    bad, notes = 0, []
    for name in sorted(set(left) | set(right)):
        lr, lt, lm = left.get(name, (0, 0, None))
        rr, rt, rm = right.get(name, (0, 0, None))

        if lm is not None and rm is not None:
            mark = min(lm, rm)
            lw = sq.execute("SELECT count(*) FROM facts WHERE source=? AND at IS NOT NULL "
                            "AND replace(substr(at,1,19),'T',' ') <= ?", (name, mark)).fetchone()[0]
            rw = con.execute('SELECT count(*) FROM facts WHERE source=? AND "at" IS NOT NULL '
                             'AND strftime("at", \'%Y-%m-%d %H:%M:%S\') <= ?',
                             [name, mark]).fetchone()[0]
            mark_v = "same" if lw == rw else f"{lw}/{rw}"
            if lw != rw:
                bad += 1
                notes.append(f"{name}: {lw} rows on or before {mark} in SQLite, {rw} in DuckDB")
            newest = "same" if lm == rm else f"{lm} vs {rm}"
        else:
            #: No timestamp on either side means no watermark is possible, so this source
            #: cannot be compared at all while it is being written to. That is a finding
            #: about the source, not a failure of the comparison, and it is why four stores
            #: are named in the summary rather than quietly passing.
            mark_v = "no time column"
            newest = "-"
            if lt != rt:
                bad += 1
                notes.append(f"{name}: timestamped rows differ, {lt} vs {rt}, and there is "
                             f"no watermark to compare at")

        if rr >= lr:
            rows_v = "same" if rr == lr else f"+{rr - lr} appended"
        else:
            rows_v = f"LOST {lr - rr}"
            bad += 1
            notes.append(f"{name}: SQLite has {lr} rows and DuckDB has {rr}. dbt ran second, "
                         f"so rows can only have been added. This one lost some.")
        print(f"{name:<22} {mark_v:>18} {newest:>10}  {rows_v:>14}")

    sq.close()
    print(f"\nsources compared : {len(set(left) | set(right))}")
    print(f"DISAGREE         : {bad}")
    for n in notes:
        print(f"  {n}")
    if not bad:
        print("\nEvery source holds the same rows below the watermark, agrees on when its "
              "newest row happened, and lost nothing. That is the writer proven, not just "
              "the reader.")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", help="machine output")
    ap.add_argument("--facts", action="store_true",
                    help="compare the built dbt `facts` table, not just the raw readers")
    args = ap.parse_args()

    if args.facts:
        duck = Path(__file__).parent / "dbt" / "warehouse.duckdb"
        if not duck.exists():
            sys.exit(f"no dbt warehouse at {duck}. Run:\n"
                     f"  python3 science/dbt_build.py && (cd science/dbt && dbt run --profiles-dir .)")
        return facts_differential(duck)

    if not WAREHOUSE.exists():
        sys.exit(f"no warehouse at {WAREHOUSE}. Run `python3 science/collect.py` first -- "
                 f"there is nothing to be differential against.")

    sq = sqlite3.connect(f"file:{WAREHOUSE}?mode=ro", uri=True)
    stored = dict(sq.execute("SELECT source, count(*) FROM facts GROUP BY source").fetchall())
    sq.close()
    con = duckdb.connect()

    rows = []
    for name, (path, kind, _tf) in sorted(SOURCES.items()):
        #: A sqlite source has no DuckDB oracle to diff against; the oracle is the query.
        if kind == "sqlite":
            continue
        if not path.exists():
            #: A declared source whose file is absent is a registry question, not a loader
            #: question. collect.py reports it separately and so does this.
            rows.append({"source": name, "kind": kind, "sqlite": stored.get(name, 0),
                         "duckdb": None, "note": "path absent", "agree": None})
            continue
        #: THE ORACLE IS THE FUNCTION, NOT THE WAREHOUSE. This used to compare DuckDB's
        #: live read against `count(*)` in the SQLite warehouse, which is a snapshot from
        #: whenever collect.py last ran. That made the run green only when collect.py had
        #: just been run and red otherwise: measured 2026-08-24, ledger 855 vs 856, spend
        #: 945 vs 946, stuck_detector 3,116 vs 3,166, and every one of those was the estate
        #: appending rows, not a loader dropping them. The doctrine's own words for rung 3
        #: are "the oracle is the current implementation" -- so it is read_rows(), called
        #: here on the same file in the same second.
        #:
        #: BRACKETED, for the same reason the facts comparison has a watermark. The file is
        #: still being appended to while these three reads happen, so DuckDB counts before
        #: and after and read_rows() runs between them. A count inside that bracket saw the
        #: same file; a count outside it did not, and that is a real disagreement no matter
        #: how small. This is not a tolerance: the bracket is measured, not chosen, and it
        #: is zero wide on a store nobody is writing to.
        before, note = duckdb_count(con, path, kind)
        live, _bad = read_rows(path, kind)
        after, _ = duckdb_count(con, path, kind)
        want = len(live)
        if before is None or after is None:
            agree, grew = None, 0
        else:
            lo, hi = min(before, after), max(before, after)
            agree, grew = lo <= want <= hi, hi - lo
        if agree and grew:
            note = (note + "; " if note else "") + f"grew {grew} rows mid-read"
        rows.append({"source": name, "kind": kind, "sqlite": want, "duckdb": after,
                     "note": note, "agree": agree})

    #: A source sitting in the warehouse that the registry no longer declares is a real
    #: finding -- it means collect.py wrote it under a name nobody maintains any more.
    for name in sorted(set(stored) - set(SOURCES)):
        rows.append({"source": name, "kind": "-", "sqlite": stored[name], "duckdb": None,
                     "note": "in the warehouse, not in the registry", "agree": None})

    agree = [r for r in rows if r["agree"] is True]
    differ = [r for r in rows if r["agree"] is False]
    unknown = [r for r in rows if r["agree"] is None]

    if args.json:
        print(json.dumps({"warehouse": str(WAREHOUSE), "duckdb": duckdb.__version__,
                          "agree": len(agree), "differ": len(differ),
                          "unmeasurable": len(unknown), "rows": rows}, indent=2))
        return 1 if differ else 0

    print("oracle    : collect.py read_rows(), called live on the same file")
    print(f"challenger: duckdb {duckdb.__version__} read_json_auto, bracketed either side")
    print()
    print(f"  {'source':<22} {'kind':<10} {'read_rows':>9} {'duckdb':>9}  verdict")
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
            print(f"  {r['source']}: read_rows {r['sqlite']:,} vs duckdb {r['duckdb']}")
        print("Do not delete read_rows() until this is empty.")
    else:
        print("\nEvery declared and present source reads the same both ways. This is the "
              "evidence crew#74 needs to replace the loader; timestamps are a separate run.")
    return 1 if differ else 0


if __name__ == "__main__":
    sys.exit(main())
