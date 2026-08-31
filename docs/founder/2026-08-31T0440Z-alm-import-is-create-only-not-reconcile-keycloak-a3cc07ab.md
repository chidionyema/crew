---
captured: 2026-08-31T04:40:39+00:00
session: 14ed6c8b-f0a9-40d7-82a8-895f336f9b78
cwd: /Users/chidionyema/dev/code
chars: 1777
source: founder prompt, verbatim (founder-doc-capture.py)
---

alm import is create-only, not reconcile. Keycloak's --import-realm applies a realm file at startup if the realm doesn't exist. It does not converge an existing realm to match the file. So a change to the realm JSON after first boot does nothing, and someone eventually fixes it in the browser. If the spec says "configured as code," it needs the mechanism that actually reconciles: the Keycloak Operator with KeycloakRealmImport resources, or keycloak-config-cli run as a Job on every deploy, or Terraform's Keycloak provider. Pick one explicitly. Without it, "as code" is true on day one and false by week three — which is the same drift class as everything else tonight.

The bootstrap admin is the one thing that can't be fully declarative. Keycloak's initial admin comes from env vars on first start; after that it's a user in the database. Keep it as a temporary bootstrap credential, create the real admin service account via the reconciler, and disable the bootstrap one. Otherwise you have a permanent admin password in a Secret that no code path ever rotates.

Given your rule, the enforceable version: the realm's live state must be diffable against git in CI. keycloak-config-cli can run in validate mode; the Operator's status reports drift. Whichever you pick, wire it so a manual browser change shows up as a failing check rather than as a surprise six weeks later. That's the control that makes "no console" real rather than aspirational.

One consequence worth accepting deliberately: no-console means debugging a broken realm config is done by reading YAML and redeploying, not by clicking. Slower when something's wrong. Worth it, but the break-glass path should include read-only admin access for diagnosis, or you'll be reasoning about auth failures blind.
