---
captured: 2026-08-10T10:41:52+00:00
session: 86b52909-2f2d-470a-a6b3-226726bf10c5
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2529
source: founder prompt, verbatim (founder-doc-capture.py)
---

Fixed a contradiction that would have made the feature silently under-deliver. prompts/generate.md hardcoded "ACROSS MANY UNRELATED SECTORS — do not cluster in any single domain" four lines below the focus directive. Any focus you set was being argued with in the same prompt. It's now {diversity_directive}: byte-for-byte the old text when no focus is set, and "diversity comes from within the constraint" when one is. Never exercised before, because no profile was ever active.

Receipts: all six profiles resolve with valid form names; both prompt paths render with zero unsubstituted placeholders; no-focus first line asserted identical to the removed text; ruff check clean; pytest tests/invariants tests/unit → 2037 passed, 2 skipped, exit 0.

You can steer it right now, before the UI exists

Two lines in config.yaml, and the daemon picks them up at the next tick (code_fingerprint hashes config.yaml and re-execs):

active_profile: tech_ai_all      # or ai_native / tech_vertical / sells_to_tech
active_market: "us-ca"           # or uk / us / us-ny / us-tx

Two corrections to the tracked ledger

docs/TELEGRAM_OPERATOR_PROGRAM.md says MAX_BUTTONS = 9; the live value is 10 (daemons.py:33). It says 15 dead actions across 30 button sites; the recount says 34. I haven't applied these to the doc yet.

What remains

Tasks 3–7: market rotation, the Focus/Market panels, the Last Run transparency panel, the Nodes panel, and the 34 dead button sites. Five of the seven, and all the gateway work.

Handoff written to checkpoints/LATEST.md with every file:line the next session needs — the gateway structures, the ratchet tests that are already at their cap, and the exact next step per task.

Two things to note: the engine changes are uncommitted on fix/storefront-header-logo-filter-jump, which already carried ~95 uncommitted paths, and another session may be live in this checkout. Say the word and I'll commit just the three files. Also expect the first steered batches to have a low pass rate — judge them on whether the kill-gate mix shifts away from moat_ungrounded, not on the pass count.

Safe point — type /clear (state saved, nothing will be lost).

✻ Cogitated for 13m 6s · 1 shell still running

  7 tasks (2 done, 5 open)
  ◻ Engine: market rotation for US as well as UK
  ◻ Telegram: Focus + Market preset panels
  ◻ Telegram: Last Run transparency (R5) — push and pull
  ◻ Telegram: R4 node priority per pipeline step
  ◻ Telegram: 15 dead buttons — build or delete, plain labels
   … +2 completed continue
