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

import datetime
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

#: The cluster's own state receipt, and the door that reaches it from a machine with no OCI
#: identity. A CronJob in the cluster (idp platform/state/cluster-state.yaml) writes the receipt
#: to Object Storage every 15 minutes from the node's instance principal; `bin/idp-cluster-state
#: --json` reads it in the oke-check workflow and prints the body into the job log. A GitHub token
#: is the only credential needed to read that log, so this works from any machine, and from CI.
IDP_REPO = os.environ.get("ESTATE_IDP_REPO", "chidionyema/idp")
CLUSTER_RECEIPT_WORKFLOW = os.environ.get("ESTATE_CLUSTER_RECEIPT_WORKFLOW", "oke-check.yml")
CLUSTER_RECEIPT_JOB = os.environ.get("ESTATE_CLUSTER_RECEIPT_JOB", "cluster-state")
#: The receipt is written every 15 min and oke-check runs daily plus on dispatch, so the freshest
#: readable receipt is usually hours old, not minutes. Past this it is not what the cluster is
#: running now and the domain says so rather than reporting a stale world as live.
CLUSTER_RECEIPT_MAX_AGE_H = float(os.environ.get("ESTATE_CLUSTER_RECEIPT_MAX_AGE_H", "36"))
#: `--json` prints the body on the flux-FAIL path and on the ok path, but a run that failed for a
#: different reason (a short DaemonSet, no monitoring rules, a stale receipt) exits before it. So
#: several runs are tried, newest first, rather than assuming the newest one carries a body.
CLUSTER_RECEIPT_RUNS = int(os.environ.get("ESTATE_CLUSTER_RECEIPT_RUNS", "8"))

#: Directories that hold copies of a repo, never the repo. Walking them reports every
#: manifest N times and hangs a 16 GB Mac (crew, 2026-08-25: load 236).
SKIP_DIRS = {".wt-", ".worktrees", "node_modules", ".git", ".venv", "venv", "__pycache__", ".claude"}

Producer = dict



#: The SKIP_DIRS entries that mark a git worktree by name. `.claude` is in SKIP_DIRS for the yaml
#: walk inside a repo; here every row lives under ~/.claude, so only the worktree markers apply.
#: These are a fast path for a path that no longer exists on disk -- the name is not the test.
WORKTREE_DIRS = (".wt-", ".worktrees")


@functools.lru_cache(maxsize=4096)
def _is_worktree_root(d: str) -> bool:
    """True when `d` is a git worktree: git writes `.git` as a FILE there (`gitdir: ...`), and as
    a directory in a normal checkout. Asking the filesystem is the test; the name is a proxy."""
    g = pathlib.Path(d) / ".git"
    try:
        return g.is_file()
    except OSError:
        return False


def _in_worktree(path: str) -> bool:
    """True when `path` sits inside a git worktree, so its rows are a second copy of a repo's
    files and not producers of their own.

    crew#320 skipped `.wt-*` and `.worktrees` by name and the gate went GREEN. crew#558,
    2026-08-28: 11 producers came back UNEXPLAINED from
    `~/.claude/state/crew-science-worktree` -- a worktree `scripts/science-collect` creates on
    every run, named nothing like the pattern. A name-matched skip grades the name; this one
    grades the thing.
    """
    segs = path.split("/")[:-1]
    if any(any(seg.startswith(s) or seg == s for s in WORKTREE_DIRS) for seg in segs):
        return True
    for i in range(len(segs), 1, -1):
        if _is_worktree_root("/".join(segs[:i])):
            return True
    return False

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
        if path and path == src:
            return {"verdict": "COLLECTED", "reader": f"science/collect.py source {name}", "entry": f"sources.json source {name}"}
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
    for r in doc.get("rows", []):
        kind = r.get("kind") or "unknown"
        ident = r.get("id") or r.get("path") or r.get("name")
        if not ident:
            continue
        # Stores are named by path (two experience_graph.db files are two producers);
        # jobs, guards, listeners and drills by the id the inventory gave them.
        if kind in ("ledger", "data") and r.get("path"):
            ident = r["path"]
        # A file inside a git worktree is a copy of a producer, never a producer: the same
        # SKIP_DIRS rule the yaml walk applies. Measured 2026-08-27 (crew#320): 6 UNEXPLAINED
        # rows, all `~/.claude/scripts/.wt-crew*/state/drills.jsonl`, held the gate RED.
        if _in_worktree(str(r.get("path") or r.get("plist") or ident)):
            continue
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
    "Node": ["ready", "kubelet_version", "pods", "cpu", "memory", "disk_pressure"],
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


