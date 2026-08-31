# Worktree audit, 2026-08-31T14:58Z

Founder, 2026-08-31 ~15:20Z: "why do we have so many worktrees, we need an audit for missing work". Tracked as crew#745.

## The answer

- **433 worktrees** are registered across four repositories: idp 323, crew 58, prospector-main 36, hermes-v2 16.
- **Why:** every session is told to work in its own worktree (rule-guard command policy line 259; R57 local proof first), so each task makes one, and nothing removes it after its pull request merges. No hook, job or rung does that. The one cleanup script that exists (`~/.claude/scripts/estate/estate_worktree_cleanup.sh`, 2026-08-23) covers the prospector checkout only and is run by nothing.
- **Missing work:** 61 worktrees hold work that reached no pull request: 45 with uncommitted edits (4461 tracked files changed in total) and 16 with commits made after their pull request merged, or on a branch that never had one (39 commits). The table below names each one and the session that made it. 2 of the 61 are the state-branch writers (`.idp-state`, `.crew-state`); their edits are generated documents, not lost work.
- **What to do (one road):** run the existing cleanup script in report mode over all four repositories; it saves every uncommitted edit as a patch to object storage and compares it back byte for byte before it would remove anything. Nothing is removed until the founder says so. After that, a worktree is removed by the session that opened its pull request, on merge.

## Where they live

| Place | Worktrees | With missing work |
|---|---|---|
| ~/dev/code/.wt-* (hand-made by sessions) | 62 | 10 |
| ~/.claude/jobs (background job sessions) | 58 | 7 |
| session scratchpad 2d8b3bd0 | 52 | 2 |
| session scratchpad 14ed6c8b | 37 | 3 |
| session scratchpad f3f21d6e | 36 | 6 |
| session scratchpad 78caaa17 | 30 | 4 |
| session scratchpad a7b41022 | 29 | 4 |
| session scratchpad 41fd24d8 | 23 | 3 |
| ~/Documents/code | 19 | 9 |
| session scratchpad 09cd04a6 | 18 | 4 |
| <repo>/.claude/worktrees (EnterWorktree tool) | 18 | 1 |
| session scratchpad d5ae1960 | 17 | 2 |
| inside the repo checkout itself | 17 | 2 |
| ~/dev/code | 5 | 0 |
| session scratchpad 80471694 | 3 | 1 |
| ~/dev/code/.*-state (state-branch writers) | 2 | 2 |
| ~/.claude/state | 2 | 0 |
| <repo>/.worktrees | 2 | 1 |
| /private/tmp | 1 | 0 |
| /private/var | 1 | 0 |
| session scratchpad ef0354ef | 1 | 0 |

## Grades

| Grade | Count | Meaning |
|---|---|---|
| MERGED | 159 | branch has a merged pull request and no commit above its head |
| UNPUSHED | 118 | commits on no remote branch (most are the pre-squash originals of a merged pull request; the missing-work table separates the real ones) |
| EMPTY | 49 | clean and at origin/main, nothing on it |
| DIRTY | 45 | uncommitted edits to tracked files |
| PUSHED-NO-PR | 38 | branch is on GitHub, no pull request was ever opened |
| CLOSED | 13 | pull request closed without merging |
| OPEN | 10 | pull request open |
| GONE | 1 | registered but the directory is missing (`git worktree prune` clears it) |

## Work that reached no pull request (61 worktrees)

Uncommitted = tracked files with edits in no commit. Commits = commits above the newest merged pull-request head on that branch (or every local commit when the branch had no merged pull request). Made by = the session whose scratchpad or job directory holds it.

| Repo | Worktree | Branch | Uncommitted | Commits | Pull request | Last commit | Made by |
|---|---|---|---|---|---|---|---|
| crew | `~/dev/code/crew/.worktrees/agent-go-345` | agent-go/345 | 277 | 0 | #399 MERGED | 2026-08-27 | <repo>/.worktrees |
| crew | `~/dev/code/.crew-state` | (detached) | 4 | 0 | - | 2026-08-31 | ~/dev/code/.*-state (state-branch writers) |
| crew | `~/dev/code/.wt-crew72` | feat/crew72-ledger-in-warehouse | 3 | 0 | #410 MERGED | 2026-08-27 | ~/dev/code/.wt-* (hand-made by sessions) |
| crew | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/crew554pw` | feat/crew554-cron-delivery-per-workflow | 1 | 0 | #582 CLOSED | 2026-08-28 | session scratchpad 14ed6c8b |
| crew | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/rv559` | (detached) | 1 | 0 | - | 2026-08-28 | session scratchpad 78caaa17 |
| crew | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-108` | science/crew108-enforcement-map-50-laws | 1 | 0 | #602 CLOSED | 2026-08-28 | session scratchpad f3f21d6e |
| crew | `~/.claude/jobs/a0d64ea4/tmp/crewboard` | fix/board-cp-line-without-colon | 1 | 0 | #553 MERGED | 2026-08-28 | ~/.claude/jobs (background job sessions) |
| crew | `~/dev/code/.wt-crew-selfscore` | fix/self-scoring-banned | 1 | 0 | #731 MERGED | 2026-08-31 | ~/dev/code/.wt-* (hand-made by sessions) |
| idp | `~/dev/code/idp/.wt-vault-seed` | main | 1571 | 0 | - | 2026-08-31 | inside the repo checkout itself |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wteth` | feat/crew584-engineering-tenets | 527 | 0 | - | 2026-08-29 | ~/.claude/jobs (background job sessions) |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wt717` | feat/crew717-otto-powers | 313 | 1 | #1014 MERGED | 2026-08-30 | session scratchpad a7b41022 |
| idp | `~/dev/code/.wt-kini-spec` | docs/kini-master-spec | 293 | 0 | #59 MERGED | 2026-08-26 | ~/dev/code/.wt-* (hand-made by sessions) |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wtmon` | feat/crew684-alertmanager-and-prometheus-have-a-door | 245 | 3 | #977 CLOSED | 2026-08-31 | session scratchpad a7b41022 |
| idp | `~/dev/code/.wt-llm-image` | evidence/crew710-minimax-headers | 224 | 0 | #1012 OPEN | 2026-08-31 | ~/dev/code/.wt-* (hand-made by sessions) |
| idp | `scratchpad:09cd04a6-12cd-4d9b-84af-10b1620739d1/scratchpad/idp-docs` | feat/founder-docs-in-backstage | 213 | 0 | #288 MERGED | 2026-08-27 | session scratchpad 09cd04a6 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtcap` | feat/crew584-capacity-row | 76 | 1 | #687 MERGED | 2026-08-29 | ~/.claude/jobs (background job sessions) |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-robot` | fix/robot-commits-to-main | 20 | 0 | - | 2026-08-29 | session scratchpad f3f21d6e |
| idp | `~/dev/code/.wt-prclear` | fix/crew66-curl-double-drains-stdin | 4 | 0 | - | 2026-08-31 | ~/dev/code/.wt-* (hand-made by sessions) |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wt677` | fix/crew677-p1-injection-and-pin | 3 | 0 | - | 2026-08-30 | session scratchpad a7b41022 |
| idp | `~/dev/code/.wt-backstage-proof` | backstage-arm64 | 3 | 0 | - | 2026-08-25 | ~/dev/code/.wt-* (hand-made by sessions) |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/lawsrace` | fix/laws-guards-page-race | 2 | 0 | - | 2026-08-31 | session scratchpad 14ed6c8b |
| idp | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/trust` | spec/crew581-trust-instruments | 2 | 0 | #610 CLOSED | 2026-08-28 | session scratchpad 78caaa17 |
| idp | `~/dev/code/.wt-deploy` | fix/rollup-duplicate-runs | 2 | 0 | - | 2026-08-31 | ~/dev/code/.wt-* (hand-made by sessions) |
| idp | `~/dev/code/.wt-idp-656` | feat/crew656-canary-ledger | 2 | 0 | - | 2026-08-31 | ~/dev/code/.wt-* (hand-made by sessions) |
| idp | `~/dev/code/.wt-otto` | fix/rego-review-silent-greens | 2 | 0 | #904 MERGED | 2026-08-30 | ~/dev/code/.wt-* (hand-made by sessions) |
| idp | `~/dev/code/idp/.claude/worktrees/.idp-state` | (detached) | 2 | 0 | - | 2026-08-27 | <repo>/.claude/worktrees (EnterWorktree tool) |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/wt645` | feat/crew290-github-escrow | 1 | 1 | #645 MERGED | 2026-08-29 | session scratchpad 14ed6c8b |
| idp | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wt687` | feat/crew584-capacity-row | 1 | 1 | #687 MERGED | 2026-08-29 | session scratchpad 41fd24d8 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/.idp-state` | (detached) | 1 | 1 | - | 2026-08-30 | session scratchpad a7b41022 |
| idp | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wtdrill` | fix/crew626-langfuse-id-token-true | 1 | 0 | #810 MERGED | 2026-08-29 | session scratchpad 41fd24d8 |
| idp | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wtux` | feat/idp780-helm-retry-hourly | 1 | 0 | - | 2026-08-29 | session scratchpad 41fd24d8 |
| idp | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/bsha` | fix/crew539-catalogue-survives-a-node-drain | 1 | 0 | #545 MERGED | 2026-08-28 | session scratchpad 78caaa17 |
| idp | `scratchpad:d5ae1960-819d-42a8-8a5c-3521ab2550fd/idpcap` | feat/crew66-agent-names-a-capability-not-a-vendor | 1 | 0 | - | 2026-08-28 | session scratchpad d5ae1960 |
| idp | `~/dev/code/.idp-state` | (detached) | 1 | 0 | - | 2026-08-28 | ~/dev/code/.*-state (state-branch writers) |
| idp | `~/dev/code/idp/.wt-idp-blind` | fix/breakglass-blind-verdict | 1 | 0 | #1073 OPEN | 2026-08-31 | inside the repo checkout itself |
| idp | `scratchpad:09cd04a6-12cd-4d9b-84af-10b1620739d1/scratchpad/wtp27` | (detached) | 0 | 11 | - | 2026-08-25 | session scratchpad 09cd04a6 |
| idp | `scratchpad:80471694-3138-4645-a870-868210b81120/scratchpad/wt-idp` | feat/crew639-cp1-messaging-spec | 0 | 3 | #838 MERGED | 2026-08-29 | session scratchpad 80471694 |
| idp | `scratchpad:09cd04a6-12cd-4d9b-84af-10b1620739d1/scratchpad/idp-k8s` | feat/founder-kubernetes-tab | 0 | 2 | #290 MERGED | 2026-08-27 | session scratchpad 09cd04a6 |
| idp | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/idp495` | (detached) | 0 | 2 | - | 2026-08-27 | session scratchpad 78caaa17 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-diag` | fix/diagnose-shows-storage-and-pending-claims | 0 | 2 | #699 CLOSED | 2026-08-29 | session scratchpad f3f21d6e |
| idp | `scratchpad:09cd04a6-12cd-4d9b-84af-10b1620739d1/scratchpad/wtp84` | (detached) | 0 | 1 | - | 2026-08-27 | session scratchpad 09cd04a6 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtall` | feat/crew618-set-root-all | 0 | 1 | #749 MERGED | 2026-08-29 | session scratchpad 2d8b3bd0 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtgp` | feat/crew627-python-golden-path | 0 | 1 | - | 2026-08-30 | session scratchpad 2d8b3bd0 |
| idp | `scratchpad:d5ae1960-819d-42a8-8a5c-3521ab2550fd/fluximg` | (detached) | 0 | 1 | - | 2026-08-28 | session scratchpad d5ae1960 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-gq` | fix/no-script-under-bin-pipes-into-grep-q | 0 | 1 | #793 MERGED | 2026-08-29 | session scratchpad f3f21d6e |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-render` | fix/namespaces-never-pruned | 0 | 1 | #686 MERGED | 2026-08-29 | session scratchpad f3f21d6e |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-roll` | fix/roll-catalogue-to-current-main | 0 | 1 | #706 MERGED | 2026-08-29 | session scratchpad f3f21d6e |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wt619` | fix619 | 0 | 1 | - | 2026-08-28 | ~/.claude/jobs (background job sessions) |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtbm` | feat/crew584-bdd-matrix | 0 | 1 | #641 MERGED | 2026-08-28 | ~/.claude/jobs (background job sessions) |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtcred` | feat/crew66-portal-lane-token | 0 | 1 | - | 2026-08-30 | ~/.claude/jobs (background job sessions) |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtes` | feat/crew290-github-escrow | 0 | 1 | #645 MERGED | 2026-08-29 | ~/.claude/jobs (background job sessions) |
| prospector-main | `~/Documents/code/wt-site-pr` | (detached) | 579 | 0 | - | 2026-08-19 | ~/Documents/code |
| prospector-main | `~/Documents/code/wt-imgflows` | fix/image-must-carry-github-workflows | 23 | 0 | - | 2026-08-20 | ~/Documents/code |
| prospector-main | `~/Documents/code/wt-pipeline` | incident/2026-08-20-deletion | 20 | 0 | - | 2026-08-20 | ~/Documents/code |
| prospector-main | `~/Documents/code/wt-deploy-buttons` | (detached) | 15 | 0 | - | 2026-08-20 | ~/Documents/code |
| prospector-main | `~/Documents/code/wt-automerge-dispatch` | ci/automerge-dispatch-before-sweep | 8 | 0 | - | 2026-08-20 | ~/Documents/code |
| prospector-main | `~/Documents/code/wt-ledger` | (detached) | 5 | 0 | - | 2026-08-20 | ~/Documents/code |
| prospector-main | `~/Documents/code/wt-mainfence` | (detached) | 5 | 0 | - | 2026-08-19 | ~/Documents/code |
| prospector-main | `~/Documents/code/wt-firstrun` | web/every-pack-two-clicks | 2 | 0 | - | 2026-08-21 | ~/Documents/code |
| prospector-main | `~/dev/code/.wt-pros-audit` | fix/store-web-npm-audit | 1 | 0 | - | 2026-08-25 | ~/dev/code/.wt-* (hand-made by sessions) |
| prospector-main | `~/Documents/code/wt-engine100x` | int-land-index-fix | 1 | 0 | - | 2026-08-20 | ~/Documents/code |

