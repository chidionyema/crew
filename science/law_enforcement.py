#!/usr/bin/env python3
"""Law enforcement coverage: which laws are machine-enforced, which are prose.

A law in prose is an instruction — compliance is probabilistic, unmeasured, and
re-billed on every request. A law in code is a constraint — it holds or it fails
loudly, and it costs nothing per request.

LAW 6 already ranks these: self-healing > guard > memory file. This probe reports
which tier each law is actually on, and whether its guard is still emitting.

Run it. Do not quote it from memory.
"""
import calendar
import contextlib
import json
import os
import re
import subprocess
import sys
import time

H = os.path.expanduser("~")
SETTINGS = f"{H}/.claude/settings.json"
SCRIPTS  = f"{H}/.claude/scripts"
LAWS     = f"{H}/AGENTS.md"
SKIP_DIRS = {"node_modules", "venv", "__pycache__", "target",
             "build", "dist", "vendor", "Pods", "DerivedData"}
STALE_H  = 24  # a tracking stream silent longer than this is not tracking


def _read(path, errors=None):
    """Whole file as text, closed on return."""
    with open(path, errors=errors) as fh:
        return fh.read()

def _load(path):
    """Parsed JSON file, closed on return."""
    with open(path) as fh:
        return json.load(fh)

def laws():
    out = {}
    try: txt = _read(LAWS)
    except OSError: return out
    for n, title in re.findall(r'^#+\s*LAW (\d+)\s*[—-]\s*(.+)$', txt, re.M):
        out.setdefault(int(n), title.strip())
    return out

def wired():
    """guard basename -> [hook events]. These are PREVENTIVE: they run in-flight."""
    w = {}
    try: cfg = _load(SETTINGS)
    except (OSError, ValueError): return w
    for event, blocks in (cfg.get("hooks") or {}).items():
        for b in blocks:
            for hk in b.get("hooks", []):
                for tok in hk.get("command", "").split():
                    if tok.endswith(".py"):
                        w.setdefault(os.path.basename(tok)[:-3], []).append(event)
    return w

def guards():
    if not os.path.isdir(SCRIPTS): return []
    return sorted(f[:-3] for f in os.listdir(SCRIPTS)
                  if f.endswith(".py") and re.search(r'guard|fence|compliance|scrub|ledger|capture', f))

_CORPUS = None
def corpus():
    """Every file that could name a guard, read once. Docs are excluded: a guard
    mentioned in LAWS-INCIDENTS.md is documented, not called."""
    global _CORPUS
    if _CORPUS is not None: return _CORPUS
    _CORPUS = {}
    roots = [SETTINGS, SCRIPTS, f"{H}/Library/LaunchAgents", f"{H}/.claude/hooks"]
    for root in roots:
        if os.path.isfile(root):
            files=[root]
        elif os.path.isdir(root):
            files=[os.path.join(d,f) for d,_,fs in os.walk(root) for f in fs]
        else:
            continue
        for f in files:
            if f.endswith(('.md','.txt','.bak','.log','.jsonl','.pyc','.json')): continue
            if '__pycache__' in f or '/.git/' in f or '.bak' in f: continue
            if os.path.basename(f) in ('index','HEAD','ORIG_HEAD','config'): continue
            try:
                if os.path.getsize(f) > 2_000_000: continue
                _CORPUS[f] = _read(f, errors="ignore")
            except OSError: pass
    return _CORPUS

def callers(name):
    """Files naming this guard, excluding the guard's own source."""
    return [p for p,txt in corpus().items()
            if name in txt and os.path.basename(p) != name + ".py"]

def scheduled(name, _depth=0):
    """Reachable from a launchd job = DETECTIVE: runs after the fact, cannot block."""
    for p in callers(name):
        if "LaunchAgents" in p: return True
        if _depth == 0 and p.endswith(".py"):
            if scheduled(os.path.basename(p)[:-3], 1): return True
    return False

def guard_path(name):
    """A guard is a .py in scripts/, or a git hook in scripts/hooks/ with no
    extension. The second kind was invisible to this probe until 2026-08-23,
    which is why it reported LAW 7 and LAW 32 as prose while both were wired."""
    #: crew#434: policy rules live in scripts/policy/*.rego (the
    #: hand-rolled-policy gate refuses a new .py guard), run by opa-hook.py.
    if name.startswith("hooks/") or name.endswith(".rego"):
        return f"{SCRIPTS}/{name}"
    return f"{SCRIPTS}/{name}.py"

