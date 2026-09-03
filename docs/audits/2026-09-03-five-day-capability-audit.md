# Five-day capability audit — 2026-08-29 to 2026-09-03

Ordered by the founder 2026-09-03: "audit git now and tell me what we have and why we have not
packaged things properly, all things working on last 5 days... look at the board also as things
could be missing from git." Every claim below comes from git (origin/main of each repo, fetched
today) or from the crew board; nothing is from memory.

## 1. What we have (merged and running)

### The platform (idp) — 14 capabilities landed on main in 444 commits

1. **Signed verification layer** — services carry measured verdicts, not claims. Signed
   verdicts, a Langfuse prover, an append-only verdict table in Backstage Postgres, and a
   mutation harness proving every probe can fail. (a7c58801, 372d7cf6, cb20f57d;
   platform/verification, Flux-deployed.)
2. **Ops page and Tools page in the portal** — cluster tile, open reds with owners, drills,
   what waits on the founder, every door on one page. (3def8593, cf1d16f6, 4dc86884.)
3. **Otto on the cluster** — otto-golden deployment, Telegram gateway with vault-fed
   allowlist, registration reconciler, otto-parity drill, restore path. (7a672326, 2fbdd965,
   ee28b5ed; runbook, demo and onboarding pages exist.)
4. **Dagster scheduler on the cluster, off the Mac**, plus a Backstage catalog provider for
   it. (d3f9dbcd, 45a9ae2c, 397c1d96.)
5. **Superset dashboards behind the gateway**, Metabase removed (decision 0018); boardroom
   dashboard, spend breaker, alert fan-out; founder dashboards recovered from the old
   server's volume. (dbdbb85a, ce5a4947, 16b20c6e, ed1fdb92.)
6. **Bitwarden as the one human door for secrets** (decisions 0017/0019) — one dispatch
   bootstraps the estate; credentials federate from one human seed. (923d2305, 439ef969.)
7. **Green pull requests land themselves** — merge queue plus auto-deploy of image-tag-only
   changes. (ada48540, a97e23f9, 6d6c8908.)
8. **LLM router grown up** — Kimi provider, image lanes, embed lane, shared Redis memory,
   Groq removed; one vendor registry generates both router configs. (84260b86, c3ded211,
   bb22e525.)
9. **One place for every estate name (R70)** — a PR adding a hardcoded estate name is
   refused; drift graded every six hours. (2812c535, fddb6731.)
10. **Demos are code** — VHS tapes rendered by CI, every demo page gains a recording; a
    one-hour buyer sandbox. (cb76ead0, fc9d539c, e8e2608d.)
11. **Estate state document every session ingests** — produced every 15 minutes, served over
    MCP. (d4150125, 2ca4dd33; platform/estate-state.)
12. **Intent compiler (Diamond Standard)** — capability intents compiled deterministically.
    (fa988113; bin/intent-compile.) *Weakest packaging of the set: a script someone must
    invoke, nothing wires it into CI or Flux.*
13. **CI gates hardened** — kubeconform on rendered manifests, no-docs-no-merge, fast local
    hooks (R58), prose-pinning tests purged (R76), self-healing must name a circuit breaker.
14. **Estate inventory graded MANAGED/DRIFTED/ORPHAN/GHOST** and a generated incident
    register. (451ac590, a3bfec4d.)

### The products

