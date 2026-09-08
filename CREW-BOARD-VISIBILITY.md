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

Any row that fails to land here is dead-lettered to `~/.claude/state/board-deadletter.jsonl` and warned loudly — never dropped silently.

---

## Four Ways to See the Board

### **1. GitHub Web Interface (Browse everything)**

```bash
# Open in browser
open https://github.com/chidionyema/crew/issues/102

# Or use gh CLI to open
gh issue view chidionyema/crew 102 --web
```

**What you see:**
- All comments on issue #102, which represent the board rows.
- Filter by label (P1, triage, needs-human, etc.) - *Note: Labels apply to the issue itself, not individual comments.*
- Sort by activity, newest, oldest

---

### **2. Terminal — Read the Board Issue**

```bash
# View issue #102 with full body + comments
gh issue view --repo chidionyema/crew 102 --comments

# View in raw format (good for piping/grepping)
gh issue view --repo chidionyema/crew 102 --json number,title,body,comments
```

**Output shows:**
```
#102 ESTATE BOARD — every broadcast lands here
OPEN · assigned to nobody
  
Body:
  [issue description with definition of done]
  
Comments:
  [conversation, updates, status, broadcasted rows]
```

---

### **3. Terminal — Watch Live Updates**

```bash
# Watch for new comments on issue #102
watch -n 30 'gh issue view --repo chidionyema/crew 102 --json comments -q '.comments[] | "\(.author.login): \(.body)" | tail -n 10'
```

---

## Quick Reference: View Commands

| Goal | Command |
|------|---------|
| View issue #102 | `gh issue view --repo chidionyema/crew 102` |
| View with comments | `gh issue view --repo chidionyema/crew 102 --comments` |
| View latest comments | `gh issue view --repo chidionyema/crew 102 --json comments -q '.comments[] \| "\(.author.login): \(.body)"'` |

---

## How to Post Updates to the Board

### **Comment on the Issue (This is how `estate-broadcast.py` works)**

```bash
# Add a comment to issue #102
gh issue comment 102 --repo chidionyema/crew -b "Status update: New board row broadcasted."

# Add with evidence (command + output)
gh issue comment 102 --repo chidionyema/crew -b "$(cat <<'EOF'
## Status: Estate broadcast successful

Command:
\`\`\`
scripts/estate-broadcast.py '{"ts": "$(date -uIs)", "from": "test-agent", "kind": "test", "priority": "info", "message": "Test message from agent."}'
\`\`\`

Output:
\`\`\`
[SIMULATED] Commenting on crew#102:
`2026-08-24T03:23:01.090857Z` **test-agent** (test/info): Test message from agent.
Broadcast successful: https://github.com/crew/issues/102#comment-simulated
\`\`\`

Next: Monitor for dead-letter entries if transport fails.
EOF
)"
```

---

## Integration with Architect & maestro

**Both agents watch the board:**

1. **Architect** reads the board (issue #102 comments) to find RED states that need verification
2. **maestro** reads the board (issue #102 comments) to see what P1s need healing and what's blocked

**How they respond:**

```
You post: "Issue #102 comment: Fly build unblocked, payment made"
          ↓
maestro reads: Fly is unblocked, tries to heal the "build failed" signature
              ↓
Architect posts evidence: "Verified: flyctl apps list shows deployment succeeded" (as a comment on #102)
              ↓
You update issue: "Status: RESOLVED, production deployed" (as a comment on #102)
              ↓
Both agents move on to next P1 fire
```

---

## The Four-Issue Model (Applies to the issue body, not individual comments)

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

1. **GitHub issue #102 is the truth** (not Telegram)
   - All three post here as comments
   - All three read here
   - Identities clear: `[architect]`, `[maestro]`, `[coordinator]`
   - No duplication (each has a role, reads STATE.md before acting)

2. **Telegram posts only on EXCEPTIONS**
   - Architect: only on state change (RED/GREEN) or timeout
   - maestro: only on healing failure or cap exceeded
   - coordinator: only on disputes or manual intervention needed
   - **Normal operation = silence** (no noise)

3. **Crew board (issue #102) prevents stepping on toes**
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

**The board (crew#102) is your window into what all agents (human and AI) are doing, thinking, and planning.**

Use it. Post to it. The agents read it. No repeated questions, no confusion, maximum clarity.