def law_refs(name):
    """Which laws does this guard itself cite? Mechanical, not guessed."""
    try: txt = _read(guard_path(name), errors="ignore")
    except OSError: return set()
    # Upper bound reads the laws file. It was hardcoded to 31, so LAW 32's own
    # gate cited a law this probe threw away. A constant that has to be edited
    # every time the estate grows is a defect, not a setting.
    top = max(laws() or {0: ""}) or 32
    return {int(n) for n in re.findall(r'LAW\s*(\d{1,2})', txt) if 1 <= int(n) <= top}

GIT_HOOK_NAMES = ("pre-push", "pre-commit", "commit-msg", "pre-rebase", "post-merge")

def git_hooks():
    """Git hooks living in the shared hooks dir, as guard names."""
    d = f"{SCRIPTS}/hooks"
    if not os.path.isdir(d): return []
    return sorted(f"hooks/{f}" for f in os.listdir(d)
                  if f in GIT_HOOK_NAMES and os.access(os.path.join(d, f), os.X_OK))

_REPOS = None
def repos():
    """Every git repository on this machine that could bind a hook.

    The denominator. Without it "2 repositories bind the hooks" sounds like a
    fact about two repositories rather than about the forty-six that do not.
    """
    global _REPOS
    if _REPOS is not None: return _REPOS
    _REPOS = []
    for base in (f"{H}/dev", f"{H}/code", f"{H}/Documents/code", f"{H}/.claude"):
        if not os.path.isdir(base): continue
        for d, subs, _ in os.walk(base):
            #: Prune hard. Without this the walk descends into node_modules and
            #: .venv and takes minutes, and the probe runs hourly.
            subs[:] = [x for x in subs if x not in SKIP_DIRS and not x.startswith(".")]
            if d.count(os.sep) - base.count(os.sep) > 3:
                subs[:] = []; continue
            if os.path.exists(os.path.join(d, ".git")):
                #: Stop at the repository boundary. Descending finds vendored
                #: checkouts and submodules, which nobody ships a feature from,
                #: and it took the walk from seconds to over a minute.
                _REPOS.append(d); subs[:] = []
    #: A bound repository must appear in its own denominator. ~/.claude/scripts
    #: sits inside ~/.claude, so the prune above would otherwise let the
    #: numerator count a repository the denominator had skipped.
    for r in hook_binds():
        if r not in _REPOS: _REPOS.append(r)
    return _REPOS

def guard_dir_reaches_impl(d):
    """Does a hooksPath directory end up running the estate's guards.

    Matching the literal path ~/.claude/scripts/hooks was right for one day.
    On 2026-08-23 the guards got a neutral address, ~/.estate/guards/hooks,
    whose _router chains to GUARD_IMPL in estate.conf, and the repositories
    were rebound to that address. This function kept comparing the old string,
    so the probe printed "0 of 48. Every push on this machine is ungated" onto
    the founder's board at the exact moment every push became gated. Follow
    the chain. Do not compare a name.
    """
    if not d: return False
    rp = os.path.realpath
    impl = rp(f"{SCRIPTS}/hooks")
    if rp(d) == impl: return True
    #: The router form. The address stays put, the body it points at moves,
    #: and one line in estate.conf is the whole of the indirection.
    if not os.path.isfile(os.path.join(d, "_router")): return False
    for conf in (os.path.join(os.path.dirname(d.rstrip("/")), "estate.conf"),
                 f"{H}/.estate/guards/estate.conf"):
        try: txt = _read(conf, errors="ignore")
        except OSError: continue
        m = re.search(r'^\s*GUARD_IMPL=(.+)$', txt, re.M)
        if not m: continue
        v = m.group(1).strip().strip('"').strip("'").replace("$HOME", H).replace("${HOME}", H)
        if rp(v) == impl: return True
    return False

_GLOBAL_BIND = None
def global_bind():
    """The hooksPath every repository inherits, when one is set.

    A per-repository sweep can never finish. A repository cloned after the
    sweep is ungated and nobody finds out until something ships. One global
    setting governs the repositories that do not exist yet, which turns reach
    from a count that is always behind into a yes or no.
    """
    global _GLOBAL_BIND
    if _GLOBAL_BIND is not None: return _GLOBAL_BIND
    _GLOBAL_BIND = False
    for cfgp in (f"{H}/.gitconfig", f"{H}/.config/git/config"):
        try: txt = _read(cfgp, errors="ignore")
        except OSError: continue
        m = re.search(r'^\s*hooksPath\s*=\s*(.+)$', txt, re.M)
        if m and guard_dir_reaches_impl(m.group(1).strip()):
            _GLOBAL_BIND = True; break
    return _GLOBAL_BIND

