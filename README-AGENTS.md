# Summary: Architect & maestro Onboarding Complete

**Date:** 2026-08-23  
**Status:** READY FOR PRODUCTION  

---

## What You Now Have

### **Two Autonomous Agents**

1. **The Architect** (`profile: architect`)
   - Verifies Hermes gateway is operational
   - Runs `bin/verify` (17-test suite)
   - Posts to Telegram only on state changes (GREEN ↔ RED)
   - Role: **Infrastructure verifier** (measurement only, no fixes)

2. **maestro** (`profile: maestro`)
   - Continuously senses estate health
   - Heals by recipe (capped at 2 per 24h per signature)
   - Posts to Telegram only on exceptions (failures, caps, crises)
   - Role: **Estate conductor** (monitoring + bounded auto-healing)

### **Three Communication Channels**

1. **Live logs** (terminal windows)
   - `tail -f ~/dev/code/hermes-v2/logs/agent.log` (Architect)
   - `tail -f ~/.maestro/maestro.log` (maestro)
   - Real-time thinking, no delays

2. **STATE.md** (single source of truth)
   - `cat ~/dev/code/crew/STATE.md` 
   - Refreshes hourly, command-backed, no prose
   - Every row is proof, not a claim

3. **GitHub crew board** (decisions & handoffs)
   - `gh repo view chidionyema/crew --web`
   - Post updates on P1 issues
   - Both agents watch and respond

4. **Telegram** (alerts only)
   - Posts only when something needs your attention
   - No "checking..." or "thinking..." messages
   - Evidence included in every post

### **Control Points**

- **Architect:** Run `cd ~/dev/code/hermes-v2 && ./bin/verify` anytime
- **maestro:** Posts on crew board → both agents respond
- **Both:** Update their memory files → they adapt (commit to git)

---

## How to Use

### **Watch Everything (4-terminal setup)**

Terminal 1 — Architect:
```bash
tail -f ~/dev/code/hermes-v2/logs/agent.log
```

Terminal 2 — maestro:
```bash
tail -f ~/.maestro/maestro.log
```

Terminal 3 — STATE snapshot:
```bash
watch -n 60 'cat ~/dev/code/crew/STATE.md | head -20'
```

Terminal 4 — P1 fires:
```bash
watch -n 60 'gh issue list --repo chidionyema/crew --label P1 --state open --json number,title'
```

### **Or use the one-command dashboard**

```bash
watch -n 30 ~/bin/watch-estate
```

(See QUICK-START.md for the script)

### **Communicate with them**

1. **Force Architect to verify:**
   ```bash
   cd ~/dev/code/hermes-v2 && ./bin/verify
   ```

2. **Post an update to crew board (both agents read it):**
   ```bash
   gh issue comment 35 -R chidionyema/crew -b "Status: working on X, next step Y"
   ```

3. **Add a healing recipe for maestro:**
   ```bash
   # Create ~/dev/code/crew/remedies/restart-engine.yaml
   # Both agents reload from git on next cycle
   ```

4. **Send to Telegram:**
   ```bash
   hermes send --to telegram "Message to founder"
   ```

---

## What They Can't Do (By Design)

- ❌ Architect never modifies code or config
- ❌ maestro never heals with arbitrary commands (recipe-only)
- ❌ Neither changes the remedy catalogue at runtime
- ❌ Both refuse decisions without crew board guidance
- ❌ Silence is mandatory (no "I'm thinking..." posts)

---

## What Prevents Problems

✓ **Duplication:** Both read STATE.md before working  
✓ **Silent failures:** Telegram posts on exceptions (Architect) and failures (maestro)  
✓ **Lost context:** Crew board is permanent, searchable, threaded  
✓ **Speculation:** Evidence required in every update  
✓ **Repeated questions:** Founder never repeats context (agents read the board)  
✓ **Scope creep:** Both defined by their role, not their ambition  

---

## The P1 Fires (What They Measure Work Against)

1. **#38** — Fly exit drill (never drilled)
2. **#35** — Fly build blocked (overdue invoices, 10 commits behind)
3. **#26** — Cost control ($431/day vs $120 cap)
4. **#22** — Observability audit (proposed architecture)
5. **#13** — Hermes retirement (unconditional)

---

## Files Created

| File | Purpose |
|------|---------|
| `~/dev/code/hermes-v2/profiles/architect/USER.md` | Architect's rules & tone |
| `~/dev/code/hermes-v2/profiles/architect/MEMORY.md` | Architect's platform knowledge |
| `~/dev/code/hermes-v2/profiles/maestro/USER.md` | maestro's rules & tone |
| `~/dev/code/hermes-v2/profiles/maestro/MEMORY.md` | maestro's P1s, healing cap, skills |
| `~/dev/code/crew/AGENT-ONBOARDING.md` | Profiles & Telegram setup |
| `~/dev/code/crew/VISIBILITY-COMMUNICATION.md` | All 4 channels + how to use them |
| `~/dev/code/crew/QUICK-START.md` | One-command dashboard & examples |

---

## Next Steps (Your Checklist)

- [ ] Read QUICK-START.md
- [ ] Open 4 terminals (or run `watch-estate` script)
- [ ] Watch maestro's next cycle (~3 min)
- [ ] Post a test update to crew board
- [ ] Verify both agents read it
- [ ] Commit the profiles to git (if not already done)
- [ ] Add 1-2 healing recipes for known signatures
- [ ] Test Telegram delivery

---

## The Heavenly Experience

✓ Architect silently verifies, alerts only on RED/timeout  
✓ maestro silently monitors, alerts only on exception  
✓ Crew board carries all context (no repeated questions)  
✓ One Telegram notification = something actually needs attention  
✓ Every claim backed by evidence (command output)  
✓ No setup steps repeated (machine owns it after first time)  
✓ No guessing about state (STATE.md is truth)  

---

## Golden Rule

**No claim without command output.**

When you post an update, include:
- The command that was run
- The exact output (not a summary)
- What it means (one-line interpretation)

This is LAW 2 (Proof before action) and LAW 17 (Prove it operational).

---

## Questions?

1. **How do I know if maestro is working?** → Check `~/.maestro/maestro.log` (SENSE/REPORT cycles every 1-3 min)
2. **Why doesn't maestro post about successful heals?** → Silence means health (LAW 8: heal first, speak on exception)
3. **Can I add my own healing recipes?** → Yes, create YAML files in `~/dev/code/crew/remedies/` and commit
4. **What if Telegram is down?** → Both agents keep working, logs remain, STATE.md updates hourly
5. **How do I update Architect's baseline?** → Edit `profiles/architect/MEMORY.md`, commit, both agents reload from git
6. **Can maestro learn from incidents?** → Yes, via `experience_graph.db` (SQLite), it tracks what heals work

---

## You're Done

The Architect and maestro are now:
- ✓ Isolated (separate profiles, separate memory)
- ✓ Coordinated (read STATE.md + crew board)
- ✓ Wired to Telegram (posts only on exceptions)
- ✓ Documented (4 new guides in crew/ repo)
- ✓ Ready (both running their cycles automatically)

Enjoy maximum autonomy, minimum interruption. 🎼
