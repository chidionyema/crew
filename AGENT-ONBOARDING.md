# Agent Onboarding — Architect & maestro to Telegram

**Date: 2026-08-23**  
**Status: PROFILES BUILT & ISOLATED**

---

## Summary

Two Hermes agent profiles have been reverse-engineered, built, and isolated:

### **The Architect** (profile: `architect`)
- **Role**: Infrastructure verifier (Hermes gateway health)
- **Measurement**: Runs `bin/verify` (17-test suite)
- **Output**: 
  - Posts to Telegram **only on state changes** (GREEN ↔ RED)
  - Posts immediately if `bin/verify` times out
  - Silent on success
- **Telegram**: `[architect] GREEN | bin/verify: 17 passed, 0 failed`
- **Never**: Fixes code, changes config, writes to git
- **Tone**: Clinical. Evidence-first. No narrative.

### **maestro** (profile: `maestro`)
- **Role**: Estate conductor (monitoring + bounded auto-healing + escalation)
- **Measurement**: Autonomous cycle, one INTENT file every ~3 minutes
- **Behavior**:
  - Senses estate state (crisis detection, audit findings)
  - Heals by recipe (remedy catalogue only, capped at 2 per 24h per signature)
  - Escalates failures or unknown signatures to crew board
  - Tracks experience (SQLite graph, healable skills)
- **Output**:
  - Posts to Telegram **only on exceptions**: healing fails, cap exceeded, crises
  - Silent on successful heals
  - P1 fire progress on crew board (not phone)
- **Telegram**: `[maestro] CRISIS | disk 95.9%, 3 P0 findings, manual intervention needed`
- **Never**: Freeform code execution, decisions without recipe approval
- **Tone**: Decisive. Facts only. No speculation.

---

## Profiles Created

| Profile | Location | Files | Status |
|---------|----------|-------|--------|
| architect | `~/dev/code/hermes-v2/profiles/architect/` | `USER.md`, `MEMORY.md` | ✓ Built |
| maestro | `~/dev/code/hermes-v2/profiles/maestro/` | `USER.md`, `MEMORY.md` | ✓ Built |

Each profile is **isolated** (separate memory, separate responsibilities, no shared state).

---

## Telegram Integration

Both agents post to: **Founder's Telegram** (chat_id: `8868748055`)

**Posting discipline:**
- Architect: State changes only (GREEN/RED/timeout)
- maestro: Exceptions only (failures, caps, crises)
- **Silence = health.** No "I'm checking..." or "still thinking..."
- Evidence required (command output or log line)

---

## Coordination Layer

All agents (Architect, maestro, work, watch, default, and you) sync via:

1. **STATE.md** (`~/dev/code/crew/STATE.md`) — single source of truth, regenerated hourly
2. **Crew GitHub board** (`chidionyema/crew/issues`) — decisions and handoffs
3. **Estate board** (`ESTATE_BOARD.jsonl`) — cross-session messages

**Before any agent starts work on a P1 fire:**
1. Read `STATE.md` (check who's already working on it)
2. Check the issue on crew board (comment with intent)
3. Report evidence (not claims) as you work

---

## P1 Fires (Priority Order)

Both agents measure work against these:

1. **#38** — Fly exit drill (never drilled)
2. **#35** — Fly build blocked (overdue invoices, 10 commits behind)
3. **#26** — Cost control ($431/day vs $120 cap)
4. **#22** — Observability audit (proposed architecture)
5. **#13** — Hermes retirement (unconditional)

---

## What This Prevents

✗ **Duplication** — All agents read STATE.md before starting  
✗ **Silent failures** — Telegram posts on state changes (Architect) and exceptions (maestro)  
✗ **Lost context** — Handoffs go to crew board (permanent, searchable, threaded)  
✗ **Speculation** — Evidence required; no claims without output  
✗ **Repeated hand-holding** — Founder never repeats context (all read the board)  

---

## How to Use

### To activate profiles:
```bash
hermes switch architect  # or maestro
hermes check doctor      # verify isolated setup
```

### To test Telegram delivery:
```bash
hermes send --to telegram "Test: Architect online"
```

### To view maestro's thinking:
```bash
tail -f ~/.maestro/maestro.log
tail -f ~/.maestro/intents/INTENT-*.json
```

### To update THE ARCHITECT's baseline:
Edit `hermes-v2/profiles/architect/MEMORY.md` (only the coordinator or founder should touch this)

### To add a healing recipe:
Add to `~/dev/code/crew/remedies/*.yaml`, then PR to crew board (no runtime decisions)

---

## Founder Experience

**Heavenly** = maximum autonomy, minimum interruption:

- Architect works silently, posts only on RED or timeout
- maestro heals silently, posts only on exception
- Crew board carries all context (no repeated questions)
- One phone notification = something actually needs your attention
- Every claim on the phone comes with proof (command output)
- No setup steps repeated (once per identity, then machine owns it)

---

## Files Modified

- ✓ `hermes-v2/profiles/architect/USER.md`
- ✓ `hermes-v2/profiles/architect/MEMORY.md`
- ✓ `hermes-v2/profiles/maestro/USER.md`
- ✓ `hermes-v2/profiles/maestro/MEMORY.md`
- ✓ Session memory updated (coordinator + agent architecture)

---

## Next Steps (for you to confirm)

1. **Test Architect**: `hermes switch architect && hermes send --to telegram "test"`
2. **Test maestro**: `hermes switch maestro && hermes send --to telegram "test"`
3. **Verify isolation**: Check that each profile only knows its own role
4. **Activate in launchd**: Wire them to their actual cron schedule or triggers
5. **Add healing recipes**: Create `crew/remedies/*.yaml` for known signatures

Once confirmed, mark this file `DONE` and architects/maestro become part of the standing coordination.
