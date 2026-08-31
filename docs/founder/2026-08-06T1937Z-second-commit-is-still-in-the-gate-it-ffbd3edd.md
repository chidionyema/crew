---
captured: 2026-08-06T19:37:55+00:00
session: 459b4820-6222-4812-b3d2-faa22c19f65d
cwd: /Users/chidionyema/Documents/code/prospector
chars: 4065
source: founder prompt, verbatim (founder-doc-capture.py)
---

Second commit is still in the gate (it ran ~9 minutes last time), so I'll confirm it lands before calling the safe point. Everything else is done.

Your four requirements, and where each stands:

┌────────────────────────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│              requirement               │                                                            status                                                            │
├────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ central cost doc other agents can read │ ✅ docs/COST_PROGRAM.md, committed + pushed in 8e9ed98, pointers added to both CLAUDE.md files                               │
├────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ proper trackable spec, not cowboy dev  │ ✅ docs/GRAPHIFY_ENFORCEMENT_SPEC.md — 12 numbered requirements, each with a runnable check; a scoreboard that exits 1 today │
├────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ never stale                            │ ⚠️ mechanism built and proven (PH1), triggers not yet wired (PH2)                                                            │
├────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ can't be bypassed                      │ ❌ designed only — the hooks are PH2                                                                                         │
├────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ measure cost savings                   │ ⚠️ two halves proven, the decisive number still unmeasured                                                                   │
└────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

On measurement, the honest split. Proven by execution: refresh costs zero tokens — sentinel-loop went STALE(41.6d) → FRESH in 46.5s with both ANTHROPIC_API_KEY and OPENAI_API_KEY unset — and query injection is capped at 2,000 tokens of local BFS. That kills the objection I'd raised against my own plan, that enforcing refresh everywhere might cost more than it saves. It cannot.

What I will not claim: how many round trips a query replaces. The saving is (N−1) × $0.1192 and N is unmeasured, so it stays a HYPOTHESIS in the doc with the A/B that settles it written out. A cheaper wrong answer isn't a saving, so that experiment checks correctness too.

Two things I deliberately did not do:

1. I did not refresh prospector's graph, even though it's the stalest thing in the estate. Its graphify-out is 318 tracked files, so --fix would drop a 318-file diff onto a branch three sessions are sharing. Untracking has its own trap — git commit --only undoes git rm --cached, and a bare commit would take the whole shared index — so it needs a dedicated worktree. Wrong order here turns a refresh into an accidental mass commit.
2. I did not git init ~/.claude. It's the only way the enforcement scripts become committed and pushed, but it holds credential-adjacent files and needs a deliberate ignore list. Recorded as decision D2.

The 40% is still sitting there. L1 needs you to quit Claude Code and relaunch from a new terminal — 6 of 8 live processes predate the config and 94% of recent requests are still Opus. Nothing in this session moves that number.

Handoff written to checkpoints/2026-08-06-graphify-cost-spec.md with a pointer appended to LATEST.md.
