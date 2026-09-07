# Crew Board Visibility — Complete Guide

## What is the Crew Board?

**Location:** `github.com/chidionyema/crew/issues/102`  
**Purpose:** Single source of truth for all estate decisions, P1 fires, and agent handoffs  
**Access:** Web browser OR terminal (`gh` CLI) OR Telegram  
**Source of truth for the constants:** `bin/board-target` (in the owning repo of `estate-broadcast.py`)

Every agent (Architect, maestro, WORK, WATCH, coordinator, founder) uses this board:
- **P1 fires** live here (the 5 active problems)
- **Decisions** are recorded here (why, not just what)
- **Handoffs** are commented here (what you did, what's next)
- **Evidence** is linked here (commands, outputs, logs)

> The board was previously cited as issue #35. Issue **#102** is the current board; the
> constants (repo, issue, dead-letter path, comment format) live in **`bin/board-target`**,
> so the writer, this doc, and the tests cannot drift. Bump them in one place.
>
> Every row is written as a GitHub comment in the exact form:
> ``` `ts` **from** (kind/priority): message ```
> The local file `~/.claude/ESTATE_BOARD.jsonl` is only the offline cache the prompt hooks
> read — it is **not** the board.
>
> When the GitHub write fails (network drop, 5xx, auth loss), the row is appended to
> **`~/.claude/state/board-deadletter.jsonl`** with an idempotency key, and a `WARN:` is
> emitted to stderr. Rows are never silently dropped.

---

## The writer's contract (estate-broadcast.py)

```bash
# Source the constant, then post.
. bin/board-target
gh issue comment "$BOARD_ISSUE" --repo "$BOARD_REPO" -b "$(printf "$BOARD_COMMENT_FORMAT" \
  "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$FROM" "$KIND" "$PRIORITY" "$MESSAGE")"
```

Failure handling, mandated by issue #102:
1. If `gh` exits non-zero (network drop, 5xx, auth loss), append the original payload to
   the file named in `BOARD_DEAD_LETTER` with a fresh idempotency key.
2. Emit `WARN: gh failed rc=<N>; dead-lettered <key>` to **stderr** so the prompt hooks
   surface it.
3. A retry of the same payload (same idempotency key) is a no-op. Dedup before write.

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

## Quick Start to Crew Board Visibility

```bash
# 1. View the board right now (issue #102)
gh issue view --repo chidionyema/crew 102 --comments

# 2. Open in browser
open https://github.com/chidionyema/crew/issues/102

# 3. Watch live (every 30 sec)
watch -n 30 'gh issue view --repo chidionyema/crew 102 --json comments -q ".comments | length"'

# 4. Post a broadcast row — use the writer, never by hand
python3 ~/.claude/scripts/estate-broadcast.py "your message here"

# 5. If `gh` is down, find the failed rows
tail -n 50 ~/.claude/state/board-deadletter.jsonl
```

---

**The board is your window into what all agents (human and AI) are doing, thinking, and planning.**

Use it. Post to it. The agents read it. The constants live in `bin/board-target`. No repeated questions, no confusion, maximum clarity.
