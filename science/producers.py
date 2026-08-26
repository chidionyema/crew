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

import json
import os
import pathlib
import plistlib
import re
import sqlite3
import subprocess
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


def _monitored(plist: str | None) -> bool:
    if not plist or not pathlib.Path(plist).exists():
        return False
    try:
        x = plistlib.load(open(plist, "rb"))
    except Exception:  # noqa: BLE001
        return False
    return any("hc-wrap" in str(a) for a in (x.get("ProgramArguments") or [x.get("Program") or ""]))


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
        ident = str(ident).replace(str(HOME) + "/", "~/")
        size = r.get("mb") or r.get("rows")
        # A scheduled job under hc-wrap pings a dead-man monitor; one without it can stop
        # and nothing says so. That is a different kind of producer, not a note.
        if kind == "scheduled_job":
            kind = "scheduled_job:" + ("monitored" if _monitored(r.get("plist")) else "unmonitored")
        prod = _p("mac", f"{kind.split(':')[0]}/{ident}", kind, MAC_MEASURES.get(kind.split(':')[0], ["exists"]),
                  r.get("plist") or r.get("path") or str(INVENTORY), size)
        # The inventory already knows which stores collect.py reads; that is a measured
        # verdict, and the register must not be asked to retype it.
        if r.get("collected") is True or r.get("member_of"):
            prod["auto"] = {"verdict": "COLLECTED",
                            "reader": f"science/collect.py source {r.get('member_of') or r.get('source') or r.get('id')}"}
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
                       capture_output=True, text=True, timeout=40)
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
                        "--json", "name,isPrivate,pushedAt"], capture_output=True, text=True, timeout=60)
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
