#!/usr/bin/env python3
"""The estate's data dictionary, generated rather than written.

The founder asked, 2026-08-24: "what of metadata, what have we missed, so i need you to
map all data points we collect, all data points we dont collect and why".

Two halves, and the second one is the half that matters.

COLLECTED is measured, never declared. It reads every row in the warehouse and walks the
JSON, so the field list is what the data actually contains today rather than what a
schema file claims it contained when somebody last edited it. Coverage is reported per
field because a field present in 79% of rows is not an optional field, it is two record
shapes sharing one source name, and that is invisible in any hand-written schema.

UNCOLLECTED is the register the estate did not have. A store nobody collects is not a
gap until somebody writes down why, because without the why every session rediscovers the
same 23 stores and re-argues the same decisions. Four reasons, and only four:

    WIRED_NEVER   the file exists and is being written; no collector reads it
    WRITER_DEAD   a collector reads it; the thing that used to write it has stopped
    NEVER_EMITTED the estate performs the act and records nothing, so there is no file
    EXCLUDED      a deliberate decision, with the reason, usually secrecy or volume

EXCLUDED is the one that makes this a register rather than a backlog. Without it, every
deliberate omission looks identical to an oversight (LAW 39: absence is a row too).

    python3 science/datamap.py             print the dictionary
    python3 science/datamap.py --json      the same thing as data
    python3 science/datamap.py --check     exit 1 if a source drifted from its last shape
"""
from __future__ import annotations

import argparse
import collections
import fnmatch
import json
import pathlib
import sqlite3
import sys

SCIENCE = pathlib.Path(__file__).resolve().parent
WAREHOUSE = SCIENCE / "warehouse.db"
SHAPES = SCIENCE / "shapes.json"

REGISTER = SCIENCE / "verdicts.json"
CENSUS = SCIENCE / "census.json"

sys.path.insert(0, str(SCIENCE))
import producers  # noqa: E402

#: Six verdicts, and only six. DECLINED comes from science/sources.json (crew#253), never
#: from verdicts.json, so a store is decided in one file. UNEXPLAINED is not a verdict: it is the absence of one,
#: and the gate fails on it. BLIND is not a verdict either: it is a domain that could not
#: see its world this run, and it fails the gate unless the register allows it by name.
VERDICTS = ("COLLECTED", "WIRED_NEVER", "WRITER_DEAD", "NEVER_EMITTED", "EXCLUDED", "DECLINED")
GAPS = ("WIRED_NEVER", "WRITER_DEAD", "NEVER_EMITTED")
CENSUS_FLOOR = 0.5   # a domain reporting under half of last run's members, without BLIND, is broken


def register() -> dict:
    reg = json.load(REGISTER.open())
    for e in reg["entries"]:
        if e["verdict"] == "DECLINED":
            raise ValueError(f"{e['key']}: DECLINED is decided in science/sources.json, not here")
        if e["verdict"] not in VERDICTS:
            raise ValueError(f"{e['key']}: verdict {e['verdict']!r} is not one of {VERDICTS}")
        if e["verdict"] == "COLLECTED" and not e.get("reader"):
            raise ValueError(f"{e['key']}: COLLECTED must name the reader")
        if e["verdict"] == "EXCLUDED" and not e.get("why"):
            raise ValueError(f"{e['key']}: EXCLUDED must state the reason")
    return reg


def _match(entries: list[dict], prod: dict) -> dict | None:
    """First entry whose key glob matches the producer's key, and whose kind glob (if any)
    matches its kind. Order in the register is precedence: put the narrow entry first."""
    for e in entries:
        if fnmatch.fnmatchcase(prod["key"], e["key"]) and \
                (not e.get("kind") or fnmatch.fnmatchcase(prod["kind"], e["kind"])):
            return e
    return None


def grade(prods: list[dict], reg: dict) -> list[dict]:
    """Attach a verdict to every producer. A table inside a store inherits the store's
    verdict; a producer the register does not name is UNEXPLAINED."""
    entries = reg["entries"]
    out = []
    for p in prods:
        e = p.get("decided") or _match(entries, p)
        if e is None and p["kind"] == "table":
            # mac/table/<store>/<t> -> the store's own row
            store = p["key"].rsplit("/", 1)[0].replace("mac/table/", "mac/data/", 1)
            e = _match(entries, {"key": store, "kind": "data"})
            if e is None:
                owner = next((q for q in prods if q["key"] == store and q.get("decided")), None)
                e = owner["decided"] if owner else None
        if e is None and p.get("auto"):
            e = p["auto"]
        g = dict(p)
        if e is None:
            g.update(verdict="UNEXPLAINED", why="No decision has been recorded about this producer.")
        else:
            g.update(verdict=e["verdict"], why=e.get("why", ""), reader=e.get("reader", ""),
                     ticket=e.get("ticket", ""), entry=e.get("key", "auto"))
        out.append(g)
    return out