_BINDS = None
def hook_binds():
    """Repositories where a push actually meets the guards.

    A git hook is only PREVENTIVE in a repository that reaches it. Every other
    checkout on this machine pushes with no gate at all, and nothing said so
    until this function existed."""
    global _BINDS
    if _BINDS is not None: return _BINDS
    _BINDS = []
    cands = [f"{H}/.claude", SCRIPTS, f"{H}/dev/code"]
    root = f"{H}/dev/code"
    if os.path.isdir(root):
        cands += [os.path.join(root, d) for d in sorted(os.listdir(root))]
    # Read .git/config directly. Shelling out to `git config` once per candidate
    # took the probe past two minutes on this machine; a config file is 2KB.
    for r in cands:
        g = os.path.join(r, ".git")
        cfgp = os.path.join(g, "config") if os.path.isdir(g) else None
        if not cfgp or not os.path.isfile(cfgp): continue
        try: txt = _read(cfgp, errors="ignore")
        except OSError: continue
        m = re.search(r'^\s*hooksPath\s*=\s*(.+)$', txt, re.M)
        if not m: continue
        v = m.group(1).strip()
        real = v if os.path.isabs(v) else os.path.join(r, v)
        if guard_dir_reaches_impl(real):
            _BINDS.append(r)
    return _BINDS

def githooks():
    """Git hooks are guards too, and the probe could not see them.

    It read settings.json and launchd and nothing else, so `hooks/pre-push`
    -- which refuses a stale branch under LAW 7 and a feature with no demo
    under LAW 20/32 -- counted as prose. That undercount is not the interesting
    part. The interesting part is REACH: a git hook only runs in a repository
    whose core.hooksPath points at it, so "the estate enforces LAW 7" is false
    when the hook is bound in two checkouts and the features ship from five.

    Returns [(hook_name, laws_it_cites)]. Reach comes from hook_binds().
    """
    d = f"{SCRIPTS}/hooks"
    out = []
    for path in git_hooks():
        fp = os.path.join(d, path.split("/")[-1])
        try: txt = _read(fp, errors="replace")
        except OSError: continue
        ls = sorted({int(n) for n in re.findall(r'LAW\s*(\d{1,2})', txt)
                     if 1 <= int(n) <= 32})
        out.append((path.split("/")[-1], ls))
    return out

# crew#80: the tracked streams used to be a hardcoded path list, and one of
# them (state/one-branch/would-have-fired.jsonl) outlived its writer by five
# days, so the lawenforcement check was red with nothing to fix. The names now
# resolve through science/sources.json, the closed-world registry the datamap
# gate keeps honest: a stream nobody registered cannot be tracked here, and a
# stream the registry drops leaves this list in the same commit. toolguard
# (state/toolguard/events.jsonl) went the same way: 77h silent on 2026-08-27,
# tool-drip-guard.py wired into no hook, not in the registry, so not tracked.
TRACKED_STREAMS = ("close_guard", "ledger", "board", "spend")
SOURCES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sources.json")

def stream_paths(sources=SOURCES, home=H):
    """(display name, absolute path) for each tracked stream, from the registry.
    A tracked name missing from the registry is an error, not a skip: silently
    dropping it is how crew#80 happened in the other direction."""
    with open(sources) as fh:
        reg = {s["name"]: s for s in json.load(fh)["sources"]}
    out = []
    for name in TRACKED_STREAMS:
        if name not in reg:
            raise KeyError(f"tracked stream {name!r} is not in {sources}")
        s = reg[name]
        if s["root"] != "home":
            raise ValueError(f"tracked stream {name!r} has root {s['root']!r}, expected 'home'")
        out.append((s["path"], os.path.join(home, s["path"])))
    return out

def streams():
    """Tracking streams and how long since each last moved."""
    now=time.time(); out=[]
    for c,p in stream_paths():
        if not os.path.exists(p): continue
        age=(now-os.path.getmtime(p))/3600
        try:
            with open(p,errors="ignore") as fh: n=sum(1 for _ in fh)
        except OSError: n=-1
        out.append((c,n,age))
    return out

CI_RUNS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ci-runs.jsonl")


