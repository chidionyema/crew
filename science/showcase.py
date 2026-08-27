#!/usr/bin/env python3
"""The science lane showcase: capabilities and progress, generated from what runs (crew#403).

Founder, 2026-08-27: "we need more transparency the capabilities and progress from the
science / research data and machine learning lane, we need a proper showcase."

Every number on the page is read from a store or a tree at generation time and is printed
next to the command that produces it, so a reader can re-run any row. A section whose
source is missing renders BLIND with the path it looked for; it never renders as empty
(LAW 45). The previous run's numbers are kept in `science/showcase-state.json`, and the
progress section is the diff against them, so "what changed" is answered by the page.

    python3 science/showcase.py            # write docs/science/SHOWCASE.md, print section sizes
    python3 science/showcase.py --print    # write nothing, show the page

Wired into `scripts/science-collect`, which launchd runs four times a day.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import sqlite3
import sys
from typing import Any

SCIENCE = pathlib.Path(__file__).resolve().parent
CREW = SCIENCE.parent
DOCS = CREW / "docs" / "science"
PAGE = DOCS / "SHOWCASE.md"
STATE = SCIENCE / "showcase-state.json"
WAREHOUSE = SCIENCE / "warehouse.db"
LEDGER = SCIENCE / "RESEARCH-LEDGER.jsonl"
SHIPS = SCIENCE / "ships.jsonl"
ATTENTION = SCIENCE / "attention.jsonl"
PREDICTIONS = SCIENCE / "predictions.jsonl"
SOURCES = SCIENCE / "sources.json"
LAUNCHD = pathlib.Path.home() / ".claude" / "scripts" / "launchagents"
WINDOW_DAYS = 7


class Blind(Exception):
    """A section that cannot see its source says so and stops."""


def _jsonl(path: pathlib.Path) -> list[dict]:
    if not path.exists():
        raise Blind(f"{path} absent")
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _docstring_line(path: pathlib.Path) -> str:
    m = re.search(r'^"""(.+?)$', path.read_text(), re.M)
    return (m.group(1) if m else "").strip().rstrip(".")


def capabilities(now: dt.datetime) -> tuple[list[dict], list[str]]:
    """One row per science/*.py: what it is, how it is invoked, and who schedules it.
    Scheduling is read from the tree and the launchd directory, never typed by hand."""
    schedulers: dict[str, str] = {}
    wrapper = CREW / "scripts" / "science-collect"
    wrapped = wrapper.read_text() if wrapper.exists() else ""
    for gate in sorted((CREW / "scripts" / "verify.d").glob("*.sh")):
        for name in re.findall(r"science/(\w+)\.py", gate.read_text()):
            schedulers.setdefault(name, f"CI: scripts/verify.d/{gate.name}")
    for name in re.findall(r"science/(\w+)\.py", wrapped):
        schedulers[name] = "launchd com.founder.sciencecollect via scripts/science-collect"
    plists = sorted(LAUNCHD.glob("*.plist")) if LAUNCHD.exists() else []
    for pl in plists:
        for name in re.findall(r"science/(\w+)\.py", pl.read_text()):
            schedulers.setdefault(name, f"launchd {pl.stem}")
    rows = []
    for py in sorted(SCIENCE.glob("*.py")):
        if py.name.startswith("_") or py.name == "showcase.py":
            continue
        rows.append({"name": py.stem, "what": _docstring_line(py)[:110],
                     "run": f"python3 science/{py.name}",
                     "scheduled": schedulers.get(py.stem, "hand-run")})
    notes = []
    if not LAUNCHD.exists():
        notes.append(f"BLIND to launchd: {LAUNCHD} absent (CI has no home tree)")
    return rows, notes


