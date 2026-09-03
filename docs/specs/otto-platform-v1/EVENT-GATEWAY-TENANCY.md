# Otto — Universal Event Gateway and tenancy (founder directive 2026-09-03)

Founder directive, verbatim record: `docs/founder/2026-09-03-otto-event-gateway-directive.md`
(same night, 01:14Z). Operative words: this is an enterprise multi-channel SaaS, not a Telegram
hobby bot; divorce infrastructure provisioning from tenant configuration; channel onboarding is
a purely database-driven event; do not write another line of Telegram-specific deployment code.

This extends spec v1.1's day-0 surface contract (`SURFACE-CONTRACT-DAY0.md`), which already
bans a channel-aware core. What was missing, and is now standard: tenancy, the control plane,
and channel configuration as data instead of as deployment.

## The standard

1. **Channel-agnostic compute.** The agent pods (otto-golden, hermes) carry no channel
   environment variables, no channel secrets, no webhook routes. They accept one internal
   envelope: `{tenant_id, message, source_channel, principal, trust_class, capabilities}`.
   `tenant_id` is a required envelope field on both `otto/surface/envelope.py` and
   `otto/spine/envelope.py`, and an observability resource attribute.
2. **One Universal Event Gateway** (`otto/ingress/`). A single highly-available service owns
   every public webhook path (`/webhook/{channel}`) for every channel and tenant. Per hit:
   resolve the presented credential to a `channel_binding` row — `(tenant_id, channel,
   external_id, secret_ref)`, Postgres-backed, secret material in Vault referenced by row —
   verify the channel's native signature via a per-channel verifier plugin, normalise through
   the existing surface bindings, publish to the spine bus. Telegram's secret-token verifier is
   plugin #1; the binding row for (tenant: estate, channel: telegram) is registry row #1 and
   carries the operator chat id from Vault.
3. **Zero-CLI onboarding.** Connecting a channel writes a registry row and a Vault entry
   through the control-plane API (OAuth flow in the portal). The gateway reads new rows live.
   No flux, no kubectl, no pipeline, no pod restart. Proof: a test registers a second tenant
   binding at runtime and routes its next message with pod start time unchanged.
4. **Tenant-shaped verification** (operations consult, this file's build order). Four receipt
   layers, all queries, no human probe:
   - pod emission: the existing telemetry-coverage receipt names the namespace;
   - delivery: gateway spans `gateway.inbound`/`gateway.outbound` carrying `tenant.id`,
     `channel`, `task.ulid` in SigNoz;
   - vendor registration: a reconciler CronJob in the gateway namespace calls each vendor's
     own truth (Telegram `getWebhookInfo`, Slack `auth.test`) where the tokens already live,
     exporting `channel_registration_ok` per tenant/channel — no token ever printed;
   - full loop: a canary tenant with a loopback channel; a probe posts a signed, ULID-stamped
     inbound through the public door and asserts the sink saw the ULID; receipt lands as a
     drill row plus a Healthchecks slug ping (`bin/idp-hc-enroll` supplies the key; whether
     the instance auto-creates checks on first ping is UNVERIFIED and must be read from the
     running instance before the canary is relied on).
   A tenant/channel is `MEASURED_OK` only when canary fresh + registration ok + pending 0 +
   pod in the coverage receipt; otherwise `MEASURED_FAIL` or `UNKNOWN`, never "working".

## Why (the night's evidence)

- The deployed golden lane shipped a placeholder `boot.yaml` with no `chat_allowlist`;
  `otto/surface/bindings/telegram.py` then classes every sender UNTRUSTED and the pipeline
  returns silence. The only proposed proof was "founder messages the bot" — which would have
  returned silence and a wrong guess. Both founder complaints were correct and measurable.
- The allowlist is deliberately NOT patched: the fix would hardcode an identity in git or add
  Telegram-specific deployment plumbing, both banned. Registry row #1 is the fix.
- 0 of 4 receipt layers existed at 01:00Z; the honest state of "is otto serving" was UNKNOWN.

## Optimised build order (LAW 51)

Naive: patch the allowlist, add a Slack webhook route beside the Telegram one, script per-channel
onboarding — 3 channel-specific lanes now, N lanes per client later, every onboarding a deploy;
rework guaranteed and rejected by the directive.

Optimised — 6 steps, one lane, nothing channel-specific outside verifier plugins:
1. `tenant_id` on both envelopes + refusal test (hermes-v2, in flight).
2. `otto/ingress/` gateway + `channel_binding` store + Telegram verifier plugin (in flight,
   branch `otto/event-gateway`).
3. Registry-as-data proof: runtime second-tenant test, zero restart (in flight).
4. Real SigNoz `TraceBackend` + `otto-obs-coverage` in CI and post-deploy (`otto/obs/coverage.py`
   today resolves to None in otlp mode — the gate can never be green in-cluster until this).
5. Deploy manifests move the public route off otto-golden onto the gateway; compute pods lose
   the Telegram secret mount; binding row #1 created through the control-plane path itself.
6. Registration reconciler + canary tenant + door probe rows (idp), turning "is otto working"
   into a per-tenant query.

Counted: channel onboarding goes from ~6 manual steps + a deploy per channel to 1 database
event; operational proof goes from 1 human probe (wrong tonight) to 4 standing queries.

## Status ledger (update in place)

- 2026-09-03: directive recorded; steps 1–3 building on hermes-v2 `otto/event-gateway`;
  steps 4–6 pending; engineering gap table and operations receipt design in the consultant
  round of this date (session record). Old otto (hermes-agent) remains permanent and becomes
  an envelope consumer in step 5's wave.
