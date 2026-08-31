---
captured: 2026-08-28T13:50:19+00:00
session: a0d64ea4-d03d-4d1f-84e1-e1739e05c615
cwd: /Users/chidionyema/dev/code/idp/.claude/worktrees/crew459-portal-polish
chars: 1502
source: founder prompt, verbatim (founder-doc-capture.py)
---

wee need to also audit the platfron for anything that breaks this standard and alert d-guard); diagnose 33176552228 still running.

On your three questions, straight:

Enterprise pattern. Vendor accounts are owned by the org's identity provider, not by a person. The platform team holds a role identity (platform-admin in the IdP, break-glass in the vault) and does every first-time vendor sign-up under that identity, over SSO. The CEO never creates an account. Then everything after day one is machine identity: OAuth clients and keys minted by API, rotated by the platform, no human.

Where we differ from that. This estate has one human in the IdP, and that human holds the admin role — so the "platform team's one-time SSO login" and "the founder" are the same pair of hands today. The step is not on you because you are CEO; it is on you because you are the only IdP admin. Sessions are barred by the harness from creating accounts or entering credentials, and there is no other human. That is the whole reason.

What makes it never recur. The Tailscale tailnet is bound to the org IdP (IDCS SSO), so it is org property; after the first OAuth client exists, every later key comes from the API under machine identity (that is what idp#582 already wires: ExternalSecrets → operator → Otto), and the no-toil gate (crew#66 CP-NoToil, policy/no-manual-steps.rego) refuses any future PR that adds a human step. One SSO tap, once, then a super-high-tech dept with zero founder toil is exactly the shape.
