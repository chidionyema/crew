---
captured: 2026-08-07T22:51:38+00:00
session: 89ffe221-5003-4154-b532-401af1f1b43e
cwd: /Users/chidionyema/Documents/code/prospector
chars: 3399
source: founder prompt, verbatim (founder-doc-capture.py)
---

RSI landed its first candidate. 86800c1

✅ Verification succeeded on attempt 1!
✅ Prompt staged for review. Telegram notification sent.

That first line has zero prior occurrences in this estate's history. Train 30 → 129.99, held-out test 30 → 130.0.

Both remaining gates were measuring the wrong thing, and I only found the second because the first one didn't add up.

The authority gate counted tasks. classify_lever only counts a task once it dies in a FAILED_STATUS — so five verification rejections later retried into done scored zero. But a prompt acts on one attempt. Same database, same hour: 5 prompt-reachable failures at task level, 525 at attempt level. The record already existed and nothing read it — 1,110 verify events, 742 rejections, each carrying the verifier's own reason string.

A 47x jump in my own favour is where to add guards, not celebrate. (exit N, no output) carries no evidence of who was wrong, so those 104 rows stay in the denominator and out of the numerator; a check that couldn't even run (command not found) is a defect in the ruler, not the work. Conservative authority: 41.9% all-time, 42.9% at 14 days. That stability is the point — the task-level number swung 12.5 → 21.7 → 9.1 across adjacent windows, which is why I refused to tune the window last session. Live now: 62.7% against a 20% floor.

The ruler paid for deletion. brevity_check scored weight × (1 − len/max_len) — every character removed earned points, while vars and clarity sat at full marks. Zero non-gameable headroom, so rc=2 every night was correct: the only reachable win was a shorter executor prompt. It's now built from the recorded rejections — data decides which failure modes are on the ruler and what each is worth, so a mode that stops occurring loses weight and drops out. length_guard replaces brevity: a ceiling with no gradient. Headroom 0.00 → 99.99.

The limit, stated plainly: a text scorer can still e remedy phrasings in, and the first candidatevisibly did — "gone/resolved/fixed", "still present, still failing, or still broken" read as written-to-the-rubric because they
were. That ceiling is not fixed. What is fixed is tler harmful: nothing on it pays for deleting aninstruction, and nothing is on it that the recorded failures didn't put there. The substance is right — it demands re-running the
check, quoting exit codes and the literal command,

168 checks across five suites, four of them falsifiation must not inflate authority, ambiguous rows must stay out of the numerator, length_guard must have no gradient, and no single character or word deletion may raise the score. One
test had asserted headroom was zero — a test pinninnverted it and kept VERIFY_PROMPT (still on the oldruler) as the exhausted-ruler case so both halves of the before/after stay proven.

Your decision. The candidate is staged, not applied — it changes executor behaviour for every task, so it's gated on you:

verify:  ~/.hermes/hermes-agent/.venv/bin/python ~/.hermes/scripts/rsi-orchestrator.py \
           --verify-prompt-tune --prompt-var EXECUT78b46
apply:   the Telegram approve button

Still open: VERIFY_PROMPT is on the old ruler and still exits rc=2; Prospector doesn't yet read the usage-wall marker; otto-server
isn't loaded and estate-watchdog's plist is absent.

Safe point — type /clear (state saved, nothing will
 need to address renaining issues to high prod standard
