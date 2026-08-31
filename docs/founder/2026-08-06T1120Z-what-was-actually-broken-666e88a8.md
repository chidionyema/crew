---
captured: 2026-08-06T11:20:46+00:00
session: 7e1f67ad-e33f-4831-8f98-7635b59e39ef
cwd: /Users/chidionyema/Documents/code/prospector
chars: 3958
source: founder prompt, verbatim (founder-doc-capture.py)
---

What was actually broken

Two defects on the path from "our brain failed" to "this idea is dead":

1. The CLI says SPEND limit; the classifier only knew USAGE limit. Verbatim from launchd.err.log at 10:24:36Z:
"api_error_status":429,"result":"You've hit your monthly spend limit · raise it at claude.ai/..."
_PERMANENT_MARKERS held "usage limit". So with the 429 attached it classified transient (60s) on the incidental HTTP code — the log shows strikes 2, 3, 4 escalating inside three seconds against a hard monthly cap. Without a 429 it scored NOT_EXHAUSTION entirely, so looks_exhausted was False, so it never became a ProviderExhaustedError.

2. Which meant a crashed verdict call was recorded as evidence about the idea. verdict_for's generic path returned a plain unverifiable check with no retrieval_failed, so an outage flowed into the kill gates. It bit at least once — store/dossiers/2102bacc6dd75cf9.kill.json is a KILL on gate min_composite whose seven checks all read unverifiable, conf 0.0, "Verdict call failed; fail-safe." A candidate killed by our own infrastructure, in a dossier that reads as fully reasoned.

Fixed in 23c4266: _ALLOWANCE_LIMIT_RE (errors.py:104) joins the PERMANENT disjunction — "rate limit" deliberately excluded so backpressure stays transient — and retrieval_failed=True (verify.py:365) routes a crashed call to the DEFER gate. Both mutation-tested: each fails when reverted. Full suite 1469 passed; POPDD python lane PASS at 1477.

How it shipped — not cleanly

My POPDD gate ran ~100s, and the concurrent session committed inside that window. My commit died on cannot lock ref 'HEAD', and because I'd already run git add, my staged files were swept into their commit. The code landed intact (verified by content: _ALLOWANCE_LIMIT_RE, retrieval_failed=True, both test files all present in HEAD) — only my commit message was lost. I left their three in-flight files untouched.

Live state

- Drain finished: 35/35 re-vetted ✅0 🛑7 ⏸️28. Provisional passes 35 → 0. But total backlog 337 → 343 — 28 of 35 merely moved from provisional pass to defer. It relabelled rather than resolved, which is precisely the blind-moat failure the other session's commit addresses.
- Two of my hypotheses were wrong and the tests caught both: the control center isn't the stale health writer (Jul-31 readers.py has zero mark_exhausted refs), and old-format marks are self-healing (missing probe_at reads as 0 = "probe now", verified behaviourally).

Two things that are yours, not mine

Money: subscription-equivalent spend is $406.60 today, uncapped (metered only $3.91/$20), and the CLI is intermittently returning the monthly-spend-limit 429 — direct probes returned OK 4/4, so it flaps rather than being hard-down. Raising or accepting that cap is your call.

I did not restart the daemon. Pid 79003 started 11:15:16 and HEAD committed at 12:08:19, so it is serving pre-fix code. A restart would deploy the fixes — but the concurrent session has uncommitted prospector/retrieval.py (mtime 12:07:55), and restarting would load their in-progress code into production. Once they land, launchctl kickstart -k gui/$(id -u)/com.prospector.scheduler.

One loose end I couldn't close: something wrote 3-key dead marks for claude_cli and the deleted cursor_cli at 10:22:49Z. I ruled out the control center, a .venv shadow install, and any second writer in the main tree. A stale copy exists at .claude/worktrees/agent-a70977a8f9cefea72/ with exactly that writer and cursor_cli in MOAT_PRIMARY, but no process was running from it. Harmless now; worth deleting that worktree.

Handoff written to checkpoints/2026-08-06-billing-failure-never-kills.md (pointer appended to LATEST.md, not overwritten).

Safe point — type /clear (state saved, nothing will be lost).

✻ Baked for 10m 10s · 1 shell still running

❯ thiis is beconinng super concerning , need this stabke and operational once and for all with all loops definitely closed and prvoven