def _repo_name():
    """The repo as ci-runs.jsonl names it (the GitHub name), not the checkout
    directory: a worktree named crew423 is still the crew repo."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        url = subprocess.run(["git", "-C", root, "config", "--get", "remote.origin.url"],
                             capture_output=True, text=True, timeout=5, check=False).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        url = ""
    name = url.rstrip("/").rsplit("/", 1)[-1] if url else os.path.basename(root)
    return name[:-4] if name.endswith(".git") else name


REPO_NAME = _repo_name()

def workflow_ran(workflow, ci_runs=CI_RUNS, repo=REPO_NAME, now=None, stale_h=30.0):
    """crew#423: a GitHub Actions gate is live when the estate's own CI record
    (science/ci-runs.jsonl, written daily by ci-runs.yml, crew#393) shows it
    completed at least one run for this repo inside the last window. The file
    existing in .github/workflows is not the question; a workflow that never
    runs enforces nothing."""
    try:
        with open(ci_runs) as fh:
            rows = [json.loads(line) for line in fh if line.strip()]
    except (OSError, ValueError):
        return False
    now = time.time() if now is None else now
    for r in rows:
        if r.get("repo") != repo or r.get("workflow") != workflow or not r.get("measured"):
            continue
        try:
            #: crew#425 review: mktime - timezone is 1h off under DST; timegm is UTC.
            at = calendar.timegm(time.strptime(r["at"][:19], "%Y-%m-%dT%H:%M:%S"))
        except (KeyError, ValueError):
            continue
        if (now - at) / 3600 <= stale_h and (r.get("completed") or 0) > 0:
            return True
    return False

#: crew#423 row 25: policy/command.rego is loaded by rule-guard.py (PreToolUse on
#: Bash), not by opa-hook.py, so its tier is rule-guard's. Every other .rego is
#: opa-hook's.
REGO_RUNNERS = {"command.rego": "rule-guard"}


def rego_runner(name):
    return REGO_RUNNERS.get(os.path.basename(name), "opa-hook")


def derive(entry, tiermap):
    """LAW 28: the state field is hand-written, so it drifts, and a map that
    says live about a dead guard is worse than no map. Derive it.

    A .py guard is live when this probe's own tier says it is reachable.
    A git hook is live when the file cites the law AND a push reaches it. A
    global core.hooksPath is the strongest form of reaching it, because it
    covers repositories nobody has cloned yet.
    """
    gs = entry.get("guards") or []
    if not gs: return "absent"
    #: crew#423: the map was renumbered on 2026-08-23 (`was` is the number the
    #: hook still cites, `law` the effective rank), so a hook citing LAW 32 was
    #: graded dead against law=9. Either number is the citation.
    cited = {n for n in (entry.get("law"), entry.get("was")) if n is not None}
    for g in gs:
        name = g[:-3] if g.endswith(".py") else g
        if g.startswith(".github/workflows/"):
            if workflow_ran(os.path.basename(g)): return "live"
            continue
        if name.startswith("hooks/"):
            reached = global_bind() or hook_binds()
            #: A rule retired to a machine has no law number to cite, so the
            #: citation test cannot apply to it. Reaching the hook is the whole
            #: question for those, and it is the right question: "refresh on
            #: main" is enforced when pre-push runs, not when pre-push says 7.
            if entry.get("law") is None:
                if reached: return "live"
            #: For a rule still attached to a law, the hook must also SAY which
            #: law it enforces. That citation is what lets the map be checked
            #: against the guard instead of against itself.
            elif cited & law_refs(name) and reached:
                return "live"
        #: crew#434: a Rego rule is live when it cites the law and its runner,
        #: opa-hook.py, is wired to a Claude Code hook. The rule cannot run any
        #: other way, so the runner's tier is the rule's tier.
        elif name.endswith(".rego"):
            if cited & law_refs(name) and tiermap.get(rego_runner(name)) == "PREVENTIVE":
                return "live"
        elif tiermap.get(os.path.basename(name)) in ("PREVENTIVE", "DETECTIVE"):
            return "live"
    return "dead"


def main():
    L, W, G = laws(), wired(), guards() + git_hooks()

    # Reachability from real entry points, not one hop.
    #   PREVENTIVE = wired to a Claude Code hook: runs in-flight, can refuse.
    #   DETECTIVE  = reached from a launchd job:  runs after the fact, cannot refuse.
    #   DEAD       = no path from either.
    tier = {}
    for g in G:
        if g.startswith("hooks/"):
            tier[g] = "PREVENTIVE" if (global_bind() or hook_binds()) else "DEAD"
        elif g in W: tier[g] = "PREVENTIVE"
        elif scheduled(g): tier[g] = "DETECTIVE"
    changed = True
    while changed:                      # propagate along the call graph
        changed = False
        for g in G:
            if g in tier: continue
            for p in callers(g):
                parent = os.path.basename(p)[:-3] if p.endswith(".py") else None
                if parent in tier:
                    tier[g] = tier[parent]; changed = True; break

    rows=[]
    for g in G:
        t = tier.get(g, "DEAD")
        if g.startswith("hooks/"):
            how = ("git hook, every repo" if global_bind()
                   else f"git hook, {len(hook_binds())} repo(s)")
        elif g in W:          how = "+".join(sorted(set(W[g])))
        elif t == "DEAD":     how = "no caller"
        elif scheduled(g):    how = "scheduled"
        else:
            cs = [os.path.basename(p) for p in callers(g)
                  if p.endswith(".py") and os.path.basename(p)[:-3] in tier]
            how = f"via {cs[0]}" if cs else "scheduled"
        rows.append((g, t, how, sorted(law_refs(g))))

    order={"PREVENTIVE":0,"DETECTIVE":1,"INDIRECT":2,"DEAD":3}
    rows.sort(key=lambda r:(order[r[1]], r[0]))

    print("="*74); print("GUARD ENFORCEMENT TIER"); print("="*74)
    for g,tier,how,ls in rows:
        print(f"  {tier:<11} {g:<24} {how:<22} {('LAW '+','.join(map(str,ls))) if ls else '-'}")
    c={}
    for _,t,_,_ in rows: c[t]=c.get(t,0)+1
    print(f"\n  {len(rows)} guards: " + "  ".join(f"{k}={v}" for k,v in sorted(c.items(), key=lambda x:order[x[0]])))

    covered={n for _,t,_,ls in rows if t in ("PREVENTIVE","DETECTIVE") for n in ls}

    GH = githooks()
    binds = hook_binds()
    if GH:
        print("\n"+"="*74); print("GIT HOOK REACH"); print("="*74)
        for name, ls in GH:
            #: A hook bound nowhere refuses nothing. Counting its laws as
            #: covered would be the probe telling a comfortable lie.
            #: Reached, not bound. A repository does not have to name the
            #: guards for a push to meet them: a global core.hooksPath governs
            #: every checkout, including the ones cloned tomorrow.
            if global_bind() or binds:
                covered |= set(ls)
            flag = "PREVENTIVE" if (global_bind() or binds) else "NOT BOUND"
            print(f"  {flag:<12} {name:<12} "
                  f"{'LAW ' + ','.join(map(str, ls)) if ls else '-'}")
        if global_bind():
            print("\n  reach : EVERY repository on this machine, and every one")
            print("          cloned from now on. core.hooksPath is set globally.")
            print(f"          {len(binds)} of {len(repos())} also name it locally, which changes nothing.")
        else:
            print(f"\n  repositories binding them : {len(binds)} of {len(repos())}")
            for r in binds: print(f"    {r}")
            if not binds:
                print("    NONE. Every push on this machine is ungated.")
            else:
                print("  a git hook runs ONLY where core.hooksPath names it.")
                print("  Bind them everywhere at once instead of one at a time:")
                print(f"    git config --global core.hooksPath {H}/.estate/guards/hooks")

    print("\n"+"="*74); print("LAW COVERAGE"); print("="*74)
    prose=[n for n in sorted(L) if n not in covered]
    print(f"  laws declared          : {len(L)}")
    print(f"  cited by a live guard  : {len(covered & set(L))}   {sorted(covered & set(L))}")
    print(f"  PROSE ONLY (no guard)  : {len(prose)}   {prose}")

    # The map is the compiler from prose to check. Without it, "which law is
    # enforced" is unanswerable and nothing fails when one stops being enforced.
    mp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "enforcement-map.json")
    gap = []
    try:
        M = _load(mp)["laws"]
    except (OSError, ValueError, KeyError) as e:
        M = []; print(f"\n  enforcement-map.json unreadable: {e}")
    if M:
        print("\n"+"="*74); print("LAW -> CHECK"); print("="*74)
        verd = {}
        for x in M: verd[x["verdict"]] = verd.get(x["verdict"], 0) + 1
        # LAW 28: state was hand-written, so it drifted. Derive it, and keep the
        # declared value only to report where the map was lying.
        tiermap = {r[0]: r[1] for r in rows}
        drift = []
        for x in M:
            real = derive(x, tiermap)
            if real != x.get("state"):
                drift.append((x.get("rule") or x["id"], x.get("state"), real))
            x["state"] = real
        #: A rule the 2026-08-23 renumber retired to a machine has no law to be
        #: a gap in. It is still tracked -- map_covers_laws.py names the three
        #: with no owner -- but counting it here would report the constitution
        #: as less enforced than it is.
        mech = [x for x in M if x["verdict"] == "mechanical" and x.get("law") is not None]
        gap  = [x for x in mech if x["state"] != "live"]
        print(f"  mechanical (a machine can decide it) : {verd.get('mechanical',0)}")
        print(f"  partial    (a smell, not a verdict)  : {verd.get('partial',0)}")
        print(f"  judgement  (will never be code)      : {verd.get('judgement',0)}")
        print(f"\n  mechanical AND live                  : {len(mech)-len(gap)} of {len(mech)}")
        print(f"  THE GAP                              : {[x['id'] for x in gap]}")
        for x in gap:
            print(f"    LAW {x['id']:<3} {x['where']!s:<12} {x['check'][:52]}")
        if drift:
            print(f"\n  MAP DRIFT (the declared state was wrong): {len(drift)}")
            for i, said, real in drift:
                print(f"    {i!s:<34} map said {said:<8} actually {real}")
        #: Both sides normalised to a bare name. The map writes a guard as
        #: `estate/in-git.py` or `hooks/pre-push`, and the probe names it
        #: `in-git` or `hooks/pre-push`, so comparing the raw strings reported
        #: every git hook as undeclared the moment the probe learned to see them.
        def _norm(x):
            x = x.split("/")[-1]
            return x[:-3] if x.endswith(".py") else x
        declared = {_norm(gg) for x in M for gg in x.get("guards", [])}
        with contextlib.suppress(OSError, ValueError, KeyError, TypeError):
            declared |= {_norm(gg)
                         for sec in _load(mp).get("sections", [])
                         for gg in sec.get("guards", [])}
        tiermap = {r[0]: r[1] for r in rows}
        undeclared = [g for g in G if _norm(g) not in declared
                      and tiermap.get(g) != "DEAD"]
        if undeclared:
            print(f"\n  LIVE guards absent from the map: {len(undeclared)}")
            print(f"    {', '.join(undeclared)}")

    print("\n"+"="*74); print("TRACKING FRESHNESS"); print("="*74)
    dead=0
    for name,n,age in streams():
        flag = "STALE" if age>STALE_H else "live"
        if age>STALE_H: dead+=1
        print(f"  {flag:<6} {age:7.1f}h  {n:>7} lines  {name}")
    print(f"\n  {dead} stream(s) silent >{STALE_H}h")

    j={"generated":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),
       "guards":[{"name":g,"tier":t,"via":h,"laws":ls} for g,t,h,ls in rows],
       "laws_total":len(L),"laws_covered":sorted(covered & set(L)),"laws_prose_only":prose,
       "mechanical":sorted({x["id"] for x in M if x["verdict"]=="mechanical"
                            and x.get("law") is not None}),
       "gap":[{"id":x["id"],"where":x["where"],"check":x["check"]} for x in gap],
       "hook_binds":hook_binds(),
       #: `global` is the field that matters. A per-repository count is
       #: always behind by however many repositories were cloned since the
       #: last sweep; a global core.hooksPath has no such gap.
       "hook_reach":{"bound":len(hook_binds()),"repos":len(repos()),
                     "global":global_bind(),
                     "impl":os.path.realpath(f"{SCRIPTS}/hooks")},
       "streams":[{"name":n,"lines":c_,"age_h":round(a,1)} for n,c_,a in streams()]}
    out=f"{H}/.claude/state/law-enforcement.json"
    try:
        with open(out,"w") as fh: json.dump(j,fh,indent=1)
        print(f"\nwrote {out}")
    except OSError as e:
        print(f"\ncould not write {out}: {e}")
    # exit 1 while any mechanical law is unenforced or any stream is stale,
    # so a scheduler can read the verdict without parsing the text
    return 1 if (gap or dead) else 0

if __name__ == "__main__":
    sys.exit(main())
