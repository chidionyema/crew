---
captured: 2026-08-06T01:17:12+00:00
session: 782601df-d4fc-46bf-93e2-b5a167928313
cwd: /Users/chidionyema/Documents/code/prospector
chars: 5468
source: founder prompt, verbatim (founder-doc-capture.py)
---

`probe_c1_green.py` (green, same legs + `to_thread` + cache-origin), `c1_backup/` (the four
C1 files as committed, sha256-verified — the pattern to reuse for future red proofs).

## Open / deferred

- `telegram.py:4517` still uses `format_message` on authored panel text (A5-class
  leftover, error path). Switching it is safe re: 400s — verified `render_panel` keeps
  output valid even with backticks inside the exception string — but it slightly changes
  visible text for pathological strings. Deliberately not folded into the A5 commit.
- **C1 leftover (small, real):** `render_activity`'s *Slowest* list does not de-dup, so one
  repeated action fills all 5 rows (seen in the red probe: `restart:gateway` 4×). Noticed
  during C1, out of its scope.
- C2 (caller identity), C3 (first run/installer), C4 (fence redesign — **blocked on
  founder decision D1**), B6 (`builds.py:176-224` runs 9 subprocesses serially → 117s
  synchronous panels).

One reusable lesson worth saving — this is the second time in this cockpit that a field was written at many sites and read at zero:

  Wrote 3 memories

C1 landed as 9e3afa9434.

It was two defects, not the one the plan named.

The planned defect was real: activity.record's source defaulted to the literal "button", and handle_estate_action(action, request_id='') has no source parameter — so /panel, a CEO instruction and a tap enter the same funnel with the same arguments. 1,051 of 1,279 live rows claim a tap. The only non-default value in the repo was "cache", which isn't an origin at all — it overwrote the origin on all 228 cache hits.

The second one the plan missed: nothing read the field. Zero readers across gateway/, plugins/, tests/ (the two grep hits are a coordinator task row at estate.py:1204 and a session dict at run.py:11375). Rewriting every row's source gave a byte-identical Activity panel — 429 bytes either way. That's B4's toast bug again, so fixing only the value would have shipped nothing visible. rollup() now returns by_source/served_cache and the panel prints 👆 848 tapped · ❔ 212 unattributed · ⚡ 212 from cache (measured against the real store, read-only).

I did not thread a source= parameter as planned. handle_estate_action is a fan-in from five modules, one of which is the fenced run.py. A contextvar declared at the three python-telegram-bot handlers covers every present and future downstream path with zero call-site edits and no touch to run.py.

Two things I checked rather than assumed, and one of them changed the design:

- _handle_text_message was the wrong seam. It only appends to _pending_text_batches and returns; dispatch happens later in _flush_text_batch. A scope there would have exited before any action ran — green in tests, inert in production. test_the_buffering_handler_does_not_dispatch guards it.
- handle_message "returns quickly by spawning background tasks" (base.py:3938), so the scope has already exited when the work runs. It survives only because create_task copies the context at creation. Proven with a gated-task experiment (spawned inside scope: 'chat' / spawned after scope: 'unknown') and pinned by a test.

That second point implies a gap I documented in activity.py rather than hid: a request queued as a pending message and drained by a pre-existing owner task records "unknown", as do non-telegram adapters. Both degrade to unattributed, never a fabricated tap. Relatedly, the default is "unknown", not "button" — a probe must not impersonate a human.

Not retroactive: the 1,051 historic rows still claim a tap. I left them alone; relabelling would invent data in the file that exists to be evidence.

Proof: 23 tests; 20 of the 22 collected fail against HEAD (verified by reverting the four files via git show HEAD: with sha256-checked backups, then restoring). The 2 that pass at HEAD are correct — a regression guard on existing behaviour, and an assertion that a key absent before the change is absent. Full suite 7433 passed, 9 failed — the same 9 pre-existing test_status_command/test_reasoning_command/test_matrix_project_context_isolation failures, unchanged in kind from 7411/9. Founder guard 2e09c2dfb586a99b… verified identical after the commit; mission.py and run.py untouched.

Liveness has changed since the last handoff, and I can't yet prove it. The again — pid 51529 at 02:01:32, which I did not trigger. All four C1 files(latest mtime 02:00:44) and A6/B4/the atlas fix predate that, so by start-time ordering everything from this session should now be loaded. But that's mtime inference, and zero
activity rows exist after 02:01:32, so there's nothing to confirm it with. no restart: after you type any command, a row with source of command, chat or unknown is only possible with C1 loaded — pre-C1 code can emit button or cache and nothing else. The exact snippet is in the handoff.

One small real thing found and left out of scope: render_activity's Slowest list doesn't de-dup, so one repeated action fills all 5 rows.

Next is #7 A2 — one action registry; estate:fix_all renders 13 buttons with no handler. I'd expect the same two-part shape.

Safe point — type /clear (state saved, nothing will be lost).

✻ Cogitated for 35m 12s

❯
  One small real thing found and left out of scope: render_activity's Slowesone repeated action fills all 5 rows.

  Next is #7 A2 — one action registry; estate:fix_all renders 13 buttons withe same two-part shape.
   need to address and we need to go faster, ue parallel agets
