---
captured: 2026-08-15T15:10:31+00:00
session: 5cb3c833-32fb-4f8e-a500-3f05a14657f9
cwd: /Users/chidionyema/Documents/code/prospector
chars: 3564
source: founder prompt, verbatim (founder-doc-capture.py)
---

DONE (diagnosis): the founder rail works. I proved it end-to-end by signing in as your account against the live API. Your browser has no session cookie — that's the whole bug.

I minted an RS256 JWT for your user with the live Jwt__SigningKeyPem and drove the real browser path:

┌────────────────────────────────────────────────────────────────────┬────────────────────────────────────────────────────┐
│                               probe                                │                       result                       │
├────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────┤
│ api.mumchimp.com/v1/founder/me (Bearer)                            │ {"founder":true} 200                               │
├────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────┤
│ mumchimp.com/api/founder/me (jwt cookie, via the storefront proxy) │ {"founder":true} 200                               │
├────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────┤
│ mumchimp.com/api/founder/packs/5b87…/download                      │ 302 → the R2 presigned zip                         │
├────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────┤
│ API log                                                            │ AUDIT founder.preview success=True user=2CF13CF9-… │
└────────────────────────────────────────────────────────────────────┴────────────────────────────────────────────────────┘

Against that, in your Chrome: fetch('/api/auth/me') on mumchimp.com → 401, and /api/founder/me → 401. No jwt cookie on that origin, so AuthContext is anonymous, so FounderPreviewLink (pack/[id].tsx:458) renders null and you see only the Buy button. Your Google sign-in is not leaving a cookie behind.

I've deleted the key and DB copies from scratch.

---
Ruled out, with receipts: allowlist (Founder__Emails = chidionyema@gmail.com), EmailConfirmed=1 + linked Google row in /data/store.db, claim resolution (sub and NameIdentifier both carry user.Id, JwtTokenService.cs:51-52), route deployed, component in the live bundle, proxy header forwarding, R2 presigning, and the in-memory 60s code store (single machine, no split-brain).

One timing note: the API machine redeployed at 14:02 UTC. ExternalAuthCodeStore is in-memory with a 60-second TTL — a sign-in in flight across that restart loses its code and lands you on /account?error=Auth.InvalidExchangeCode. If you logged in around then, just signing in again may be the entire fix. Do that, then open XXXXXXXXXXXXXXXXXXXX/api/auth/me: 200 means you're in and the "Open the pack (founder preview)" link is sitting under the Buy button; 401 means the exchange is genuinely broken and I'll go straight at the Set-Cookie.

Note the bypass never removes the payment CTA — it adds that link below it, on desktop and mobile both.

Your mobile report is captured in full (all five items, verbatim) and is the next task. I have not started it. Two traps already found: pages/sample.tsx and sample-report.json are modified-uncommitted, so the live page ≠ your local file; and the Chrome extension's resize does not change the viewport (innerWidth stayed 1152 at a 390px window), so that section needs a real 390px Playwright run, not the extension.

Handoff written to checkpoints/LATEST.md.

Safe point — type /clear (state saved, nothing will be lost) so what doe ths nean
