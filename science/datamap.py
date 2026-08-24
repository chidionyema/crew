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
import json
import pathlib
import sqlite3
import sys

SCIENCE = pathlib.Path(__file__).resolve().parent
WAREHOUSE = SCIENCE / "warehouse.db"
INVENTORY = pathlib.Path.home() / ".estate" / "state" / "inventory.json"
SHAPES = SCIENCE / "shapes.json"

#: Why each known store is not in the warehouse. The path is a substring match against
#: the inventory's own path, so a store that moves still matches on its distinctive tail.
#:
#: Every row here was measured on 2026-08-24 and carries the reason a human gave. A store
#: found by the inventory and absent from this table is reported as UNEXPLAINED, which is
#: the finding worth the most: it is a store nobody has decided about.
WHY_UNCOLLECTED: dict[str, tuple[str, str]] = {
    ".claude/projects": (
        "WIRED_NEVER",
        "76k session transcripts, 6.5 GB. Every tool call, every result, every word he "
        "typed. Only per-day spend is extracted. This is the largest unread asset the "
        "estate owns and the one that would answer most questions about how agents work.",
    ),
    ".claude/telemetry": (
        "EXCLUDED",
        "1.2 GB of the CLI's own failed telemetry uploads. Not our data, not our schema, "
        "and it grows without bound. The correct action is deletion and a size guard, "
        "not ingestion.",
    ),
    "prospector/.claude/worktrees": (
        "WIRED_NEVER",
        "2,330 scored candidate dossiers, 131 MB, stranded in an abandoned agent "
        "worktree. Every vetting decision the estate has ever made is in here and the "
        "live store beside it holds zero files.",
    ),
    ".claude/state/toolguard": (
        "WIRED_NEVER",
        "28.5 MB, one file per tool decision. The `toolguard` source in the warehouse "
        "carries counters only, so which tool call was refused and why is not queryable.",
    ),
    ".maestro/intents": (
        "WIRED_NEVER",
        "One file per sensing cycle. What maestro noticed is recorded; whether it was "
        "right is not, because nothing joins an intent to what happened next.",
    ),
    "experience_graph.db": (
        "WIRED_NEVER",
        "The skills maestro can heal with. Read live by maestro, never sampled into a "
        "series, so 'is the experience graph growing' has no answer.",
    ),
    "state/coord/jobs.sqlite": (
        "WIRED_NEVER",
        "Job coordination state. Small, and the timeline files beside it are the part "
        "worth having.",
    ),
    ".claude/directives": (
        "WIRED_NEVER",
        "6,932 of his prompts. Now collected in DERIVED form as the daily `attention` "
        "counts, which is a count of his messages and not the messages. The text itself "
        "is still unqueryable.",
    ),
    "state/prompt-ledger": (
        "WIRED_NEVER",
        "7,046 rows recording the same prompts as `directives`, in a second format, with "
        "an open/closed state the other one lacks. Two ledgers of one thing (LAW 39).",
    ),
    ".claude/history.jsonl": (
        "WIRED_NEVER",
        "12,928 rows, the largest single-file ledger on the machine and the only one "
        "spanning every project. Nothing reads it.",
    ),
    "state/tickets": (
        "WIRED_NEVER",
        "11 local tickets that do not join to the 26 GitHub issues. The duplication is "
        "the finding; collecting it is how the duplication becomes visible.",
    ),
    "jobs/": (
        "WIRED_NEVER",
        "Six per-job timeline files, 316 rows. No code refers to any of them, so these "
        "are the clearest deletion candidates on the machine.",
    ),
    "estate-board.jsonl": (
        "WIRED_NEVER",
        "The peer channel under `.estate`. A second copy of the board already collected "
        "from `~/.claude`, and no code refers to this one.",
    ),
    "estate-push.j": ("WIRED_NEVER", "Push receipts. Superseded by the `bundle_push` source."),
    "estate-worktr": ("WIRED_NEVER", "Worktree cleanup receipts, 2 rows."),
    "founder-actio": ("WIRED_NEVER", "One row. The mechanism was replaced by the prompt ledger."),
    "prospector/store": (
        "WIRED_NEVER",
        "The live dossier store, and it holds zero files. Listed so the emptiness is a "
        "row rather than an absence.",
    ),
    "knowledge/maestro": ("WIRED_NEVER", "A second copy of the experience graph, under `.estate`."),
}