def warehouse(now: dt.datetime) -> dict:
    if not WAREHOUSE.exists():
        raise Blind(f"{WAREHOUSE} absent")
    db = sqlite3.connect(f"file:{WAREHOUSE}?mode=ro", uri=True)
    rows, sources, last = db.execute("select count(*), count(distinct source), max(ingested_at) from facts").fetchone()
    per = dict(db.execute("select source, max(at) from facts group by source").fetchall())
    reg = json.load(SOURCES.open()) if SOURCES.exists() else {"sources": [], "default_stale_after_hours": 48}
    default = reg.get("default_stale_after_hours", 48)
    stale = []
    for s in reg["sources"]:
        newest = per.get(s["name"])
        if not newest:
            continue
        try:
            age_h = (now - dt.datetime.fromisoformat(newest.replace("Z", "+00:00")).replace(tzinfo=None)).total_seconds() / 3600
        except ValueError:
            continue
        if age_h > s.get("stale_after_hours", default):
            stale.append(f"{s['name']} ({age_h:.0f}h)")
    contracted = sum(all(k in s for k in ("owner", "method", "retention_days", "sensitivity")) for s in reg["sources"])
    return {"rows": rows, "sources": sources, "last_ingest": last, "stale": stale,
            "declared": len(reg["sources"]), "contracted": contracted}


def _contract_violations(dm: Any) -> list | str:
    """datamap.contract_violations lands with crew#71 (crew#402); until then the row is BLIND."""
    fn = getattr(dm, "contract_violations", None)
    if not callable(fn):
        return "BLIND (crew#71 not merged)"
    return list(fn())


def datamap(now: dt.datetime) -> dict:
    sys.path.insert(0, str(SCIENCE))
    import datamap as dm
    if not dm.REGISTER.exists():
        raise Blind(f"{dm.REGISTER} absent")
    reg = json.load(dm.REGISTER.open())
    census = json.load(dm.CENSUS.open()) if dm.CENSUS.exists() else {}
    shapes = json.load(dm.SHAPES.open()) if dm.SHAPES.exists() else {}
    from collections import Counter
    verdicts = Counter(e["verdict"] for e in reg["entries"])
    return {"entries": len(reg["entries"]), "verdicts": dict(verdicts),
            "producers": sum(census.get("domains", {}).values()),
            "blind": sorted(census.get("blind", {})),
            "field_paths": sum(len(v.get("fields", {})) for v in shapes.values()),
            "contract_violations": _contract_violations(dm)}


def research(now: dt.datetime) -> dict:
    rows = _jsonl(LEDGER)
    with_decision = [r for r in rows if r.get("decision_fed")]
    last = [{"date": r.get("date"), "question": (r.get("question") or "")[:140],
             "decision": (r.get("decision_fed") or "(none)")[:160],
             "metric": f"{r.get('metric_before', '?')} -> {r.get('metric_after', '?')}" if r.get("metric") else ""}
            for r in rows[-3:]]
    return {"entries": len(rows), "with_decision": len(with_decision),
            "first": min((r.get("date") or "" for r in rows), default=""),
            "last_date": max((r.get("date") or "" for r in rows), default=""), "last": last}


def outcomes(now: dt.datetime) -> dict:
    since = (now - dt.timedelta(days=WINDOW_DAYS)).date().isoformat()
    ships = [r for r in _jsonl(SHIPS) if r.get("day", "") >= since]
    # one row per (day, repo); the newest collection wins
    latest: dict[tuple, dict] = {}
    for r in ships:
        latest[(r["day"], r.get("repo"))] = r
    commits = sum(r.get("commits", 0) for r in latest.values())
    att = {r["day"]: r for r in _jsonl(ATTENTION) if r.get("day", "") >= since}
    messages = sum(r.get("messages", 0) for r in att.values())
    complaints = sum(r.get("complaints", 0) for r in att.values())
    spend = None
    if WAREHOUSE.exists():
        db = sqlite3.connect(f"file:{WAREHOUSE}?mode=ro", uri=True)
        per_day: dict[str, float] = {}
        for (payload,) in db.execute("select payload from facts where source='spend' order by at"):
            p = json.loads(payload)
            if p.get("day", "") >= since and isinstance(p.get("total"), (int, float)):
                per_day[p["day"]] = p["total"]        # newest sample of the day wins
        spend = round(sum(per_day.values()), 2)
    return {"window_days": WINDOW_DAYS, "commits": commits, "repos": len({k[1] for k in latest}),
            "messages": messages, "complaints": complaints,
            "complaint_rate": round(100 * complaints / messages, 1) if messages else None,
            "spend_usd": spend,
            "usd_per_commit": round(spend / commits, 2) if spend and commits else None}