def census_check(graded: list[dict], blind: dict[str, str]) -> list[str]:
    """A discoverer that quietly finds far fewer members than last time is the same
    failure as one that raised, minus the honesty. Compare against the last census."""
    now = collections.Counter(g["domain"] for g in graded)
    msgs = []
    if CENSUS.exists():
        was = json.load(CENSUS.open()).get("domains", {})
        for d, n_was in was.items():
            if d in blind:
                continue
            n_now = now.get(d, 0)
            if n_was and n_now < n_was * CENSUS_FLOOR:
                msgs.append(f"{d}: {n_now} members, was {n_was}; a discoverer went half-blind without saying so")
    for d in producers.DOMAINS:
        if d not in now and d not in blind:
            msgs.append(f"{d}: 0 members and not BLIND; a domain never returns nothing silently")
    return msgs


def violations(graded: list[dict], blind: dict[str, str], reg: dict, census: list[str]) -> list[str]:
    """The gate. Every line here is one thing the founder's law forbids."""
    v = []
    unexplained = [g for g in graded if g["verdict"] == "UNEXPLAINED"]
    if unexplained:
        v.append(f"{len(unexplained)} producer(s) UNEXPLAINED (first: {unexplained[0]['key']})")
    unticketed = sorted({g["entry"] for g in graded if g["verdict"] in GAPS and not g.get("ticket")})
    if unticketed:
        v.append(f"{len(unticketed)} gap entr(y/ies) without a ticket: {', '.join(unticketed[:5])}")
    allowed = reg.get("blind_allowed", {})
    for d, why in blind.items():
        if d not in allowed:
            v.append(f"domain {d} BLIND and not allowed: {why}")
    v.extend(census)
    return v


def file_tickets(graded: list[dict], reg: dict, repo: str) -> int:
    """One crew issue per unticketed gap entry (crew#320's third box), written back into
    the register so the gate goes green on the same run that filed them."""
    import subprocess
    by_entry: dict[str, list[dict]] = collections.defaultdict(list)
    for g in graded:
        if g["verdict"] in GAPS and not g.get("ticket"):
            by_entry[g["entry"]].append(g)
    filed = 0
    for e in reg["entries"]:
        if e.get("ticket") or e["verdict"] not in GAPS:
            continue
        members = by_entry.get(e["key"], [])
        sample = "\n".join(f"- `{m['key']}` ({m['kind']}; can measure: {', '.join(m['measures'][:5])})" for m in members[:15])
        more = f"\n- ... and {len(members) - 15} more" if len(members) > 15 else ""
        body = (f"Filed by `science/datamap.py --file-tickets` (LAW 50, crew#320).\n\n"
                f"**Verdict:** {e['verdict']}\n**Register entry:** `{e['key']}`"
                f"{' kind `' + e['kind'] + '`' if e.get('kind') else ''}\n**Members this run:** {len(members)}\n\n"
                f"**Why it is a gap:** {e.get('why','')}\n\n{sample}{more}\n\n"
                f"Done when the entry's verdict in `science/verdicts.json` is COLLECTED with a named reader, "
                f"or EXCLUDED with a reason, and `datamap.py --check` is green.")
        title = f"datamap {e['verdict']}: {e['key']}" + (f" [{e['kind']}]" if e.get("kind") else "")
        r = subprocess.run(["gh", "issue", "create", "-R", repo, "--title", title[:200], "--body", body,
                            "--label", "datamap"], capture_output=True, text=True, timeout=60, check=False)
        if r.returncode != 0:
            print(f"  could not file for {e['key']}: {r.stderr.strip()[:160]}", file=sys.stderr)
            continue
        num = r.stdout.strip().rsplit("/", 1)[-1]
        e["ticket"] = f"{repo.split('/')[-1]}#{num}"
        filed += 1
        print(f"  filed {e['ticket']}  {title}")
    if filed:
        REGISTER.write_text(json.dumps(reg, indent=1) + "\n")
    return filed


