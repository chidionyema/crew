---
captured: 2026-08-06T12:37:20+00:00
session: dd3b6665-4192-4cd0-9d12-0eaeceb5cbff
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2178
source: founder prompt, verbatim (founder-doc-capture.py)
---

ansaction manager, not a resource manager — it commits and leaves the fd open. All three stores used return conn (23 call sites), leaking db+WAL per call. Latent for months because every caller was O(1); the brake's per-row survey is the first O(backlog) caller and crossed launchd's maxfiles 256 four seconds after startup. It surfaced as Failed to write heartbeat: [Errno 24] — never as a DB error — and was unhealable, because the process stays alive (so KeepAlive won't restart it) while the heartbeat is exactly what can't be written (so the watchdog is blind).

Brake now live and correct: 334 drainable rows >= schedule.backlog_cap 100 — generating 15 more would dig, so this tick only drains. Full suite 1554 passed, 3 skipped.

Your question: why does the same trap keep firing?

Because memory records the fact but the command was re-authored by hand every time — I hit two zsh traps in this session alone, both already written down. So I removed the authoring step: tools/commit_mine.sh (5581c9f) handles all five recorded commit traps once — "$@" argv so there's nothing to word-split, always --only, auto-git add for untracked, waits out index.lock, never pipes, and verifies the landed file list against the named one. It caught two of its own failures on first use instead of reporting exit 0. Memory updated to point at the mechanism rather than restate the trap.

One thing that is not mine, and is a live hazard

config.yaml:21 declares spend.daily_subscription_soft_cap_usd but prospector/config.py:146 Spend has no such field, so load_config raises TypeError right now. The running daemon is safe (load_config is called once, at run_scheduled.py:1367, before the break) — but any restart dies at startup, and under KeepAlive that is a respawn loop. Untracked tests/scheduler/test_subscription_soft_cap.py says a concurrent session is mid-implementation, so I deliberately did not patch it — adding the field blind would collide with their commit. One line if it's still broken in a few minutes: daily_subscription_soft_cap_usd: float = 0.0 on Spend.

Handoff written to checkpoints/2026-08-06-daemon-rails-and-fd-leak.md with a pointer appended to LATEST.md.
