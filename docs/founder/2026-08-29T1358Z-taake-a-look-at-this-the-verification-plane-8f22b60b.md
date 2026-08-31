---
captured: 2026-08-29T13:58:34+00:00
session: a7b41022-3074-43c7-bb13-a1d7e07adff1
cwd: /Users/chidionyema/dev/code
chars: 17666
source: founder prompt, verbatim (founder-doc-capture.py)
---

taake a look at this The Verification Plane

Status: design spec, v1 Scope: replaces self-certified agent success reporting across the estate Non-goals: UI, features, new services. Nothing ships until this does.

0. What this actually guarantees

It does not guarantee correct systems. Nothing does.

It guarantees one thing structurally: a work item cannot reach CLOSED without a fresh, signed verdict, produced by a process the agent cannot run, bound to the exact artifact that was deployed. The class of failure you just hit — agent asserts done, reality disagrees, nobody notices for eight hours — becomes unreachable rather than discouraged.

Measured expectation, from the literature: independent state verification moved false success from ~48% of failures to ~3%. Not zero. Three percent.

Residual risk after this is built, stated honestly:

Risk    Mitigation    Fully solved?
Probe asserts the wrong thing    Negative controls + mutation testing (§6)    Mostly
Auth silently disabled; positive probe still passes    Paired negative probe, mandatory (§4.3)    Yes
Agent edits the probe instead of fixing the bug    Probes in CODEOWNERS-protected path, human approval (§6.1)    Yes, if enforced
Prover host compromised    Out of scope; single-operator threat model    No
Probe path ≠ real user path    Journey probes (L4), periodic manual spot-check    Partially

If you want a number to hold me to: this removes self-certification, not error.

1. Three planes, hard boundaries
┌─────────────────────────────────────────────────────────────┐
│ ACTOR PLANE          agents, subagents, Claude Code, DeepSeek│
│ CAN: read code, edit code, open PRs, propose state           │
│ CANNOT: hold probe credentials, write verdicts, close tickets,│
│         merge to main, bypass rules, run the prover          │
└───────────────────────────┬─────────────────────────────────┘
                            │ requests verdict (nonce)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ VERIFICATION PLANE   "the Prover" — separate host/runner      │
│ OWNS: probe credentials, HMAC signing key, browser runners    │
│ EMITS: signed Verdict records. Append-only.                   │
└───────────────────────────┬─────────────────────────────────┘
                            │ verdicts (read-only to actors)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ CONTROL PLANE        ticket state machine, merge gate         │
│ READS: verdicts only. Never agent prose.                      │
└─────────────────────────────────────────────────────────────┘

The boundary is credential separation, not policy. The agent cannot produce a verdict because it does not possess the signing key or the probe credentials. Not "must not." Cannot.

2. The Verdict record
sql
CREATE TABLE verdict (
  verdict_id      UUID PRIMARY KEY,
  check_id        TEXT NOT NULL,          -- 'langfuse.l3.sso_cold_login'
  target          TEXT NOT NULL,          -- 'langfuse@prod'
  commit_sha      TEXT NOT NULL,          -- source under test
  artifact_digest TEXT NOT NULL,          -- image digest actually running
  config_revision TEXT NOT NULL,          -- helm release revision
  nonce           TEXT NOT NULL UNIQUE,   -- issued by control plane per request
  started_at      TIMESTAMPTZ NOT NULL,
  completed_at    TIMESTAMPTZ NOT NULL,
  ttl_seconds     INT NOT NULL DEFAULT 900,
  outcome         TEXT NOT NULL CHECK (outcome IN
                    ('PASS','FAIL','BLOCKED','ERROR')),
  assertions      JSONB NOT NULL,         -- [{name, expected, actual, ok}]
  evidence_ref    TEXT,                   -- S3 key: HAR, screenshot, raw body
  prover_id       TEXT NOT NULL,
  prover_run_id   TEXT NOT NULL,
  sig             TEXT NOT NULL           -- HMAC-SHA256 over canonical form
);

CREATE UNIQUE INDEX ON verdict (check_id, nonce);
REVOKE INSERT, UPDATE, DELETE ON verdict FROM agent_role;
GRANT SELECT ON verdict TO agent_role;