## How each row was graded

Read-only, from the Mac, 2026-08-31 14:18Z to 14:55Z (Mac load 740 the whole time). Per repository: `git worktree list --porcelain` and one `gh pr list --state all --json headRefName,headRefOid,number,state`. Per worktree: `git status --porcelain --untracked-files=no` (uncommitted), `git rev-list --count origin/main..HEAD` (ahead), `git rev-list HEAD --not --remotes` (commits on no remote), `git log -1 --format=%cs` (last commit). A commit that is the head of a merged pull request is merged, and so is everything below it; only commits above it count as missing (a squash-merged branch whose remote branch was deleted otherwise reads as unpushed). The scripts and the row data ship next to this file: `worktree-audit.py`, `worktree-refine.py`, `worktrees.jsonl`.

Not measured: untracked files (a new file never added to git is not in this count); worktrees of repositories outside these four; whether a commit's content reached main by another branch.


## Every worktree (433 rows)

| Repo | Worktree | Branch | Grade | Uncommitted | Commits missing | Pull request | Last commit |
|---|---|---|---|---|---|---|---|
| crew | `scratchpad:09cd04a6-12cd-4d9b-84af-10b1620739d1/scratchpad/wt-prod` | code-crew320-worktree-copy-is-not-a-producer | CLOSED | 0 | 0 | #556 CLOSED | 2026-08-28 |
| crew | `scratchpad:09cd04a6-12cd-4d9b-84af-10b1620739d1/scratchpad/wt371` | feat/crew371-spend-by-model | MERGED | 0 | 0 | #546 MERGED | 2026-08-28 |
| crew | `scratchpad:09cd04a6-12cd-4d9b-84af-10b1620739d1/scratchpad/wt558` | feat/crew558-bootstrap-ceiling | MERGED | 0 | 0 | #559 MERGED | 2026-08-28 |
| crew | `scratchpad:09cd04a6-12cd-4d9b-84af-10b1620739d1/scratchpad/wt558cp4` | feat/crew558-cluster-live-from-ci | MERGED | 0 | 0 | #563 MERGED | 2026-08-28 |
| crew | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/crew554pw` | feat/crew554-cron-delivery-per-workflow | DIRTY | 1 | 0 | #582 CLOSED | 2026-08-28 |
| crew | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/crewcd` | cp1 | EMPTY | 0 | 0 | - | 2026-08-28 |
| crew | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/detach` | fix/crew437-detached-checkout-moves | MERGED | 0 | 0 | #591 MERGED | 2026-08-28 |
| crew | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/pskew` | fix/crew583-the-portability-row-cannot-go-green-on-a-dead-clock | CLOSED | 0 | 0 | #587 CLOSED | 2026-08-28 |
| crew | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/psy` | docs/crew598-operator-clinical-note | CLOSED | 0 | 0 | #599 CLOSED | 2026-08-28 |
| crew | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/wtdocs` | fix/docs-name-paths-that-exist | MERGED | 0 | 0 | #616 MERGED | 2026-08-29 |
| crew | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/wtstate` | fix/crew488-snapshot-lost-the-ready-count | MERGED | 0 | 0 | #615 MERGED | 2026-08-29 |
| crew | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/r591` | (detached) | PUSHED-NO-PR | 0 | 0 | - | 2026-08-28 |
| crew | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtcrew` | feat/crew701-cp1-first-run-fixes | MERGED | 0 | 0 | #712 MERGED | 2026-08-30 |
| crew | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtml` | fix/crew701-mlflow-sqlite | MERGED | 0 | 0 | #714 MERGED | 2026-08-30 |
| crew | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtprod` | feat/product-function | MERGED | 0 | 0 | #610 MERGED | 2026-08-29 |
| crew | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wt629c` | feat/crew629-cp2-template | MERGED | 0 | 0 | #635 MERGED | 2026-08-29 |
| crew | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wtcrew` | fix/crew626-cp19-accept-when | MERGED | 0 | 0 | #634 MERGED | 2026-08-29 |
| crew | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/cs` | docs/crew516-report-correction | MERGED | 0 | 0 | #519 MERGED | 2026-08-27 |
| crew | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/cs2` | fix/crew519-pr-evidence-fenced-heading | UNPUSHED | 0 | 0 | #521 MERGED | 2026-08-27 |
| crew | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/rv559` | (detached) | DIRTY | 1 | 0 | - | 2026-08-28 |
| crew | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/rv563` | (detached) | PUSHED-NO-PR | 0 | 0 | - | 2026-08-28 |
| crew | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/rv569` | (detached) | PUSHED-NO-PR | 0 | 0 | - | 2026-08-28 |
| crew | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/wt510` | (detached) | PUSHED-NO-PR | 0 | 0 | - | 2026-08-27 |
| crew | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/wt511` | (detached) | PUSHED-NO-PR | 0 | 0 | - | 2026-08-27 |
| crew | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wtcrew631cp4` | feat/crew631-cp4-false-success | MERGED | 0 | 0 | #637 MERGED | 2026-08-29 |
| crew | `scratchpad:ef0354ef-fa6b-4b6b-a5e2-5d6f7889b3b8/scratchpad/wt-crew-audit` | docs/worktree-audit-2026-08-31 | EMPTY | 0 | 0 | - | 2026-08-31 |
| crew | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/crew612` | chore/no-peer-review-gate | MERGED | 0 | 0 | #614 MERGED | 2026-08-29 |
| crew | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-108` | science/crew108-enforcement-map-50-laws | DIRTY | 1 | 0 | #602 CLOSED | 2026-08-28 |
| crew | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-16` | docs/crew596-decision-rights | CLOSED | 0 | 0 | #600 CLOSED | 2026-08-28 |
| crew | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-c2` | chore/crew63-c2-metric-after | MERGED | 0 | 0 | #621 MERGED | 2026-08-29 |
| crew | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-crewdocs` | docs/adr0002-diataxis-sweep | CLOSED | 0 | 0 | #605 CLOSED | 2026-08-28 |
| crew | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-r49` | guard/r49-pr-evidence-no-secret-value | CLOSED | 0 | 0 | #601 CLOSED | 2026-08-28 |
| crew | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-spec` | spec/crew568-migration | CLOSED | 0 | 0 | #617 CLOSED | 2026-08-29 |
| crew | `~/.claude/jobs/a0d64ea4/tmp/crew139` | science/control-plane-research | MERGED | 0 | 0 | #139 MERGED | 2026-08-27 |
| crew | `~/.claude/jobs/a0d64ea4/tmp/crew206` | science/cluster-cost-ledger | MERGED | 0 | 0 | #206 MERGED | 2026-08-27 |
| crew | `~/.claude/jobs/a0d64ea4/tmp/crew537` | feat/crew537-cp4-ideas-rows | MERGED | 0 | 0 | #551 MERGED | 2026-08-28 |
| crew | `~/.claude/jobs/a0d64ea4/tmp/crew537b` | feat/crew537-cp5-first-idea | MERGED | 0 | 0 | #552 MERGED | 2026-08-28 |
| crew | `~/.claude/jobs/a0d64ea4/tmp/crewboard` | fix/board-cp-line-without-colon | DIRTY | 1 | 0 | #553 MERGED | 2026-08-28 |
| crew | `~/.claude/state/crew-science-worktree` | (detached) | EMPTY | 0 | 0 | - | 2026-08-31 |
| crew | `~/.claude/state/crew-snapshot-worktree` | (detached) | EMPTY | 0 | 0 | - | 2026-08-31 |
| crew | `~/dev/code/.crew-state` | (detached) | DIRTY | 4 | 0 | - | 2026-08-31 |
| crew | `~/dev/code/.wt-c90b` | fix/crew90-science-collect-runs-mains-code | UNPUSHED | 0 | 0 | #501 MERGED | 2026-08-27 |
| crew | `~/dev/code/.wt-crew-crewai` | docs/audits-20260831 | MERGED | 0 | 0 | #735 MERGED | 2026-08-31 |
| crew | `~/dev/code/.wt-crew-docs-gate` | feat/dspy-instructor | OPEN | 0 | 0 | #738 OPEN | 2026-08-31 |
| crew | `~/dev/code/.wt-crew-selfscore` | fix/self-scoring-banned | DIRTY | 1 | 0 | #731 MERGED | 2026-08-31 |
| crew | `~/dev/code/.wt-crew-vl` | ci/vendor-lock-gate | MERGED | 0 | 0 | #274 MERGED | 2026-08-26 |
| crew | `~/dev/code/.wt-crew655` | feat/crew655-body-lint | PUSHED-NO-PR | 0 | 0 | - | 2026-08-30 |
| crew | `~/dev/code/.wt-crew656-spec` | fix/crew656-spec-file | OPEN | 0 | 0 | #728 OPEN | 2026-08-31 |
| crew | `~/dev/code/.wt-crew72` | feat/crew72-ledger-in-warehouse | DIRTY | 3 | 0 | #410 MERGED | 2026-08-27 |
| crew | `~/dev/code/.wt-research-worker` | research/gpt-researcher-worker | MERGED | 0 | 0 | #672 MERGED | 2026-08-30 |
| crew | `~/dev/code/crew/.claude/worktrees/crew70-no-payer-emails` | fix/crew70-no-payer-emails | MERGED | 0 | 0 | #414 MERGED | 2026-08-27 |
| crew | `~/dev/code/crew/.claude/worktrees/standards-llm` | fix/crew66-standards-llm-row | MERGED | 0 | 0 | #534 MERGED | 2026-08-27 |
| crew | `~/dev/code/crew/.worktrees/agent-go-275` | agent-go/275 | PUSHED-NO-PR | 0 | 0 | - | 2026-08-25 |
| crew | `~/dev/code/crew/.worktrees/agent-go-345` | agent-go/345 | DIRTY | 277 | 0 | #399 MERGED | 2026-08-27 |
| crew | `~/dev/code/crew/.wt-lanes` | docs/lanes-crew-40 | MERGED | 0 | 0 | #330 MERGED | 2026-08-26 |
| crew | `~/dev/code/crew/.wt-opmodel` | feat/opmodel-gate | UNPUSHED | 0 | 0 | #294 MERGED | 2026-08-26 |
| crew | `~/dev/code/crew/.wt-stale` | ci/stale-pr-policy | CLOSED | 0 | 0 | #305 CLOSED | 2026-08-26 |
| crew | `~/dev/code/crew/r591` | (detached) | PUSHED-NO-PR | 0 | 0 | - | 2026-08-28 |
| hermes-v2 | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtsummary` | fix/telegram-rich-summary-card | MERGED | 0 | 0 | #53 MERGED | 2026-08-30 |
| hermes-v2 | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/hsig` | fix/crew570-hermes-signature-findable | MERGED | 0 | 0 | #47 MERGED | 2026-08-28 |
| hermes-v2 | `scratchpad:80471694-3138-4645-a870-868210b81120/scratchpad/hv2` | fix/crew561-exec-bits-existing-volume | MERGED | 0 | 0 | #51 MERGED | 2026-08-30 |
| hermes-v2 | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wt561h` | feat/crew561-estate-mcp | OPEN | 0 | 0 | #57 OPEN | 2026-08-30 |
| hermes-v2 | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wt717h` | feat/crew717-otto-powers | OPEN | 0 | 0 | #58 OPEN | 2026-08-30 |
| hermes-v2 | `scratchpad:d5ae1960-819d-42a8-8a5c-3521ab2550fd/h2` | fix/crew516-image-carries-the-provider-sdk | MERGED | 0 | 0 | #44 MERGED | 2026-08-28 |
| hermes-v2 | `scratchpad:d5ae1960-819d-42a8-8a5c-3521ab2550fd/hermesbase` | (detached) | EMPTY | 0 | 0 | - | 2026-08-28 |
| hermes-v2 | `scratchpad:d5ae1960-819d-42a8-8a5c-3521ab2550fd/hermesmac` | fix/crew516-verify-row10-no-local-gateway | CLOSED | 0 | 0 | #46 CLOSED | 2026-08-28 |
| hermes-v2 | `scratchpad:d5ae1960-819d-42a8-8a5c-3521ab2550fd/scratchpad/hv2-img` | feat/crew516-cp4-image-carries-the-estate | UNPUSHED | 0 | 0 | #40 MERGED | 2026-08-27 |
| hermes-v2 | `scratchpad:d5ae1960-819d-42a8-8a5c-3521ab2550fd/scratchpad/hv2-main` | feat/crew524-cp2-evolution-lane | MERGED | 0 | 0 | #41 MERGED | 2026-08-27 |
| hermes-v2 | `scratchpad:d5ae1960-819d-42a8-8a5c-3521ab2550fd/scratchpad/hv2-sign` | fix/crew516-cosign-sign-retry | GONE | 0 | 0 | - |  |
| hermes-v2 | `~/dev/code/.wt-hermes-audit` | fix/npm-audit-high | UNPUSHED | 0 | 0 | #9 MERGED | 2026-08-25 |
| hermes-v2 | `~/dev/code/.wt-hermes-crew66` | crew66-remove-fly-target | PUSHED-NO-PR | 0 | 0 | - | 2026-08-26 |
| hermes-v2 | `~/dev/code/.wt-hermes-p0` | fix/crew736-cp2-boot-contract | EMPTY | 0 | 0 | - | 2026-08-30 |
| hermes-v2 | `~/dev/code/.wt-hermes-readme` | estate/security-scan | UNPUSHED | 0 | 0 | #8 MERGED | 2026-08-25 |
| hermes-v2 | `~/dev/code/.wt-hermes-ssh` | feat/crew561-ssh-client | MERGED | 0 | 0 | #50 MERGED | 2026-08-29 |
| idp | `scratchpad:09cd04a6-12cd-4d9b-84af-10b1620739d1/scratchpad/idp-cs` | fix/crew388-otel-agent-psa-namespace | UNPUSHED | 0 | 0 | #309 MERGED | 2026-08-27 |
| idp | `scratchpad:09cd04a6-12cd-4d9b-84af-10b1620739d1/scratchpad/idp-docs` | feat/founder-docs-in-backstage | DIRTY | 213 | 0 | #288 MERGED | 2026-08-27 |
| idp | `scratchpad:09cd04a6-12cd-4d9b-84af-10b1620739d1/scratchpad/idp-k8s` | feat/founder-kubernetes-tab | UNPUSHED | 0 | 2 | #290 MERGED | 2026-08-27 |
| idp | `scratchpad:09cd04a6-12cd-4d9b-84af-10b1620739d1/scratchpad/idp-r4` | feat/founder-surface-source-gate | UNPUSHED | 0 | 0 | #294 MERGED | 2026-08-27 |
| idp | `scratchpad:09cd04a6-12cd-4d9b-84af-10b1620739d1/scratchpad/idp-tc` | fix/telemetry-coverage-print-errors | MERGED | 0 | 0 | #285 MERGED | 2026-08-27 |
| idp | `scratchpad:09cd04a6-12cd-4d9b-84af-10b1620739d1/scratchpad/wt-sweep` | code-graphify-findings-exit | MERGED | 0 | 0 | #546 MERGED | 2026-08-28 |
| idp | `scratchpad:09cd04a6-12cd-4d9b-84af-10b1620739d1/scratchpad/wt131` | identity-commerce-mesh | MERGED | 0 | 0 | #131 MERGED | 2026-08-28 |
| idp | `scratchpad:09cd04a6-12cd-4d9b-84af-10b1620739d1/scratchpad/wt307` | code-crew307-drill-identity-equals-founder | MERGED | 0 | 0 | #554 MERGED | 2026-08-28 |
| idp | `scratchpad:09cd04a6-12cd-4d9b-84af-10b1620739d1/scratchpad/wt477` | (detached) | UNPUSHED | 0 | 0 | - | 2026-08-27 |
| idp | `scratchpad:09cd04a6-12cd-4d9b-84af-10b1620739d1/scratchpad/wtp246` | crew344-generated-alert-coverage | MERGED | 0 | 0 | #246 MERGED | 2026-08-27 |
| idp | `scratchpad:09cd04a6-12cd-4d9b-84af-10b1620739d1/scratchpad/wtp27` | (detached) | UNPUSHED | 0 | 11 | - | 2026-08-25 |
| idp | `scratchpad:09cd04a6-12cd-4d9b-84af-10b1620739d1/scratchpad/wtp84` | (detached) | UNPUSHED | 0 | 1 | - | 2026-08-27 |
| idp | `scratchpad:09cd04a6-12cd-4d9b-84af-10b1620739d1/scratchpad/wtp87` | (detached) | UNPUSHED | 0 | 0 | - | 2026-08-27 |
| idp | `scratchpad:09cd04a6-12cd-4d9b-84af-10b1620739d1/scratchpad/wtp91` | (detached) | EMPTY | 0 | 0 | - | 2026-08-27 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/chaosfix` | fix/chaos-workflow-duration-forbidden | PUSHED-NO-PR | 0 | 0 | - | 2026-08-29 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/consc` | fix/crew583-a-dead-clock-cannot-call-stale-research-fresh | MERGED | 0 | 0 | #621 MERGED | 2026-08-28 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/drills` | fix/every-scheduled-workflow-is-graded | EMPTY | 0 | 0 | - | 2026-08-29 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/founder` | fix/crew583-cp5-founder-page-clock | MERGED | 0 | 0 | #623 MERGED | 2026-08-28 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/goauth` | fix/store-google-oauth-registry | MERGED | 0 | 0 | #1033 MERGED | 2026-08-31 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/identity` | feat/customer-identity-keycloak | OPEN | 0 | 0 | #1066 OPEN | 2026-08-31 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/idp-research` | feat/research-worker-spike | EMPTY | 0 | 0 | - | 2026-08-30 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/idp-rollout` | fix/storefront-image-reaches-the-cluster | MERGED | 0 | 0 | #1023 MERGED | 2026-08-31 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/lawsrace` | fix/laws-guards-page-race | DIRTY | 2 | 0 | - | 2026-08-31 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/next` | fix/crew583-cp6-estate-next-clock | EMPTY | 0 | 0 | - | 2026-08-28 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/pog` | fix/push-on-green-unknown-merge-state | MERGED | 0 | 0 | #857 MERGED | 2026-08-29 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/shopbackup` | feat/shop-db-offsite-backup | MERGED | 0 | 0 | #1056 MERGED | 2026-08-31 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/skew2` | fix/crew583-a-clock-behind-the-receipt-is-not-freshness | MERGED | 0 | 0 | #612 MERGED | 2026-08-28 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/surge` | fix/crew583-a-node-is-not-deleted-on-a-runners-clock | MERGED | 0 | 0 | #622 MERGED | 2026-08-28 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/tsacl` | fix/crew562-the-acl-locks-the-founder-out-of-his-own-mac | MERGED | 0 | 0 | #606 MERGED | 2026-08-28 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/wt488` | feat/crew488-named-object-closure-guard | MERGED | 0 | 0 | #654 MERGED | 2026-08-29 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/wt51` | crew584/law51-judges-new-prs | MERGED | 0 | 0 | #738 MERGED | 2026-08-29 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/wt623` | wip/crew583-cp5-rebase | EMPTY | 0 | 0 | - | 2026-08-29 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/wt645` | feat/crew290-github-escrow | DIRTY | 1 | 1 | #645 MERGED | 2026-08-29 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/wt648` | wip/crew488-cp5-merge-main | PUSHED-NO-PR | 0 | 0 | - | 2026-08-29 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/wtcp6` | feat/crew488-cp6-oci-cli-pip-cache | MERGED | 0 | 0 | #662 MERGED | 2026-08-29 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/wtfloor` | crew488/floor-9-to-10 | MERGED | 0 | 0 | #736 MERGED | 2026-08-29 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/wtidocs` | fix/docs-name-paths-that-exist | MERGED | 0 | 0 | #701 MERGED | 2026-08-29 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/wtlint` | fix/lint-debt-blocking-precommit | MERGED | 0 | 0 | #683 MERGED | 2026-08-29 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/wtmain` | (detached) | EMPTY | 0 | 0 | - | 2026-08-28 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/wtmainred` | fix/crew612-main-red-founder-screen-description | MERGED | 0 | 0 | #672 MERGED | 2026-08-29 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/wtpeer` | (detached) | PUSHED-NO-PR | 0 | 0 | - | 2026-08-28 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/wtpre` | (detached) | PUSHED-NO-PR | 0 | 0 | - | 2026-08-28 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/wtratchet` | fix/crew488-drill-can-still-beat-the-floor | MERGED | 0 | 0 | #682 MERGED | 2026-08-29 |
| idp | `scratchpad:14ed6c8b-f0a9-40d7-82a8-895f336f9b78/scratchpad/wtsurge` | fix/crew583-surge-node-clock | PUSHED-NO-PR | 0 | 0 | - | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/r623` | (detached) | EMPTY | 0 | 0 | - | 2026-08-28 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wt568` | feat/crew568-phase5-hermes-key | UNPUSHED | 0 | 0 | #815 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wt568b` | feat/crew568-delivery-push-is-loud | UNPUSHED | 0 | 0 | #821 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wt583` | feat/crew583-cp2-cluster-state-telemetry | UNPUSHED | 0 | 0 | #739 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wt586` | feat/crew66-tailscale-mint-by-api | MERGED | 0 | 0 | #624 MERGED | 2026-08-28 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wt606` | (detached) | EMPTY | 0 | 0 | - | 2026-08-28 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wt607` | feat/crew607-cp1-pr-age | MERGED | 0 | 0 | #652 MERGED | 2026-08-28 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wt607c` | feat/crew607-sweep-app-lane | PUSHED-NO-PR | 0 | 0 | - | 2026-08-28 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wt620` | feat/crew620-cp2-shell-ci | PUSHED-NO-PR | 0 | 0 | - | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wt620-baseline` | (detached) | EMPTY | 0 | 0 | - | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wt625` | fix/crew625-ghcr-pull-restore | UNPUSHED | 0 | 0 | #799 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtall` | feat/crew618-set-root-all | UNPUSHED | 0 | 1 | #749 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtbs` | fix/diagnose-backstage-log | PUSHED-NO-PR | 0 | 0 | - | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtcat` | fix/crew624-catalogue-publishes-again | UNPUSHED | 0 | 0 | #798 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtcat2` | fix/crew624-dispatch-default-commit | CLOSED | 0 | 0 | #802 CLOSED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtcf` | feat/crew66-cloudflare-root-is-a-named-secret | UNPUSHED | 0 | 0 | #746 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtcur` | feat/crew659-cursor-is-a-provider-root | OPEN | 0 | 0 | #973 OPEN | 2026-08-30 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtdoors` | feat/crew612-doors-first | MERGED | 0 | 0 | #871 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtedge` | feat/edge-manners | MERGED | 0 | 0 | #695 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtemb` | fix/crew659-embed-lane-survives-an-empty-google-account | UNPUSHED | 0 | 0 | #950 MERGED | 2026-08-30 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtfed` | feat/crew66-tailscale-federated-identity | UNPUSHED | 0 | 0 | #754 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtfed2` | fix/crew66-federated-exchange-answer-is-checked | UNPUSHED | 0 | 0 | #763 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtfix` | fix/crew584-timing-rung-at-least-3s | UNPUSHED | 0 | 0 | #757 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtgp` | feat/crew627-python-golden-path | UNPUSHED | 0 | 1 | - | 2026-08-30 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wthub` | feat/crew624-cluster-in-catalogue | UNPUSHED | 0 | 0 | #792 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtk8s` | feat/k8sgpt-reads-to-telegram | MERGED | 0 | 0 | #696 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtk8s2` | fix/k8sgpt-secret-env-exception-and-unapplied-revision | UNPUSHED | 0 | 0 | #733 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtk8s3` | feat/k8sgpt-analyzer-requests | UNPUSHED | 0 | 0 | #740 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtk8seyes` | fix/founder-dm-is-not-an-alert-sink | UNPUSHED | 0 | 0 | #732 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtkey` | fix/router-key-widens-lanes | MERGED | 0 | 0 | #999 MERGED | 2026-08-30 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtns` | fix/crew648-namespace-unstick | MERGED | 0 | 0 | #688 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtotto` | feat/k8sgpt-findings-in-the-receipt | MERGED | 0 | 0 | #704 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtpage` | fix/crew618-set-root-trust-credentials | UNPUSHED | 0 | 0 | #752 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtpolish` | feat/crew612-portal-hierarchy-and-visuals | UNPUSHED | 0 | 0 | #850 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtpy` | feat/crew620-cp4-python-ci | UNPUSHED | 0 | 0 | #781 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtscan` | fix/security-scan-per-file-fallback | UNPUSHED | 0 | 0 | #993 MERGED | 2026-08-30 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtsci` | feat/crew659-science-router-key | UNPUSHED | 0 | 0 | #938 MERGED | 2026-08-30 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtseed` | feat/crew66-tailscale-seed-from-repo-secret | UNPUSHED | 0 | 0 | #742 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtsso` | fix/crew503-next-auth-route | MERGED | 0 | 0 | #665 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtsub` | fix/crew66-federated-subject-is-immutable | UNPUSHED | 0 | 0 | #773 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtts` | feat/crew66-federated-from-code | UNPUSHED | 0 | 0 | #779 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtv` | feat/crew66-vendor-roots-are-named-secrets | UNPUSHED | 0 | 0 | #748 MERGED | 2026-08-29 |
| idp | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtview` | feat/crew624-cp1-estate-view | UNPUSHED | 0 | 0 | #795 MERGED | 2026-08-29 |
| idp | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wt379` | fix/crew301-login-drill-red-is-readable-and-green-closes | MERGED | 0 | 0 | #728 MERGED | 2026-08-29 |
| idp | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wt687` | feat/crew584-capacity-row | DIRTY | 1 | 1 | #687 MERGED | 2026-08-29 |
| idp | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wt692` | feat/crew584-optimised-gate | MERGED | 0 | 0 | #692 MERGED | 2026-08-29 |
| idp | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wt808` | fix/crew626-drill-clicks-the-langfuse-sso-button | MERGED | 0 | 0 | #808 MERGED | 2026-08-29 |
| idp | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wtadr` | docs/adr-0012-staging-options-and-cost | UNPUSHED | 0 | 0 | #839 MERGED | 2026-08-29 |
| idp | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wtbump` | fix/image-bump-lands | UNPUSHED | 0 | 0 | #744 MERGED | 2026-08-29 |
| idp | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wtci` | fix/idp-ci-skips-directories-in-bin | UNPUSHED | 0 | 0 | #851 MERGED | 2026-08-29 |
| idp | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wtcore` | fix/crew626-langfuse-one-core | UNPUSHED | 0 | 0 | #835 MERGED | 2026-08-29 |
| idp | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wtcp1` | fix/crew626-cp1-layer-not-thing | UNPUSHED | 0 | 0 | #814 MERGED | 2026-08-29 |
| idp | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wtcpk` | feat/crew584-cpk-request-pr-flips-the-switch | MERGED | 0 | 0 | #730 MERGED | 2026-08-29 |
| idp | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wtdiag` | fix/crew626-langfuse-auth-log | UNPUSHED | 0 | 0 | #820 MERGED | 2026-08-29 |
| idp | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wtdrill` | fix/crew626-langfuse-id-token-true | DIRTY | 1 | 0 | #810 MERGED | 2026-08-29 |
| idp | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wthome` | feat/crew307-home-quick-find | UNPUSHED | 0 | 0 | #743 MERGED | 2026-08-29 |
| idp | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wtlf` | fix/crew626-langfuse-web-boot-outlives-the-probe | PUSHED-NO-PR | 0 | 0 | - | 2026-08-29 |
| idp | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wtmain` | feat/crew584-staging-namespace | MERGED | 0 | 0 | #846 MERGED | 2026-08-29 |
| idp | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wtpolish` | feat/crew459-portal-super-polish | UNPUSHED | 0 | 0 | #747 MERGED | 2026-08-29 |
| idp | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wtten` | feat/crew584-engineering-tenets | PUSHED-NO-PR | 0 | 0 | - | 2026-08-29 |
| idp | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wtux` | feat/idp780-helm-retry-hourly | DIRTY | 1 | 0 | - | 2026-08-29 |
| idp | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wtva` | feat/crew584-vault-audit-scheduled | MERGED | 0 | 0 | #737 MERGED | 2026-08-29 |
| idp | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wtvr` | fix/crew584-vault-reads-out-of-oke-check | MERGED | 0 | 0 | #734 MERGED | 2026-08-29 |
| idp | `scratchpad:41fd24d8-96a0-417e-bc3f-b7b15aceb026/scratchpad/wtword` | fix/crew626-front-page-says-service | UNPUSHED | 0 | 0 | #834 MERGED | 2026-08-29 |
| idp | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/alarm` | fix/crew307-the-alarm-could-not-open-the-issue | UNPUSHED | 0 | 0 | #568 MERGED | 2026-08-28 |
| idp | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/alert` | (detached) | EMPTY | 0 | 0 | - | 2026-08-28 |
| idp | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/apis` | fix/crew307-catalogue-can-actually-roll | UNPUSHED | 0 | 0 | #564 MERGED | 2026-08-28 |
| idp | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/bgfix` | fix/crew570-diagnose-reads-init-container-logs | MERGED | 0 | 0 | #577 MERGED | 2026-08-28 |
| idp | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/bsha` | fix/crew539-catalogue-survives-a-node-drain | DIRTY | 1 | 0 | #545 MERGED | 2026-08-28 |
| idp | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/eyes` | fix/crew307-home-page-is-graded | UNPUSHED | 0 | 0 | #557 MERGED | 2026-08-28 |
| idp | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/gfix` | fix/crew307-ban-the-deadlock-shape-at-admission | MERGED | 0 | 0 | #573 MERGED | 2026-08-28 |
| idp | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/hstart` | fix/crew573-hindsight-api-is-killed-before-it-can-start | MERGED | 0 | 0 | #607 MERGED | 2026-08-28 |
| idp | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/idp-scan` | fix/security-scan-head-only | MERGED | 0 | 0 | #494 MERGED | 2026-08-27 |
| idp | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/idp-tmp` | fix/crew458-estate-mcp-writable-tmp | MERGED | 0 | 0 | #489 MERGED | 2026-08-27 |
| idp | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/idp495` | (detached) | UNPUSHED | 0 | 2 | - | 2026-08-27 |
| idp | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/idpc` | feat/crew516-cp4-cpu-requests-fit-the-fleet | PUSHED-NO-PR | 0 | 0 | - | 2026-08-27 |
| idp | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/idpd` | (detached) | EMPTY | 0 | 0 | - | 2026-08-27 |
| idp | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/idpm` | (detached) | EMPTY | 0 | 0 | - | 2026-08-27 |
| idp | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/idpr` | feat/crew535-actions-billing-refusal-is-one-founder-action | UNPUSHED | 0 | 0 | #482 MERGED | 2026-08-27 |
| idp | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/kycap` | fix/crew292-a-capped-kyverno-block-drops-the-first-failing-dir | MERGED | 0 | 0 | #603 MERGED | 2026-08-28 |
| idp | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/mainav` | (detached) | EMPTY | 0 | 0 | - | 2026-08-28 |
| idp | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/mongate` | fix/crew573-alerting-gated-behind-an-optional-consumer | MERGED | 0 | 0 | #601 MERGED | 2026-08-28 |
| idp | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/rv556` | (detached) | EMPTY | 0 | 0 | - | 2026-08-28 |
| idp | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/rvenv` | fix/crew539-hardened-init-cannot-preserve-times | UNPUSHED | 0 | 0 | #593 MERGED | 2026-08-28 |
| idp | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/trust` | spec/crew581-trust-instruments | DIRTY | 2 | 0 | #610 CLOSED | 2026-08-28 |
| idp | `scratchpad:78caaa17-0304-47a6-837b-896a02f066d8/scratchpad/vimg` | fix/crew570-signature-findable-by-third-party | MERGED | 0 | 0 | #583 MERGED | 2026-08-28 |
| idp | `scratchpad:80471694-3138-4645-a870-868210b81120/scratchpad/wt-idp` | feat/crew639-cp1-messaging-spec | UNPUSHED | 0 | 3 | #838 MERGED | 2026-08-29 |
| idp | `scratchpad:80471694-3138-4645-a870-868210b81120/scratchpad/wt-idp-ts` | fix/crew66-seed-from-the-page | CLOSED | 0 | 0 | #843 CLOSED | 2026-08-29 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/.idp-state` | (detached) | DIRTY | 1 | 1 | - | 2026-08-30 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wt561` | feat/crew561-otto-full-powers | MERGED | 0 | 0 | #1013 MERGED | 2026-08-30 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wt631cp3b` | feat/crew631-cp3-refuse-test | UNPUSHED | 0 | 0 | #842 MERGED | 2026-08-29 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wt648clock` | feat/crew648-estate-state-on-the-estates-clock | MERGED | 0 | 0 | #995 MERGED | 2026-08-30 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wt677` | fix/crew677-p1-injection-and-pin | DIRTY | 3 | 0 | - | 2026-08-30 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wt678` | feat/crew678-cp2-self-heal-has-breaker | UNPUSHED | 0 | 0 | #939 MERGED | 2026-08-30 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wt682` | docs/crew682-notification-channels | UNPUSHED | 0 | 0 | #907 MERGED | 2026-08-30 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wt684d` | feat/crew684-owner-rule | UNPUSHED | 0 | 0 | #922 MERGED | 2026-08-30 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wt717` | feat/crew717-otto-powers | DIRTY | 313 | 1 | #1014 MERGED | 2026-08-30 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wtcap` | feat/crew645-capacity-vpa | EMPTY | 0 | 0 | - | 2026-08-29 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wtdirect` | fix/crew561-mac-run-uses-the-mounted-key | UNPUSHED | 0 | 0 | #949 MERGED | 2026-08-30 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wtds` | feat/downshift-row-armed | MERGED | 0 | 0 | #1017 MERGED | 2026-08-30 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wtfix` | feat/estate-reds-suspend-and-langfuse | MERGED | 0 | 0 | #1016 MERGED | 2026-08-30 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wtgit` | feat/otto-parity-git-in-pod | MERGED | 0 | 0 | #1018 MERGED | 2026-08-30 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wthc` | fix/crew684-healthchecks-tile-presents-the-allowed-host | UNPUSHED | 0 | 0 | #957 MERGED | 2026-08-30 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wtinc` | docs/incident-langfuse-stalled-rollout | MERGED | 0 | 0 | #856 MERGED | 2026-08-29 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wtlean` | feat/crew584-run-lean | PUSHED-NO-PR | 0 | 0 | - | 2026-08-29 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wtmet` | feat/crew645-cp5-metrics-on-backstage | MERGED | 0 | 0 | #861 MERGED | 2026-08-29 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wtmon` | feat/crew684-alertmanager-and-prometheus-have-a-door | DIRTY | 245 | 3 | #977 CLOSED | 2026-08-31 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wtnodes` | fix/crew684-ops-tiles-read-nodes | UNPUSHED | 0 | 0 | #947 MERGED | 2026-08-30 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wtotto` | fix/crew561-mac-run-private-key-dir | UNPUSHED | 0 | 0 | #935 MERGED | 2026-08-30 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wtprr` | fix/gate-checksum-manifests-out-of-secret-scan | UNPUSHED | 0 | 0 | #910 MERGED | 2026-08-30 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wtreg` | fix/crew679-register-test-writes-before-it-reads | UNPUSHED | 0 | 0 | #943 MERGED | 2026-08-30 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wtroll` | feat/crew684-catalogue-roll-measures-the-door | UNPUSHED | 0 | 0 | #952 MERGED | 2026-08-30 |
| idp | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wtver` | feat/crew628-cp1-claims-are-commands | UNPUSHED | 0 | 0 | #874 MERGED | 2026-08-29 |
| idp | `scratchpad:d5ae1960-819d-42a8-8a5c-3521ab2550fd/fluximg` | (detached) | UNPUSHED | 0 | 1 | - | 2026-08-28 |
| idp | `scratchpad:d5ae1960-819d-42a8-8a5c-3521ab2550fd/idp-arch` | crew516-architect-doctor | MERGED | 0 | 0 | #553 MERGED | 2026-08-28 |
| idp | `scratchpad:d5ae1960-819d-42a8-8a5c-3521ab2550fd/idp545` | (detached) | EMPTY | 0 | 0 | - | 2026-08-28 |
| idp | `scratchpad:d5ae1960-819d-42a8-8a5c-3521ab2550fd/idp546` | (detached) | PUSHED-NO-PR | 0 | 0 | - | 2026-08-28 |
| idp | `scratchpad:d5ae1960-819d-42a8-8a5c-3521ab2550fd/idpcap` | feat/crew66-agent-names-a-capability-not-a-vendor | DIRTY | 1 | 0 | - | 2026-08-28 |
| idp | `scratchpad:d5ae1960-819d-42a8-8a5c-3521ab2550fd/idpjudge` | crew516-the-judge-loads-the-estates-own-policies | MERGED | 0 | 0 | #556 MERGED | 2026-08-28 |
| idp | `scratchpad:d5ae1960-819d-42a8-8a5c-3521ab2550fd/idpstuck` | crew516-automerge-stuck-graded-the-wrong-field | UNPUSHED | 0 | 0 | #560 MERGED | 2026-08-28 |
| idp | `scratchpad:d5ae1960-819d-42a8-8a5c-3521ab2550fd/scratchpad/idp-r491 5b5152a` | (detached) | EMPTY | 0 | 0 | - | 2026-08-27 |
| idp | `scratchpad:d5ae1960-819d-42a8-8a5c-3521ab2550fd/scratchpad/idp-r91 7cb145f` | (detached) | EMPTY | 0 | 0 | - | 2026-08-27 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/idp612` | feat/crew612-company-cards | MERGED | 0 | 0 | #677 MERGED | 2026-08-29 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-66` | docs/crew66-adr0008-self-service | MERGED | 0 | 0 | #646 MERGED | 2026-08-28 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-699b` | test/diagnose-storage-rows-pinned | MERGED | 0 | 0 | #720 MERGED | 2026-08-29 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-a1` | feat/crew63-a1-evidence-row | UNPUSHED | 0 | 0 | #765 MERGED | 2026-08-29 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-audit` | fix/new-validate-rules-enter-as-audit | UNPUSHED | 0 | 0 | #703 MERGED | 2026-08-29 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-cat` | fix/catalogue-entity-audit-until-drift-zero | EMPTY | 0 | 0 | - | 2026-08-29 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-diag` | fix/diagnose-shows-storage-and-pending-claims | UNPUSHED | 0 | 2 | #699 CLOSED | 2026-08-29 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-diag2` | fix/diagnose-founder-surfaces | MERGED | 0 | 0 | #714 MERGED | 2026-08-29 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-doc` | docs/crew568-model-stack-page | UNPUSHED | 0 | 0 | #756 MERGED | 2026-08-29 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-docpol` | docs/documentation-policy | MERGED | 0 | 0 | #658 MERGED | 2026-08-28 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-docs` | docs/adr0002-diataxis-sweep | MERGED | 0 | 0 | #647 MERGED | 2026-08-28 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-doors` | feat/every-interface-is-a-door-grouped-home | MERGED | 0 | 0 | #735 MERGED | 2026-08-29 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-gq` | fix/no-script-under-bin-pipes-into-grep-q | UNPUSHED | 0 | 1 | #793 MERGED | 2026-08-29 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-hooks` | fix/fixture-repos-do-not-run-the-operators-git-hooks | UNPUSHED | 0 | 0 | #786 MERGED | 2026-08-29 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-img` | feat/crew307-require-qualified-image | PUSHED-NO-PR | 0 | 0 | - | 2026-08-29 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-kyv` | fix/kyverno-judge-grep-q-sigpipe-reads-green | PUSHED-NO-PR | 0 | 0 | - | 2026-08-29 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-laptop` | feat/crew568-laptop-on-the-spine | MERGED | 0 | 0 | #768 MERGED | 2026-08-29 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-ns` | fix/no-admission-rule-on-claims | MERGED | 0 | 0 | #700 MERGED | 2026-08-29 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-otto` | fix/gateway-starts-without-sidecar-secret | UNPUSHED | 0 | 0 | #767 MERGED | 2026-08-29 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-otto2` | fix/otto-sidecar-pins-a-tag-ghcr-never-published | UNPUSHED | 0 | 0 | #778 MERGED | 2026-08-29 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-ottoalert` | fix/otto-down-is-an-alert-a-person-reads | MERGED | 0 | 0 | #770 MERGED | 2026-08-29 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-p1` | feat/crew568-claude-is-a-lane-on-the-router | UNPUSHED | 0 | 0 | #788 MERGED | 2026-08-29 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-render` | fix/namespaces-never-pruned | UNPUSHED | 0 | 1 | #686 MERGED | 2026-08-29 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-robot` | fix/robot-commits-to-main | DIRTY | 20 | 0 | - | 2026-08-29 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-roll` | fix/roll-catalogue-to-current-main | UNPUSHED | 0 | 1 | #706 MERGED | 2026-08-29 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-spend` | feat/crew568-router-spend-playbook | UNPUSHED | 0 | 0 | #745 MERGED | 2026-08-29 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-sync` | fix/flux-sync-every-minute | MERGED | 0 | 0 | #711 MERGED | 2026-08-29 |
| idp | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-ts` | feat/cluster-access-over-tailscale | PUSHED-NO-PR | 0 | 0 | - | 2026-08-29 |
| idp | `/private/tmp/pr493-merge` | (detached) | UNPUSHED | 0 | 0 | - | 2026-08-27 |
| idp | `/private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/pytest-of-chidionyema/pytest-1944/popen-gw1/test_incident_crew474_worktree0/scratchpad/wt-render` | wt-render | PUSHED-NO-PR | 0 | 0 | - | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/devloop` | (detached) | EMPTY | 0 | 0 | - | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/idp292` | feat/crew292-drills-row-in-ci | MERGED | 0 | 0 | #526 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/idp292fix` | feat/crew292-drills-row-self-reference | MERGED | 0 | 0 | #580 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/idp412` | fix/crew412-founder-surfaces-reach-portal | EMPTY | 0 | 0 | - | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/idp441` | feat/crew300-recover-drill-wt | PUSHED-NO-PR | 0 | 0 | - | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/idp516` | feat/crew516-verify-drill-tolerates-resize | MERGED | 0 | 0 | #548 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/idp516-otto` | feat/crew516-otto-hands-on-the-mac | MERGED | 0 | 0 | #582 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/idp539r` | fix/crew539-robusta-stalled | MERGED | 0 | 0 | #570 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/idp554` | feat/crew554-drills-row-counts-firings | MERGED | 0 | 0 | #527 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/idp554b` | feat/crew554-app-jwt-bearer | MERGED | 0 | 0 | #550 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/idp554c` | feat/crew554-drill-dispatcher | MERGED | 0 | 0 | #529 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/idp562` | feat/crew562-mac-remote-desk | MERGED | 0 | 0 | #567 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/idp66` | feat/crew66-oci-caller-ratchet | MERGED | 0 | 0 | #552 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/idp66gate` | feat/crew66-no-toil-gate | MERGED | 0 | 0 | #575 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/idp66pol` | feat/crew66-provider-independence-policy | MERGED | 0 | 0 | #555 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/idpdeps` | fix/crew539-platform-rows-never-wait-on-the-portal | MERGED | 0 | 0 | #565 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/idpdiag` | fix/crew483-diagnose-telemetry | MERGED | 0 | 0 | #562 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/idphubble` | feat/crew539-cp12-cilium-replace | MERGED | 0 | 0 | #561 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/idpkube` | feat/crew66-idp-kube | MERGED | 0 | 0 | #558 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wt619` | fix619 | UNPUSHED | 0 | 1 | - | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wt84` | fix84 | EMPTY | 0 | 0 | - | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtbm` | feat/crew584-bdd-matrix | UNPUSHED | 0 | 1 | #641 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtcap` | feat/crew584-capacity-row | DIRTY | 76 | 1 | #687 MERGED | 2026-08-29 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtcl` | (detached) | EMPTY | 0 | 0 | - | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtcred` | feat/crew66-portal-lane-token | UNPUSHED | 0 | 1 | - | 2026-08-30 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtdf` | fix/crew539-alert-drill-timeout | MERGED | 0 | 0 | #870 MERGED | 2026-08-29 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtdisp` | fix/crew554-dispatcher-covers-slow-crons | MERGED | 0 | 0 | #715 MERGED | 2026-08-29 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtdm` | feat/crew562-decision-matrix | MERGED | 0 | 0 | #651 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtdr` | feat/crew584-drill-wait-on-floor | MERGED | 0 | 0 | #667 MERGED | 2026-08-29 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtdrift` | fix/crew584-agent-release-drift-detection | MERGED | 0 | 0 | #712 MERGED | 2026-08-29 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtdx` | feat/crew584-ci-dedupe-and-timing | MERGED | 0 | 0 | #636 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtes` | feat/crew290-github-escrow | UNPUSHED | 0 | 1 | #645 MERGED | 2026-08-29 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wteth` | feat/crew584-engineering-tenets | DIRTY | 527 | 0 | - | 2026-08-29 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtfb` | feat/crew584-enable-feature-template | MERGED | 0 | 0 | #691 MERGED | 2026-08-29 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtfeat` | fix/crew584-break-glass-agent-namespace | MERGED | 0 | 0 | #710 MERGED | 2026-08-29 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtfg` | feat/crew584-fast-gate | MERGED | 0 | 0 | #671 MERGED | 2026-08-29 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtgp` | feat/crew584-green-pr-push-guard | MERGED | 0 | 0 | #632 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtgu` | feat/crew562-guacamole-screen | MERGED | 0 | 0 | #659 MERGED | 2026-08-29 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wthc` | fix/crew584-helm-cache-race | MERGED | 0 | 0 | #634 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtkyv` | feat/crew584-ci-kyverno-parallel | MERGED | 0 | 0 | #625 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtlaws` | feat/crew254-pause-laws-gate | MERGED | 0 | 0 | #627 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtlm` | feat/crew584-cp4-loop-meter | MERGED | 0 | 0 | #639 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtmr` | feat/crew584-mirrord-dev-loop | MERGED | 0 | 0 | #678 MERGED | 2026-08-29 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtpc` | feat/crew584-pre-commit-lint | MERGED | 0 | 0 | #668 MERGED | 2026-08-29 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtpe` | fix/crew562-founder-screen-plain-english | CLOSED | 0 | 0 | #673 CLOSED | 2026-08-29 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtpp` | feat/crew562-pair-phone-card | MERGED | 0 | 0 | #653 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtrd` | feat/crew290-recover-from-mirrors | PUSHED-NO-PR | 0 | 0 | - | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtsn` | feat/crew562-sunshine-seed | MERGED | 0 | 0 | #657 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtss` | feat/crew66-self-service-portal | MERGED | 0 | 0 | #895 MERGED | 2026-08-30 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wttf` | feat/crew584-tests-for-worker-cap | MERGED | 0 | 0 | #663 MERGED | 2026-08-29 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtts` | feat/crew516-tailscale-operator-admission | MERGED | 0 | 0 | #649 MERGED | 2026-08-28 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtvp` | fix/crew562-vault-prune-secret-versions | MERGED | 0 | 0 | #674 MERGED | 2026-08-29 |
| idp | `~/.claude/jobs/a0d64ea4/tmp/wtzb` | feat/crew584-ci-zero-bottleneck | MERGED | 0 | 0 | #628 MERGED | 2026-08-28 |
| idp | `~/dev/code/.idp-state` | (detached) | DIRTY | 1 | 0 | - | 2026-08-28 |
| idp | `~/dev/code/.wt-adr0010` | fix/crew66-federated-scopes | UNPUSHED | 0 | 0 | #860 MERGED | 2026-08-29 |
| idp | `~/dev/code/.wt-backstage-proof` | backstage-arm64 | DIRTY | 3 | 0 | - | 2026-08-25 |
| idp | `~/dev/code/.wt-backups` | fix/registries-conf-read | MERGED | 0 | 0 | #1036 MERGED | 2026-08-31 |
| idp | `~/dev/code/.wt-blindline` | fix/blind-line-names-the-real-fault | OPEN | 0 | 0 | #1054 OPEN | 2026-08-31 |
| idp | `~/dev/code/.wt-catguard` | fix/gate-reads-head-catalogue | MERGED | 0 | 0 | #1048 MERGED | 2026-08-31 |
| idp | `~/dev/code/.wt-control` | feat/every-infra-change-ships-a-control | MERGED | 0 | 0 | #1042 MERGED | 2026-08-31 |
| idp | `~/dev/code/.wt-crew631-wall` | fix/crew612-plain-english-buttons | UNPUSHED | 0 | 0 | #1052 MERGED | 2026-08-31 |
| idp | `~/dev/code/.wt-crew693-auto` | crew693-finish | PUSHED-NO-PR | 0 | 0 | - | 2026-08-30 |
| idp | `~/dev/code/.wt-deploy` | fix/rollup-duplicate-runs | DIRTY | 2 | 0 | - | 2026-08-31 |
| idp | `~/dev/code/.wt-estate-audit` | audit/estate-inventory-and-backup | UNPUSHED | 0 | 0 | - | 2026-08-31 |
| idp | `~/dev/code/.wt-fastgates` | fix/blueprint-fast-gates | MERGED | 0 | 0 | #1031 MERGED | 2026-08-31 |
| idp | `~/dev/code/.wt-idp-1050` | feat/crew631-cp9-signoz | MERGED | 0 | 0 | #1050 MERGED | 2026-08-31 |
| idp | `~/dev/code/.wt-idp-656` | feat/crew656-canary-ledger | DIRTY | 2 | 0 | - | 2026-08-31 |
| idp | `~/dev/code/.wt-idp-693` | feat/crew693-prospector-image-automation-v3 | MERGED | 0 | 0 | #925 MERGED | 2026-08-30 |
| idp | `~/dev/code/.wt-idp-docs-gate` | ci/no-docs-no-merge | MERGED | 0 | 0 | #1069 MERGED | 2026-08-31 |
| idp | `~/dev/code/.wt-idp-langfuse` | fix/langfuse-sso-signup | UNPUSHED | 0 | 0 | #1058 MERGED | 2026-08-31 |
| idp | `~/dev/code/.wt-idp-p0` | feat/crew740-estate-inventory | OPEN | 0 | 0 | #1072 OPEN | 2026-08-31 |
| idp | `~/dev/code/.wt-idp-pipaudit` | fix/pip-audit-install-failure-blind | UNPUSHED | 0 | 0 | #134 MERGED | 2026-08-25 |
| idp | `~/dev/code/.wt-idp-pipignore` | ci/pip-audit-ignores | OPEN | 0 | 0 | #1071 OPEN | 2026-08-31 |
| idp | `~/dev/code/.wt-idp-reqs` | docs/founder-requirements-sweep | UNPUSHED | 0 | 0 | #136 MERGED | 2026-08-25 |
| idp | `~/dev/code/.wt-idp-search` | feat/backstage-search-page | EMPTY | 0 | 0 | - | 2026-08-31 |
| idp | `~/dev/code/.wt-idp-signoz-header` | fix/signoz-dashboards-shape | MERGED | 0 | 0 | #1064 MERGED | 2026-08-31 |
| idp | `~/dev/code/.wt-idp-signoz-logs` | fix/webhooks-restart-playbook | UNPUSHED | 0 | 0 | - | 2026-08-30 |
| idp | `~/dev/code/.wt-idp-spec` | spec/phone-idea-flow-agnostic | UNPUSHED | 0 | 0 | #142 MERGED | 2026-08-26 |
| idp | `~/dev/code/.wt-idp-ts-tag` | fix/tailscale-operator-tag | UNPUSHED | 0 | 0 | #1065 OPEN | 2026-08-31 |
| idp | `~/dev/code/.wt-kini-spec` | docs/kini-master-spec | DIRTY | 293 | 0 | #59 MERGED | 2026-08-26 |
| idp | `~/dev/code/.wt-kini-suspend` | fix/kini-suspend-temporal | UNPUSHED | 0 | 0 | #923 MERGED | 2026-08-30 |
| idp | `~/dev/code/.wt-kubeconform` | feat/kubeconform-before-merge | MERGED | 0 | 0 | #1046 MERGED | 2026-08-31 |
| idp | `~/dev/code/.wt-llm-image` | evidence/crew710-minimax-headers | DIRTY | 224 | 0 | #1012 OPEN | 2026-08-31 |
| idp | `~/dev/code/.wt-macrun` | docs/crew561-otto-mac-setup-notes | MERGED | 0 | 0 | #991 MERGED | 2026-08-30 |
| idp | `~/dev/code/.wt-observability` | observability/signoz | UNPUSHED | 0 | 0 | #133 MERGED | 2026-08-25 |
| idp | `~/dev/code/.wt-otto` | fix/rego-review-silent-greens | DIRTY | 2 | 0 | #904 MERGED | 2026-08-30 |
| idp | `~/dev/code/.wt-otto-roll` | fix/crew561-mac-run-hash-rolls-the-pod | UNPUSHED | 0 | 0 | #970 MERGED | 2026-08-30 |
| idp | `~/dev/code/.wt-otto-token` | crew717-rebase | UNPUSHED | 0 | 0 | - | 2026-08-31 |
| idp | `~/dev/code/.wt-parity561` | fix/crew561-parity-proves-gh | UNPUSHED | 0 | 0 | - | 2026-08-30 |
| idp | `~/dev/code/.wt-pgflake` | fix/messaging-demo-postgres-flake | MERGED | 0 | 0 | #1045 MERGED | 2026-08-31 |
| idp | `~/dev/code/.wt-prclear` | fix/crew66-curl-double-drains-stdin | DIRTY | 4 | 0 | - | 2026-08-31 |
| idp | `~/dev/code/.wt-reload` | feat/estate-wide-auto-reload | MERGED | 0 | 0 | #1032 MERGED | 2026-08-31 |
| idp | `~/dev/code/.wt-reload-base` | (detached) | UNPUSHED | 0 | 0 | - | 2026-08-31 |
| idp | `~/dev/code/.wt-secrets-rotation` | fix/crew727-intervals-one-value | MERGED | 0 | 0 | #1057 MERGED | 2026-08-31 |
| idp | `~/dev/code/.wt-suitelock` | fix/one-suite-per-machine | EMPTY | 0 | 0 | - | 2026-08-31 |
| idp | `~/dev/code/.wt-tailscale-root` | fix/tailscale-operator-runs-as-root | OPEN | 0 | 0 | #1051 OPEN | 2026-08-31 |
| idp | `~/dev/code/.wt-td-catalogue` | fix/teardown-catalogue | MERGED | 0 | 0 | #1035 MERGED | 2026-08-31 |
| idp | `~/dev/code/.wt-td-surface` | fix/teardown-surface | MERGED | 0 | 0 | #1034 MERGED | 2026-08-31 |
| idp | `~/dev/code/idp-wt-345` | crew345-verification-identity | UNPUSHED | 0 | 0 | #269 MERGED | 2026-08-27 |
| idp | `~/dev/code/idp/.claude/worktrees/.idp-state` | (detached) | DIRTY | 2 | 0 | - | 2026-08-27 |
| idp | `~/dev/code/idp/.claude/worktrees/agent-a12b72866f50f808f` | feat/crew468-dagster-entity-provider | UNPUSHED | 0 | 0 | #370 MERGED | 2026-08-27 |
| idp | `~/dev/code/idp/.claude/worktrees/agent-a1cdaba7548804c1e` | feat/crew480-catalogue-providers | CLOSED | 0 | 0 | #371 CLOSED | 2026-08-27 |
| idp | `~/dev/code/idp/.claude/worktrees/commerce-dark` | feat/commerce-primitive-dark | MERGED | 0 | 0 | #800 MERGED | 2026-08-29 |
| idp | `~/dev/code/idp/.claude/worktrees/crew325-fix-the-map` | feat/crew401-catalogue-drift | UNPUSHED | 0 | 0 | #291 MERGED | 2026-08-27 |
| idp | `~/dev/code/idp/.claude/worktrees/crew401-drift-exitcode` | fix/crew401-drift-exitcode | UNPUSHED | 0 | 0 | #301 MERGED | 2026-08-27 |
| idp | `~/dev/code/idp/.claude/worktrees/crew401-store-entity` | feat/crew401-store-entity | UNPUSHED | 0 | 0 | #303 MERGED | 2026-08-27 |
| idp | `~/dev/code/idp/.claude/worktrees/crew459-portal-polish` | feat/crew66-root-trust | UNPUSHED | 0 | 0 | #609 MERGED | 2026-08-28 |
| idp | `~/dev/code/idp/.claude/worktrees/crew488-drill-settle` | crew488/drill-wait-settles-on-the-cluster | PUSHED-NO-PR | 0 | 0 | - | 2026-08-29 |
| idp | `~/dev/code/idp/.claude/worktrees/crew539` | feat/crew539-scheduling-immunity | MERGED | 0 | 0 | #492 MERGED | 2026-08-27 |
| idp | `~/dev/code/idp/.claude/worktrees/crew66-cp5a` | feat/crew66-cp5a-cloud-verbs | MERGED | 0 | 0 | #474 MERGED | 2026-08-27 |
| idp | `~/dev/code/idp/.claude/worktrees/crew66-cp5b` | feat/crew66-cp5b-identity-flux | UNPUSHED | 0 | 0 | #476 MERGED | 2026-08-27 |
| idp | `~/dev/code/idp/.claude/worktrees/crew66-cp5c` | feat/crew66-cp5c-guards | MERGED | 0 | 0 | #478 MERGED | 2026-08-27 |
| idp | `~/dev/code/idp/.claude/worktrees/crew66-cp5d` | feat/crew66-cp5d-cluster-noun | MERGED | 0 | 0 | #490 MERGED | 2026-08-27 |
| idp | `~/dev/code/idp/.claude/worktrees/crew66-cp5e` | feat/crew66-cp5e-provider-adapter | MERGED | 0 | 0 | #475 MERGED | 2026-08-27 |
| idp | `~/dev/code/idp/.wt-bs-tag` | chore/login-drill-graded | UNPUSHED | 0 | 0 | #189 MERGED | 2026-08-26 |
| idp | `~/dev/code/idp/.wt-chaos` | fix/chaos-inject-label | UNPUSHED | 0 | 0 | #190 MERGED | 2026-08-26 |
| idp | `~/dev/code/idp/.wt-chaos2` | feat/chaos-drill-receipt | UNPUSHED | 0 | 0 | #191 MERGED | 2026-08-26 |
| idp | `~/dev/code/idp/.wt-cp2` | feat/cp2-litellm-real | UNPUSHED | 0 | 0 | #179 MERGED | 2026-08-26 |
| idp | `~/dev/code/idp/.wt-crew345-sweep` | fix/crew345-no-file-routes-to-oci-session | UNPUSHED | 0 | 0 | #275 MERGED | 2026-08-27 |
| idp | `~/dev/code/idp/.wt-gate` | fix/gate-drills-from-pr-head | UNPUSHED | 0 | 0 | #192 MERGED | 2026-08-26 |
| idp | `~/dev/code/idp/.wt-idp-blind` | fix/breakglass-blind-verdict | DIRTY | 1 | 0 | #1073 OPEN | 2026-08-31 |
| idp | `~/dev/code/idp/.wt-idp-ghapp` | feat/github-app-per-lane | UNPUSHED | 0 | 0 | #168 MERGED | 2026-08-26 |
| idp | `~/dev/code/idp/.wt-keyless` | feat/laptop-keyless | UNPUSHED | 0 | 0 | #188 MERGED | 2026-08-26 |
| idp | `~/dev/code/idp/.wt-p0` | feat/github-app-installation-from-ci | MERGED | 0 | 0 | #230 MERGED | 2026-08-26 |
| idp | `~/dev/code/idp/.wt-stale` | ci/stale-pr-policy | UNPUSHED | 0 | 0 | #194 MERGED | 2026-08-26 |
| idp | `~/dev/code/idp/.wt-temporal` | feat/crew396-kini-finish-trigger | UNPUSHED | 0 | 0 | #280 MERGED | 2026-08-27 |
| idp | `~/dev/code/idp/.wt-vault-seed` | main | DIRTY | 1571 | 0 | - | 2026-08-31 |
| prospector-main | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtpros` | feat/edge-manners | EMPTY | 0 | 0 | - | 2026-08-29 |
| prospector-main | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtpros568` | feat/crew568-agents-md | EMPTY | 0 | 0 | - | 2026-08-29 |
| prospector-main | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtreland` | feat/edge-manners-reland | PUSHED-NO-PR | 0 | 0 | - | 2026-08-29 |
| prospector-main | `scratchpad:2d8b3bd0-3d43-40d9-862b-712be5c41803/scratchpad/wtrevert` | hotfix/revert-774-store-404 | EMPTY | 0 | 0 | - | 2026-08-29 |
| prospector-main | `scratchpad:a7b41022-3074-43c7-bb13-a1d7e07adff1/scratchpad/wtedge` | feat/crew684-monitoring-listeners | EMPTY | 0 | 0 | - | 2026-08-30 |
| prospector-main | `scratchpad:d5ae1960-819d-42a8-8a5c-3521ab2550fd/scratchpad/own-prospector` | chore/crew88-codeowners | EMPTY | 0 | 0 | - | 2026-08-27 |
| prospector-main | `scratchpad:d5ae1960-819d-42a8-8a5c-3521ab2550fd/scratchpad/pros-hc` | feat/crew177-hc-listener | EMPTY | 0 | 0 | - | 2026-08-27 |
| prospector-main | `scratchpad:f3f21d6e-8df9-44b8-ae46-def299e0298c/scratchpad/wt-pros` | feat/every-interface-is-a-door | EMPTY | 0 | 0 | - | 2026-08-29 |
| prospector-main | `~/Documents/code/prospector` | (detached) | PUSHED-NO-PR | 0 | 0 | - | 2026-08-24 |
| prospector-main | `~/Documents/code/prospector-rust` | docs/the-engine-architecture-and-its-decisions | EMPTY | 0 | 0 | - | 2026-08-23 |
| prospector-main | `~/Documents/code/prospector/.claude/worktrees/agent-aaecfffaa54620133` | worktree-agent-aaecfffaa54620133 | EMPTY | 0 | 0 | - |  |
| prospector-main | `~/Documents/code/wt-automerge-dispatch` | ci/automerge-dispatch-before-sweep | DIRTY | 8 | 0 | - | 2026-08-20 |
| prospector-main | `~/Documents/code/wt-automerge-sweep` | (detached) | EMPTY | 0 | 0 | - |  |
| prospector-main | `~/Documents/code/wt-converge` | feat/console-money-data-ia | EMPTY | 0 | 0 | - |  |
| prospector-main | `~/Documents/code/wt-deploy-buttons` | (detached) | DIRTY | 15 | 0 | - | 2026-08-20 |
| prospector-main | `~/Documents/code/wt-dr` | audit/recoverability-escrow | PUSHED-NO-PR | 0 | 0 | - | 2026-08-20 |
| prospector-main | `~/Documents/code/wt-engine100x` | int-land-index-fix | DIRTY | 1 | 0 | - | 2026-08-20 |
| prospector-main | `~/Documents/code/wt-firstrun` | web/every-pack-two-clicks | DIRTY | 2 | 0 | - | 2026-08-21 |
| prospector-main | `~/Documents/code/wt-fly-migration` | feat/ops-console-public-https | EMPTY | 0 | 0 | - |  |
| prospector-main | `~/Documents/code/wt-imgflows` | fix/image-must-carry-github-workflows | DIRTY | 23 | 0 | - | 2026-08-20 |
| prospector-main | `~/Documents/code/wt-incidents` | (detached) | EMPTY | 0 | 0 | - |  |
| prospector-main | `~/Documents/code/wt-integrate` | (detached) | EMPTY | 0 | 0 | - |  |
| prospector-main | `~/Documents/code/wt-ledger` | (detached) | DIRTY | 5 | 0 | - | 2026-08-20 |
| prospector-main | `~/Documents/code/wt-mainfence` | (detached) | DIRTY | 5 | 0 | - | 2026-08-19 |
| prospector-main | `~/Documents/code/wt-mainred` | (detached) | EMPTY | 0 | 0 | - |  |
| prospector-main | `~/Documents/code/wt-pipeline` | incident/2026-08-20-deletion | DIRTY | 20 | 0 | - | 2026-08-20 |
| prospector-main | `~/Documents/code/wt-site-pr` | (detached) | DIRTY | 579 | 0 | - | 2026-08-19 |
| prospector-main | `~/Documents/code/wt-storefront` | (detached) | EMPTY | 0 | 0 | - |  |
| prospector-main | `~/dev/code/.wt-keda` | feat/keda-scale-to-zero | PUSHED-NO-PR | 0 | 0 | - | 2026-08-27 |
| prospector-main | `~/dev/code/.wt-pros-audit` | fix/store-web-npm-audit | DIRTY | 1 | 0 | - | 2026-08-25 |
| prospector-main | `~/dev/code/.wt-store-release` | fix/kill-gate-band-is-readable | PUSHED-NO-PR | 0 | 0 | - | 2026-08-31 |
| prospector-main | `~/dev/code/.wt-tone-audit` | main | EMPTY | 0 | 0 | - | 2026-08-30 |
| prospector-main | `~/dev/code/prospector-main/.wt-chaos-task` | chore/kyverno-admit-workflow-task-pods | EMPTY | 0 | 0 | - | 2026-08-26 |
| prospector-main | `~/dev/code/prospector-main/.wt-crew203-pr3` | chore/crew203-retire-fly-readers | PUSHED-NO-PR | 0 | 0 | - | 2026-08-26 |
| prospector-main | `~/dev/code/prospector-main/.wt-crew326` | fix/crew326-shim-respects-hookspath | PUSHED-NO-PR | 0 | 0 | - | 2026-08-26 |
| prospector-main | `~/dev/code/prospector-main/.wt-stale` | ci/stale-pr-policy | PUSHED-NO-PR | 0 | 0 | - | 2026-08-26 |
