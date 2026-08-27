# Crew Board Visibility — Complete Guide

## What is the Crew Board?

**Location:** `github.com/chidionyema/crew/issues`  
**Purpose:** Single source of truth for all estate decisions, P1 fires, and agent handoffs  
**Access:** Web browser OR terminal (`gh` CLI) OR Telegram  

Every agent (Architect, maestro, WORK, WATCH, coordinator, founder) uses this board:
- **P1 fires** live here (the 5 active problems)
- **Decisions** are recorded here (why, not just what)
- **Handoffs** are commented here (what you did, what's next)
- **Evidence** is linked here (commands, outputs, logs)

---

## Four Ways to See the Board

### **1. GitHub Web Interface (Browse everything)**

```bash
# Open in browser
open https://github.com/chidionyema/crew/issues

# Or use gh CLI to open
gh repo view chidionyema/crew --web
```

**What you see:**
- All open issues, grouped by label
- Recent comments on each issue
- Filter by label (P1, triage, needs-human, etc.)
- Sort by activity, newest, oldest

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
  -q '.[] | "[\(.number)] \(.title) [\(.assignees[0].login // "unassigned")]"'
```

---

### **3. Terminal — Read a Specific Issue**

```bash
# View issue #35 (Fly build blocked)
gh issue view --repo chidionyema/crew 35

# View issue #35 with full body + comments
gh issue view --repo chidionyema/crew 35 --comments

# View in raw format (good for piping/grepping)
gh issue view --repo chidionyema/crew 35 --json number,title,body,comments
```

**Output shows:**
```
#35 Fly.io refuses to build: the account has overdue invoices
OPEN · assigned to someone
  
Body:
  [issue description with evidence]
  
Comments:
  [conversation, updates, status]
```

---

### **4. Terminal — Watch Live Updates**

```bash
# Watch for new comments on P1 issues
watch -n 30 'gh issue list --repo chidionyema/crew --label P1 --state open --json number,title,comments -q ".[] | \"[#\(.number)] \(.title) (\(.comments | length) comments)\""'

# Or create a live dashboard (see section below)
```

---

## Quick Reference: View Commands

| Goal | Command |
|------|---------|
| List all open issues | `gh issue list --repo chidionyema/crew --state open` |
| List P1 fires only | `gh issue list --repo chidionyema/crew --label P1` |
| List issues assigned to you | `gh issue list --repo chidionyema/crew --assignee @me` |
| List by status | `gh issue list --repo chidionyema/crew --label in-progress` |
| View issue #35 | `gh issue view --repo chidionyema/crew 35` |
| View with comments | `gh issue view --repo chidionyema/crew 35 --comments` |
| Search issues | `gh issue list --repo chidionyema/crew --search "keyword"` |
| View latest comments | `gh issue view --repo chidionyema/crew 35 --json comments -q '.comments[] \| "\(.author.login): \(.body)"'` |

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

Fly           | NOT RUN — account empty, `fly apps list` returns "No apps found" (2026-08-26)

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
# Watch for new comments on P1 #35

while true; do
  clear
  echo "=== ISSUE #35 (Fly build blocked) ==="
  echo ""
  
  # Show the issue
  gh issue view --repo chidionyema/crew 35 --json title,body,comments \
    -q '"Title: " + .title + "\n\n" + .body + "\n\n--- COMMENTS ---\n" + (.comments | map("\(.author.login) (\(.createdAt | fromdateiso8601 | now - . | if . < 3600 then "\(. / 60 | floor)m ago" elif . < 86400 then "\(. / 3600 | floor)h ago" else "\(. / 86400 | floor)d ago" end)):\n\(.body)\n") | join("\n"))'
  
  echo ""
  echo "Last refreshed: $(date)"
  sleep 30
done
```

---

## How to Post Updates to the Board

### **Comment on an Issue**

```bash
# Add a comment to issue #35
gh issue comment 35 --repo chidionyema/crew -b "Status update: Fly payment resolved, unblocking builds"

# Add with evidence (command + output)
gh issue comment 35 --repo chidionyema/crew -b "$(cat <<'EOF'
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
gh issue edit 35 --repo chidionyema/crew --add-label in-progress

# Assign to yourself
gh issue edit 35 --repo chidionyema/crew --assignee @me

# Close an issue
gh issue close 35 --repo chidionyema/crew
```

---

## Integration with Architect & maestro

**Both agents watch the board:**

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
# 1. View P1 fires right now
gh issue list --repo chidionyema/crew --label P1 --json number,title

# 2. Open in browser
open https://github.com/chidionyema/crew/issues

# 3. Watch live (every 30 sec)
watch -n 30 'crew-board'

# 4. Post a status update
gh issue comment 35 --repo chidionyema/crew -b "Status: working on X, next step Y"

# 5. Watch Architect/maestro respond by reading the board
tail -f ~/.maestro/maestro.log
```

---

**The board is your window into what all agents (human and AI) are doing, thinking, and planning.**

Use it. Post to it. The agents read it. No repeated questions, no confusion, maximum clarity.
