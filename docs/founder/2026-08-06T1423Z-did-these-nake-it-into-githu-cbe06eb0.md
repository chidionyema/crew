---
captured: 2026-08-06T14:23:28+00:00
session: 05862f2f-f1f6-43b5-a777-419ba8c13840
cwd: /Users/chidionyema/Documents/code/prospector
chars: 3123
source: founder prompt, verbatim (founder-doc-capture.py)
---

did these nake it into githu 
- chidionyema/prospector is PUBLIC — and its entire history contains 0 key-shaped strings. No public exposure.
- chidionyema/hermes-config is PRIVATE: 0 forks, 0 deploy keys, 1 collaborator (you).

Scope is wider than the two files

A one-pass sweep of all 11,678 blobs found 9 leaky ones — not 2. Six are historical config.yaml versions (HEAD and working tree verified clean). The ninth was the real find: config.yaml.corrupt.20260617-135424.bak, still tracked and on disk, holding a DeepSeek key that hash-matches the one live in .env today. Its name ends in a bare .bak, so neither pattern I'd added an hour earlier caught it.

bin/tirith is a false positive — Mach-O binary, and the sk-proj- hit is a compiled-in detection pattern sitting beside "Review usage in the dashboard for unexpected spend".

Which leaked values are still live

Hash-compared against your current .env, no values printed:

┌──────────────────────────────────────────────────────────────────────────────────────────────┬───────────────────┐
│                                          Still live                                          │   Already gone    │
├──────────────────────────────────────────────────────────────────────────────────────────────┼───────────────────┤
│ TELEGRAM_BOT_TOKEN, TELEGRAM_WEBHOOK_SECRET, RSI_SIGNING_KEY, EXA, MINIMAX, GEMINI, DEEPSEEK │ ANTHROPIC, OPENAI │
└──────────────────────────────────────────────────────────────────────────────────────────────┴───────────────────┘

Shipped and pushed

Untracked all of it (disk copies intact), then fixed the control rather than the symptom. Three near-miss .gitignore patterns for one file class meant name-matching was the wrong mechanism, so auto-push.sh now refuses content: it unstages any credential-shaped file and warns, and never blocks the sync — a false positive costs one file's backup, not the estate's.

scripts/test_auto_push_secret_guard.sh extracts the regex from auto-push.sh so the two can't drift. 5/5 credential shapes refused, 0/4 false positives, and mutation-checked — I replaced the regex with a non-matching literal and confirmed the test goes red. It doesn't pass vacuously.

What's left is yours, and one of them matters more than you'd think

Rotate, in this order of blast radius: TELEGRAM_BOT_TOKEN (the estate's control channel — someone holding it can impersonate Otto to you) → TELEGRAM_WEBHOOK_SECRET (forge inbound calls to the gateway) → RSI_SIGNING_KEY (forge "verified" entries in the evidence ledger) → EXA/MINIMAX/GEMINI (metered spend) → DEEPSEEK last. My memory says DeepSeek's balance is −$0.22 and therefore unspendable, but that's a lead, not evidence — re-check before you rely on it.

On rewriting history: I'd deprioritise it. A force-push does not guarantee GitHub deletes the unreachable objects — they stay fetchable by SHA until GitHub garbage-collects, which needs a support request. Rotation is the control that actually closes this; the rewrite is cosmetic by comparison.

Safe point — type /clear (state saved, nothing will be lost).

✻ Baked for 10m 40s

❯ ok

Everything's commi
