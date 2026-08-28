#!/usr/bin/env python3
"""Every producer of data in the estate, discovered by class rather than typed by hand.

The founder asked, 2026-08-26: "map all the data points in the estate, anything that
produces data and anything that can be measured ... nothing is missed from infra to
platform to agent transcripts to apps and apis to our k8s and internals ... find a way
to automate this so this is the first and last time we ever need to do this and a way
to guarantee you don't miss anything."

A hand-typed list is missing whatever nobody typed. `datamap.py` carried one such list
(WHY_UNCOLLECTED, 18 entries) and it judged only the 38 Mac stores the inventory marked
`collected: False`; the other 279 inventory rows, every cluster workload, every hostname,
every hook, every MCP server and every GitHub workflow had no verdict at all. So the
guarantee here is structural, not diligent:

  1. A DOMAIN is a class of producer and a function that enumerates every member from the
     world itself (the inventory file, the manifests in git, the plists the inventory read, the hook
     table, `gh`). Nobody types a member.
  2. Every member must match an entry in `verdicts.json`. One that does not is UNEXPLAINED,
     and the gate in `datamap.py --check` fails on a single one.
  3. A domain that cannot see its world says BLIND and names why. BLIND fails the gate
     unless the register allows it with a reason (a discoverer that silently returns []
     is the class of failure that dropped 10 criticals in 18 hours with no test failing).
  4. The census (`census.json`) remembers how many members each domain had last run. A
     domain shrinking by more than half without becoming BLIND is also a failure.

The residual, stated (LAW 45 step 5): a class of producer with no domain here is still
invisible. The list of domains is the one thing that stays hand-typed, and it is kept
short enough to read in one screen. Add a domain the moment the estate grows a new kind of
world; do not add a member.

Each producer is a record:

    domain     which world it was found in
    key        stable id, `<domain>/<...>`, the thing verdicts.json matches on
    kind       what sort of thing it is inside the domain
    measures   what can be measured about it, whether or not anything does today
    evidence   where the discoverer saw it (a path, a manifest, a command)
    size       bytes or rows when the discoverer knows them
"""
from __future__ import annotations

import functools
import json
import os
import pathlib
import plistlib
import re
import sqlite3
import subprocess
import sys
from collections.abc import Callable, Iterator

HOME = pathlib.Path.home()
SCIENCE = pathlib.Path(__file__).resolve().parent
CODE = pathlib.Path(os.environ.get("ESTATE_CODE", HOME / "dev" / "code"))
IDP = pathlib.Path(os.environ.get("ESTATE_IDP", CODE / "idp"))
INVENTORY = pathlib.Path(os.environ.get("ESTATE_INVENTORY", HOME / ".estate" / "state" / "inventory.json"))
WAREHOUSE = SCIENCE / "warehouse.db"
CLAUDE_HOME = pathlib.Path(os.environ.get("CLAUDE_CONFIG_DIR", HOME / ".claude"))
OKE_KUBECONFIG = pathlib.Path(os.environ.get("ESTATE_OKE_KUBECONFIG", HOME / ".kube" / "oke-estate"))

#: Directories that hold copies of a repo, never the repo. Walking them reports every
#: manifest N times and hangs a 16 GB Mac (crew, 2026-08-25: load 236).
SKIP_DIRS = {".wt-", ".worktrees", "node_modules", ".git", ".venv", "venv", "__pycache__", ".claude"}

Producer = dict



#: The SKIP_DIRS entries that mark a git worktree. `.claude` is in SKIP_DIRS for the yaml walk
#: inside a repo; here every row lives under ~/.claude, so only the worktree markers apply.
WORKTREE_DIRS = (".wt-", ".worktrees")


@functools.lru_cache(maxsize=4096)
def _is_linked_worktree(dirpath: str) -> bool:
    """True when `dirpath` is the root of a linked git worktree.

    git's own on-disk shape answers this: a primary checkout's `.git` is a directory, a linked
    worktree's `.git` is a regular file holding one `gitdir:` line. Measured 2026-08-28:
    ~/dev/code/crew/.git is a directory, ~/dev/code/crew/.wt-lanes/.git is a 66-byte file,
    ~/.claude/state/crew-science-worktree/.git is a 78-byte file.
    """
    try:
        return (pathlib.Path(dirpath) / ".git").is_file()
    except OSError:
        return False


