# Visibility & Communication With Architect & maestro

## Four Channels: Live Logs → State Snapshot → GitHub Board → Telegram

---

## **1. LIVE LOGS (Real-time thinking)**

### The Architect
```bash
# Watch The Architect's latest verification run
tail -f ~/dev/code/hermes-v2/logs/agent.log

# Run a fresh verification right now
cd ~/dev/code/hermes-v2 && ./bin/verify
```

**Output format:**
```
bin/verify
==================== test session starts ====================
tests/verify.py::test_gateway_responds PASSED
tests/verify.py::test_telegram_reachable PASSED
...
==================== 17 passed in 2.34s ====================
```

State machine: IDLE → MEASURE → REPORT → (GREEN or RED)

---

### maestro
```bash
# Watch maestro's live state machine
tail -f ~/.maestro/maestro.log

# See every cycle
tail -50 ~/.maestro/maestro.log | grep "State:"

# Watch what maestro senses on each cycle
tail -f ~/.maestro/maestro.log | grep -E "State:|REPORT|TELEGRAM|findings"
```

**Output format:**
```
2026-08-23 22:10:38,709 | INFO     | maestro | State: SENSE
2026-08-23 22:11:38,900 | INFO     | maestro | State: REPORT
2026-08-23 22:12:39,100 | INFO     | maestro | All clear — no digest sent (P3)
2026-08-23 22:12:39,103 | INFO     | maestro | State: IDLE
```

State machine: IDLE → SENSE (audit/status) → REPORT (post if exception) → IDLE

---

## **2. STATE SNAPSHOT (Single source of truth, refreshed hourly)**

```bash
# Read current estate state (command + output for every claim)
cat ~/dev/code/crew/STATE.md

# Or regenerate fresh (takes ~40 seconds)
~/dev/code/crew/scripts/estate-snapshot

# Watch it regenerate automatically (cron job)
tail -f ~/dev/code/crew/STATE.md
```

**What you see:**
```
| The Architect | GREEN | `bin/verify`: 17 passed, 0 failed |
| maestro | GREEN | last cycle 2 min ago (INTENT-20260823-210335-0d20f3e7.json) |
| &nbsp;&nbsp;skills | GREEN | 1 skill(s) it can heal with |
| Fly | 2 deployed, 12 suspended | `flyctl apps list` |
| crew P1 | 5 open | the fires nobody has put out |
```

**Every row is proof, not a claim.** GREEN/RED is binary. NOT RUN means the measurement itself failed.

---

## **3. GITHUB BOARD (Decisions & handoffs)**

```bash
# Open the crew board in browser
gh repo view chidionyema/crew --web

# Or from the phone
hermes send --to telegram "Open crew board"
```

