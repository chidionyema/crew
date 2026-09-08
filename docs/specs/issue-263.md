# Build: Identity & Commerce Mesh: auth and billing are infrastructure, not application code

Issue: https://github.com/chidionyema/crew/issues/263
Written by pm-agent on 2026-08-25 from conversation with @founder.

## What the founder asked for

Founder, 2026-08-25 (verbatim): "our .NET API should not know what a JWT is. It should not
contain Stripe SDKs. It should not know how to salt a password. If you change from .NET to
Rust tomorrow, your auth and payments should not even blink."

"The Concept: The Zero-Trust Header Architecture. We remove the burden of authentication and
subscription checks from the application code entirely. We push it up to the API Gateway."

"1. The Bouncer (The API Gateway) ... Envoy, Traefik, or Kong ... intercepts every request. It
catches the JWT ... asks the Identity Primitive: Is this token valid, and what is their
subscription tier?"

"2. The Passport Office (Headless Identity) ... Ory Kratos/Oathkeeper or Keycloak ... only job
is to mint JWTs, handle password resets, and store user metadata."

"3. The Tollbooth (Headless Billing) ... Lago for usage-based billing, or a headless Stripe
sync worker ... continuously updates the Passport Office with the user's current subscription
tier. If they stop paying, the Identity Primitive instantly revokes their Pro status."

"If the JWT is invalid, or the user hasn't paid, the Gateway rejects the request with a 401
Unauthorized or 402 Payment Required. The request never even reaches your .NET API."

"The Gateway strips the JWT, takes the user's data, and injects it as standard, trusted HTTP
Headers ... X-Estate-User-Id, X-Estate-Subscription-Tier."

"The New Startup Rule: deploy the Gateway, Identity, and Billing primitives. You write a tiny
50-line API in Python that reads the headers."

"Because all traffic passes through the Gateway, OpenTelemetry automatically tracks exactly how
many requests Free users make vs Pro users."

"This is the ultimate evolution of Law 2: The Fractal Primitive ... In the Living Estate, Auth
and Billing are infrastructure."

Founder addition, 2026-08-25 (verbatim): "prospector store will be adding ability for
subscriptions and will be a good use case to test this."

## Where this sits

- Evolution of LAW 2 (The fractal primitive), `crew/docs/ARCHITECTURE_LAWS.md`, merged
  crew#255: "a headless, containerized primitive with an exposed API... The web UI is a thin
  shell over those APIs." Auth and billing become two more fractal primitives, not app code.
- Sits under crew#250 (R36 cloud-agnostic platform, "End state: tear down and rebuild from the
  phone with confidence, and every past error is a gate that cannot recur").
- Supersedes the application-side parts of crew#227 (enterprise auth v2.0, machine/founder
  identity). CP4 of crew#227 (SPIFFE SVIDs between agents, spec 4.4) stays as-is — that is
  machine identity for agent-to-agent calls, not customer identity for an HTTP API, and this
  issue does not touch it.
- Gateway row: Traefik is already the estate's chosen edge (`idp/platform/edge/traefik.yaml`,
  `docs/STANDARDS.md` substrate row) — this issue adds ForwardAuth to it, it does not replace
  it or evaluate Envoy/Kong again (LAW 23, smaller road).
- Estate rule: one mature tool per layer, named with a falsifiable reason, never a menu
  (`docs/STANDARDS.md` header: "This page names ONE standard per layer").

## Layer choices (one per layer, falsifiable, no menu)

- **Identity primitive: Ory Kratos + Oathkeeper.** Headless by design (API-only, no bundled
  admin UI to secure or theme), Apache-2.0, and Oathkeeper's `authenticator`/`authorizer` chain
  is built specifically to sit behind a reverse proxy and emit the trusted headers this spec
  needs. Rejected: Keycloak — Java/WildFly-based, ships a full admin console and realm model
  built for enterprise SSO federation the estate does not need, heavier resource footprint on
  the Mac/free-tier k8s substrate (R14), and its primary integration pattern is "app talks to
  Keycloak" (adapters, SPI), not "gateway asks a sidecar," which fights this architecture
  instead of serving it.
