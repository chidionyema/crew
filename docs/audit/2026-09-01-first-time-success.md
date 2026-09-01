# First-time success of agent builds and releases across infrastructure, since 2026-08-25

Founder, 2026-09-01: "can you run the numbers and tell me the percentage of agent builds and releases across
infra that succeeded first time". Counted on 2026-09-01 from GitHub's own records, never from memory.

## Method

- **Pull request green on the first push:** a merged pull request counts as first-time success only when it
  has exactly one commit and every check on that commit passed. A second commit means a fix-up.
- **Main-branch runs, first attempt:** every completed workflow run on `main` since 2026-08-25, counted as
  first-time success when its first attempt concluded `success`.
- Repositories: `idp` (the platform, where infrastructure lives) and `prospector` (the product).
- Not measurable from GitHub: whether Flux applied each merge to the cluster on the first reconcile. That
  number needs the cluster's Kustomization history and is the founder's read.
- Script: `first_time.py` (this page's appendix). Output below verbatim.

## Output, verbatim

```

=== chidionyema/idp (since 2026-08-25) ===
merged PRs: 89 | with checks on the first commit: 70 | no checks recorded: 19
PR green on the FIRST push (one commit, every check passed): 20/70 = 29%
commits per merged PR: median 2, max 22; PRs needing 2+ commits: 48/89
main-branch runs, completed, first-attempt pass rate (name: first-attempt pass / runs, re-runs):
  flux-events                                       675/687  =  98%  re-runs 0
  estate-state                                       67/67   = 100%  re-runs 0
  login-drill                                        19/27   =  70%  re-runs 0
  ticket-verification                                25/25   = 100%  re-runs 0
  verdict-backstage                                  23/23   = 100%  re-runs 0
  verdict-signoz                                      0/22   =   0%  re-runs 0
  verdict-langfuse                                   19/22   =  86%  re-runs 0
  storefront-drill                                   19/20   =  95%  re-runs 0
  otto-parity                                         0/20   =   0%  re-runs 0
  stale                                              19/19   = 100%  re-runs 0
  ci                                                  8/14   =  57%  re-runs 1
  conscience-ask                                      0/10   =   0%  re-runs 0
  founder-word                                        0/10   =   0%  re-runs 0
  estate-escrow                                       6/6    = 100%  re-runs 0
  oke-check                                           0/6    =   0%  re-runs 0
  build-multiarch                                     4/4    = 100%  re-runs 0
  wake-blocked                                        4/4    = 100%  re-runs 0
  ping                                                0/3    =   0%  re-runs 0
  pr-age                                              0/3    =   0%  re-runs 0
  vault-reads                                         0/3    =   0%  re-runs 0
  ALL main runs: 888/995 = 89% passed first attempt; 1 re-runs

=== chidionyema/prospector (since 2026-08-25) ===
merged PRs: 51 | with checks on the first commit: 46 | no checks recorded: 5
PR green on the FIRST push (one commit, every check passed): 28/46 = 61%
commits per merged PR: median 1, max 13; PRs needing 2+ commits: 23/51
main-branch runs, completed, first-attempt pass rate (name: first-attempt pass / runs, re-runs):
  PR keeper                                         106/240  =  44%  re-runs 0
  Merge when green                                  213/222  =  96%  re-runs 0
  Approve parked runs                                76/78   =  97%  re-runs 0
  Live storefront smoke                              49/57   =  86%  re-runs 0
  container images                                   49/50   =  98%  re-runs 0
  CI                                                 44/50   =  88%  re-runs 0
  k8s manifests                                      35/35   = 100%  re-runs 0
  DNS drift drill                                     7/9    =  78%  re-runs 0
  stale                                               6/6    = 100%  re-runs 0
  ALL main runs: 585/747 = 78% passed first attempt; 0 re-runs

```

## Reading it

- Infrastructure pull requests (idp) went green on the first push **29%** of the time (20 of 70 with checks);
  48 of 89 merged pull requests needed two or more commits (median 2, worst 22).
- Product pull requests (prospector) went green on the first push **61%** of the time (28 of 46).
- Image builds passed first time: idp `build-multiarch` 4 of 4, prospector `container images` 49 of 50,
  prospector `k8s manifests` 35 of 35.
- The infrastructure release check `oke-check` on main passed **0 of 6** first attempts since 2026-08-25;
  the other zero rows (`verdict-signoz`, `otto-parity`, `conscience-ask`, `founder-word`, `ping`, `pr-age`,
  `vault-reads`) are scheduled probes whose failures are findings about the estate, not about a build.
- All main-branch runs: idp 89% (888 of 995), prospector 78% (585 of 747), with almost no re-runs, which
  means a red run is left red rather than retried.

## Appendix: the script

```python
import json, subprocess, collections, sys
SINCE="2026-08-25"
def gh(path, paginate=False):
    cmd=["gh","api",path]+(["--paginate"] if paginate else [])
    out=subprocess.run(cmd,capture_output=True,text=True,timeout=300).stdout
    if not paginate: return json.loads(out) if out.strip() else []
    # --paginate concatenates JSON docs; split with a decoder
    dec=json.JSONDecoder(); i=0; res=[]
    while i<len(out):
        while i<len(out) and out[i].isspace(): i+=1
        if i>=len(out): break
        obj,j=dec.raw_decode(out,i); res.append(obj); i=j
    return res
for repo in ["chidionyema/idp","chidionyema/prospector"]:
    print(f"\n=== {repo} (since {SINCE}) ===")
    # A) pull requests: did the FIRST commit's checks all pass?
    prs=gh(f"repos/{repo}/pulls?state=closed&sort=updated&direction=desc&per_page=100")
    prs=[p for p in prs if p.get("merged_at") and p["merged_at"]>=SINCE]
    first_green=0; graded=0; nocheck=0; pushes=[]
    for p in prs:
        commits=gh(f"repos/{repo}/pulls/{p['number']}/commits?per_page=100")
        if not commits: continue
        pushes.append(len(commits))
        sha=commits[0]["sha"]
        cr=gh(f"repos/{repo}/commits/{sha}/check-runs?per_page=100")
        runs=[c for c in (cr.get("check_runs") or []) if c.get("conclusion") not in (None,"skipped","neutral")]
        if not runs: nocheck+=1; continue
        graded+=1
        if all(c["conclusion"]=="success" for c in runs) and len(commits)==1: first_green+=1
    print(f"merged PRs: {len(prs)} | with checks on the first commit: {graded} | no checks recorded: {nocheck}")
    if graded: print(f"PR green on the FIRST push (one commit, every check passed): {first_green}/{graded} = {100*first_green/graded:.0f}%")
    if pushes:
        pushes.sort(); print(f"commits per merged PR: median {pushes[len(pushes)//2]}, max {pushes[-1]}; PRs needing 2+ commits: {sum(1 for x in pushes if x>1)}/{len(pushes)}")
    # B) workflow runs on main: first-attempt success per build/deploy workflow
    runs=[]
    for page in gh(f"repos/{repo}/actions/runs?created=%3E%3D{SINCE}&branch=main&per_page=100", paginate=True):
        runs+=page.get("workflow_runs",[])
    by=collections.defaultdict(lambda: collections.Counter())
    for r in runs:
        if r.get("status")!="completed": continue
        k=r["name"]; by[k]["runs"]+=1
        if r["conclusion"]=="success": by[k]["success"]+=1
        if r.get("run_attempt",1)>1: by[k]["reruns"]+=1
        if r.get("run_attempt",1)==1 and r["conclusion"]=="success": by[k]["first_ok"]+=1
    tot=collections.Counter()
    print("main-branch runs, completed, first-attempt pass rate (name: first-attempt pass / runs, re-runs):")
    for k,c in sorted(by.items(), key=lambda kv:-kv[1]["runs"]):
        if c["runs"]<3: continue
        tot.update(c)
        print(f"  {k[:48]:48s} {c['first_ok']:4d}/{c['runs']:<4d} = {100*c['first_ok']/c['runs']:3.0f}%  re-runs {c['reruns']}")
    if tot["runs"]: print(f"  ALL main runs: {tot['first_ok']}/{tot['runs']} = {100*tot['first_ok']/tot['runs']:.0f}% passed first attempt; {tot['reruns']} re-runs")
```