**What lives here:**
- **P1 fires** (#38, #35, #26, #22, #13) — who's working on each
- **Checkpoints** — progress on active work
- **Triage issues** — findings that need decisions
- **Post-mortems** — lessons learned

**How to communicate:**
1. Find the relevant P1 fire issue
2. Add a comment with your update and evidence
3. maestro watches the board and acts on state changes

**Example:**
```
## Working on #35: Fly build blocked

Issue: Fly.io account has overdue invoices
Blocker: Payment required before any builds
Evidence: 
  $ fly auth status
  Account chidionyema: Invoice $XXX overdue since 2026-08-20
  
Next step: (awaiting founder decision on payment)
```

---

## **4. TELEGRAM (Alerts only)**

Your phone receives:
- **Architect posts**: When state changes GREEN ↔ RED, or verify times out
- **maestro posts**: When healing fails, cap exceeded, or crises detected

**No notifications = everything green.**

---

## **HOW TO COMMUNICATE WITH THEM**

### **Option 1: Direct Command (Architect)**

```bash
# Ask The Architect to run verification now
cd ~/dev/code/hermes-v2 && ./bin/verify

# Force a Telegram post (even if no state change)
hermes switch architect
hermes send --to telegram "[architect] Verification run 2026-08-23 22:15 UTC"
```

### **Option 2: Direct Command (maestro)**

```bash
# Read what maestro is thinking
tail -50 ~/.maestro/maestro.log | tail -20

# Force a status report to Telegram
hermes switch maestro
hermes send --to telegram "[maestro] Cycle complete. All clear."

# Force maestro to re-sense the estate right now
kill -USR1 $(pgrep -f "maestro.*process" | head -1)  # or restart it
```

### **Option 3: GitHub Board (Both agents watch)**

**Post on the relevant P1 issue:**

```
## Status Update: Issue #35 (Fly build blocked)

Command:
```
$ fly auth whoami
Invalid token
```

Finding: Fly token is stale. Last valid login 2026-08-01.
Action: maestro cannot heal (decision-required, not recipe-based)
Next: Awaiting founder to re-auth Fly or update token in ~code/crew/secrets
```

Both agents read the crew board and respond:
- Architect adds verification that the blockage is real
- maestro escalates to Telegram if the P1 fire is blocked

### **Option 4: Update Their Memory**

```bash
# Tell The Architect a new baseline
vim ~/dev/code/hermes-v2/profiles/architect/MEMORY.md
# Edit: "Healthy state: X" or add platform changes
git add -A && git commit -m "architect: updated baseline after platform change"

# Tell maestro about a new healing recipe
vim ~/dev/code/crew/remedies/new-recipe.yaml
# Format: signature, remedy script, verify command, radius, cap
git add -A && git commit -m "maestro: added healing recipe for X"
```

---

## **VISIBILITY DASHBOARD (Everything in one place)**

```bash
#!/bin/bash
# Save this as ~/bin/watch-estate

echo "=== THE ARCHITECT (live verification) ==="
tail -20 ~/dev/code/hermes-v2/logs/agent.log | tail -5

echo ""
echo "=== MAESTRO (live sensing) ==="
tail -20 ~/.maestro/maestro.log | grep -E "State:|REPORT|findings"

echo ""
echo "=== STATE SNAPSHOT (single source of truth) ==="
cat ~/dev/code/crew/STATE.md | head -20

echo ""
echo "=== P1 FIRES (crew board) ==="
gh issue list --repo chidionyema/crew --label P1 --state open --json number,title -q '.[] | "[\(.number)] \(.title)"'

echo ""
echo "=== LAST MAESTRO CYCLE ==="
ls -lt ~/.maestro/intents/ | head -1
```

Run it:
```bash
chmod +x ~/bin/watch-estate
watch-estate

# Or watch it live
watch -n 10 watch-estate
```

---

## **COMMUNICATION PATTERNS**

### **You → Architect** (request verification)
1. Run `cd ~/dev/code/hermes-v2 && ./bin/verify`
2. Check `STATE.md` for result
3. If RED, post finding to crew board P1 issue

### **You → maestro** (request status)
1. Check `~/.maestro/maestro.log` (tail -20)
2. Or wait for next hourly `STATE.md` snapshot
3. If blocked, post on crew board

### **You → Both** (directive/update)
1. Post on the relevant P1 issue: "Next step: …"
2. Both agents read crew board and adjust

### **Architect → You** (alert)
Telegram post only if state changes:
```
[architect] RED | bin/verify: 2 failed
- test_telegram_reachable FAILED
- test_gateway_responds TIMED OUT
```

### **maestro → You** (alert)
Telegram post only on exception:
```
[maestro] HEALING FAILED | Disk still at 97.2% after cleanup
Remedy cap reached (2/2 attempts today)
Manual intervention required: du -sh ~/* | sort -rh
```

---

## **EVIDENCE FORMAT**

Every communication includes:
- **The command** that was run
- **The exact output** (not a summary)
- **When** it ran (timestamp)
- **What it means** (one-line interpretation)

**Good:**
```
$ ~/.maestro/intents/INTENT-20260823-210335-0d20f3e7.json
2026-08-23 21:03:35 UTC — maestro cycle complete
State: SENSE completed, no findings, cycle time 1.2s
```

**Bad:**
```
maestro is running fine
```

---

## **QUICK REFERENCE**

| What you want | Command | Output |
|---|---|---|
| See Architect thinking | `tail -f ~/dev/code/hermes-v2/logs/agent.log` | Verification lines |
| See maestro thinking | `tail -f ~/.maestro/maestro.log` | State transitions |
| See current state | `cat ~/dev/code/crew/STATE.md` | Truth table |
| Force Architect to verify | `cd ~/dev/code/hermes-v2 && ./bin/verify` | PASS/FAIL counts |
| Post to crew board | `gh issue comment <n> -R chidionyema/crew -b "…"` | Issue updated |
| Send to Telegram | `hermes send --to telegram "message"` | Delivered |
| Watch everything | `watch -n 10 watch-estate` | Live dashboard |

---

## **GOLDEN RULE**

**No claim without command output.**

When you post an update anywhere (Telegram, GitHub, memory), include the exact command and its output. This is LAW 2 and LAW 17 in action.

Don't say: "maestro is cycling fine"  
Do say: `ls -lt ~/.maestro/intents/ | head -1` → latest INTENT file is 2 min old

Don't say: "Architect is healthy"  
Do say: `cd ~/dev/code/hermes-v2 && ./bin/verify` → 17 passed, 0 failed