# A dict is a record when its keys are schema, and a map when its keys are data.
# Both are dicts, and walking them the same way is what produced 810 "fields" for
# agent_cert out of 12 rows: 160 test IDs used as keys, times 5 attributes each.
# Those 800 paths are not schema. No contract can be written against them, because
# the next certification run invents new ones.
#
# The tell is not the key count on its own -- a wide record is legal. It is that a
# map's values all have the SAME shape as each other, because they are instances of
# one thing, while a record's values are unrelated. So: many keys AND near-identical
# child key sets means a map, and the child shape is recorded once under `path.*`
# instead of once per key. The thresholds are deliberately conservative so a genuinely
# wide record is not misread as a map.
MAP_MIN_KEYS = 12      # below this, a wide record is more likely than a map
MAP_SHAPE_AGREEMENT = 0.8   # share of children that must have the modal key set


def _is_map(v: dict) -> bool:
    """True when this dict's keys are data rather than schema."""
    if len(v) < MAP_MIN_KEYS:
        return False
    children = [c for c in v.values() if isinstance(c, dict)]
    if len(children) < len(v) * MAP_SHAPE_AGREEMENT:
        return False          # values are not uniformly records
    shapes = collections.Counter(frozenset(c) for c in children)
    modal, n = shapes.most_common(1)[0]
    return bool(modal) and n >= len(children) * MAP_SHAPE_AGREEMENT


def sh_fields(rows: list[dict]) -> tuple[collections.Counter, dict[str, str]]:
    """Walk every row and return each leaf field path, how often it appeared, and its type.

    Nested dicts become dotted paths. Lists are leaves: their contents vary row to row and
    counting inside them produces a field list that grows with the data rather than with
    the schema. A dict whose keys are data rather than schema is treated the same way as a
    list: recorded once as a map, with its child shape under `path.*`, so the field count
    describes the schema instead of growing with the rows.
    """
    keys: collections.Counter = collections.Counter()
    types: dict[str, str] = {}

    def walk(obj: object, prefix: str = "") -> None:
        if not isinstance(obj, dict):
            return
        for k, v in obj.items():
            path = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict) and _is_map(v):
                keys[path] += 1
                types.setdefault(path, "map")
                # Record the child shape once, from the modal child, so the fields
                # inside the map are still described and still contractable.
                children = [c for c in v.values() if isinstance(c, dict)]
                shapes = collections.Counter(frozenset(c) for c in children)
                modal = shapes.most_common(1)[0][0]
                for c in children:
                    if frozenset(c) == modal:
                        walk(c, f"{path}.*")
                        break
            elif isinstance(v, dict):
                walk(v, path)
            else:
                keys[path] += 1
                types.setdefault(path, type(v).__name__)

    for r in rows:
        walk(r)
    return keys, types


def collected() -> dict:
    if not WAREHOUSE.exists():
        return {}
    db = sqlite3.connect(f"file:{WAREHOUSE}?mode=ro", uri=True)
    out: dict = {}
    for (src,) in db.execute("SELECT DISTINCT source FROM facts ORDER BY 1"):
        rows = []
        bad = 0
        for (p,) in db.execute("SELECT payload FROM facts WHERE source = ?", (src,)):
            try:
                rows.append(json.loads(p))
            except json.JSONDecodeError:
                bad += 1
        keys, types = sh_fields(rows)
        n = len(rows) or 1
        out[src] = {
            "rows": len(rows),
            "unparseable": bad,
            "fields": {
                k: {"type": types[k], "coverage": round(100.0 * c / n)}
                for k, c in sorted(keys.items(), key=lambda kv: (-kv[1], kv[0]))
            },
        }
    return out


