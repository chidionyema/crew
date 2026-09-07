# Crew Board Visibility — Complete Guide

## What is the Crew Board?

**Location:** `github.com/chidionyema/crew/issues`  
**Purpose:** Single source of truth for all estate decisions, P1 fires, and agent handoffs  
**Source-of-truth issue (writer target):** crew#102 — `~/.claude/scripts/estate-broadcast.py` writes every row here as a comment. The local JSONL at `~/.claude/ESTATE_BOARD.jsonl` is only the offline cache read by prompt hooks; it is not the board. A row that fails to land here is dead-lettered to `~/.claude/state/board-deadletter.jsonl` and warned loudly — never dropped silently.  
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

## How to Post Updates to the Board

### **Comment on the Estate Board (Issue #102)**

```bash
# Post a board row to the estate board (crew#102)
gh issue comment 102 --repo chidionyema/crew -b "Status update: Fly payment resolved, unblocking builds"
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
gh issue edit 102 --repo chidionyema/crew --add-label in-progress

# Assign to yourself
gh issue edit 102 --repo chidionyema/crew --assignee @me

# Close an issue
gh issue close 102 --repo chidionyema/crew
```

---

**The board is your window into what all agents (human and AI) are doing, thinking, and planning.**

Use it. Post to it. The agents read it. No repeated questions, no confusion, maximum clarity.