def _in_worktree(path: str) -> bool:
    """True when `path` sits inside a git worktree: a copy of a producer, never a producer.

    crew#320 (09cd04a6, 2026-08-28): this used to grade the directory NAME against WORKTREE_DIRS,
    and a name is a proxy. `scripts/science-collect:68` (crew#90) keeps a detached worktree at
    ~/.claude/state/crew-science-worktree so the contract check runs main's collect.py; that
    checkout carries the repo's own tracked ledgers, its name starts with neither `.wt-` nor
    `.worktrees`, and the gate went RED with 11 UNEXPLAINED producers that were all second copies
    of registered rows. The name check is kept -- it still catches a worktree whose `.git` has been
    pruned -- and every ancestor is now asked what it actually is.
    """
    return _worktree_root(path) is not None


def _abs(path: str) -> pathlib.Path:
    """The filesystem path behind an inventory value. Keys read `mac/ledger/~/...`."""
    raw = "~/" + path.split("~/")[-1] if "~/" in path else path
    return pathlib.Path(os.path.expanduser(raw))


def _worktree_root(path: str) -> pathlib.Path | None:
    """The worktree directory `path` is a copy inside, or None when `path` is the real thing."""
    segs = path.split("/")[:-1]
    for i, seg in enumerate(segs):
        # `.wt-crew69` IS the worktree; `.worktrees` is a directory OF them, so the root is the
        # segment after it. Getting this wrong rewrites a copy onto a path that does not exist.
        take = i + 2 if seg == ".worktrees" else i + 1
        if any(seg.startswith(s) or seg == s for s in WORKTREE_DIRS) and take <= len(segs):
            return _abs("/".join(segs[:take]))
    here = _abs(path).parent
    for anc in (here, *here.parents):
        if _is_linked_worktree(str(anc)):
            return anc
        if (anc / ".git").is_dir():  # the primary checkout: stop, this path is the real producer
            return None
    return None


