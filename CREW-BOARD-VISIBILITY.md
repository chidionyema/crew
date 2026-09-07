# Crew Board Visibility — Complete Guide

## What is the Crew Board?

**Location:** `github.com/chidionyema/crew/issues/102` (issue 102 IS the board)  
**Purpose:** Single source of truth for all estate decisions, P1 fires, and agent handoffs  
**Access:** Web browser OR terminal (`gh` CLI) OR Telegram  

Every agent (Architect, maestro, WORK, WATCH, coordinator, founder) uses this board:
- **P1 fires** live here (the 5 active problems)
- **Decisions** are recorded here (why, not just what)
- **Handoffs** are commented here (what you did, what's next)
- **Evidence** is linked here (commands, outputs, logs)

> **Cutover:** 2026-08-24. The board moved from issue 35 to issue 102 (founder ruling, 2026-08-24: "why not just use github issues? why reinvent the wheel badly"). Every `gh` command below now points at `#102`, not `#35`.

---

## Four Ways to See the Board

### **1. GitHub Web Interface (Browse everything)**

```bash
# Open in browser
open https://github.com/chidionyema/crew/issues/102

# Or use gh CLI to open
gh repo view chidionyema/crew --web
```

**What you see:**
- All comments on issue #102 in chronological order
- Founder directives first, then session handoffs, then alerts
- Backfills land at the top so old rows are not lost
- Filter by label (P1, triage, needs-human, etc.) on the issue list page

---

### **2. Terminal — List All Issues**

```bash
# Show all open issues with labels
gh issue list --repo chidionyema/crew --state open \
  --json number,title,labels \
  -q '.[] | "\(.number | tostring | lpad(3)) | \(.title) | \(.labels | map(.name) | join(","))"'

# Show just P1 fires
gh issue list --repo chidionyema/crew --label P1 --state open \
  --json number,title \
  -q '.[] | "[#\(.number)] \(.title)"'

# Show by status (in-progress, pr-open, merged, etc.)
gh issue list --repo chidionyema/crew --label in-progress --state open \
  --json number,title,assignees \
  -q '.[] | "[\(.number)] \(.title) [\(.assignees[0].login // "unassigned")]'
```

---

### **3. Terminal — Read the Board (issue #102)**

```bash
# View issue #102 (the estate board)
gh issue view --repo chidionyema/crew 102

# View issue #102 with full body + comments
gh issue view --repo chidionyema/crew 102 --comments

# View in raw format (good for piping/grepping)
gh issue view --repo chidionyema/crew 102 --json number,title,body,comments
```

**Output shows:**
```
#102 ESTATE BOARD — every broadcast lands here
OPEN

Body:
  [the board contract: JSONL is offline cache, every row lands here as a comment,
   failures dead-letter loudly to ~/.claude/state/board-deadletter.jsonl]

Comments:
  [every broadcast row in chronological order, oldest first]
```

### **4. Terminal — Watch Live Updates**

```bash
# Watch for new comments on the board
watch -n 30 'gh issue view --repo chidionyema/crew 102 --json comments \
  -q ".comments | length | tostring + \" comments\""'
```

---

## Quick Reference: View Commands

| Goal | Command |
|------|---------|
| List all open issues | `gh issue list --repo chidionyema/crew --state open` |
| List P1 fires only | `gh issue list --repo chidionyema/crew --label P1` |
| List issues assigned to you | `gh issue list --repo chidionyema/crew --assignee @me` |
| List by status | `gh issue list --repo chidionyema/crew --label in-progress` |
| View the board (issue #102) | `gh issue view --repo chidionyema/crew 102` |
| View with comments | `gh issue view --repo chidionyema/crew 102 --comments` |
| Search issues | `gh issue list --repo chidionyema/crew --search "keyword"` |
| View latest comments | `gh issue view --repo chidionyema/crew 102 --json comments -q '.comments[] \| "\(.author.login): \(.body)"'` |

---

## What You See on the Board Right Now

### **P1 Fires (5 open)**

```
#38 - The exit from Fly has never once been drilled: the escape hatch cannot pass
     Status: unknown / not drilled
     Assigned: ?
     
#35 - Fly.io refuses to build: the account has overdue invoices, production 10 commits behind
     Status: blocked (needs payment/decision)
     Assigned: ?
     
#26 - Estate spend is $431/day against a $120 cap and the only brake reaches 0.03% of it
     Status: needs audit + cost control strategy
     Assigned: ?
     
#22 - Observability: the proposed architecture covers a third of the estate — audit needed
     Status: audit in progress or planned
     Assigned: ?
     
#13 - Retire the Hermes estate — unconditional, Hermes is discontinued
     Status: planning / conditional on P1 #35
     Assigned: ?
```

### **Triage Issues (many)**

Issues waiting for decision or assignment. Examples:
- #53: Ticket gate covers Claude Code only, not codex/gemini
- #52: aiden WAITING alerts are noise
- #51: rule-guard.py matches command strings inside quotes
- #50: Lost previous session's work

---

## Current Board State (from STATE.md)

```
The Architect | RED | bin/verify: 16 passed, 1 failed
              └─ FAIL: every job reaches founder delivers to nobody (session-coordinator monitor)

maestro       | GREEN | last cycle 2 min ago
              └─ skills: 1 skill it can heal with

Fly           | 2 deployed, 12 suspended

crew P1       | 5 open (all fires)
```

**Key:** Architect is RED (the cron job I created isn't delivering to Telegram).

---

## Creating the Crew Board Dashboard

### **One-Command View (All Issues)**

```bash
#!/bin/bash
# Save as ~/bin/crew-board

echo "════════════════════════════════════════════════════════════════"
echo "                    CREW BOARD (all open issues)"
echo "════════════════════════════════════════════════════════════════"

echo ""
echo "🔥 P1 FIRES (5 open, need work)"
gh issue list --repo chidionyema/crew --label P1 --state open \
  --json number,title,assignees,comments \
  -q '.[] | "[#\(.number | tostring | lpad(3))] \(.title) | assigned:\(.assignees[0].login // "nobody") | \(.comments | length) comments"'

echo ""
echo "⚙️  IN PROGRESS (who is working on what)"
gh issue list --repo chidionyema/crew --label in-progress --state open \
  --json number,title,assignees \
  -q '.[] | "[#\(.number | tostring | lpad(3))] \(.title) | assigned:\(.assignees[0].login // "nobody")"'

echo ""
echo "📋 TRIAGE (waiting for decision)"
gh issue list --repo chidionyema/crew --label triage --state open \
  --json number,title \
  -q '.[] | "[#\(.number | tostring | lpad(3))] \(.title)"' | head -10

echo ""
echo "🔗 NEEDS HUMAN (decision-required)"
gh issue list --repo chidionyema/crew --label needs-human --state open \
  --json number,title \
  -q '.[] | "[#\(.number | tostring | lpad(3))] \(.title)"'

echo ""
echo "Last updated: $(date)"
```

Run it:
```bash
chmod +x ~/bin/crew-board
crew-board              # once
watch -n 60 crew-board  # every 60 seconds
```

---

### **P1 Fires Only Dashboard**

```bash
#!/bin/bash
# Save as ~/bin/p1-watch

watch -n 30 'echo "=== P1 FIRES ===" && \
gh issue list --repo chidionyema/crew --label P1 --state open \
  --json number,title,labels,assignees,comments \
  -q ".[] | \"[#\(.number)] \(.title)\n   Status: \(.labels | map(.name) | join(\",\")) | Assigned: \(.assignees[0].login // \"nobody\") | \(.comments | length) comments\n\"" && \
echo "Last updated: $(date)"'
```

---

### **Live Comment Feed**

```bash
#!/bin/bash
# Watch for new comments on the board (issue #102)

while true; do
  clear
  echo "=== ISSUE #102 (ESTATE BOARD) ==="
  echo ""
  
  # Show the issue
  gh issue view --repo chidionyema/crew 102 --json title,body,comments \
    -q '"Title: " + .title + "\n\n" + .body + "\n\n--- COMMENTS ---\n" + (.comments | map("\(.author.login) (\(.createdAt | fromdateiso8601 | now - . | if . < 3600 then "\(. / 60 | floor)m ago" elif . < 86400 then "\(. / 3600 | floor)h ago" else "\(. / 86400 | floor)d ago" end)):\n\(.body)\n") | join("\n"))'
  
  echo ""
  echo "Last refreshed: $(date)"
  sleep 30
done
```

---

## How to Post Updates to the Board

### **Comment on the Board (issue #102)**

```bash
# Add a comment to the estate board
gh issue comment 102 --repo chidionyema/crew -b "Status update: Fly payment resolved, unblocking builds"

# Add with evidence (command + output)
gh issue comment 102 --repo chidionyema/crew -b "$(cat <<'EOF'
## Status: Fly invoice paid

Command:
\`\`\`
fly auth status
\`\`\`

Output:
\`\`\`
Account chidionyema
Status: Active
Invoice: PAID
\`\`\`

Next: Retry build (production 10 commits behind)
EOF
)"
```

> **Always post via `gh issue comment 102 --repo chidionyema/crew -b ...`.** Direct writes to `~/.claude/ESTATE_BOARD.jsonl` have produced 56 unparseable rows in the past — the reader repairs them on read, but the writer must use the API.

### **Create a New Issue**

```bash
gh issue create --repo chidionyema/crew \
  --title "New finding: X needs Y" \
  --body "Description with evidence" \
  --label triage
```

### **Change Issue Status**

```bash
# Add label (mark as in-progress)
gh issue edit 102 --repo chidionyema/crew --add-label in-progress

# Assign to yourself
gh issue edit 102 --repo chidionyema/crew --assignee @me
```

---

## When the Board Writer Fails — Dead-Letter Path

The board is **issue #102**. Every broadcast row must land there as a comment. If the `gh` write fails (network drop, 5xx, auth loss), the row **must not be dropped silently**.

**On failure, the writer:**
1. Appends `{ts, from, kind, priority, message, idempotency_key}` to `~/.claude/state/board-deadletter.jsonl`
2. Prints a loud warning to `stderr`
3. Emits a board-row of `kind=deadletter` so the failure is visible on the board itself
4. Returns a non-zero exit code

**Replay:**
```bash
# Inspect the dead-letter queue
jq '.' ~/.claude/state/board-deadletter.jsonl

# Count un-replayed rows (must be 0 in normal operation)
jq 'length' ~/.claude/state/board-deadletter.jsonl 2>/dev/null || echo 0

# Replay one row by hand (read dead-letter row, re-post to the board)
jq -r '.[].comment' ~/.claude/state/board-deadletter.jsonl | \
  xargs -I {} gh issue comment 102 --repo chidionyema/crew -b {}
```

The dead-letter file is **not** the board. It is the safety net that the loud failure class (board writer with no failure handling) was creating. Rows that reach it must be replayed; they cannot stay there.

---

## Integration with Architect & maestro

**Both agents watch the board (issue #102):**

1. **Architect** reads the board to find RED states that need verification
2. **maestro** reads the board to see what P1s need healing and what's blocked

**How they respond:**

```
You post: "Issue #35: Fly build unblocked, payment made"
          ↓
maestro reads: Fly is unblocked, tries to heal the "build failed" signature
              ↓
Architect posts evidence: "Verified: flyctl apps list shows deployment succeeded"
              ↓
You update issue: "Status: RESOLVED, production deployed"
              ↓
Both agents move on to next P1 fire
```

---

## The Four-Issue Model

Every issue follows this pattern:

```
## Origin — what was asked
[The problem statement]

## Evidence — what we found
[Raw command output, logs, metrics]

## Analysis — what it means
[Interpretation, root cause, blocked by what]

## Next Step
[What needs to happen next]
```

This means:
- ✓ Every issue has proof, not claims
- ✓ Next step is always clear
- ✓ Both agents know what to do
- ✓ Founder doesn't repeat questions

---

## Addressing Your Question: Managing 3 Bots on One Interface

**Challenge:** Architect + maestro + coordinator (me) all posting to same Telegram + GitHub board

**Solution:**

1. **GitHub board is the truth** (not Telegram)
   - All three post here
   - All three read here
   - Identities clear: `[architect]`, `[maestro]`, `[coordinator]`
   - No duplication (each has a role, reads STATE.md before acting)

2. **Telegram posts only on EXCEPTIONS**
   - Architect: only on state change (RED/GREEN) or timeout
   - maestro: only on healing failure or cap exceeded
   - coordinator: only on disputes or manual intervention needed
   - **Normal operation = silence** (no noise)

3. **Crew board prevents stepping on toes**
   - Each agent reads the board before starting
   - "I'm working on #35" posted = others know not to redo it
   - Handoff is a comment, not a DM
   - Founder reads one board, not three separate channels

4. **Evidence prevents disputes**
   - Every claim includes command output
   - If Architect says "RED", here's the failing test
   - If maestro says "healing failed", here's the attempt and result
   - No "I think X is happening" (only measured facts)

**Result:** Three agents, one board, zero confusion. All operating autonomously within their role.

---

## Quick Start to Crew Board Visibility

```bash
# 1. View the board (issue #102) right now
gh issue view --repo chidionyema/crew 102 --comments | tail -20

# 2. Open in browser
open https://github.com/chidionyema/crew/issues/102

# 3. Watch live (every 30 sec)
watch -n 30 'gh issue view --repo chidionyema/crew 102 --json comments \
  -q ".comments | length | tostring + \" comments\""'

# 4. Post a status update to the board
gh issue comment 102 --repo chidionyema/crew -b "Status: working on X, next step Y"

# 5. Check the dead-letter queue is empty
jq 'length' ~/.claude/state/board-deadletter.jsonl 2>/dev/null || echo 0
```

---

**The board is your window into what all agents (human and AI) are doing, thinking, and planning.**

Use it. Post to it. The agents read it. No repeated questions, no confusion, maximum clarity.
