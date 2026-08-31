---
captured: 2026-08-26T11:20:08+00:00
session: 78caaa17-0304-47a6-837b-896a02f066d8
cwd: /Users/chidionyema/dev/code
chars: 1916
source: founder prompt, verbatim (founder-doc-capture.py)
---

What this does (the hard version)
1. Auto-Objective Assignment
Agent finishes a task → stop hook fires → goal-guard.py says "no objective"
auto-objective.py FORCE-ASSIGNS the oldest open crew# item from the board
The session cannot end. The agent must execute or declare BLOCKED:
Only escape: founder says STOP
2. Idle Guard v2 — Hard Block
Agent backgrounds a long command → claims "nothing independent to do"
idle-guard-v2.py scans the board for unassigned open items
If any exist → HARD BLOCK. Session cannot end.
Agent must start the independent task immediately
If the agent lies about "nothing independent" → violation logged, flagged
3. Session Timeout — Terminate
Agent produces zero commits, zero PRs, zero output for 10 minutes
session-timeout.sh kills the session
Objective is preserved and reassigned to the next session
Agent cannot "think" or "recon" for 10 minutes without shipping
4. BLOCKED — Validated Escape
Agent may declare BLOCKED: <exact reason> with:
What they tried
Exact error
What they need
Who can unblock
Peer agent or founder validates within 1 hour
Real blocker → reassigned to unblocking agent
False blocker → rogue session, agent flagged
5. Stop Hook Chain
plain
goal-guard → auto-objective → idle-guard-v2 → session-timeout → dod-guard → enterprise-guard
Any one fails → session cannot end.
How to deploy it
Step 1: Add auto-objective.py to the stop hooks. Immediate. No grace period.
Step 2: Add idle-guard-v2.py to the stop hooks. Immediate.
Step 3: Add session-timeout.sh as a cron job running every 5 minutes. 24h grace for agents to adapt, then hard.
Step 4: Add BLOCKED validation to the board scan.
What changes for the founder
You never say "keep moving" again. The system moves them. You only say:
STOP — session ends, objective back to board
RELEASE — session ends, objective reassigned
BLOCKED: <reason> — same as agent, but you authorize it
Everything else is automatic.