def _gh_json(args: list[str], timeout: int = 60):
    """`gh` with the estate's failure grammar: a non-zero exit names why, it never returns []."""
    r = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=timeout, check=False)
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout).strip().splitlines()[-1][:200] if (r.stderr or r.stdout).strip()
                           else f"gh {' '.join(args[:3])} exited {r.returncode} with no output")
    return json.loads(r.stdout)


def _receipt_from_log(text: str) -> dict | None:
    """The one line of a job log that is the receipt body.

    Each log line is `<rfc3339>Z <content>`, and the body is a single line of JSON tens of
    kilobytes long -- `gh run view --log` drops it, the raw API does not, which is why this reads
    the API. Matched on a key of the receipt rather than on position, so a step printing JSON
    before it cannot be mistaken for it.
    """
    for line in text.splitlines():
        if '"flux_not_ready"' not in line:
            continue
        start = line.find('{"')
        if start < 0:
            continue
        try:
            body = json.loads(line[start:])
        except ValueError:
            continue
        if isinstance(body, dict) and "flux" in body and "at" in body:
            return body
    return None


def cluster_receipt() -> tuple[dict, str]:
    """The newest readable cluster-state receipt, and the command that produced it.

    Every failure raises with the reason, because a discoverer that returns [] on a bad day is the
    class that dropped 10 criticals in 18 hours with no test failing.
    """
    runs = _gh_json(["run", "list", "--repo", IDP_REPO, "--workflow", CLUSTER_RECEIPT_WORKFLOW,
                     "--status", "completed", "--limit", str(CLUSTER_RECEIPT_RUNS),
                     "--json", "databaseId,createdAt"])
    if not runs:
        raise RuntimeError(f"no completed {CLUSTER_RECEIPT_WORKFLOW} run in {IDP_REPO}")
    tried = []
    for run in runs:
        try:
            jobs = _gh_json(["api", f"repos/{IDP_REPO}/actions/runs/{run['databaseId']}/jobs"])
        except RuntimeError as e:
            tried.append(f"{run['databaseId']}: jobs unreadable ({e})")
            continue
        job = next((j for j in jobs.get("jobs", []) if j.get("name") == CLUSTER_RECEIPT_JOB), None)
        if job is None:
            tried.append(f"{run['databaseId']}: no {CLUSTER_RECEIPT_JOB} job")
            continue
        cmd = ["api", f"repos/{IDP_REPO}/actions/jobs/{job['id']}/logs"]
        r = subprocess.run(["gh", *cmd], capture_output=True, text=True, timeout=120, check=False)
        if r.returncode != 0:
            tried.append(f"job {job['id']}: log unreadable")
            continue
        body = _receipt_from_log(r.stdout)
        if body is None:
            # `--json` prints the body on the flux-FAIL and ok paths only; every other FAIL exits
            # first. Not an error, just a run that carries no receipt: try the one before it.
            tried.append(f"job {job['id']}: no receipt body in the log")
            continue
        return body, f"gh {' '.join(cmd)}"
    raise RuntimeError(f"no receipt body in the last {len(runs)} {CLUSTER_RECEIPT_WORKFLOW} run(s): "
                       + "; ".join(tried[:4]))