@functools.lru_cache(maxsize=4096)
def _primary_checkout(worktree: str) -> str | None:
    """The working tree of the checkout a linked worktree belongs to, asked of git itself."""
    try:
        out = subprocess.run(["git", "-C", worktree, "rev-parse", "--path-format=absolute",
                              "--git-common-dir"], capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    common = pathlib.Path(out.stdout.strip())
    return str(common.parent) if common.name == ".git" and common.parent.is_dir() else None


def _primary_path(path: str) -> str | None:
    """`path` rewritten into the primary checkout, or None when git cannot say where that is.

    crew#556 review (d5ae1960, 2026-08-28): dropping every copy dropped the LAST row for 23 of
    them. Eleven science ledgers -- ships, dora, velocity, revenue, predictions, attention,
    pr-hygiene, ci-runs, RESEARCH-LEDGER, RESEARCH-INTAKE, risk/REGISTER -- exist in the Mac
    inventory ONLY as copies inside `~/.claude/state/crew-{science,snapshot}-worktree`, because
    the inventory walk never reaches `~/dev/code/crew` itself (measured: 2 of its 319 rows are
    under that checkout, both `.db` files). So `continue` did not deduplicate them, it blinded the
    register to them -- the exact failure this module exists to make impossible. Worse, the copies
    are stale: `science/ships.jsonl` reads 57 rows in both worktrees and 150 in the real ledger,
    so every science number reported off ships came off a copy less than half its size.

    A copy therefore resolves to its primary instead of vanishing, and is restated from the file
    that is actually there.
    """
    wt = _worktree_root(path)
    if wt is None:
        return None
    primary = _primary_checkout(str(wt))
    if primary is None:
        return None
    try:
        rel = _abs(path).relative_to(wt)
    except ValueError:
        return None
    resolved = pathlib.Path(primary) / rel
    return str(resolved) if resolved.exists() else None


def _restat(row: dict, path: str) -> dict:
    """`row` with its size read off `path`, so a resolved row never carries the copy's number."""
    out = dict(row)
    f = pathlib.Path(path)
    if not f.is_file():
        return out  # a directory store keeps the size the inventory measured; it walked it, we do not
    if out.get("rows") is not None:
        with f.open("rb") as fh:
            out["rows"] = sum(1 for _ in fh)
    if out.get("mb") is not None:
        out["mb"] = round(f.stat().st_size / 1e6, 3)
    return out


def _dedupe_copies(rows: list[dict]) -> list[dict]:
    """Every inventory row, with each worktree copy resolved onto its primary and deduplicated.

    A copy that resolves onto a path another row already covers is dropped -- that is the
    deduplication crew#320 wanted. A copy that resolves onto a path NOTHING else covers is kept,
    rewritten to the primary and restated.

    A copy git cannot place is the third case, and it is not a drop. `~/Documents/code/prospector/
    .claude/worktrees/agent-aaecfffaa54620133` is a stranded worktree: its `.git` file points into
    an iCloud path that no longer exists, so `git rev-parse` says "not a git repository", and it
    holds 130.9 MB of dossiers that no other row covers. Dropping it makes the register blind to
    130 MB. So an unplaceable copy is dropped only when some other row already covers the same
    repo-relative file, and kept and marked otherwise.
    """
    def where(r: dict) -> str:
        return str(r.get("path") or r.get("plist") or r.get("id") or r.get("name") or "")

    def tail(p: str) -> str:
        """`p` relative to the worktree it sits in: the repo-relative file two copies share."""
        wt = _worktree_root(p)
        try:
            return str(_abs(p).relative_to(wt)) if wt else str(_abs(p))
        except ValueError:
            return str(_abs(p))

    real = [r for r in rows if where(r) and not _in_worktree(where(r))]
    covered = {str(_abs(where(r))) for r in real}

    def elsewhere(t: str) -> bool:
        """True when some row outside a worktree already holds this repo-relative file. A row
        outside a worktree has no repo root to be relative to, so the suffix is the comparison."""
        return any(c == t or c.endswith("/" + t) for c in covered)

    out, promoted = list(real), set()
    for r in rows:
        p = where(r)
        if not p or not _in_worktree(p):
            continue
        primary = _primary_path(p)
        if primary is None:
            # git cannot place it. Drop only when the file is already covered somewhere else.
            t = tail(p)
            if elsewhere(t) or t in promoted:
                continue
            promoted.add(t)
            out.append({**r, "stranded_copy": True})
            continue
        if primary in covered or primary in promoted:
            continue
        promoted.add(primary)
        promoted.add(tail(p))
        out.append({**_restat(r, primary), "path": primary, "resolved_from": p})
    return out

def _p(domain: str, key: str, kind: str, measures: list[str], evidence: str,
       size: float | int | None = None) -> Producer:
    return {"domain": domain, "key": f"{domain}/{key}", "kind": kind,
            "measures": measures, "evidence": evidence, "size": size}


def _walk_yaml(root: pathlib.Path) -> Iterator[pathlib.Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not any(d.startswith(s) or d == s for s in SKIP_DIRS)]
        for f in filenames:
            if f.endswith((".yaml", ".yml")):
                yield pathlib.Path(dirpath) / f


# ---------------------------------------------------------------- domains

#: What each kind of Mac inventory row can be measured on. The inventory itself is the
#: discoverer (`~/.estate/scripts/inventory.py`, launchd `com.estate.inventory`); this is
#: the measurables vocabulary, which is the half the founder asked for and the half the
#: inventory does not carry.
MAC_MEASURES = {
    "ledger": ["rows", "bytes", "hours_since_last_write", "rows_per_day", "field_shape_drift"],
    "data": ["bytes", "hours_since_last_write", "tables", "rows_per_table"],
    "scheduled_job": ["last_exit_status", "run_duration_s", "runs_per_day", "hours_since_last_run",
                      "stdout_bytes", "stderr_bytes", "loaded"],
    "guard": ["invocations", "refusals", "false_refusals", "latency_ms"],
    "listener": ["events_received", "events_dropped", "hours_since_last_event"],
    "repo": ["commits_no_remote_holds", "dirty_files", "oldest_stranded_commit_days",
             "open_prs", "ci_pass_rate", "hours_since_last_push"],
    "drill": ["last_run_at", "last_verdict", "run_duration_s", "runs_per_week"],
}


SCHEDULE_YML = pathlib.Path(os.environ.get("ESTATE_SCHEDULE_YML", IDP / "scheduler" / "schedule.yml"))


def _dagster_jobs() -> set[str]:
    """Labels Dagster runs from schedule.yml; it writes exit status and duration per run (dagster-runs)."""
    try:
        import yaml
        return set((yaml.safe_load(SCHEDULE_YML.read_text()) or {}).get("jobs") or {})
    except Exception:  # noqa: BLE001  (no idp checkout, no yaml: nothing is monitored by Dagster)
        return set()


def _monitored(plist: str | None, label: str | None = None) -> bool:
    # crew#373: a job Dagster schedules is monitored by the run store (last_exit_status,
    # run_duration_s per run, collected as dagster-runs since crew#376), hc-wrap or not.
    if label and label in _dagster_jobs():
        return True
    if not plist or not pathlib.Path(plist).exists():
        return False
    try:
        with open(plist, "rb") as fh:
            x = plistlib.load(fh)
    except Exception:  # noqa: BLE001
        return False
    return any("hc-wrap" in str(a) for a in (x.get("ProgramArguments") or [x.get("Program") or ""]))


def _sources_decision(row: dict) -> dict | None:
    """The verdict science/sources.json already holds for an inventory row, or None."""
    try:
        import collect
    except ImportError:
        sys.path.insert(0, str(SCIENCE))
        import collect
    rid = row.get("id")
    path = pathlib.Path(row.get("path") or "")
    if rid in collect.DECLINED:
        return {"verdict": "DECLINED", "why": collect.DECLINED[rid], "entry": f"sources.json declined {rid}"}
    for did, d in collect.DECLINED_DIRS.items():
        # crew#320: a decline may name one file (consult.jsonl) as well as a directory. The
        # inventory ids a file by its relative path, not the decline's id, so the path is
        # the only thing the two have in common.
        if path and (path == d or str(path).startswith(str(d) + "/")):
            return {"verdict": "DECLINED", "why": collect.DECLINED[did], "entry": f"sources.json declined {did}"}
    for name, (src, _k, _t) in collect.SOURCES.items():
        if not path:
            break
        if path == src:
            return {"verdict": "COLLECTED", "reader": f"science/collect.py source {name}", "entry": f"sources.json source {name}"}
        # crew#556: a source is identified by its path INSIDE the repo, not by which checkout the
        # inventory happened to walk. The 11 crew ledgers reach the Mac inventory only through the
        # science/snapshot worktrees, and `_dedupe_copies` resolves them onto ~/dev/code/crew --
        # a different absolute path from the `src` collect.py computes from its own __file__.
        try:
            rel = src.relative_to(SCIENCE.parent)
        except ValueError:
            continue
        if str(path).endswith("/" + str(rel)):
            return {"verdict": "COLLECTED", "reader": f"science/collect.py source {name}",
                    "entry": f"sources.json source {name} (matched on the repo-relative path {rel})"}
    return None


@functools.lru_cache(maxsize=1)
def _ledger_hooks() -> frozenset[str]:
    """Every hook name the hook-outcomes ledger has recorded a run for. crew#374 (2026-08-27):
    `mac/guard/*` was graded NEVER_EMITTED as one block while 19 of its 46 members were the
    settings hooks `hook-run.py` already writes to the ledger (source `hook_outcomes`). The
    ledger is the measurement; a guard it has rows for is COLLECTED, whatever the register says.
    Path: $HOOK_OUTCOMES (what hook-run.py honours) or the `hook_outcomes` source."""
    try:
        import collect
    except ImportError:
        sys.path.insert(0, str(SCIENCE))
        import collect
    path = pathlib.Path(os.environ.get("HOOK_OUTCOMES") or collect.SOURCES["hook_outcomes"][0])
    names = set()
    try:
        with path.open() as fh:
            for line in fh:
                try:
                    names.add(json.loads(line)["hook"])
                except (ValueError, KeyError, TypeError):
                    continue
    except FileNotFoundError:
        # No ledger at all: hook-run.py has never written one here, so no guard has a
        # measured run and the register's verdict stands. That is an honest empty.
        return frozenset()
    except OSError as e:
        # A ledger that exists and cannot be read is not an empty ledger. Returning
        # frozenset() here graded all 46 guards NEVER_EMITTED with no signal (crew#453
        # residual, 2026-08-27); raising makes the mac domain BLIND, which the gate fails.
        raise RuntimeError(f"hook-outcomes ledger unreadable at {path}: {type(e).__name__}: {e}") from e
    return frozenset(names)


def _listener_class(row: dict) -> str:
    """forward | system | app, from the inventory row alone. crew#375 (2026-08-27): `mac/listener/*`
    was one NEVER_EMITTED block over 32 rows that are three different things. A `ssh:` forward is a
    transport whose workload is a container in the colima VM (crew#458), not the port. A macOS or
    VM-host daemon (ControlCenter, rapportd, limactl, a desktop .app) is not an estate workload.
    Everything else is an estate process that owns the port and can be asked what it received."""
    path = str(row.get("path") or "")
    proc = str(row.get("process") or "")
    if path == "ssh:" or proc == "ssh":
        return "forward"
    if proc == "ollama":  # Ollama.app ships under /Applications but is an estate model server (crew#460 review)
        return "app"
    if path.startswith(("/System/", "/usr/libexec/", "/Applications/")) or proc in ("limactl", "rapportd", "ControlCenter"):
        return "system"
    return "app"


def mac() -> list[Producer]:
    """Every row the Mac inventory found: ledgers, stores, jobs, guards, listeners, repos, drills."""
    doc = json.load(INVENTORY.open())
    out = []
    for r in _dedupe_copies(doc.get("rows", [])):
        kind = r.get("kind") or "unknown"
        ident = r.get("id") or r.get("path") or r.get("name")
        if not ident:
            continue
        # Stores are named by path (two experience_graph.db files are two producers);
        # jobs, guards, listeners and drills by the id the inventory gave them.
        if kind in ("ledger", "data") and r.get("path"):
            ident = r["path"]
        # `_dedupe_copies` has already resolved every worktree copy onto its primary and dropped
        # the duplicates. A row still reading as a copy here is one git could not place AND that
        # nothing else covers: it is the only record of that data, so it stays a producer.
        if _in_worktree(str(r.get("path") or r.get("plist") or ident)) and not r.get("stranded_copy"):
            continue
        if r.get("resolved_from") and kind in ("ledger", "data") and r.get("path"):
            ident = r["path"]
        ident = str(ident).replace(str(HOME) + "/", "~/")
        size = r.get("mb") or r.get("rows")
        # A scheduled job under hc-wrap pings a dead-man monitor; one without it can stop
        # and nothing says so. That is a different kind of producer, not a note.
        if kind == "scheduled_job":
            kind = "scheduled_job:" + ("monitored" if _monitored(r.get("plist"), r.get("id")) else "unmonitored")
        if kind == "listener":
            kind = "listener:" + _listener_class(r)
        prod = _p("mac", f"{kind.split(':')[0]}/{ident}", kind, MAC_MEASURES.get(kind.split(':')[0], ["exists"]),
                  r.get("plist") or r.get("path") or str(INVENTORY), size)
        # The inventory already knows which stores collect.py reads; that is a measured
        # verdict, and the register must not be asked to retype it.
        if r.get("collected") is True or r.get("member_of"):
            prod["auto"] = {"verdict": "COLLECTED",
                            "reader": f"science/collect.py source {r.get('member_of') or r.get('source') or r.get('id')}"}
        # science/sources.json is the one register of stores collect.py reads or declines
        # (crew#253). A decline recorded there is a verdict, and it outranks verdicts.json so
        # the same store is never decided in two files.
        decided = _sources_decision(r)
        # A guard the hook-outcomes ledger has rows for is measured (crew#374); the ledger,
        # not the register, decides it, the same way sources.json decides a store.
        if not decided and kind == "guard" and r.get("id") in _ledger_hooks():
            decided = {"verdict": "COLLECTED", "reader": "science/collect.py source hook_outcomes",
                       "entry": "hook-outcomes ledger has rows for this hook (crew#374)"}
        if decided:
            prod["decided"] = decided
        out.append(prod)
        # A store that is a database is many producers: one per table.
        path = r.get("path") or ""
        if kind == "data" and path.endswith((".db", ".sqlite", ".sqlite3")) and pathlib.Path(path).exists():
            try:
                db = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
                for (t,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'"):
                    out.append(_p("mac", f"table/{ident}/{t}", "table",
                                  ["rows", "rows_per_day", "field_shape_drift"], path))
                db.close()
            except sqlite3.Error as e:
                out.append(_p("mac", f"table/{ident}/UNREADABLE", "table", [], f"{path}: {e}"))
    return out


def warehouse() -> list[Producer]:
    """Every table and every fact source in the science warehouse."""
    if not WAREHOUSE.exists():
        raise FileNotFoundError(f"no warehouse at {WAREHOUSE}")
    db = sqlite3.connect(f"file:{WAREHOUSE}?mode=ro", uri=True)
    out = []
    for (t,) in db.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')"):
        (n,) = db.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()
        out.append(_p("warehouse", f"table/{t}", "table", ["rows", "rows_per_day", "field_shape_drift"],
                      str(WAREHOUSE), n))
    if db.execute("SELECT 1 FROM sqlite_master WHERE name='facts'").fetchone():
        for src, n in db.execute("SELECT source, COUNT(*) FROM facts GROUP BY 1"):
            out.append(_p("warehouse", f"source/{src}", "source",
                          ["rows", "hours_since_last_write", "field_shape_drift", "coverage_per_field"],
                          f"{WAREHOUSE}#facts", n))
    db.close()
    return out


#: Cluster kinds and what each can be measured on. Anything declared in git under these
#: kinds is a producer whether or not the cluster is reachable to read it.
CLUSTER_MEASURES = {
    "Deployment": ["replicas_ready", "restarts", "cpu", "memory", "image_age_days", "rollout_duration_s"],
    "StatefulSet": ["replicas_ready", "restarts", "cpu", "memory", "pvc_used_bytes"],
    "DaemonSet": ["nodes_ready", "restarts", "cpu", "memory"],
    "Job": ["last_completion", "duration_s", "failures"],
    "CronJob": ["last_run_at", "duration_s", "failures", "missed_schedules"],
    "HelmRelease": ["ready", "revision", "hours_since_last_reconcile", "reconcile_failures"],
    "Kustomization": ["ready", "revision", "hours_since_last_reconcile", "reconcile_failures"],
    "GitRepository": ["ready", "revision", "hours_since_last_fetch"],
    "Service": ["endpoints_ready", "requests_per_s", "p50_latency_ms", "error_rate"],
    "HTTPRoute": ["requests_per_s", "status_5xx_rate", "p95_latency_ms"],
    "Gateway": ["listeners_ready", "tls_days_left"],
    "Certificate": ["ready", "days_to_expiry", "renewals"],
    "PersistentVolumeClaim": ["capacity_bytes", "used_bytes", "bound"],
    "ExternalSecret": ["synced", "hours_since_last_sync", "sync_failures"],
    "ClusterPolicy": ["admissions_blocked", "admissions_audited", "policy_ready"],
    "PolicyException": ["matches"],
    "Alert": ["fired", "delivered"],
    "Provider": ["ready", "deliveries_failed"],
    "Secret": ["age_days", "rotations"],
    "ConfigMap": ["age_days", "revisions"],
    "Namespace": ["pods", "cpu", "memory"],
}


def cluster() -> list[Producer]:
    """Every workload, route, policy and store the platform declares in git (idp)."""
    if not IDP.exists():
        raise FileNotFoundError(f"no idp checkout at {IDP}")
    import yaml  # PyYAML is in crew's requirements-dev
    out, seen = [], set()
    for f in list(_walk_yaml(IDP / "clusters")) + list(_walk_yaml(IDP / "platform")):
        try:
            docs = list(yaml.safe_load_all(f.read_text()))
        except Exception as e:  # noqa: BLE001 - a broken manifest is a producer we must name
            out.append(_p("cluster", f"UNPARSEABLE/{f.relative_to(IDP)}", "manifest", [], f"{f}: {e}"))
            continue
        for d in docs:
            if not isinstance(d, dict) or "kind" not in d or not isinstance(d.get("metadata"), dict):
                continue
            kind = d["kind"]
            if kind not in CLUSTER_MEASURES:
                continue
            ns = d["metadata"].get("namespace") or "-"
            name = d["metadata"].get("name") or "-"
            key = f"{ns}/{kind}/{name}"
            if key in seen:
                continue
            seen.add(key)
            out.append(_p("cluster", key, kind, CLUSTER_MEASURES[kind], str(f.relative_to(IDP))))
            # Each container port is a scrape target or an API surface in its own right.
            spec = (d.get("spec") or {})
            tmpl = ((spec.get("template") or {}).get("spec") or {}) if isinstance(spec, dict) else {}
            for c in tmpl.get("containers") or []:
                for port in c.get("ports") or []:
                    pn = port.get("containerPort")
                    if pn:
                        out.append(_p("cluster", f"{key}/port/{pn}", "port",
                                      ["listening", "requests_per_s", "scraped"],
                                      str(f.relative_to(IDP))))
    return out


def cluster_live() -> list[Producer]:
    """What the cluster is actually running, read through the OKE kubeconfig."""
    if not OKE_KUBECONFIG.exists():
        raise FileNotFoundError(f"no kubeconfig at {OKE_KUBECONFIG}")
    r = subprocess.run(["kubectl", "--kubeconfig", str(OKE_KUBECONFIG), "--request-timeout=15s",
                        "get", "deploy,sts,ds,cronjob,svc,pvc,helmrelease", "-A", "-o", "json"],
                       capture_output=True, text=True, timeout=40, check=False)
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout).strip().splitlines()[-1][:200])
    out = []
    for item in json.loads(r.stdout).get("items", []):
        kind = item["kind"]
        md = item["metadata"]
        out.append(_p("cluster_live", f"{md.get('namespace','-')}/{kind}/{md['name']}", kind,
                      CLUSTER_MEASURES.get(kind, ["exists"]), "kubectl get -A"))
    return out