#: Things the estate DOES and does not record at all. There is no file to point at, which
#: is exactly why these never appear in an inventory of files and never get fixed. Each
#: one is an act performed many times a day whose outcome vanishes the moment it happens.
NEVER_EMITTED: list[tuple[str, str, str]] = [
    ("revenue", "money coming in",
     "2 rows in 5,548 mention revenue. Every efficiency number is a cost over nothing."),
    ("agent_decisions", "what an agent chose, and what it rejected",
     "The transcripts hold the reasoning and nothing extracts it. The `decisions` source "
     "was built for this and its writer has been dead 55 hours."),
    ("research", "what was researched, and what changed because of it",
     "RESEARCH-LEDGER.jsonl has 8 entries, all hand-written by an agent that remembered, "
     "and 0 of 8 record the decision the research fed. LAW 35 has no mechanism."),
    ("task_outcome", "did the thing an agent built actually work",
     "Commits and PRs are counted. Whether the change held, was reverted, or broke "
     "something is not, so there is no denominator for quality."),
    ("run_duration", "how long each scheduled job takes",
     "launchd runs 43 jobs and records exit codes in log files. No series of durations "
     "exists, so 'is anything getting slower' is unanswerable."),
    ("guard_outcome", "what a guard refused, and whether the refusal was correct",
     "LAW 38 grades a guard by whether it allows correct work. Refusals are counted; "
     "false refusals are not recorded at all, so the law cannot be measured."),
    ("model_routing", "which model served each call, and what it cost",
     "`spend` records dollars per owner per day. Cost per model, per task type and per "
     "outcome is in the transcripts and is not extracted."),
    ("context_waste", "tokens spent re-reading context that did not change",
     "`method_metrics` computes output tokens per call for one project, once. It is a "
     "single row, generated by hand, not a series."),
]


def sh_fields(rows: list[dict]) -> tuple[collections.Counter, dict[str, str]]:
    """Walk every row and return each leaf field path, how often it appeared, and its type.

    Nested dicts become dotted paths. Lists are leaves: their contents vary row to row and
    counting inside them produces a field list that grows with the data rather than with
    the schema.
    """
    keys: collections.Counter = collections.Counter()
    types: dict[str, str] = {}

    def walk(obj: object, prefix: str = "") -> None:
        if not isinstance(obj, dict):
            return
        for k, v in obj.items():
            path = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
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


def uncollected() -> list[dict]:
    if not INVENTORY.exists():
        return []
    rows = json.load(INVENTORY.open()).get("rows", [])
    out = []
    for r in rows:
        if r.get("collected") is not False or r.get("member_of"):
            continue
        path = r.get("path") or r.get("name") or ""
        reason, why = "UNEXPLAINED", "No decision has been recorded about this store."
        for frag, (rsn, txt) in WHY_UNCOLLECTED.items():
            if frag in path:
                reason, why = rsn, txt
                break
        out.append({
            "path": path,
            "kind": r.get("kind"),
            "mb": r.get("mb"),
            "rows": r.get("rows"),
            "reason": reason,
            "why": why,
            "referenced_by_code": bool(r.get("referenced")),
        })
    return sorted(out, key=lambda r: (r["reason"], -(r.get("mb") or 0)))


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
                    help="exit 1 if any source changed shape since the last run")
    args = ap.parse_args()

    col = collected()
    unc = uncollected()
    changes = drift(col)

    if args.json:
        json.dump({"collected": col, "uncollected": unc,
                   "never_emitted": [{"id": a, "what": b, "why": c} for a, b, c in NEVER_EMITTED],
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
        print(f"UNCOLLECTED  {len(unc)} stores that exist and nothing reads")
        print("-" * 78)
        for r in unc:
            if r.get("mb"):
                size = f"{r['mb']:.1f} MB"
            elif r.get("rows") is not None:
                size = f"{r['rows']} rows"
            else:
                size = "unsized"
            # Two stores can share a basename and mean different things: there is an
            # experience_graph.db under .maestro and another under a stale worktree, and
            # printing both as "experience_graph.db" reads as the same row twice. Show
            # the parent as well, trimmed from the left so the distinguishing end
            # survives rather than the shared "/Users/chidionyema" head.
            label = r["path"].replace(str(pathlib.Path.home()) + "/", "~/")
            print(f"  {r['reason']:<14} {label[-44:]:<44} {size:>10}")

        print()
        print(f"NEVER EMITTED  {len(NEVER_EMITTED)} things the estate does and does not record")
        print("-" * 78)
        for name, what, why in NEVER_EMITTED:
            print(f"  {name:<16} {what}")

        if changes:
            print()
            print("SHAPE CHANGED SINCE LAST RUN")
            print("-" * 78)
            for m in changes:
                print(f"  {m}")

    SHAPES.write_text(json.dumps(col, indent=1))
    return 1 if (args.check and changes) else 0


if __name__ == "__main__":
    sys.exit(main())
