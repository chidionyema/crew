---
captured: 2026-08-06T08:32:36+00:00
session: 6ae36fe5-f8bb-4fd3-900c-44f2f3cdb210
cwd: /Users/chidionyema/Documents/code/prospector
chars: 3042
source: founder prompt, verbatim (founder-doc-capture.py)
---

we need to warp up this is epensive and costing tokens ed endpoint, the pid and how to resume, the full 63-pack measurement with the verdict that time_to_first_revenue and card_line gaps are by design rather than damage, the one real defect and its fix, the baseline numbers for the final diff, and the three gotchas — including that "dossiers written" is not a backfill counter because the daemon writes concurrently.

Safe point — type /clear (state saved, nothing will be lost).

✻ Crunched for 1m 47s · 2 shells still running

⏺ Background command "Wait for the n=20 measurement and report" completed (exit code 0)

  Read 1 file

The n=20 measurement finished — this closes the last open measurement.

Field-by-field salvage takes listing survival from 10/20 to 19/20 (+9 rescued, 1 unsalvageable). Under the old whole-blob claim-check, half the listings were discarded entirely because one field failed; salvage keeps the fields that pass.

The rescues are not marginal — most kept 4–5 fields. subhead, proof_point and what_you_get survived in all 9; card_line in 6 of 9; headline in 4 of 9. That last figure is the direct explanation for what the backfill is showing live: roughly half the patched packs keep headline == title because the generated headline is the field claim-check most often drops, and fill_from_floor then restores the title.

Adding this to the handoff.

⏺ Update(~/.claude/projects/-Users-chidionyema-Documents-code-prospector/checkpoints/2026-08-06-copy-backfill.md)
Added 11 lines, removed 3 lines
session tokens. `kill 38904` stops it; it is safely resumable because target selection is
"live packs with no `listing_page`", so a rerun skips what already landed.

Also running: n=20 salvage measurement, **pid 9405**, log at
`/private/tmp/claude-501/…/d4f75d9c-…/scratchpad/measure20b.log` (13/20 at last look;
counts RESCUED / OLD-PASS / STILL-NONE).
## n=20 salvage measurement — FINISHED (pid 9405, complete)
Whole-blob claim-check vs field-by-field salvage, on 20 sampled dossiers:
```
OLD survival (blob)      10/20
NEW survival (+salvage)  19/20   (+9 rescued)
unsalvageable             1/20
```
Per-field survival across the 9 rescues: `subhead`, `proof_point`, `what_you_get` in 9/9;
`card_line` 6/9; `headline` 4/9. That last number explains the live backfill yield — the
generated headline is the field claim-check drops most, so `fill_from_floor` restores the title
and the pack reads `headline == title`. Expected, not a failure.

## Measurement (all 63 live packs, read from disk not the API projection)
- 39 packs have no `listing_page` — the backfill's target set.

Handoff updated with the finished measurement. Nothing is being polled; the only thing still running is the detached backfill (pid 38904), which costs no session tokens and writes its summary to /private/tmp/claude-501/…/4c73cfb9-…/tasks/bp6tzriil.output when it exits. ! kill 38904 stops it if you'd rather reclaim the usage.

Safe point — type /clear (state saved, nothing will be lost).

✻ Baked for 27s · 1 shell still running
