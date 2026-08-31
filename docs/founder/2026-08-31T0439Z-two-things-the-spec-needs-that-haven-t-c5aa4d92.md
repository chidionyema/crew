---
captured: 2026-08-31T04:39:46+00:00
session: 14ed6c8b-f0a9-40d7-82a8-895f336f9b78
cwd: /Users/chidionyema/dev/code
chars: 1854
source: founder prompt, verbatim (founder-doc-capture.py)
---

Two things the spec needs that haven't come up, plus one measurement still outstanding.

**Multi-tenancy shape, decided now.** Enterprise clients mean tenant isolation, and Keycloak forces the choice early: one realm with a tenant claim on each user, or a realm per enterprise client. Realm-per-tenant gives clean isolation and independent IdP federation but doesn't scale past a few dozen and makes shared config painful. Single realm with tenant as a claim scales but means every authorization check in your application must be tenant-aware from day one. This is the decision that's genuinely expensive to reverse. Given you expect a handful of enterprise clients rather than hundreds, realm-per-enterprise-client with storefront customers in a shared realm is probably right — but it needs deciding before code, not after.

**Machine identity.** You said staff, storefront, third parties — but the estate is full of services authenticating to each other, and right now that's presumably tokens in Secrets. Keycloak does client credentials and service accounts, and if it's going to be the identity layer, it should own that too rather than leaving a second credential system in place. Otherwise you've solved human identity and left exactly the pattern your decision record forbids, one layer down.

**Still unmeasured, and the spec can't be written without them:**
- The account count from that SQLite file
- Keycloak's actual memory footprint against your ~16.7 GB
- Whether the storefront's orders key off a local user ID (you said no — worth confirming from the schema, since it's the one thing that turns an afternoon into a project)

That's it. Everything else is in the earlier threads: broker chosen, cutover shape chosen, Oracle out, hash question deferred until the count comes back, backups first.

Run the count and the spec writes itself.
