---
captured: 2026-08-29T11:37:07+00:00
session: 2d8b3bd0-3d43-40d9-862b-712be5c41803
cwd: /Users/chidionyema/dev/code/idp
chars: 2331
source: founder prompt, verbatim (founder-doc-capture.py)
---

You can fully automate it — and I was wrong about the wildcard. Tailscale does support globs: values can contain an * to match any character, with all other characters matched literally. Your repo:chidionyema/idp:* failed on the literal prefix, because the real sub is repo:chidionyema@377396/idp@1344360654:... and idp: never matches idp@1344360654:.

More usefully: the whole trust credential is API-managed, so nothing here needs the console. Federated identities can be created via the Tailscale Terraform provider, tailscale-client-go-v2, or POST /api/v2/tailnet/-/keys with keyType: federated.

The cleanest shape is to stop pinning the subject tightly and pin on custom claims instead, which are flat and ID-stable:

data "github_repository" "idp" {

  full_name = "chidionyema/idp"

}



resource "tailscale_federated_identity" "idp_ci" {

  description = "estate"

  issuer      = "https://token.actions.githubusercontent.com"

  subject     = "repo:chidionyema@*/idp@${data.github_repository.idp.repo_id}:*"

  scopes      = ["auth_keys", "devices:core"]

  tags        = ["tag:ci"]



  custom_claim_rules = {

    repository_id = tostring(data.github_repository.idp.repo_id)

    ref           = "refs/heads/main"

  }

}

The repo ID comes from the GitHub API at plan time, so there’s no chicken-and-egg — you never have to run the workflow and read the error to learn your own subject.

Audience is derived, not assigned: Tailscale generates it as api.tailscale.com/<client ID>. So once Terraform creates the credential you can compute it and feed it straight to the action — no secrets to copy:

permissions:

  id-token: write

steps:

  - uses: tailscale/github-action@v4

    with:

      oauth-client-id: ${{ vars.TS_CLIENT_ID }}

      audience: ${{ vars.TS_AUDIENCE }}

      tags: tag:ci

Two things to watch:

Bootstrapping. Terraform needs credentials to create the first identity. Chicken-and-egg is real here, but only once — create one credential by hand, then have that one manage the rest. The provider itself can authenticate via oauth_client_id + identity_token, so after bootstrap your TF runner authenticates with its own OIDC token.
The ref claim rule locks you to main. PR-triggered runs present a different ref and will be rejected. Drop that line or widen it if you need PR runs to mint tokens.
