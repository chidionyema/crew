---
captured: 2026-08-16T10:35:41+00:00
session: 624f78c0-c292-4190-8d9e-c4b8729b047a
cwd: /Users/chidionyema/Documents/code/prospector
chars: 3566
source: founder prompt, verbatim (founder-doc-capture.py)
---

also needs review ad action lso 
DONE: audited the platform and wrote the launch ops plan to docs/LAUNCH_OPS_PROGRAM.md. Three blockers, nine risks, all measured today.

The three that stop a launch:

1. Nothing is committed. 201 uncommitted paths; branch 52 ahead / 29 behind origin/main. The daemon runs code that exists in one working tree. No rollback point.
2. 35 finished packs cannot be bought. Shelf is 62 live (/catalog/stats → {"listed":62,"registered":146}). Publishing is automated; the pack linter blocks them and nothing ever retries. That is 56% of the shelf, built and stranded.
3. The spend brake reads a 207 MB file. store/prospector.jsonl is 216,974,821 bytes. A cold read measured 108s. No rotation code exists anywhere. The daily cap works only while a cache file survives.

The loudest alert is wrong. "Generation DEAD: 8 barren ticks" fired while the consumer wrote 264 dossiers. Its three suggested checks cannot be the cause.

---
What I actually found

R4 — the alert names the wrong cause (proven). 8 of today's 28 ticks carry generation_suppressed: "grounding degraded: the retrieval probe did not answer within 120s". _trailing_barren_count (run_scheduled.py:1691) skips only dry_run and guard-skipped rows, so a tick the engine deliberately suppressed counts as barren, and alerts.py:461 pages CRITICAL at 3. Meanwhile find store/dossiers -newermt 2026-08-16 → 264 (135 kill, 129 pass). Saved as a memory.

R5 — grounding runs on one provider. exa: 97 HTTP 402 lines today, starting 03:15Z, no alert. SearXNG measures 0.10 coverage against min_relevance 0.35. claude_cli is backstop-only. ddg alone carries it — which is what triggers R4.

R6 — 25 MiniMax calls hit the 600s hard deadline today. R7 — launchd.err.log is 25 MB, no rotation exists. R8 — 11 docs still name cursor_cli (deleted 08-06), 4 name standardcompute, RUN.md:95 names a Gemini quota, RUN.md:60 points at a 0-byte stub, 3 docs are untracked. Only one runbook exists. R9 — batching guard inert, control-centre password is test, both Stripe key modes in .env.

What is already good and should not be rebuilt: five launchd jobs, kill switch plus two half-stops, 15-min watchdog that SIGKILLs
a wedged daemon, escalating retries, alerts on fouram with a delivery test, nightly R2 backup, restoredrill script. The automation exists. Several of its meters read the wrong number, and the last mile from PASS to buyer is not
closed.

The plan, in order

- P0 Freeze and land — commit by explicit path, merrove a fresh clone starts.
- P1 Self-clearing shelf — lint repair loop, publish sweep every tick, clear the 35. Highest revenue item.
- P2 Honest meters — ledger rotation, barren-streakt on the first 402, extend the state probe to coverlive catalog count, TLS, Stripe mode, disk, stranded count.
- P3 Survives without you — prove the consumer is wy digest, run the restore drill for real.
- P4 Docs that cannot go stale — one RUNBOOK.md, plus scripts/doc_lint.py in CI failing on dead provider names and missing script paths. A lint, not discipline.,
- 222 ideas are parked and revivable with one command, whenever you say. i shoud nnnit need  large languane nodel to tell e this, this is why we have the adnin interface it is supposed to be intelliget and useful , If you want more ideas getting through, the lever is not outage handling. It's that we retrieve sources that don't answer the question. That's search quality, and it's a bigger piece of work than a patch.
 u are nniing up the internet outage with 24  hours of data, not very scientifc, 2 sepaate issues,