HOST_RE = re.compile(r"\b[a-z0-9][a-z0-9.-]*\.(?:mumchimp\.com|fly\.dev|onrender\.com)\b")
#: Routes name hosts as `hostnames:` list items, sometimes through a `${ESTATE_ZONE}`-style
#: substitution Flux resolves at apply time; the unresolved form is still a producer.
HOSTLIST_RE = re.compile(r"^\s*-\s*[\"']?([a-z0-9][A-Za-z0-9.${}_-]*\.[A-Za-z0-9${}_.-]+)[\"']?\s*$", re.M)
ZONE_RE = re.compile(r"ESTATE_ZONE[\"']?\s*[:=]\s*[\"']?([a-z0-9.-]+\.[a-z]{2,})")


def endpoints() -> list[Producer]:
    """Every public hostname the platform manifests name."""
    if not IDP.exists():
        raise FileNotFoundError(f"no idp checkout at {IDP}")
    hosts, zone = set(), os.environ.get("ESTATE_ZONE", "")
    texts = [f.read_text(errors="replace") for f in list(_walk_yaml(IDP / "clusters")) + list(_walk_yaml(IDP / "platform"))]
    for text in texts:
        zone = zone or next(iter(ZONE_RE.findall(text)), "")
    for text in texts:
        hosts.update(HOST_RE.findall(text))
        for m in re.finditer(r"^\s*hostnames:\s*\n((?:\s*-\s*.*\n)+)", text, re.M):
            hosts.update(HOSTLIST_RE.findall(m.group(1)))
    if zone:
        hosts = {h.replace("${ESTATE_ZONE}", zone) for h in hosts}
    return [_p("endpoint", h, "hostname",
               ["http_status", "tls_days_left", "dns_resolves", "p95_latency_ms", "uptime_pct"],
               "clusters/ + platform/ manifests") for h in sorted(hosts)]