def drift(now: dict) -> list[str]:
    """Say which sources changed shape since the last run.

    A field appearing or vanishing is the single cheapest signal that a producer changed
    and nothing downstream was told. It is not an error, so it never reaches a log; it
    surfaces weeks later as a view that quietly returns NULL.
    """
    if not SHAPES.exists():
        return []
    was = json.load(SHAPES.open())
    msgs = []
    for src, cur in now.items():
        old = was.get(src)
        if not old:
            msgs.append(f"{src}: new source")
            continue
        added = set(cur["fields"]) - set(old.get("fields", {}))
        gone = set(old.get("fields", {})) - set(cur["fields"])
        if added:
            msgs.append(f"{src}: +{len(added)} field(s): {', '.join(sorted(added)[:4])}")
        if gone:
            msgs.append(f"{src}: -{len(gone)} field(s): {', '.join(sorted(gone)[:4])}")
    for src in set(was) - set(now):
        msgs.append(f"{src}: source disappeared")
    return msgs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", help="emit the dictionary as data")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 on any UNEXPLAINED producer, unticketed gap, disallowed BLIND "
                         "domain, half-blind discoverer, or a source that changed shape")
    ap.add_argument("--domains", default="", help="comma list of domains to run (default all)")
    ap.add_argument("--file-tickets", action="store_true",
                    help="open one crew issue per unticketed gap entry and write it back")
    ap.add_argument("--repo", default="chidionyema/crew")
    args = ap.parse_args()

    reg = register()
    col = collected()
    changes = drift(col)
    only = set(args.domains.split(",")) - {""} or None
    prods, blind = producers.discover(only)
    graded = grade(prods, reg)
    if args.file_tickets:
        n = file_tickets(graded, reg, args.repo)
        print(f"filed {n} ticket(s)")
        graded = grade(prods, reg)
    census = census_check(graded, blind) if only is None else []
    bad = violations(graded, blind, reg, census)

    counts = collections.Counter((g["domain"], g["verdict"]) for g in graded)
    domains = sorted({g["domain"] for g in graded} | set(blind))

    if args.json:
        json.dump({"collected": col, "producers": graded, "blind": blind, "violations": bad,
                   "drift": changes}, sys.stdout, indent=1)
        print()
    else:
        total = sum(len(v["fields"]) for v in col.values())
        print(f"COLLECTED  {len(col)} sources, "
              f"{sum(v['rows'] for v in col.values())} rows, {total} distinct field paths")
        print("-" * 78)
        for src, v in col.items():
            partial = [k for k, f in v["fields"].items() if f["coverage"] < 100]
            note = f"  ({len(partial)} field(s) not in every row)" if partial else ""
            print(f"  {src:<18} {v['rows']:>6} rows  {len(v['fields']):>4} fields{note}")

        print()
        print(f"DATA MAP  {len(graded)} producers in {len(domains)} domains, "
              f"{sum(len(g['measures']) for g in graded)} measurables")
        print("-" * 78)
        head = f"  {'domain':<13}{'total':>7}" + "".join(f"{v[:9]:>11}" for v in VERDICTS) + f"{'UNEXPL':>8}"
        print(head)
        for d in domains:
            if d in blind:
                print(f"  {d:<13}{'BLIND':>7}   {blind[d][:60]}")
                continue
            row = f"  {d:<13}{sum(n for (dd, _), n in counts.items() if dd == d):>7}"
            row += "".join(f"{counts.get((d, v), 0):>11}" for v in VERDICTS)
            row += f"{counts.get((d, 'UNEXPLAINED'), 0):>8}"
            print(row)

        gaps = [g for g in graded if g["verdict"] in GAPS]
        by_entry = collections.Counter(g["entry"] for g in gaps)
        print()
        print(f"GAPS  {len(gaps)} producers under {len(by_entry)} register entries; each entry carries a ticket")
        print("-" * 78)
        for entry, n in by_entry.most_common():
            g = next(x for x in gaps if x["entry"] == entry)
            print(f"  {g['verdict']:<14}{entry[-40:]:<40}{n:>6}  {g.get('ticket') or 'NO TICKET'}")

        unexplained = [g for g in graded if g["verdict"] == "UNEXPLAINED"]
        if unexplained:
            print()
            print(f"UNEXPLAINED  {len(unexplained)} producers nobody has decided about")
            print("-" * 78)
            for g in unexplained[:40]:
                print(f"  {g['key'][-60:]:<60} {g['kind']}")

        if changes:
            print()
            print("SHAPE CHANGED SINCE LAST RUN")
            print("-" * 78)
            for m in changes:
                print(f"  {m}")

        print()
        if bad:
            print(f"GATE  RED  {len(bad)} violation(s)")
            for b in bad:
                print(f"  {b}")
        else:
            print("GATE  GREEN  every producer has a verdict, every gap has a ticket, no domain silently blind")

    SHAPES.write_text(json.dumps(col, indent=1))
    if only is None:
        CENSUS.write_text(json.dumps({"domains": dict(collections.Counter(g["domain"] for g in graded)),
                                      "blind": blind}, indent=1) + "\n")
    return 1 if (args.check and (bad or changes)) else 0


if __name__ == "__main__":
    sys.exit(main())
