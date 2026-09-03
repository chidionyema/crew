# Built but not shipped: the 7-day audit (2026-08-27 → 2026-09-03)

Founder ask, 2026-09-03: "you built it so why not shipped, what else we have lying around not
shipped, i need an audit of past 7 days across github and macbook."

Method: every repo pushed in the last 7 days (GitHub REST, 15 repos); every branch not merged
into main joined against the **full** pull-request history by head ref (squash merges make
`--no-merged` alone a lie); every git checkout and worktree under `~/dev/code` swept for dirty
tracked files and unpushed local branches.

## 1. The Redis answer first

LiteLLM Redis was built and it DID ship — for 31 minutes.

- PR **idp#1182** (shared router memory + bounded answer cache) merged 2026-09-03 01:28Z.
- PR **idp#1192** reverted it at 01:59Z **on the founder's own order**: the cache shipped as a
  one-replica Deployment, the estate's Kyverno availability policy (crew#555) refused it, and
  that refusal wedged the llm Kustomization plus twenty dependents. The founder's ruling in
  1192: no exception for your own non-compliant change; it returns compliant or with a design
  he approves first.
- Since then a session REBUILT it and never pushed: local branch `feat/litellm-redis`
  (idp checkouts, committed 2026-09-03, 5 commits, 270 lines: redis.yaml, config wiring,
  availability waiver with named remedy, balloon reserve payment, tests, demo + onboarding
  docs). It is 57 commits behind main and sits only on the MacBook.
- Decision needed: the rebuild answers the admission failure with a **waiver + named remedy**,
  not the two-replica shape 1192 named. One word decides: rebase-and-PR it as-is, or demand
  two replicas first.

## 2. GitHub: what is lying around

### idp (the platform repo), branches not merged, last 7 days
| verdict | count | meaning |
|---|---|---|
| open PR | 5 | #1241 image pin, #1239 portal look, #1238 superset login, #1196 live diagram, #1166 dependabot |
| never PR'ed | **42** | built, pushed, never offered for ship |
| PR closed unmerged | 24 | deliberately dropped or superseded — branches never deleted |
| merged (squash) litter | 58 | shipped; stale branch left behind |

The 42 never-PR'ed with real platform weight:
`feat/security-end-to-end` (2026-09-02), `fix/priority-class-on-platform-workloads`,
`fix/kyverno-judge-audit-warn-split`, `fix/image-update-pr-control`, `feat/bitwarden-decision`,
`docs/self-service-tenancy`, `docs/otto-install-map`, `docs/amend-0002-docs-directories`,
`docs/elite-shipping-audit` (an unshipped audit about shipping), `fix/crew718-cluster-doctor`,
`fix/phone-drill-reads-door-names`, `feat/portal-modern-home`, `deepseek-build-lane`,
`strip-omg-job`, plus ~28 older (08-27..08-29) crew-checkpoint branches.

### crew
0 open PRs. ~30 never-PR'ed branches — the heavy ones are **specs and rulings**:
`spec/otto-platform-v1`, `spec/otto-gateway-tenancy`, `docs/r75-enterprise-client-zero`,
`docs/ultimate-edict-full-text`, `docs/research-engine-spec-v1`,
`audit/rulings-implementation-gaps`, `rescued-work-20260830`. Founder records that never
reached main are exactly the "void" he banned.

### hermes-v2 (Otto)
14 never-PR'ed `otto/*` checkpoint branches (cp0-evals … cp6-obs, v1-hardening, w3-demo,
w4-onboard, kimi-primary). Later otto branches DID merge (event-gateway, ingress-entrypoint,
boot-surface, otto-tests-in-ci) — the checkpoints need a triage: superseded or lost work.

### Other repos, open PRs sitting
- **prospector #808** one-shot rebuild — active, plus 2 dependabot.
- **claude-estate**: 5 open, oldest from 2026-08-24 (LAW 24 estate-state commit, pi-bridge
  run-logging, executor primer, verification-layer hooks, founder-actions register).
- **claude-guards #240** (blind-session refusal — active today), **hermes-config** 4 (incl. a
  security-scan CI gate open since 08-25), **estate-secrets** 4 (secret-hygiene deletions,
  crew#227, and the sops encryption gate open since 08-24), **hermes-agent** 12 dependabot.

## 3. MacBook: work that exists nowhere but this laptop

- **20 worktrees with uncommitted tracked edits.** Worst: `.wt-kini-spec` (293 dirty files,
  since 08-26), `.wt-llm-image` (224), the main `idp/` checkout sitting on
  `feat/mumchimp-oneshot-rebuild` with 44 dirty files, `.wt-idp-ts-tag` (16), the `crew/`
  main checkout with 9 dirty science/board files.
- **~120 local idp branches ahead of or absent from origin.** Most are stale duplicates of
  remote branches; the ones that exist ONLY here and are recent:
  `feat/litellm-redis` (the Redis rebuild, above), `docs/provider-key-console-intake`
  (2026-09-03, no upstream), `rescue/research-scaffolding-3cda8e18`, `imgfix-celery`,
  `release/approved-wave-0902` (ahead 10), `feat/otto-staging` (ahead 11),
  `fiu` (ahead 24), `evidence/crew710-minimax-headers` (ahead 32),
  `bot/conscience-page` (ahead 48), `feat/crew684-alertmanager…door` (ahead 73),
  `fix/diagnose-shows-storage-and-pending-claims` (ahead 75).
- **`~/dev/code` itself is a git repo with NO remote** — checkpoint commits (7d01c8e) that
  would die with this Mac. LAW 24 violation as a standing state.
- crew local: unpushed `docs/r75-enterprise-client-zero`, `docs/speed-build-record` (ahead 6),
  `docs/ultimate-edict-full-text` (ahead 1) — more founder records not in the remote.

## 4. The pattern, named once

Three leaks, in order of loss risk:
1. **Mac-only work** (never pushed): dies with the laptop. Redis rebuild, founder-record docs,
   ~10 real local-only branches, 20 dirty worktrees.
2. **Pushed, never PR'ed** (~90 branches across repos): survives the laptop, invisible to the
   ship pipeline; nobody will ever merge what was never offered.
3. **Open PRs nobody is driving** (claude-estate since 08-24, hermes-config since 08-25,
   estate-secrets since 08-24): offered, then abandoned mid-door.

Standing rules already cover 1 and 2 (LAW 24, LAW 16 leave-a-path-back, R57 one push wave);
the audit shows they are not being closed out at session end. The enforcement gap — a
sweep that grades session-end state — is a decision for the founder, not another script
written tonight (headline rule 1).

## 5. One-word decisions queued for the founder
- **REDIS**: rebase `feat/litellm-redis`, PR it with the waiver design for your approval —
  or say TWO-REPLICAS and it returns in the 1192-compliant shape.
- **SPECS**: land the crew spec/ruling branches (otto-platform-v1, r75, ultimate-edict,
  research-engine) to crew main so the records leave the void.
- **TRIAGE**: the 42 idp never-PR'ed branches get a one-line verdict each (ship / close /
  superseded) — batched, one pass.