def hooks() -> list[Producer]:
    """Every hook command Claude Code runs; each one is a decision the estate makes and forgets."""
    settings = json.load((CLAUDE_HOME / "settings.json").open())
    out = []
    for event, entries in (settings.get("hooks") or {}).items():
        for entry in entries:
            for h in entry.get("hooks", []):
                cmd = h.get("command", "")
                script = next((t for t in cmd.split() if t.endswith((".py", ".sh"))), cmd[:60])
                out.append(_p("hook", f"{event}/{pathlib.Path(script).name}", event,
                              ["invocations", "refusals", "false_refusals", "latency_ms", "exit_codes"],
                              f"{CLAUDE_HOME / 'settings.json'}#hooks.{event}"))
    return out


def mcp() -> list[Producer]:
    """Every MCP server sessions can call; each call is a tool use nothing records."""
    cfg = json.load((HOME / ".claude.json").open())
    return [_p("mcp", name, "server", ["calls", "errors", "latency_ms", "tokens_returned"], "~/.claude.json")
            for name in (cfg.get("mcpServers") or {})]


def github() -> list[Producer]:
    """Every repo the account owns, and every workflow in the local checkouts."""
    r = subprocess.run(["gh", "repo", "list", "chidionyema", "--limit", "300", "--no-archived",
                        "--json", "name,isPrivate,pushedAt"], capture_output=True, text=True, timeout=60, check=False)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:200])
    out = []
    for repo in json.loads(r.stdout):
        out.append(_p("github", f"repo/{repo['name']}", "repo",
                      ["open_issues", "open_prs", "pr_age_days", "merged_prs_7d", "actions_pass_rate",
                       "hours_since_last_push", "stranded_commits"], "gh repo list"))
    for wf_dir in sorted(CODE.glob("*/.github/workflows")):
        repo = wf_dir.parents[1].name
        if repo.startswith("."):
            continue
        for wf in sorted(wf_dir.glob("*.y*ml")):
            text = wf.read_text(errors="replace")
            kind = "scheduled" if re.search(r"^\s*schedule:", text, re.M) else "triggered"
            out.append(_p("github", f"workflow/{repo}/{wf.name}", kind,
                          ["runs_per_day", "run_duration_s", "pass_rate", "queue_wait_s", "cost_minutes"],
                          str(wf.relative_to(CODE))))
    return out


