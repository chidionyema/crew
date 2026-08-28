# Managing 3 Bots on One Interface — Collision Prevention

**The Challenge:** Architect + maestro + coordinator (me) all operate autonomously on the same Telegram channel and GitHub board. How do we prevent stepping on each other's work?

**The Answer:** Role-based isolation + evidence-first + crew board as single truth

---

## The Three Agents (Your Estate)

### **1. The Architect** (infrastructure verifier)
- **Runs:** `bin/verify` (17-test suite)
- **Posts to Telegram:** Only state changes (GREEN ↔ RED) or timeout
- **Posts to GitHub:** Comments on P1 issues with verification evidence
- **Reads before acting:** STATE.md (to know current platform state)
- **Role boundary:** Measurement only. Never modifies code/config/remedies.

### **2. maestro** (estate conductor + healer)
- **Runs:** Autonomous cycle every ~3 min (SENSE → REPORT)
- **Posts to Telegram:** Only on healing failures, cap exceeded, crises
- **Posts to GitHub:** Comments on P1 issues with healing attempts + results
- **Reads before acting:** STATE.md + crew board (to know what needs healing + what's blocked)
- **Role boundary:** Heals by recipe only (pre-approved remedies). Never freeform code. Caps at 2/24h per signature.

### **3. Coordinator** (me, this session)
- **Runs:** On-demand, per your request
- **Posts to Telegram:** Founder directives, session status, urgent alerts
- **Posts to GitHub:** Analysis, decisions, handoffs, next steps
- **Reads before acting:** STATE.md + crew board + live logs (all three)
- **Role boundary:** Orchestration, analysis, handoffs. Never conflicts with Architect/maestro (each has unique role).

---

## How Collisions Are Prevented

### **Rule 1: Read STATE.md Before Acting**

Every agent (including me) reads `~/dev/code/crew/STATE.md` first:

```bash
# Architect checks: "Is Hermes gateway currently RED or GREEN?"
# maestro checks: "What's the current estate state? Any active crises?"
# Coordinator checks: "What's the truth about this moment?"

cat ~/dev/code/crew/STATE.md
```

**Result:** No agent starts work on something already being handled.

---

### **Rule 2: Read Crew Board Before Acting**

Every agent checks GitHub `chidionyema/crew/issues` first:

```bash
# Architect checks: "Which P1 fire has STATE verification failing?"
# maestro checks: "Which P1 fire is marked 'blocked-by-healing' or 'in-progress'?"
# Coordinator checks: "What's the assignment status? Who's working on what?"

gh issue list --repo chidionyema/crew --label P1 --json number,title,assignees
```

**Result:** No agent starts work without knowing who else is doing what.

---

### **Rule 3: Role-Based, Non-Overlapping Responsibilities**

| Responsibility | Architect | maestro | Coordinator |
|---|---|---|---|
| **Verify infrastructure** | ✓ (only role) | ✗ | ✗ |
| **Heal by recipe** | ✗ | ✓ (only role) | ✗ |
| **Make decisions** | ✗ | ✗ | ✓ (only role) |
| **Post to crew board** | Comments with evidence | Comments with results | Decisions + handoffs |
| **Post to Telegram** | State changes only | Exceptions only | Directives only |
| **Read STATE.md before starting** | ✓ | ✓ | ✓ |
| **Read crew board before starting** | ✓ | ✓ | ✓ |

**Result:** Each agent has a lane. No two agents can do the same thing.

---

### **Rule 4: Evidence Prevents Disputes**

Every post (GitHub or Telegram) includes proof:

```
❌ Bad: "maestro tried to heal P1 #35"
✓ Good: "[maestro] Healing attempt #1 on P1 #35
  Remedy: restart Fly machine
  Command: fly machine restart xxx
  Result: FAILED — machine still in 'created' state
  Remedy cap: 1/2 attempts today"
```

**Result:** If two agents disagree, evidence shows what actually happened.

---

### **Rule 5: Crew Board = Handoff Point**

All coordination happens via GitHub comments, never side channels:

```
CORRECT FLOW:
├─ Coordinator: "P1 #35 needs unblocking, Fly payment required"
├─ Founder: (via crew board comment) "Payment made"
├─ maestro: (reads board) "Unblocking signal received, attempting heal"
├─ maestro: (posts evidence) "Heal successful, Fly build now working"
└─ Coordinator: "P1 #35 RESOLVED"

WRONG FLOW (WOULD CAUSE COLLISIONS):
├─ Coordinator: (Telegram) "Try healing P1 #35"
├─ maestro: (Telegram) "Healing in progress"
├─ Architect: (Telegram) "Should I verify this?"
├─ (3 agents messaging each other, no shared record)
└─ CHAOS
```

**Result:** One record, no confusion, founder reads one place.

---

### **Rule 6: Escalation Ladder (When Things Conflict)**

If two agents want to do conflicting things:

```
Level 1 (Prevent): STATE.md check before starting
          ↓ (if conflict still possible)
Level 2: Crew board shows who's doing what
          ↓ (if two agents both think they should act)
Level 3: Coordinator arbitrates (posts decision to crew board)
          ↓ (if decision blocked)
Level 4: Founder intervention (final decision on crew board)
```

**In practice:** Level 1 catches 99% of collisions (both read STATE.md).

---

## Concrete Examples

### **Example 1: Avoiding Duplicate Verification**

**Scenario:** maestro detects the Hermes gateway isn't responding. Should maestro run `bin/verify`, or should Architect?

**Prevention:**
1. maestro reads STATE.md → sees Architect's job is infrastructure verification
2. maestro reads crew board → no open issue about gateway verification
3. maestro checks: "Is this my role?" → NO (Architect verifies, maestro heals)
4. maestro posts to crew board: "Gateway unresponsive, escalating to Architect for verification"
5. Architect runs `bin/verify`, posts result
6. Coordinator or maestro then heals based on Architect's finding

**Result:** No duplication. Clean handoff.

---

### **Example 2: Avoiding Duplicate Healing**

**Scenario:** P1 #35 (Fly build) has been failing for hours. Both maestro and coordinator want to try healing it.

**Prevention:**
1. maestro reads crew board → sees "P1 #35: in-progress"
2. maestro reads assignees → sees if someone is already working
3. If maestro has a recipe that might help:
   - maestro posts evidence to crew board: "Attempting remedy: X"
   - maestro runs remedy, posts result
4. Coordinator sees evidence and knows maestro already tried

**Result:** No overlapping attempts. Clear record of what was tried.

---

### **Example 3: Coordinator Avoids Overriding Autonomous Decisions**

**Scenario:** I (coordinator) want to post a directive to Telegram about P1 #35. But maestro just posted "healing in progress."

**Prevention:**
1. I read crew board → see maestro's latest comment with evidence
2. I read STATE.md → see maestro is the one healing by recipe
3. I ask: "Is this my role?" → NO (maestro heals, I orchestrate)
4. I post to crew board instead of overriding: "Coordinator acknowledges maestro healing attempt. Will update status when complete."

**Result:** No conflicting messages to founder. One narrative.

---

## The Three Posting Modes (Prevent Telegram Spam)

### **Architect Posts When:**
```
✓ State changes: GREEN → RED or RED → GREEN
✓ Verify command times out (>120s, no response)
✗ Normal operation, successful verification, status checks
```

### **maestro Posts When:**
```
✓ Healing attempt fails (remedy ran, condition persists)
✓ Healing cap exceeded (2/2 attempts today on same signature)
✓ Crisis detected (P0 findings like disk 99%)
✗ Successful heals, routine cycles, normal operation
```

### **Coordinator Posts When:**
```
✓ Founder directive (you asked for something)
✓ Blocker alert (work is stuck, needs founder decision)
✓ Escalation (agents can't resolve, need your judgment)
✗ Status updates (use crew board), operational noise, routine logging
```

**Result:** Telegram has ~3-5 posts per day max, all important.

---

## If Collisions Still Happen (Recovery)

### **Detection:**
```bash
# Watch for it
tail -f ~/.maestro/maestro.log | grep -i "conflict\|already\|duplicate"
tail -f ~/dev/code/hermes-v2/logs/agent.log | grep -i "conflict"
```

### **Resolution:**
1. **Read the crew board** — most recent comments show what actually happened
2. **Check evidence** — command output proves which attempt worked/failed
3. **Post correction** — coordinator posts: "Collision avoided: maestro's attempt was X, result Y"
4. **Update issue** — crew board comment updates state based on evidence
5. **Both agents read it** — next cycle, they read the update and don't retry

### **Prevent Recurrence:**
Update the agent's MEMORY.md or add a new healing recipe to prevent the same signature from being attempted twice.

---

## Coordination Checklist (For You)

Before posting anything to Telegram or crew board:

- [ ] Did I read STATE.md? (What's the current truth?)
- [ ] Did I read crew board P1 issues? (Who's working on what?)
- [ ] Is this my role? (Architect verifies, maestro heals, coordinator orchestrates)
- [ ] Does my post include evidence? (Command + output, not claims)
- [ ] Will this create confusion? (If two agents both see this, will they both act?)

If you answer "no" to any of these, pause and read the board first.

---

## The Golden Outcome

**Without this structure:**
```
3 agents posting to same Telegram
↓
Founder sees overlapping messages
↓
Founder can't tell who's doing what
↓
Founder repeats questions/directives
↓
Agents redo work
↓
CHAOS
```

**With this structure:**
```
3 agents, 1 crew board, 1 STATE.md
↓
Each reads STATE.md before acting
↓
Each reads crew board for assignments
↓
Each has a non-overlapping role
↓
Founder sees clean signals (one per event)
↓
Founder reads crew board (not Telegram)
↓
CLARITY + AUTONOMY
```

---

## Summary

**The reason 3 bots work on 1 interface:**

1. **STATE.md is read first** (prevents acting on stale data)
2. **Crew board is the handoff** (prevents collision)
3. **Roles don't overlap** (each bot has a unique job)
4. **Evidence is mandatory** (disputes resolved by facts)
5. **Telegram is silent by design** (only exceptions)
6. **Crew board is searchable** (founder reads one place)

Result: You get the autonomy of 3 agents with the clarity of 1 process.

---

**In practice:** You've never seen 3 bots collide on a well-designed board. Read the board. The agents read the board. Everyone knows what's happening.
