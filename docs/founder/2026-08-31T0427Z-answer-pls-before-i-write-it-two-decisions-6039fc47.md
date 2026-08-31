---
captured: 2026-08-31T04:27:39+00:00
session: 14ed6c8b-f0a9-40d7-82a8-895f336f9b78
cwd: /Users/chidionyema/dev/code
chars: 2706
source: founder prompt, verbatim (founder-doc-capture.py)
---

answer pls Before I write it, two decisions change the whole shape, and guessing wrong wastes the spec:

1. Broker. Keycloak, Zitadel, Authentik, or Ory Hydra? On your estate the real discriminator is memory — Keycloak wants ~1GB+ and a Postgres; Zitadel is leaner and ships its own; Hydra is minimal but has no user store, so you'd keep Identity as the backing store behind it. Given the two-node free-tier constraint you were just costing, that's not a preference question, it's a capacity one.

2. Cutover shape. Full migration (users move to the broker, Identity is deleted), or broker-in-front (Hydra/broker handles OIDC, ASP.NET Identity stays as the credential store)? The second is dramatically lower risk and keeps your hashes where they are, but leaves you running both.

Tell me those two and I'll write the real spec. If you'd rather I pick, I'd say Zitadel, full migration for a greenfield-ish estate this size, or Hydra in front of existing Identity if you have users you can't afford to disrupt.

Meanwhile, here's what the spec covers regardless of those answers — the parts that are actually hard:

Password hashes. ASP.NET Identity v3 hashes are PBKDF2-HMAC-SHA256, 10k iterations, with a proprietary version-byte prefix. Keycloak can be taught to verify them via a custom credential provider; Zitadel supports pbkdf2 import with the right encoding; most others can't, which forces either a password reset for every user or a shadow-verify migration where the first successful login rehashes into the broker. That decision alone determines whether this is a weekend or a quarter.

Claims and roles. Identity's role/claim model has to map to broker groups or scopes, and every downstream service reading ClaimTypes.Role needs to keep working. Usually means mapping roles into a custom claim in the token and adjusting the resource servers' claim type mapping.

The bootstrap trap. If the broker runs in the cluster and cluster tooling authenticates through the broker, a broker outage locks you out of the thing you'd fix it with. Needs a break-glass local admin path that does not depend on the broker, defined before cutover, not after.

Rollback. Feature-flag the auth path per-application so you can flip one service back without redeploying everything. Dual-issuer validation during the window — resource servers accept tokens from both old and new issuer — so a rollback doesn't invalidate live sessions.

Session cutover. Existing cookies aren't OIDC sessions. Either force reauth at a chosen moment, or run both auth paths and let sessions age out naturally.

Give me the two answers and I'll turn this into the actual document — phases, manifests, verification gates at each step.
