# Lanes: one session, one worktree, and the two rules that stop collisions

Source: crew#40. Written 2026-08-26 from the feed, not from memory.

## What a lane is

A lane is a git worktree. One session writes in one worktree at a time. The
lane name is the worktree directory basename (`.wt-p0`, `.wt-catalog-404`,
`code`), and it is the third field of every feed header in
`~/.estate/feed.md`:

    ## <UTC time> · session <id> · lane <worktree>

The main checkout of any repo is not a lane. Nobody edits there.

## The two rules

| # | Rule | Enforced where | Proof |
|---|------|----------------|-------|
| 1 | Never `git add -A` or `git add .` in this estate. Stage named paths: `git add -- path/one path/two`. `store/` and `storage/` are tracked runtime state that pytest writes to, so add-all commits another process's output. | `~/.claude/scripts/rule-guard.py`, PreToolUse on Bash, every session | Refuse half: the guard blocked `git add -A && git commit -m x` on 2026-08-26 17:49Z. Permit half: `git add -- docs/A.md && git commit -m x` exits 0. |
| 2 | One lane per session. Say which lane you are in before you touch it, and name what you will change. | `~/.claude/scripts/feed-guard.py` on Stop, `policy/feed.rego`: every handoff carries `🔧 TOUCHES:` and `🔀 OVERLAP:`, "none" is an answer, empty is refused (crew#259) | `feed_test.rego` |

## What a conflict is

Two sessions in one repo on different branches in different worktrees: fine.
Two sessions staging in the same checkout: not fine. Two sessions changing
the same launchd job, the same guard file, or the same shared config: not
fine. Before touching any of those, read the last handoff of every live
session in the feed and check its `TOUCHES:` line.

## Measured on 2026-08-26

Last handoff per session, 02:32Z to 17:47Z, from `~/.estate/feed.md`:

| lane | sessions |
|------|----------|
| `.wt-p0` | 41fd24d8, 6776e0e4, a5a4e547, cf92e8fb, dce21d1c |
| `idp` | 079631d5, 8f034e1e, 9f8f4f5f, d91dce44 |
| `code` | d636e984 |
| `.wt-catalog-404` | 78caaa17 |
| `.crew-state` | abf8d1ad |
| `hermes-v2` | faeecb13 |
| `backstage` | 4e5b5e8f |

Five sessions in `.wt-p0` and four in `idp` is the failure crew#40 was
opened for. Rule 1 stops the worst damage (a stray add-all). Rule 2 makes
the overlap visible but does not refuse it: nothing today stops a second
session from writing a handoff under a lane another live session holds.

## The lane list from crew#40 (2026-08-23), status on 2026-08-26

| # | Lane | Issues | Open today |
|---|------|--------|------------|
| 1 | Estate spend | #26 | #26 |
| 2 | Fly billing and the exit drill | #35 #38 #6 | none; R1 closed Fly |
| 3 | Canonical root migration | #32 | #32 |
| 4 | Estate guards and the load-bearing sweep | claude-guards, claude-estate | rolling |
| 5 | Rust engine licence | #33 | #33 |
| 6 | Observability | #22 #25 | closed |
| 7 | The Architect's Telegram | #30 | closed |
| 8 | Maestro capability gaps | #28 | closed |

Claim a lane by naming it in your feed handoff. First claim in the feed wins.
If the lane is held, take another worktree.
