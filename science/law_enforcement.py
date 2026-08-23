#!/usr/bin/env python3
"""Law enforcement coverage: which laws are machine-enforced, which are prose.

A law in prose is an instruction — compliance is probabilistic, unmeasured, and
re-billed on every request. A law in code is a constraint — it holds or it fails
loudly, and it costs nothing per request.

LAW 6 already ranks these: self-healing > guard > memory file. This probe reports
which tier each law is actually on, and whether its guard is still emitting.

Run it. Do not quote it from memory.
"""
import json, os, re, subprocess, sys, time

H = os.path.expanduser("~")
SETTINGS = f"{H}/.claude/settings.json"
SCRIPTS  = f"{H}/.claude/scripts"
LAWS     = f"{H}/AGENTS.md"
STALE_H  = 24  # a tracking stream silent longer than this is not tracking

def laws():
    out = {}
    try: txt = open(LAWS).read()
    except OSError: return out
    for n, title in re.findall(r'^#+\s*LAW (\d+)\s*[—-]\s*(.+)$', txt, re.M):
        out.setdefault(int(n), title.strip())
    return out

def wired():
    """guard basename -> [hook events]. These are PREVENTIVE: they run in-flight."""
    w = {}
    try: cfg = json.load(open(SETTINGS))
    except Exception: return w
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
                _CORPUS[f] = open(f, errors="ignore").read()
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

def law_refs(name):
    """Which laws does this guard itself cite? Mechanical, not guessed."""
    try: txt = open(f"{SCRIPTS}/{name}.py", errors="ignore").read()
    except OSError: return set()
    return {int(n) for n in re.findall(r'LAW\s*(\d{1,2})', txt) if 1 <= int(n) <= 31}

def streams():
    """Tracking streams and how long since each last moved."""
    cands = ["state/toolguard/events.jsonl","state/close-guard-observe.jsonl",
             "state/one-branch/would-have-fired.jsonl","state/ledger.jsonl",
             "ESTATE_BOARD.jsonl","estate-spend-history.jsonl"]
    now=time.time(); out=[]
    for c in cands:
        p=f"{H}/.claude/{c}"
        if not os.path.exists(p): continue
        age=(now-os.path.getmtime(p))/3600
        try: n=sum(1 for _ in open(p,errors="ignore"))
        except OSError: n=-1
        out.append((c,n,age))
    return out

def main():
    L, W, G = laws(), wired(), guards()

    # Reachability from real entry points, not one hop.
    #   PREVENTIVE = wired to a Claude Code hook: runs in-flight, can refuse.
    #   DETECTIVE  = reached from a launchd job:  runs after the fact, cannot refuse.
    #   DEAD       = no path from either.
    tier = {}
    for g in G:
        if g in W: tier[g] = "PREVENTIVE"
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
        if g in W:            how = "+".join(sorted(set(W[g])))
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
    print("\n"+"="*74); print("LAW COVERAGE"); print("="*74)
    prose=[n for n in sorted(L) if n not in covered]
    print(f"  laws declared          : {len(L)}")
    print(f"  cited by a live guard  : {len(covered & set(L))}   {sorted(covered & set(L))}")
    print(f"  PROSE ONLY (no guard)  : {len(prose)}   {prose}")

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
       "streams":[{"name":n,"lines":c_,"age_h":round(a,1)} for n,c_,a in streams()]}
    out=f"{H}/.claude/state/law-enforcement.json"
    try:
        json.dump(j,open(out,"w"),indent=1); print(f"\nwrote {out}")
    except OSError as e:
        print(f"\ncould not write {out}: {e}")
    # exit 1 when any law is unenforced or any stream is stale -> readable by a scheduler
    return 1 if (prose or dead) else 0

if __name__ == "__main__":
    sys.exit(main())