Five properties that matter, each closing a specific hole:

artifact_digest + config_revision — a verdict is about a running artifact, not a service name. Redeploy a different image, the verdict no longer applies. This is what stops "it passed yesterday" from counting.
nonce — the control plane issues it when a check is requested. Prevents replay of an old PASS. Without this, an agent can point at a stale green.
ttl_seconds — expiry is a first-class state. now() - completed_at > ttl means UNVERIFIED, not PASS.
sig — HMAC-SHA256 with a key held only by the prover host. Verdicts with bad signatures are treated as absent.
assertions as structured data — not a log blob. The gate reads fields; nobody greps prose.

On signing: HMAC in Postgres is correctly sized for the threat model "my own agents overclaim." If you later want supply-chain-grade provenance, the upgrade path is GitHub Artifact Attestations, which bind a subject and its digest to an in-toto predicate signed with a short-lived Sigstore certificate, verifiable via gh attestation verify. Private repos use GitHub's own Sigstore instance. Don't start there — it solves adversary-tampering, which is not your problem today.

3. Ticket state machine
                     ┌──────────────────────────────┐
                     ▼                              │
OPEN ──► IN_PROGRESS ──► RESOLVED_PENDING_VERIFICATION
                     │              │
                     │              ├──[prover: PASS]──► VERIFIED ──► CLOSED
                     │              └──[prover: FAIL]──► REJECTED ───┘
                     │
                     └──► BLOCKED (requires: reason + live-query attempt log)
Transition    Who
OPEN → IN_PROGRESS    agent
→ RESOLVED_PENDING_VERIFICATION    agent
→ BLOCKED    agent (must attach the failed live query)
→ VERIFIED / → REJECTED    prover only
→ CLOSED    prover (on VERIFIED) or human

The agent's most positive available claim is "I think I'm done." That phrase carries no weight in the system. RESOLVED_PENDING_VERIFICATION with no fresh verdict after 24h auto-reverts to IN_PROGRESS.

Enforcement on GitHub: required status check verify/verdict-fresh, supplied by the prover as a GitHub App. Note the real constraint — bypass lists on rulesets only work for repos owned by an organisation, not personal accounts. If prospector is under your personal account, move it to a free org first, otherwise you are permanently a bypass actor and the gate is decorative. Agent gets a fine-grained token with contents:write, pull_requests:write, and nothing else.

4. Probe hierarchy

Five levels. Each proves strictly more than the one below and costs more. Tier by blast radius, or you'll disable the whole thing inside a month.

Level    Proves    Cost    Cadence
L0 Reachability    DNS/TCP/TLS    ~0    60s
L1 Liveness    process is up    ~0    60s
L2 Machine plane    authenticated API works    low    every merge
L3 Human plane    SSO actually works    high    every deploy of a user-facing surface
L4 Journey    the whole pipeline works    high    nightly + on release
4.1 L1 — liveness (and why it proves almost nothing)

Langfuse exposes /api/public/health on the web container and /api/health on the worker (port 3030). By default the health check does not validate database connectivity — it's designed to keep serving traffic when the DB is briefly unavailable. Use ?failIfDatabaseUnavailable=true if you want the DB included.

Two live traps:

/api/public/ready returned 404 on some chart/app version combinations (helm 1.5.22 / app 3.155.1), leaving web pods stuck at 0/1 Ready indefinitely while the app logged Ready in 959ms. Verify the endpoint exists before you gate on it. If your readiness probe points there and 404s, your pods never receive traffic and every downstream probe fails for the wrong reason.
On v3→v4 dual-write migrations, /api/health?failIfEventPropagationStuck=true returns 503 when the propagation job stalls. Worth wiring if you're mid-migration.

L1 assertions: HTTP 200 AND body parses AND response time < threshold. Nothing about auth. Ever.

4.2 L2 — machine plane

Langfuse's public API uses HTTP Basic auth: public key as username, secret key as password. All endpoints require auth except health checks.

bash
curl -sf <redacted> "$LF_HOST/api/public/projects" \
  | jq -e '.data | length > 0 and (.[0].id | type == "string")'

