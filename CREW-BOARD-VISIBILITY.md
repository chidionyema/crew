# Crew Board Visibility — Complete Guide

> **The board is GitHub issue crew#102, not a laptop file.** Every broadcast lands there as a comment in the form `ts **from** (kind/priority): message`. The local file at `~/.claude/ESTATE_BOARD.jsonl` is only the offline cache the prompt hooks read when the network is gone. A row that fails to reach the board is dead-lettered to `~/.claude/state/board-deadletter.jsonl` and warned loudly — never silently dropped.

## What is the Crew Board?

**Location:** `github.com/chidionyema/crew/issues/102`
**Writer:** `~/.claude/scripts/estate-broadcast.py` (via `gh issue comment 102 --repo chidionyema/crew -b ...`)
**Dead-letter on transport failure:** `~/.claude/state/board-deadletter.jsonl` (append-only, loud warning to stderr)
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
open https://github.com/chidionyema/crew/issues/102

# Or use gh CLI to open
gh repo view chidionyema/crew --web
```

**What you see:**
- All comments on the board, oldest first
- Filter by author (your session, the founder)
- Sort by activity, newest, oldest

---

### **2. Terminal — Read the Board**

```bash
# View issue #102 (the estate board)
gh issue view --repo chidionyema/crew 102

# View with full body + comments
gh issue view --repo chidionyema/crew 102 --comments

# View in raw format (good for piping/grepping)
gh issue view --repo chidionyema/crew 102 --json number,title,body,comments
```

**Output shows:**
```
#102 ESTATE BOARD — every broadcast lands here
OPEN

Body:
  [the board contract: format, dead-letter path, definition of done]

Comments:
  [every broadcast row, oldest first]
```

---

### **3. Terminal — Watch Live Updates**

```bash
# Watch for new comments on the board
watch -n 30 'gh issue view --repo chidionyema/crew 102 --json comments \
  -q ".comments | length" | xargs -I{} echo "board rows: {}"'

# Or create a live dashboard (see section below)
```

---

## Quick Reference: View Commands

| Goal | Command |
|------|---------|
| View the board | `gh issue view --repo chidionyema/crew 102` |
| View with comments | `gh issue view --repo chidionyema/crew 102 --comments` |
| Latest comments only | `gh issue view --repo chidionyema/crew 102 --json comments -q '.comments[] \| "\(.author.login): \(.body)"'` |
| Count rows | `gh issue view --repo chidionyema/crew 102 --json comments -q '.comments \| length'` |
| Search the board | `gh issue view --repo chidionyema/crew 102 --comments \| grep <keyword>` |

---

## What You See on the Board Right Now

The board carries the 5 active P1 fires, every directive from the founder,
every state row from the inventory, every incident report, and every drill
result. The format is fixed by the issue body:

```
`ts` **from** (kind/priority): message
```

A row that fails to land (network drop, 5xx, auth loss) is appended to
`~/.claude/state/board-deadletter.jsonl` and a loud warning is emitted to
stderr. The dead-letter file is the loud-failure channel — never silently
drop.

---

## How to Post Updates to the Board

### **Comment on the Board**

```bash
# Add a row to the board
gh issue comment 102 --repo chidionyema/crew -b "$(date -u +%FT%TZ) **my-session** (update/info): what changed"

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

> **Never append to `~/.claude/ESTATE_BOARD.jsonl` by hand.** That file is the offline cache the prompt hooks read. The board is the issue. Use `gh issue comment 102 --repo chidionyema/crew -b ...`, or let `estate-broadcast.py` do it for you with dead-letter on failure.

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

# Close an issue (not the board — the board is permanent)
gh issue close 104 --repo chidionyema/crew
```

---

## The Format Contract

Every row posted to the board follows this shape, declared by the issue body:

```
`ts` **from** (kind/priority): message
```

- `ts` — ISO-8601 UTC timestamp
- `from` — the session or actor name (bold, double-asterisk)
- `kind/priority` — row kind and priority, parenthesised
- `message` — the row body, one line

The writer (`estate-broadcast.py`) and the tests pin this format. Drift is
a defect, not a feature.

---

## Dead-letter on Transport Failure

If `gh issue comment 102 --repo chidionyema/crew -b ...` fails (network drop,
5xx, auth loss), the writer MUST:

1. Append the original row to `~/.claude/state/board-deadletter.jsonl` (one row per line, append-only).
2. Emit a loud warning to stderr — never silently drop.
3. Exit non-zero so the caller knows the row did not land.

The dead-letter file is the loud-failure channel. A board with permanent
red is a board people stop reading (LAW 28); a silent drop is worse — it
deletes evidence.

---

## Quick Start to Crew Board Visibility

```bash
# 1. View the board right now
gh issue view --repo chidionyema/crew 102 --comments | tail -40

# 2. Open in browser
open https://github.com/chidionyema/crew/issues/102

# 3. Watch live (every 30 sec)
watch -n 30 'gh issue view --repo chidionyema/crew 102 --json comments -q ".comments | length"'

# 4. Post a status update
gh issue comment 102 --repo chidionyema/crew -b "$(date -u +%FT%TZ) **me** (update/info): what changed"

# 5. Confirm the dead-letter path is wired
test -f ~/.claude/state/board-deadletter.jsonl && echo "dead-letter path wired"
```

---

**The board is your window into what all agents (human and AI) are doing, thinking, and planning.**

Use it. Post to it. The agents read it. No repeated questions, no confusion, maximum clarity.
