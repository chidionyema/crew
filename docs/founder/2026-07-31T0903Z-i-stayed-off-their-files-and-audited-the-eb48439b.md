---
captured: 2026-07-31T09:03:10+00:00
session: a001b933-9471-404c-9b35-eb3d27761882
cwd: /Users/chidionyema/Documents/code/prospector
chars: 1783
source: founder prompt, verbatim (founder-doc-capture.py)
---

I stayed off their files and audited the one thing that's squarely mine — whether that token-price door is reachable by a real buyer. It isn't, and the code matches its documentation on every claim:

- Bogus key → HTTP 401. Note what it does not do: fall through to a full-price sale. That's the right call, and the header comment says why — falling through would bill £49 for a mistyped test key.
- Empty key → HTTP 200, amount_total=4900 gbp, livemode=true. Ordinary sale, correct price. I checked the amount rather than trusting the status code.
- Unconfigured key fails closed — IsNullOrWhiteSpace(expectedKey) is tested before the compare, so an unconfigured deployment can't treat empty-equals-empty as a match.
- Constant-time compare over SHA-256 of both sides, which avoids FixedTimeEquals leaking the key length through its early length-mismatch return. That's a subtle one and they got it right.
- Store:InternalApiKey appears nowhere in Store.Web/src — the bundle can't produce it.

One thing worth separating, because I don't want their fix credited with explaining my observation: their bug is the embedded overlay on mumchimp.com (preopenedClientSecret rejecting real secrets that contain %2F). The error I hit was on the hosted checkout.stripe.com page — a different surface. So their fix may well be the whole story, but I can't claim it explains what I saw, and the hosted-page question is still open.

smoke_checkout.sh is now the right way to answer it, and I've just verified the mechanism it relies on is safe. That gets you a real live render at token price instead of £49.

I've left the browser alone since you stopped it — say the word if you want me to drive their smoke script, or I'll leave that surface to them. also to consider, report fron other agent