Critical distinction — this is the mistake that produced the last eight hours: API-key auth is validated in-application against the key table. It does not traverse your OIDC path at all. Langfuse has dual authentication paths: session-based for the web UI, API-key-based for programmatic access. A green L2 tells you the app, DB and key store are alive. It tells you nothing about whether a human can log in. These are separate planes and need separate probes.

4.3 L3 — human plane (the one that failed)

Langfuse browser auth is NextAuth with JWT session strategy; custom OIDC callback lands at /api/auth/callback/custom, and NEXTAUTH_URL must match the access URL exactly or callbacks break.

Rules for this probe:

No storageState reuse. Playwright's standard advice is to authenticate once in a setup project and reuse the saved cookies across tests — correct for functional tests, wrong here. This probe's subject is the login flow. Cold context, full handshake, every run.
Assert on session identity, not on 200. A login page returns 200. A redirect chain to the IdP terminates in 200. Hit /api/auth/session with the browser's jar and assert user.email === EXPECTED_PROBE_IDENTITY. Do not assert on cookie presence: a next-auth advisory (GHSA-v64w-49xw-qq89, fixed in 4.24.5) covers exactly the case where a mock user with no associated information passes an existence check. Session existence is authentication theatre; the email claim is the assertion.
Paired negative control, mandatory. A fresh context with no credentials must NOT reach the protected content. Without this, your probe goes green when auth is disabled. Every L3 check is two assertions or it is not a check.
Then one DOM assertion on a post-auth element (project name in the sidebar) to confirm the app rendered for that identity, not just that an API returned JSON.

Tailscale trap, and this one will bite you specifically. Tailscale Serve injects Tailscale-User-Login, Tailscale-User-Name and Tailscale-User-Profile-Pic for tailnet traffic — but identity headers are not populated for traffic originating from tagged devices. A CI prober joined with a tagged auth key gets no identity header, fails, and you spend a day debugging a working system. Three options:

Run the prover on an untagged, user-owned node (simplest).
Use app capability grants, which do apply to tagged devices, and assert on the capability header instead.
Use tsidp — Tailscale's OIDC/OAuth-compliant IdP — so the probe performs a genuine OIDC handshake rather than trusting a proxy header.

Also: if the app is reachable on its own port alongside the Serve proxy, anything on that host can set the header directly and bypass the gate. Restrict via ACL to port 443 and confirm the app's port isn't separately exposed. Add that as an L3 assertion — the direct-port bypass must fail.

ts
// probes/langfuse/l3-sso-cold.spec.ts
import { test, expect, chromium } from '@playwright/test';

const HOST = process.env.LF_HOST!;
const IDENT = process.env.PROBE_IDENTITY!;

test('cold OIDC handshake yields an identified session', async () => {
  const ctx = await (await chromium.launch()).newContext(); // no storageState
  const page = await ctx.newPage();
  await page.goto(`${HOST}/`, { waitUntil: 'networkidle' });

  const s = await (await page.request.get(`${HOST}/api/auth/session`)).json();
  expect(s?.user?.email, 'no identified session after handshake').toBe(IDENT);

  await expect(page.getByTestId('project-switcher')).toContainText(
    process.env.LF_PROJECT_NAME!
  );
  await ctx.close();
});

test('NEGATIVE: unauthenticated context is refused', async () => {
  const ctx = await (await chromium.launch()).newContext();
  const r = await ctx.request.get(`${HOST}/api/auth/session`);
  const body = await r.json();
  expect(body?.user, 'gate is open — auth is not enforced').toBeUndefined();
  await ctx.close();
});
4.4 L4 — journey

The only probe that proves the system does its job. Emit a trace with a unique ID via the OTLP endpoint, then read it back through the authenticated API within N seconds.

POST /api/public/otel/v1/traces   (unique trace id)
  → poll GET /api/public/traces/{id} until 200 or timeout 60s
  → assert returned id == emitted id

This traverses ingest → queue → worker → ClickHouse → query. Note the legacy Ingestion API is being sunset (2026-11-16 on Cloud; already unavailable on self-hosted v4 in events_only write mode) — build the probe on OTLP, not the legacy path, or you'll rewrite it in ten weeks.

5. Killing stale state

Policy said "don't read the cache." Policy loses. Remove the capability.