def cluster_live() -> list[Producer]:
    """What the cluster is actually running, read from its own receipt through the GitHub API.

    This ran `kubectl` against ~/.kube/oke-estate until 2026-08-28 and was BLIND on every machine
    an agent works on. The kubeconfig execs `oci ce cluster generate-token` with no --profile,
    ~/.oci/config carries no DEFAULT profile, and both of its profiles authenticate with a browser
    session that expires in hours -- so the one domain that could say what RUNS was answered by
    nobody, and all 233 `cluster` producers beside it are what git DECLARES. That is not a broken
    laptop, it is the estate being operable only from one desk (crew#558).

    The cluster already publishes what it runs, and CI already reads it. The only thing missing was
    a door that needs no OCI identity: a GitHub token, which every session and every runner has.
    """
    body, evidence = cluster_receipt()
    at = body.get("at") or ""
    try:
        age_h = (datetime.datetime.now(datetime.UTC)
                 - datetime.datetime.fromisoformat(at.replace("Z", "+00:00"))).total_seconds() / 3600
    except ValueError as e:
        raise RuntimeError(f"receipt carries no readable timestamp ({at!r}): {e}") from e
    if age_h > CLUSTER_RECEIPT_MAX_AGE_H:
        raise RuntimeError(f"the freshest readable receipt is {age_h:.0f}h old "
                           f"(max {CLUSTER_RECEIPT_MAX_AGE_H:.0f}h): {at}; what it lists is not what runs now")
    ev = f"{evidence}  # receipt at {at}"
    out, seen = [], set()

    def add(ns: str, kind: str, name: str) -> None:
        key = f"{ns or '-'}/{kind}/{name}"
        if not name or key in seen:
            return
        seen.add(key)
        out.append(_p("cluster_live", key, kind, CLUSTER_MEASURES.get(kind, ["exists"]), ev))

    # Flux owns what is deployed: every Kustomization, HelmRelease, GitRepository and
    # ExternalSecret the cluster reconciles, each with its own Ready condition.
    for r in body.get("flux") or []:
        add(r.get("ns"), r.get("kind") or "FluxObject", r.get("name"))
    for d in body.get("daemonsets") or []:
        add(d.get("ns"), "DaemonSet", d.get("name"))
    for e in body.get("policy_exceptions") or []:
        add(e.get("ns"), "PolicyException", e.get("name"))
    for n in body.get("nodes") or []:
        add("-", "Node", n.get("name"))
    if not out:
        raise RuntimeError(f"receipt at {at} lists no flux object, DaemonSet, PolicyException or Node")
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


# crew#558. Where a domain's members come from, and the only number in this file that is
# supposed to fall.
#
# LAW 50 makes `datamap.py --check` the TEMPORARY bootstrap: "what exists and what does not
# emit yet, every gap a ticket. It retires surface by surface as the query takes over." The
# founder refused crew#394 as the law on 2026-08-27 -- "No more custom code for discovery. The
# platform discovers itself ... coverage is verified by querying the backend, not by scanning
# files" -- and then nothing measured whether any surface ever retired. On 2026-08-28 the answer
# was none: 8162 of 8324 producers (98.1%) came from walking one laptop's disk.
#
# `scan` means the domain answers by reading files on whatever machine happens to run it. That
# is why the register could see git worktree copies at all (crew#556: science/ships.jsonl read
# 57 rows in a copy and 150 in the real file, and every ships number the founder was given came
# off the copy) -- a worktree is an artefact of how agents work, not a thing the estate has. A
# scanner has to be taught about them; a backend query never hears of them.
#
# `query` means the domain asks a live API or backend, and its answer does not depend on this
# machine's filesystem.
#
# THE UNIT IS DOMAINS, NOT ROWS, and that is deliberate. The row count moves every hour on its
# own -- a new session writes transcripts, an agent adds a ledger -- so a ceiling counted in rows
# would go red for correct work, which is an outage (LAW 38). A domain moves from `scan` to
# `query` only when somebody retires it. That is the thing LAW 50 asks for, so that is the thing
# the ceiling counts.
PROVENANCE: dict[str, str] = {
    "mac": "scan",           # ~/.estate/state/inventory.json, a walk of this Mac
    "warehouse": "query",    # sqlite over the science warehouse
    "cluster": "scan",       # a yaml walk of the local idp checkout: what git DECLARES
    "cluster_live": "query", # kubectl against the cluster API: what actually RUNS
    "endpoint": "scan",      # the same yaml walk
    "hook": "scan",          # ~/.claude/settings.json
    "mcp": "scan",           # ~/.claude.json
    "github": "query",       # gh repo list
    "transcript": "scan",    # a walk of ~/.claude/projects
    "act": "scan",           # verdicts.json, the register's own hand-typed rows
}


def scan_domains() -> list[str]:
    """The domains still answered by reading files. This list is what retires."""
    return sorted(d for d in DOMAINS if PROVENANCE.get(d) == "scan")


def untagged_domains() -> list[str]:
    """A domain with no provenance. The register is closed-world; so is this."""
    return sorted(set(DOMAINS) - set(PROVENANCE))


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