def predictions(now: dt.datetime) -> dict:
    latest: dict = {}
    for r in _jsonl(PREDICTIONS):       # append-only; the newest row per id wins
        latest[r.get("id")] = r
    rows = list(latest.values())
    scored = [r for r in rows if r.get("scored_at")]
    hits = [r for r in scored if r.get("correct") is True]
    return {"recorded": len(rows), "scored": len(scored), "hits": len(hits),
            "hit_rate": round(100 * len(hits) / len(scored)) if scored else None}


SECTIONS = [
    ("Capabilities", capabilities, "python3 science/showcase.py  (reads science/*.py, scripts/science-collect, scripts/verify.d, launchd)"),
    ("Warehouse", warehouse, "sqlite3 science/warehouse.db \"select count(*), count(distinct source), max(ingested_at) from facts\""),
    ("Data map (LAW 50)", datamap, "python3 science/datamap.py --check"),
    ("Research ledger", research, "python3 -c \"import json; print(sum(1 for l in open('science/RESEARCH-LEDGER.jsonl')))\""),
    ("Delivery outcomes", outcomes, "python3 science/outcomes.py ship --days 7; python3 science/outcomes.py attention --days 7"),
    ("Predictions", predictions, "python3 science/outcomes.py rate"),
]


def build(now: dt.datetime) -> tuple[dict, dict]:
    data, blind = {}, {}
    for title, fn, _ in SECTIONS:
        try:
            data[title] = fn(now)
        except Blind as e:
            blind[title] = str(e)
    return data, blind


def numbers(data: dict) -> dict[str, float]:
    """The scalars the progress section diffs. Flat, named, and stable across runs."""
    n: dict[str, float] = {}
    w, d, r, o, p = (data.get(k) for k in ("Warehouse", "Data map (LAW 50)", "Research ledger", "Delivery outcomes", "Predictions"))
    if w:
        n.update({"warehouse rows": w["rows"], "warehouse sources": w["sources"], "stale sources": len(w["stale"]),
                  "sources with a contract": w["contracted"]})
    if d:
        n.update({"register entries": d["entries"], "producers discovered": d["producers"],
                  "field paths": d["field_paths"]})
        if isinstance(d["contract_violations"], list):
            n["contract violations"] = len(d["contract_violations"])
    if r:
        n.update({"research entries": r["entries"], "research entries with a decision": r["with_decision"]})
    if o:
        n.update({f"commits, {o['window_days']}d": o["commits"], f"complaints, {o['window_days']}d": o["complaints"]})
        if o["spend_usd"] is not None:
            n[f"spend USD, {o['window_days']}d"] = o["spend_usd"]
        if o["usd_per_commit"] is not None:
            n["USD per commit"] = o["usd_per_commit"]
    if p:
        n.update({"predictions recorded": p["recorded"], "predictions scored": p["scored"]})
    if data.get("Capabilities"):
        rows, _ = data["Capabilities"]
        n["capabilities"] = len(rows)
        n["capabilities scheduled"] = sum(r["scheduled"] != "hand-run" for r in rows)
    return n


