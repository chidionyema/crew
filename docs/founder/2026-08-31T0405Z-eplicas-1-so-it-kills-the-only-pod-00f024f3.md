---
captured: 2026-08-31T04:05:13+00:00
session: 80471694-3138-4645-a870-868210b81120
cwd: /Users/chidionyema/dev/code/hermes-v2
chars: 2480
source: founder prompt, verbatim (founder-doc-capture.py)
---

eplicas: 1 — so it kills the only pod, then starts the new one. Everything in that pod stops: - Telegram polling — the bot answers nobody for the whole gap. That's what you hit. - The cron scheduler — every tick due in t

PASTED

I was wrong about the probe. The strategy is Recreate, not RollingUpdate — so there was never a moment where both pods existed and readiness could have held the old one open. Kubernetes killed the old pod first by design, and no probe change alters that. My whole answer assumed the wrong strategy. The agent's read is correct and mine wasn't.

Given Recreate + single-holder token, the gap is structural. Only three levers actually exist:

Shrink the four minutes. Pod created 03:44:35, first Telegram attempt 03:49:01 — that's 4m26s before the app even tries, and it's the largest single component of your outage. Whatever runs before the DoH discovery is the thing to measure. This is almost certainly where the win is.

Queue what's lost rather than dropping it. The cron ticks that fall in the gap are gone, not deferred. If the scheduler persisted next-due times and caught up on boot, the gap stops costing you work — it just delays it. That's a bigger change but it converts an outage into latency.

Accept and announce it. If the gap can't go below ~30s, the honest fix is that the bot posts on shutdown and on connect, so you know what happened rather than staring at silence.

The Preflight compression: ~197,486 tokens on every boot is worth pulling on separately. If a SIGTERM mid-turn means the next pod reloads the full conversation and compacts before it can answer, that's compounding the gap — a clean shutdown that checkpoints compacted state would remove it from the critical path. Might be a meaningful chunk of the four minutes.

Good catch on evolution being crontab-in-a-JSONL-file rather than one bad character. A file that has never once parsed and never once alerted is the purest example of tonight's pattern — the loader failed silently at boot forever. The CI check is right; make it assert the file loads with the same parser the loader uses, not just that it's valid JSON.

One thing outside the technical stack: $320/day estate spend and 75% of your weekly limit, at 5am, on a night where the merge that ends the outage is still sitting unmerged. Merge #1030 and stop. The evolution lane has been broken since the day it was added — one more night won't change that, and everything else here is better decided rested.