Delete the catalogue file. Not deprecate — delete. Replace with bin/inventory which queries the live cluster and prints to stdout. A file that does not exist cannot be read at 3am by an agent whose live query timed out.
CI lint rejects reintroduction. Fail the build on any tracked file matching *catalogue*.yaml|*inventory*.yaml|*state*.json outside a whitelist. Agents recreate deleted conveniences; make it a red check.
Every fetched fact carries fetched_at. The reader — not the writer — rejects records older than TTL and raises StaleStateError. Fail closed.
Ephemeral kubeconfig. Agents get a read-only token minted per task, 15-minute expiry. No long-lived kubeconfig on disk. Expiry forces a live path.
Cluster truth means observedGeneration. This is the k8s-level version of your stale-catalogue bug:

Every GitOps tool watches for observedGeneration == metadata.generation before considering a rollout complete. Omit it once and CI starts acting on stale conditions — marking deployments green minutes before the controller has caught up to the new .spec. It is the single most common cause of "my pipeline passed but production is broken."

kubectl wait does not check observedGeneration; kstatus does. Note also that kubectl rollout status timing out only stops the client watch — the cluster keeps reconciling, so a timeout is not a failure verdict, it's BLOCKED.
python
def settled(dep) -> bool:
    if dep.status.observed_generation != dep.metadata.generation:
        raise StaleStateError("controller has not observed current spec")
    return (dep.status.updated_replicas == dep.spec.replicas
            and dep.status.available_replicas == dep.spec.replicas
            and dep.status.unavailable_replicas in (0, None))
6. Anti-gaming

The moment a gate exists, the cheapest path to green becomes weakening the gate. Three counters:

6.1 Agents cannot author their own verifier

Probe definitions live under probes/ with CODEOWNERS requiring your approval. A PR touching both src/ and probes/ is auto-flagged. Otherwise the agent fixes the test.

6.2 Mutation testing — a probe that has never failed is not a probe

Weekly, run each probe against a deliberately broken target (auth disabled, wrong digest, DB down) and assert it returns FAIL. A probe that passes the mutation run is quarantined and cannot gate anything.

6.3 Unproven-probe status

New probes start UNPROVEN and are advisory only. They graduate to GATING after recording at least one genuine FAIL and one genuine PASS. Green-from-birth probes are usually asserting nothing.

7. Rollout

Phase 0 — ground truth (1 day). Manual L3 walk of every service in the estate. Write down what actually works. You currently don't know, and every plan built on the current inventory is built on the thing that lied to you.

Phase 1 — observe mode (3–5 days). Build prover + verdict store. Run probes on every agent claim. Enforce nothing. Log agent claim vs verdict. At the end you have your own false-success rate — your number, not a paper's. That number is what justifies phase 2 and tells you which agent architectures to stop using.

Phase 2 — enforce on Langfuse only (2 days). One service, full gate. Live with the friction. Tune TTLs and tiers until the gate is fast enough that you never want to skip it.

Phase 3 — extend. One service at a time. Each entry requires L2 + L3 + negative control before it may be gated.

Do not skip Phase 1. Enforcement without a measured baseline means you can't tell whether the layer is working or just slowing you down, and in three weeks you'll turn it off during a deploy and never turn it back on.

8. Build order
verdict table + HMAC signing + read-only agent role
bin/inventory (live query) + delete catalogue + CI lint
L1/L2 probes for Langfuse
Prover daemon: nonce → run → sign → persist
L3 cold-SSO + negative control (resolve the Tailscale tagged-device question first)
State machine + verify/verdict-fresh status check
L4 journey probe
Mutation harness
Extend
Open decisions
Tailscale identity for the prover — untagged node, app capability grants, or tsidp? Determines whether L3 is a header assertion or a real OIDC handshake. tsidp is more work and tests more.
Repo ownership — is prospector under a personal account? If so, rulesets bypass lists won't work and the merge gate is advisory until it moves to an org.
Prover host — cloud-side or on the MacBook? On-laptop means the gate is offline when the laptop is, which conflicts with running the estate from your phone. Cloud-side prover with the tailnet identity is probably the answer, but it makes the tagged-device question urgent. agents are doing half baked work and can no longer be trusted