- **Billing primitive: a headless Stripe sync worker, not Lago.** Prospector's storefront
  already needs real card processing and Stripe as merchant of record now (crew#232, the
  subscriptions use case). Lago is a usage-metering and invoicing engine that sits in front of
  a payment processor — it does not replace Stripe, it would add a second billing system with
  Stripe still required underneath. Rejected: Lago — solves usage-based metering the estate
  does not yet have a product for, adds a service and a Postgres schema with no requirement it
  covers that a sync worker does not, revisit only if/when a usage-metered product (not a flat
  subscription tier) ships.
- **Gateway: Traefik ForwardAuth**, not a new gateway. Already the edge row
  (`idp/platform/edge/traefik.yaml`); `ForwardAuthMiddleware` -> Oathkeeper decision API is the
  smallest diff (LAW 23) over installing Envoy or Kong for the first time.

## Proving ground

The Prospector store's new subscriptions feature (Store.Api / Store.Web,
`~/dev/code/prospector-main`) is CP4: the first real product built through the mesh instead of
Stripe-SDK-in-.NET. Cross-links: crew#232 (storefront bake-off), crew#235 (Bytesync front door,
multi-brand tiers), crew#239 (mumchimp media company). Any change to Store.Web or ports
3000/8000/9000 is owned by the crew#259 sync (storefront collision lane) — this issue does not
bypass that ownership; CP4 work coordinates through crew#259 before touching those files/ports.

## Checkpoints

  decision endpoint on every request. The JWT never reaches an app. Invalid/unpaid requests get
  401/402 at the edge, before any backend service sees them. `X-Estate-User-Id` and
  `X-Estate-Subscription-Tier` are injected by the gateway; the same headers arriving from the
  public internet are stripped before ForwardAuth runs (no header spoofing).
  the cluster. Mints JWTs, handles password reset, stores user metadata and subscription tier.
  State is a Postgres row and S3-compatible object storage only (LAW 1 / R36 cloud-agnostic —
  no provider-only datastore).
  primitive on payment events. A lapsed subscription revokes Pro within one webhook round trip
  — no app code is involved in the revocation.
  only the two trusted headers. Proved by a grep count of JWT/Stripe/password-hash references
  in Store.Api going to 0, and a differential replay: the same request set against the old
  in-app auth path and the new header-only path returns the same authorization decisions. This
  is the subscriptions feature for the Prospector store (crew#232/#235/#239), coordinated
  through the crew#259 storefront sync before Store.Web or ports 3000/8000/9000 change.
  tiering on day 1 with zero auth code of its own — demo and onboarding doc included (LAW 32).
  pro request counts are visible in the trace store with no application code emitting them
  (LAW 3, the default nervous system).

## Checkpoints

### CP1: Gateway auth at the edge. Traefik ForwardAuth/ext-auth calls the identity primitive's

Verified by `@pytest.mark.cp1` in `checkpoints/`.

### CP2: Headless identity primitive (Ory Kratos + Oathkeeper) deployed from idp manifests onto

Verified by `@pytest.mark.cp2` in `checkpoints/`.

### CP3: Headless billing primitive (Stripe sync worker) updates the tier in the identity

Verified by `@pytest.mark.cp3` in `checkpoints/`.

### CP4: Prospector Store.Api loses its JWT parsing, Stripe SDK and password hashing, and reads

Verified by `@pytest.mark.cp4` in `checkpoints/`.

### CP5: New-startup rule. A 50-line Python API deployed behind the same gateway gets auth and

Verified by `@pytest.mark.cp5` in `checkpoints/`.

### CP6: The nervous system. Gateway spans carry the subscription tier as an attribute; free-vs-

Verified by `@pytest.mark.cp6` in `checkpoints/`.