def transcripts() -> list[Producer]:
    """Every project's session transcripts: the largest unread asset the estate owns (crew#319)."""
    root = CLAUDE_HOME / "projects"
    if not root.exists():
        raise FileNotFoundError(f"no transcripts at {root}")
    out = []
    for proj in sorted(p for p in root.iterdir() if p.is_dir()):
        n = 0
        size = 0
        with os.scandir(proj) as it:
            for e in it:
                if e.name.endswith(".jsonl"):
                    n += 1
                    size += e.stat().st_size
        if n == 0:
            continue
        out.append(_p("transcript", proj.name, "project",
                      ["sessions", "bytes", "tool_calls", "tool_failures", "tokens_in", "tokens_out",
                       "cost_usd", "founder_messages", "compactions", "hours_since_last_session"],
                      str(proj), round(size / 1e6, 1)))
    return out


def acts() -> list[Producer]:
    """Things the estate does that leave no file. There is no world to enumerate, so the
    register's own `act/*` entries are the members; this domain exists so they are graded
    by the same gate and so each one must carry a ticket."""
    reg = json.load((SCIENCE / "verdicts.json").open())
    return [_p("act", e["key"].split("/", 1)[1], "act", e.get("measures", []), "verdicts.json")
            for e in reg["entries"] if e["key"].startswith("act/")]