- **hermes-v2**: Otto Platform v1 with six lanes (78e54b7, PR #62), Telegram buttons and
  voice (097fe9a), a universal event gateway (9fdff665, 3c2b68b), a 255-test CI suite
  (4ddde8d), a boot contract (b7158c7), kimi as primary (922fbc6).
- **prospector**: the mumchimp storefront shipped (7489661f, e428946b, a6223ef6, 3da7ac78,
  b6ce2fc6), the https-otto edge listener (6bf7783e), Superset wiring (bc985f18), orderable
  image tags (e1dbcd6a).

### The crew and estate repos

- crew: docs-gate, pr-evidence and self-scoring-floor gates (e75db6e, 1495914, 55a3847), the
  science lane (a410ce0, 8256b4d), the incident ledger (de7503b).
- estate: shared checks run in worktrees, bin/litellm-status, a guard that no vendor key ever
  leaves the laptop, agent role files naming router lanes.
- infra-crew: skeleton on main (e2ccd31); **queue mode is stranded on branch
  infra-crew/step-1-foundation** (c189891, 8e2f402), never merged.

Board delivery: 12 board items delivered in the window, roughly 45 still open.

## 2. What the board says exists but git does not hold

- crew#771: the SHOWCASE launchd job was **built but never installed** — the board says
  delivered, no machine runs it (the silent-green class).
- crew#780: Backstage UI work claimed on the board matches **no commit** in any repo.
- hermes-v2 untracked on disk: scripts/check-age-drill.sh, scripts/founder-blocked-watch.sh,
  a crew#751 incident test, the whole deploy/fly/ directory, and a modified config.yaml.
- idp uncommitted on disk: **67 files**, including a full portal redesign wave (DoorGrid.tsx,
  homeLayout.tsx, doorCopy.ts and ~25 modified home/nav/theme files), bin/idp-infra-crew-drill,
  decision docs 0014/0015, an Otto incident report.
- crew untracked: docs/FRAMEWORK_DEEP_DIVE.md, docs/product/, docs/rulings/R33, three specs.
- estate untracked: bin/estate-presence.
- **67 real working branches unmerged** on idp (plus 280 backup/rescue snapshots), including
  feat/portal-modern-home, feat/security-end-to-end, fix/otto-kimi-router-lane.

## 3. Why things are not packaged properly

One cause, four faces. **Work is called finished at "built", and nothing enforces the last
mile from built to installed.**

1. **The finish line is in the wrong place.** The Definition of Done already says merged code
   is inventory, not progress — but no gate makes a capability prove it is *installed and
   reachable* before its board item closes. That is exactly how #771 closed with a launchd
   job no machine runs, and how the intent compiler landed with nothing invoking it.
2. **The products never moved onto the platform's install road.** The estate has exactly one
   good delivery road — git push, Flux, the cluster, image automation rolling tags — and only
   idp platform services ride it. hermes-v2 still runs as a launchd job on one Mac with its
   deploy files untracked; prospector deploys through its own workflow. Each product keeps
   the bespoke hand-install it had before the road existed.
3. **Building outruns landing.** 67 branches and 67 uncommitted files is five days of real
   capability sitting outside main, in direct breach of the trunk-only rule (same-day merge
   or close) and of "load-bearing means in git". Sessions start the next capability before
   the last one lands.
4. **The board and git are not reconciled by a machine.** A board item can say delivered with
   no commit behind it (#780) because nothing cross-checks the two; the audit that caught it
   was ordered by hand today.

## 4. Why we are still installing our products this way

Because installation was never made a platform capability. The platform got the one install
road; the products (which predate it) were never onboarded, and no rule refuses a product
that installs by hand. So every product install is still the stitched thing the headline
bans: a launchd job here, a workflow there, an untracked deploy/ directory nobody can rebuild
from git.

## 5. The one answer

Stop building; land and onboard. In order: (1) commit the three on-disk waves (idp portal
redesign, hermes-v2 scripts and config, estate-presence) — they are load-bearing and only on
disk; (2) triage the 67 real branches same-day, merge or delete, per the trunk-only rule
already on the books; (3) onboard hermes-v2 and prospector onto the Flux road as catalogued
workloads, retiring the launchd/hand installs; (4) add the admission rule that closes the
class: a board item may not close, and a capability may not be announced, until a probe shows
it installed and answering. No new capability starts before these four are done — subject to
the founder's word, since starting anything new without it is barred.

---
Sources: two audit agents, 2026-09-03 ~13:0xZ — one over idp+estate git (origin/main
fetched), one over hermes-v2, prospector, crew, infra-crew git and the crew board. Repos were
read, not modified.
