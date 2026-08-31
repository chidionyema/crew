---
captured: 2026-08-06T11:28:43+00:00
session: 18b8b0a3-3e8e-41d6-a8db-c0ac388551c6
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2903
source: founder prompt, verbatim (founder-doc-capture.py)
---

fed up with ecuses, need this fully prod ready yesterdat Still running the full suite. Recording the trap from my own error while it finishes:

  Ran 3 shell commands, wrote 1 memory

Commit is alive — pid 97380, POPDD gate at 1:40 running the full suite. Worth flagging: a third concurrent session (pid 11429) is mid-flight running its own pytest and mutating tools/queue_yield_batch.sh in the working tree (append → test → restore). That's the torn-read hazard, so if POPDD fails on something unrelated to my diff I'll re-run rather than debug it.

Where this stands while the gate runs:

What you asked for — graceful recovery — is the part that was actually missing. The refusal you quoted was correct but terminal: PAUSE halts the entire tick, and the drain lived inside _default_generate, so stopping the treadmill and stopping the cure were the same act. Setting PAUSE at 10:30Z could never have cleared those 343 rows no matter how long it ran.

Landed in 23c4266 (already committed): the drain refuses a blind moat instead of relabelling rows.

Pending in the running commit:
- _drain_pass() extracted — a tick can now drain without generating.
- PAUSE_GENERATION (operator half-stop) and schedule.backlog_cap (automatic, default off, set to 100). Both keep the drain running. The brake releases itself when the count falls under the cap — no human, no file.
- Drain-only ticks get 15 rows/tick instead of 3, on a 900s cadence clamped to never exceed the generation interval. Without that branch, _tick_unproductive sees dossiers == 0 and escalates 5m→2h — slowing a working drain down exactly as it makes progress.
- A blind moat still outranks the brake: no drain either.

Proven against the live config and store, read-only:

live drainable backlog ->  343
generation_suppressed  ->  backlog brake: 343 >= backlog_cap 100 — this tick only drains
drain_only bound       ->  15 rows/tick (vs resume_per_tick 3)
drain_only cadence     ->  900s (vs interval 7200)
moat_blind             ->  (moat can rule)      ← healed on its own since 11:07Z
ETA at 15/tick / 900s  ->  23 ticks = 5.8 h

Two things I have not done, both needed before any of this is live: the daemon (pid 79003, started 10:15Z) predates every one of these commits, so it must be restarted; and PAUSE must then be swapped for the automatic brake. Order matters — removing PAUSE before the restart would let the stale daemon mint 15 more.

One correction on my own work: 23c4266 contains nine files, not the four I staged. git add <paths> + a bare git commit commits the whole shared index, and a concurrent session had staged CLAUDE.md, errors.py, verify.py and two tests seconds earlier. Their code is in the tree and not lost, but their commit message is, and mine misdescribes five of its files. I've saved that as a memory and switched to git commit --only for everything since.

✻ Worked for 8m 53s · 1 shell still running
