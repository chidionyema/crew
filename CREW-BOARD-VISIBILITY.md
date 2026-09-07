# Crew Board Visibility — Complete Guide

## What is the Crew Board?

**Location:** `github.com/chidionyema/crew/issues/102`  
**Purpose:** Single source of truth for all estate decisions, P1 fires, and agent handoffs  
**Access:** Web browser OR terminal (`gh` CLI) OR Telegram  

Every agent (Architect, maestro, WORK, WATCH, coordinator, founder) uses this board:
- **P1 fires** live here (the 5 active problems)
- **Decisions** are recorded here (why, not just what)
- **Handoffs** are commented here (what you did, what's next)
- **Evidence** is linked here (commands, outputs, logs)

> The board was previously cited as issue #35. Issue **#102** is the current board; the
> constant lives in `bin/board-target` in the owning repo of `estate-broadcast.py`, so the
> doc, writer and test cannot drift.
>
> Every row is written as a GitHub comment with this format:
> `ts **from** (kind/priority): message`. The local file `~/.claude/ESTATE_BOARD.jsonl`
> is only the offline cache that prompt hooks read; **it is not the board**.
>
> When the GitHub write fails (network drop, 5xx, auth loss), the row is appended to
> `~/.claude/state/board-deadletter.jsonl` and a loud warning is emitted to stderr.
> Rows are never silently dropped.

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
  -q '.[] | "[\(.number)] \(.title) [\(.assignees[0].login // "unassigned")]""'
```

---

### **3. Terminal — Read a Specific Issue**

```bash
# View the board (issue #102)
gh issue view --repo chidionyema/crew 102

# View the board with full body + comments
gh issue view --repo chidionyema/crew 102 --comments

# View in raw format (good for piping/grepping)
gh issue view --repo chidionyema/crew 102 --json number,title,body,comments
```

**Output shows:**
```
#102 ESTATE BOARD — every broadcast lands here
OPEN
  
Body:
  [the board contract: format, dead-letter path, doD]
  
Comments:
  [broadcast rows: ts **from** (kind/priority): message]
```

---

### **4. Terminal — Watch Live Updates**

```bash
# Watch for new comments on the board (issue #102)
watch -n 30 'gh issue view --repo chidionyema/crew 102 --comments --json comments \
  -q ".comments | length" | xargs -I{} echo "live comments: {}"'
```

---

## Quick Reference: View Commands

| Goal | Command |
|------|---------|
| List all open issues | `gh issue list --repo chidionyema/crew --state open` |
| List P1 fires only | `gh issue list --repo chidionyema/crew --label P1` |
| List issues assigned to you | `gh issue list --repo chidionyema/crew --assignee @me` |
| List by status | `gh issue list --repo chidionyema/crew --label in-progress` |
| View the board (#102) | `gh issue view --repo chidionyema/crew 102` |
| View the board with comments | `gh issue view --repo chidionyema/crew 102 --comments` |
| Search issues | `gh issue list --repo chidionyema/crew --search "keyword"` |
| View latest comments | `gh issue view --repo chidionyema/crew 102 --json comments -q '.comments[] \| "\(.author.login): \(.body)"'` |

---

## Posting a Board Row (the writer's contract)

```bash
# The writer `estate-broadcast.py` posts to issue #102, not #35.
gh issue comment 102 --repo chidionyema/crew -b "$COMMENT"
```

Where `$COMMENT` has the exact form:

```
ts **from** (kind/priority): message
```

If the `gh` call fails (network drop, 5xx, auth loss), the writer appends the same row to
`~/.claude/state/board-deadletter.jsonl` with an idempotency key and emits a `WARN:` to
stderr. The next retry of the same payload is a no-op (deduped by the key). No row is
silently dropped.

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

## Integration with Architect & maestro

**Both agents watch the board:**

1. **Architect** reads the board to find RED states that need verification
2. **maestro** reads the board to see what P1s need healing and what's blocked

**How they respond:**

```
You post: "Issue #102: Fly build unblocked, payment made"
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
# 1. View the board right now (issue #102)
gh issue view --repo chidionyema/crew 102 --comments

# 2. Open in browser
open https://github.com/chidionyema/crew/issues/102

# 3. Watch live (every 30 sec)
watch -n 30 'gh issue view --repo chidionyema/crew 102 --json comments -q ".comments | length"'

# 4. Post a status update (via estate-broadcast.py, never by hand)
python3 ~/.claude/scripts/estate-broadcast.py "your message here"

# 5. Watch Architect/maestro respond by reading the board
tail -f ~/.maestro/maestro.log
```

---

**The board is your window into what all agents (human and AI) are doing, thinking, and planning.**

Use it. Post to it. The agents read it. No repeated questions, no confusion, maximum clarity.
