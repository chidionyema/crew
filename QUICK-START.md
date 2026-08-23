# Quick Start: Watch & Control Architect & maestro

## Watch Everything (live dashboard)

```bash
# 1. Open 4 terminals (or use tmux/screen)

# Terminal 1: The Architect (verification)
tail -f ~/dev/code/hermes-v2/logs/agent.log

# Terminal 2: maestro (sensing)
tail -f ~/.maestro/maestro.log

# Terminal 3: STATE snapshot (truth)
watch -n 60 'cat ~/dev/code/crew/STATE.md | head -20'

# Terminal 4: P1 fires (crew board)
watch -n 60 'gh issue list --repo chidionyema/crew --label P1 --state open --json number,title -q ".[] | \"[\(.number)] \(.title)\""'
```

When you open these 4 terminals:
- **Terminal 1** shows The Architect's live verification runs (RED/GREEN state changes)
- **Terminal 2** shows maestro's thinking (SENSE → REPORT cycles, healing attempts)
- **Terminal 3** shows the official estate state (refreshes hourly, command-backed)
- **Terminal 4** shows open P1 fires (who's working on what)

---

## One-Command Dashboard

```bash
# Create this script at ~/bin/watch-estate
#!/bin/bash
clear
echo "════════════════════════════════════════════════════════════════"
echo "                     ESTATE DASHBOARD"
echo "════════════════════════════════════════════════════════════════"

echo ""
echo "📐 THE ARCHITECT (latest 5 verification lines)"
echo "─────────────────────────────────────────────────────────────────"
tail -20 ~/dev/code/hermes-v2/logs/agent.log | grep -E "PASSED|FAILED|passed|failed" | tail -5

echo ""
echo "🎼 MAESTRO (latest cycle)"
echo "─────────────────────────────────────────────────────────────────"
tail -20 ~/.maestro/maestro.log | grep -E "State:" | tail -3
ls -lt ~/.maestro/intents/ | head -1 | awk '{print "Latest INTENT: " $9 " (" $6 " " $7 " " $8 ")"}'

echo ""
echo "🔍 ESTATE STATE (official, refreshed hourly)"
echo "─────────────────────────────────────────────────────────────────"
cat ~/dev/code/crew/STATE.md | grep "^|" | tail -10

echo ""
echo "🔥 P1 FIRES (open issues)"
echo "─────────────────────────────────────────────────────────────────"
gh issue list --repo chidionyema/crew --label P1 --state open --json number,title -q '.[] | "[#\(.number)] \(.title)"' | head -5

echo ""
echo "Last updated: $(date)"
```

Run it:
```bash
chmod +x ~/bin/watch-estate
watch-estate        # once
watch -n 30 watch-estate  # every 30 seconds
```

---

## Control Points

### Tell The Architect to verify now
```bash
cd ~/dev/code/hermes-v2
./bin/verify
```
Look at output immediately. If RED, post to crew board.

### Tell maestro to sense now
```bash
# maestro cycles every ~3 min automatically
# To force a cycle:
tail -1 ~/.maestro/maestro.log  # see if it just ran
# Wait up to 3 min, or check the code to force a cycle
```

### Tell both agents about a change
```bash
# Edit the issue on the crew board
gh issue comment 35 -R chidionyema/crew -b "Update: payment made, Fly.io is unblocked"

# Both agents read this and respond automatically
```

### Update Architect's baseline (platform changed)
```bash
vim ~/dev/code/hermes-v2/profiles/architect/MEMORY.md
# Change: Healthy state, platform map, baselines
git add -A && git commit -m "architect: platform baseline updated"
```

### Add a healing recipe for maestro
```bash
# Create file: ~/dev/code/crew/remedies/restart-fly-app.yaml
cat > ~/dev/code/crew/remedies/restart-fly-app.yaml << 'EOF'
signature: "app_id: prospector-engine status: created (3xx attempts)"
remedy: "fly machine restart {{ machine_id }} --app prospector-engine"
verify: "fly status -a prospector-engine | grep -q running"
radius: "one machine, ~30s downtime, app auto-restarts"
cap: "2 per 24h"
EOF

git add -A && git commit -m "maestro: added healing recipe for stuck Fly machines"
```

---

## Telegram Integration

Both agents post to your phone automatically:

```bash
# The Architect posts only on:
# - State change: GREEN → RED or RED → GREEN
# - Verify timeout (>120s)

# maestro posts only on:
# - Healing failure (remedy tried 2x, still RED)
# - Healing cap reached (past 2/24h limit)
# - Crisis detection (P0 findings like disk 99%)

# To send a manual message to Telegram:
hermes send --to telegram "Manual status update from founder"
```

**No notification = no problem.**

---

## The 4-Channel Flow

```
ARCHITECT                 MAESTRO              YOU                 TELEGRAM
────────────────────────────────────────────────────────────────────────────
  Run                   Sense (cycle)       Read logs          (silent)
  bin/verify            audit estate        STATE.md
    ↓                      ↓                  ↓
  GREEN/RED          findings/ok?        (truth source)
    ↓                      ↓
  Log result          Report (or heal)
    ↓                      ↓
  STATE.md updated    GitHub issue updated
    ↓                      ↓
  (if RED)            (if exception)
  → Telegram post    → Telegram post
```

---

## Examples

### Example 1: Architect detects a problem

```
$ tail -f ~/dev/code/hermes-v2/logs/agent.log
...
tests/verify.py::test_telegram_reachable FAILED (timeout after 30s)

Architect logs: test_telegram_reachable FAILED
               ↓
STATE.md updates: The Architect | RED | bin/verify: 16 passed, 1 failed
                  ↓
Telegram alerts:  [architect] RED | test_telegram_reachable timed out
                  ↓
You read crew board, post: "Telegram service degraded, investigating"
```

### Example 2: maestro detects a state change

```
$ tail -f ~/.maestro/maestro.log
2026-08-23 22:15:35,100 | INFO | maestro | State: SENSE
2026-08-23 22:15:36,200 | INFO | maestro | audit: 0 findings
2026-08-23 22:15:36,300 | INFO | maestro | State: REPORT
2026-08-23 22:15:36,400 | INFO | maestro | All clear

maestro logs: no findings
              ↓
STATE.md updates: maestro | GREEN | last cycle 2 min ago
                  ↓
Telegram silent (no exception, no crisis)
                  ↓
You see STATE.md: estate is healthy, P1 fires are the only concern
```

### Example 3: You add a P1 fire update

```
$ gh issue comment 35 -R chidionyema/crew -b "Solution: Fly invoices paid, account unblocked"

crew board updates: Issue #35 state: in-progress
                    ↓
Both agents read the board on next cycle
                    ↓
maestro re-senses: Fly is now reachable
                    ↓
STATE.md: Fly | 2 deployed, 12 suspended | flyctl apps list (success)
                    ↓
Telegram: [maestro] P1 #35 unblocked. Progress: Fly is reachable again
```

---

## One-Minute Health Check

```bash
#!/bin/bash
# Copy to ~/bin/health-check and run anytime

echo "Checking estate health..."

ARCH=$(tail -1 ~/dev/code/hermes-v2/logs/agent.log | grep -c "passed")
MAES=$(ls -t ~/.maestro/intents/ | head -1 | xargs stat -f %Sm -t %s)
STATE=$(test -f ~/dev/code/crew/STATE.md && echo "OK" || echo "MISSING")
P1S=$(gh issue list --repo chidionyema/crew --label P1 --state open --json number | grep -c "#")

echo "Architect: $([[ $ARCH -gt 0 ]] && echo "✓" || echo "✗")"
echo "maestro: $([[ $(echo $(date +%s) - $MAES | bc) -lt 300 ]] && echo "✓ (fresh)" || echo "⚠ (stale)")"
echo "STATE.md: $STATE"
echo "P1 Fires: $P1S open"

echo ""
echo "Details:"
tail -1 ~/dev/code/hermes-v2/logs/agent.log | tail -1
ls -lt ~/.maestro/intents/ | head -1 | awk '{print "Latest maestro: " $9}'
```

---

## Remember

1. **STATE.md is truth** — every other piece is context for understanding it
2. **Both agents are always running** — you're watching their output, not controlling them step-by-step
3. **Silence = health** — no Telegram = no exceptions
4. **Evidence in everything** — if you post an update, include the command that proves it
5. **Crew board is the handoff** — that's where all agents (human and AI) sync