DOMAINS: dict[str, Callable[[], list[Producer]]] = {
    "mac": mac,
    "warehouse": warehouse,
    "cluster": cluster,
    "cluster_live": cluster_live,
    "endpoint": endpoints,
    "hook": hooks,
    "mcp": mcp,
    "github": github,
    "transcript": transcripts,
    "act": acts,
}


def discover(only: set[str] | None = None) -> tuple[list[Producer], dict[str, str]]:
    """Run every domain. Returns (producers, blind) where blind maps a domain that could
    not see its world to the reason, verbatim. A domain never returns a partial answer
    silently: it returns members or it raises, and raising is what makes it BLIND."""
    producers: list[Producer] = []
    blind: dict[str, str] = {}
    for name, fn in DOMAINS.items():
        if only and name not in only:
            continue
        try:
            producers.extend(fn())
        except Exception as e:  # noqa: BLE001 - the reason is the receipt
            blind[name] = f"{type(e).__name__}: {e}"[:200]
    return producers, blind


if __name__ == "__main__":
    ps, bl = discover()
    import collections
    for d, n in sorted(collections.Counter(p["domain"] for p in ps).items()):
        print(f"{d:<14}{n:>6}")
    for d, why in bl.items():
        print(f"{d:<14} BLIND  {why}")