def render(now: dt.datetime, data: dict, blind: dict, prev: dict) -> str:
    out = ["# Science lane showcase", "",
           f"Generated {now.strftime('%Y-%m-%dT%H:%MZ')} by `python3 science/showcase.py`. Every number is read at generation",
           "time; the command under each heading reproduces it. A section that cannot see its source says BLIND.", ""]
    cur = numbers(data)
    prev_n = prev.get("numbers", {})
    out += ["## Progress since the previous run", ""]
    if not prev_n:
        out.append("First run: nothing to diff yet.")
    else:
        out.append(f"Previous run: {prev.get('generated', '?')}.")
        out.append("")
        changed = [(k, prev_n.get(k), v) for k, v in cur.items() if k in prev_n and prev_n[k] != v]
        new = [k for k in cur if k not in prev_n]
        if not changed and not new:
            out.append("No number changed.")
        for k, a, b in changed:
            out.append(f"- {k}: {a} -> {b}")
        for k in new:
            out.append(f"- {k}: {cur[k]} (new)")
    out.append("")

    for title, _, cmd in SECTIONS:
        out += [f"## {title}", "", f"`{cmd}`", ""]
        if title in blind:
            out += [f"BLIND: {blind[title]}", ""]
            continue
        d = data[title]
        if title == "Capabilities":
            rows, notes = d
            out += ["| Capability | What it answers | Run | Scheduled by |", "|---|---|---|---|"]
            out += [f"| {r['name']} | {r['what']} | `{r['run']}` | {r['scheduled']} |" for r in rows]
            out += [""] + [f"{n}" for n in notes]
        elif title == "Warehouse":
            out += [f"- {d['rows']:,} rows across {d['sources']} sources; last ingest {d['last_ingest']}",
                    f"- {d['contracted']} of {d['declared']} declared sources carry owner, method, retention and sensitivity",
                    f"- stale past their SLA: {', '.join(d['stale']) if d['stale'] else 'none'}"]
        elif title == "Data map (LAW 50)":
            v = ", ".join(f"{k} {n}" for k, n in sorted(d["verdicts"].items()))
            out += [f"- {d['entries']} register entries ({v}); {d['producers']} producers discovered at the last census",
                    f"- {d['field_paths']} field paths in the last shape walk",
                    f"- domains blind at the last census: {', '.join(d['blind']) if d['blind'] else 'none'}",
                    "- contract violations now: " + (str(len(d["contract_violations"])) if isinstance(d["contract_violations"], list) else d["contract_violations"])]
        elif title == "Research ledger":
            out += [f"- {d['entries']} entries, {d['first']} to {d['last_date']}; {d['with_decision']} record the decision they fed", ""]
            for r in d["last"]:
                out += [f"- **{r['date']}** {r['question']}", f"  - decision: {r['decision']}"]
                if r["metric"]:
                    out.append(f"  - metric: {r['metric']}")
        elif title == "Delivery outcomes":
            out += [f"- last {d['window_days']} days: {d['commits']} commits across {d['repos']} repos",
                    f"- founder messages {d['messages']}, complaints {d['complaints']}"
                    + (f" ({d['complaint_rate']}%)" if d['complaint_rate'] is not None else ""),
                    f"- spend USD {d['spend_usd']}" + (f", USD per commit {d['usd_per_commit']}" if d['usd_per_commit'] is not None else "")
                    if d["spend_usd"] is not None else "- spend: BLIND (warehouse absent)",
                    "- machine learning: none. Nothing here trains a model; every number is a count or a ratio."]
        elif title == "Predictions":
            rate = f"{d['hit_rate']}%" if d["hit_rate"] is not None else "n/a (none scored)"
            out += [f"- {d['recorded']} recorded before a repair, {d['scored']} scored after, hit rate {rate}"]
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--print", action="store_true", dest="dry", help="write nothing, show the page")
    args = ap.parse_args()
    now = dt.datetime.now(dt.UTC).replace(microsecond=0, tzinfo=None)
    data, blind = build(now)
    prev = json.load(STATE.open()) if STATE.exists() else {}
    page = render(now, data, blind, prev)
    if args.dry:
        print(page)
        return 0
    DOCS.mkdir(parents=True, exist_ok=True)
    PAGE.write_text(page)
    STATE.write_text(json.dumps({"generated": now.strftime("%Y-%m-%dT%H:%MZ"), "numbers": numbers(data)}, indent=1) + "\n")
    print(f"wrote {PAGE.relative_to(CREW)}")
    for title, _, _ in SECTIONS:
        print(f"  {title:<20} {'BLIND: ' + blind[title] if title in blind else 'ok'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
