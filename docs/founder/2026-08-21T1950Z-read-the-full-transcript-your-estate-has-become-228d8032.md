---
captured: 2026-08-21T19:50:34+00:00
session: c65fd112-6b2f-43c0-9073-2ca4bf1d648f
cwd: /Users/chidionyema
chars: 3171
source: founder prompt, verbatim (founder-doc-capture.py)
---

read the full transcript. Your estate has become a Rube Goldberg machine where the governance layer (43 scripts, 35 daemons, 9 probes, 17k lines) is now larger and more fragile than the actual product you're trying to ship. The core problem isn't a lack of tools—it's that you've built a custom operating system on top of your laptop instead of using standard primitives.
Here's the honest diagnosis and a concrete path out:
What's Actually Broken
Table
Symptom    Root Cause
Load average 40    35 launchd jobs + 9 blocking probes + recursive hook chains
Agents "forget" everything    State stored in local JSON files instead of git commits
You can't leave the laptop    Board is a local HTML file; no cloud API
3.65s tax per turn    37 hook entries firing synchronously on every tool call
Secrets in plaintext    No secret manager; history file is mode 600 but unrotated
No branch protection    Free-tier GitHub + local "main-admission-guard" doing reverts
347s probe runtime    founder_board.py runs all probes inline instead of reading cached logs
The Architecture You Actually Need
Stop building. Start wiring existing standards together.
1. Single Source of Truth: GitHub Projects (or Linear)
4 lanes: Engine, API, UI, Ops
P0/P1/P2/P3 labels
Each issue = one agent task, one branch, one PR
This replaces ESTATE_BOARD.jsonl, scratchpads, and custom ledgers
2. Agent Isolation: Git Worktrees (not shared checkouts)
plain
~/code/prospector-main      (your working copy)
~/code/prospector-agent-1   (worktree for agent-1, branch issue-123)
~/code/prospector-agent-2   (worktree for agent-2, branch issue-124)
No more detached HEAD, no more index.lock collisions, no more agents stepping on each other.
3. Mobile Control Plane: Hermes → GitHub API (not local files)
Hermes on your phone reads/writes GitHub Issues directly via GraphQL API
Commands: /lanes, /priority API 123 P0, /deploy engine
No local state. Your laptop can be offline and the board is still current.
4. Laptop Agent Runtime: Strip to 3 hooks max
Pre-commit: secret scan (1 script)
Pre-push: fast test run (1 script)
Nothing else. Delete rule-guard.py, goal-guard.py, peer-loop-fence.py, memory-loop.py.
Move "laws" into AGENTS.md (already done) and let the LLM read it. Stop trying to enforce behavior with Python scripts.
5. CI/CD: Use GitHub Actions (even on free tier)
Required status checks block merge. If GitHub won't enforce it on free private repos, make the repo public or pay $4/mo for Pro.
Delete main-admission-guard.py. A script on your laptop reverting main is not a merge gate.
What To Do Right Now (in order)
Kill the 12 dormant ai.hermes. launchd plists* — launchctl unload them today
Delete the 15 dead scripts already identified — they're gone, don't replace them
Unhook rule-guard.py, guard-autocommit.py, and all non-security hooks from settings.json
Move AGENTS.md to the project repo root (not ~/.claude) and make it the only governance file
Rotate that Stripe live key immediately — it's in history.jsonl line 61304
Set up GitHub Projects with 4 lanes and migrate your open tasks there
Wire Hermes to the GitHub API so /lanes on your phone returns real data. ok net work for you
