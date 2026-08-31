---
captured: 2026-08-19T17:42:52+00:00
session: 56afe97f-8483-45e8-b4d3-402ab744d759
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2771
source: founder prompt, verbatim (founder-doc-capture.py)
---

address this before niving on , cat continnure beting strangled 

WORKING: audit done, measured, one fix applied. The two dials are wrong in opposite directions and I can only fix one for free.

Both, measured on this session (8.6h, 23 compactions):
- Too aggressive — CLAUDE_CODE_AUTO_COMPACT_WINDOW=150000 (~/.claude/settings.json:3), hand-set, while the model is opus[1m] = 1,000,000. We compact at 15% of the context we pay for. Gaps collapsed from 26m to 8m.
- Too slow — median 117s each, 45 min total = 9% of the session. Summaries ran 1,646–2,839 words against our own 1,200-word cap. 0 of 23 met it.

Applied now (free, cuts duration): rewrote Compact Instructions to an allocated per-section budget, so the cap is a rule with numbers instead of a sentence.

Raising the window is the wrong fix for your constraint — cache_read is 55.6% of spend, so it buys time and costs money. The lever that cuts both is the floor, and it's your call.

---

The floor — 40k tokens rebuilt after every compaction, re-read on every request

┌──────────────────────────────────┬─────────┐
│                                  │ tokens  │
├──────────────────────────────────┼─────────┤
│ system prompt + tool schemas     │ ~13,000 │
├──────────────────────────────────┼─────────┤
│ ~/.claude/CLAUDE.md              │ 7,859   │
├──────────────────────────────────┼─────────┤
│ prospector/CLAUDE.md             │ 7,461   │
├──────────────────────────────────┼─────────┤
│ MEMORY.md index                  │ 4,528   │
├──────────────────────────────────┼─────────┤
│ laws hook (LAW 0–2, re-injected) │ 2,144   │
├──────────────────────────────────┼─────────┤
│ the fresh summary                │ ~5,000  │
└──────────────────────────────────┴─────────┘

Trigger fires at ~118k (LATEST.md header: 117749->13639 tokens), so working room is ~104k. At this session's tool volume that is 8 minutes.

The lever that cuts frequency AND cost: the two CLAUDE.md files are 15.3k tokens, 38% of the floor, paid on every request all day. Both headers say they carry "the RULE" while memory files carry the incident — but they carry three full worked examples with timings and measurements. Cutting them to rules-only gives back ~8k of working room per window and saves ~8k on every request. Those are your directives verbatim, so I'm not touching them without you.

Two hypotheses I killed before reporting them: the checkpoint is not re-injected on compaction (memory-loop.py:219, laws_only path), and "All user messages" is only 150–368 words, not the growth engine. The ser, not one runaway section.

The honest root cause of "too aggressive" is me. Our own rule at ~85k and immediately at ~140k. The trigger fires at 118k.Autocompact did that job 23 times because I never took the safe point.
