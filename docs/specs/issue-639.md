# Build: Messaging platform day 0 (NATS JetStream, outbox, contracts) in Go

Issue: https://github.com/chidionyema/crew/issues/639
Written by pm-agent on 2026-08-29 from conversation with @chidionyema.

## What the founder asked for

Founder, 2026-08-29: "new request for principal/staff engineer: review, architect, build, operationalise and demo app. need policy and save this doc in line with our doc standards. this is a founder level doc not engineer." "Golang is preferred stack for this day 0 layer." "once designed, MiniMax is here to go halves with, spec it thoroughly, wanna see BDD."

## Principal review of the founder's specification (v0.1), against the estate

The specification is sound and is adopted as written for its four locked contracts (D1 subject grammar, D2 CloudEvents binary + protobuf, D3 outbox as the sole publish path, D4 operator mode with one account per domain). The findings below are where the estate already answers a section, or where the estate's laws change a value. Each is a ruling, not an option.

1. Reuse, not a second broker (headline rule, LAW 39). idp#800 (crew#623) already carries `platform/event-bus`: the official nats-io Helm chart 2.14.6 (nats-server 2.14.6) as a Flux HelmRelease, dark. Day 0 builds on that row. The hand-written `nats-server.conf` in §3.1 becomes chart values; nothing in this platform writes a server config file by hand.
2. Version. The spec says nats-server ≥ 2.11; the chart pins 2.14.6. The platform pins the chart minor and upgrades lab-first, as §3.1 says.
3. Replicas (§3.2). The OKE cluster has 2 worker nodes (pod list of run 33255009034: two csi-oci-node, two kube-proxy). R3 across three zones cannot exist on it. Day 0 runs `num_replicas: 1` with the outbox as the disaster-recovery truth (the spec's own §3.3 and §8.1 say the stream is not the system of record); R3 is switched on by one values change when the node pool has three nodes (`policy/node_pool.rego` caps that spend). This is the one place the spec's number is not the day-0 number, and it is recorded here so nobody rediscovers it.
4. Secrets (§6.1). Operator and account seeds live in OCI Vault and reach the cluster as ExternalSecrets (`idp/platform/secret-store`), never a generic "secrets manager" and never a file on a laptop. `nsc` JWTs are committed; the resolver is preloaded from them.
5. Telemetry (LAW 50). `prometheus-nats-exporter` and the relay and consumer metrics are scraped into the estate collector (SigNoz); traces go OTLP to the same collector; the seven alerts of §10 are PrometheusRule rows in `platform/monitoring` routed to alertmanager, never to the founder's chat (memory: founder DM is not an alert sink). Coverage is proved by querying the backend.
6. Admission. Every pod (NATS, relay, DLQ processor, exporter) passes the cluster's Kyverno policies in `platform/edge`: requests, probes, read-only root, non-root. Proved by `bin/idp-kyverno-dirs` before the PR, as the commerce layer was.
7. Ports. 4222, 6222 and 8222 are rows in `catalog/ports.yaml` (`bin/port-gate`); 8222 is cluster-internal only.
8. Schema registry (§5.4, LAW 23 smaller road). The schemas live in this platform's tree (`platform/messaging/schemas/{domain}/{aggregate}_{action}/v{n}.proto` with `SUBJECTS.md`), graded by `buf breaking` in CI. A separate `platform-schemas` repository is the §1.2 trigger (more than three producing teams), not day 0.
9. Language. Go for the relay, the consumer library, the DLQ processor and the `ops replay` tool: one module `platform/messaging` (go 1.23, `nats.go` JetStream API, `pgx`, `buf`). Images are multi-arch on ghcr.io (`bin/multiarch-gate`), bumped by Flux image automation. A .NET client is a later checkpoint when the store (prospector, .NET) consumes; not day 0.
10. Demo and onboarding (LAW 32). `bin/idp-messaging-demo` inserts one `orders.event.order.placed.v1` through the outbox of a demo service, watches the relay publish it, a demo consumer process it once, and prints the trace id read back from SigNoz. `docs/how-to/onboard-a-service-to-messaging.md` is the onboarding.
11. Acceptance (§11) is the BDD. Each of the eight acceptance tests is a scenario in `docs/prose/messaging-*.feature`, run on the portability drill's throwaway k3s job first (the spec's "staging"), then re-graded weekly on the cluster by a scheduled drill (`drills/catalogue.yaml`).
12. Postgres. Each service keeps its own database (as today: lago, langfuse, temporal each have one); the outbox table is per service database, exactly as §7.1. No shared event database.
13. Deferred items (§1.2) stand. Nothing on that table is built; the trigger column is the rule.
14. Two words in the spec are changed to the estate's: "secrets manager" means OCI Vault through ExternalSecrets; "staging" means the k3s job of the portability drill until crew#584 CP-H lands the staging namespace.

Risks, one sentence each: R1 on two nodes means a node loss pauses the bus until the pod reschedules (outbox replays, nothing is lost); operator-mode auth is unfamiliar to every session and is the part most likely to be misconfigured, so CP6 proves the refusal, not the grant; the founder's store is .NET and cannot consume until a .NET client exists (deferred, named).

Optimised: naive plan is 10 checkpoints x (1 PR + 1 CI run + 1 cluster reconcile + 1 drill) = 40 round trips, bottleneck the cluster reconcile and the k3s acceptance job (about 12 minutes each). Batched: CP2 to CP5 are graded locally against a NATS container and a Postgres container in the Go test suite (no cluster), CP6 to CP8 share one k3s job run, and CP9 reuses that run's artefacts; cluster reconciles collapse to two (broker on, everything on). Count after: 10 PRs, 10 CI runs, 2 reconciles, 2 k3s runs = 24 round trips.

Standard: NATS JetStream (Apache-2.0, official chart) is the row "Event bus" to add to `crew/docs/STANDARDS.md` in CP1; Go is the row for platform daemons.

## The founder's specification, verbatim (v0.1, 2026-08-29)

### Messaging Platform Specification — Day 0

**Status:** Draft for implementation
**Version:** 0.1
**Owner:** Chidi
**Broker:** NATS Server ≥ 2.11 with JetStream (CNCF / Apache-2.0 line)
**System of record:** PostgreSQL ≥ 16

#### 1. Purpose and scope

This document specifies the day-0 event backbone for the company: a NATS JetStream cluster, a transactional-outbox publish path, a message contract, a security model, and consumer-side delivery rules. An engineer should be able to build and operate the platform from this document alone.

**Design principle:** durability lives in the contracts (subjects, envelope, idempotency, single publish path), not in the broker. Every component here is replaceable except the contracts in §4 and §5.

##### 1.1 Goals

- Atomic "write state + emit event" via transactional outbox (no dual-write window).
- Effectively-once delivery **into** streams; at-least-once delivery **out of** streams with mandatory consumer idempotency.
- Tenant/domain isolation via NATS accounts from day one.
- Full traceability (W3C trace context) on every message from message one.
- Swappable broker: no application code speaks NATS directly for business events.

##### 1.2 Non-goals (explicitly deferred — do not build)

| Deferred item | Trigger to revisit |
|---|---|
| Multi-region supercluster / gateways | Second region with latency SLO |
| Leaf nodes (edge/robotics) | First offline-capable edge deployment |
| MQTT gateway | First fleet of MQTT-only devices |
| Kafka / Redpanda / WarpStream + bridge | Analytics ingestion > ~50 GB/day into a lakehouse |
| CDC (Debezium etc.) | A consumer that needs row-level DB changes, not domain events |
| Schema registry *server* | >3 teams producing schemas; until then, the schema git repo is the registry |

#### 2. Architecture overview

```
                    ┌────────────────────────────────────────────┐
                    │              NATS Cluster (R3)             │
   ┌──────────┐     │  ┌────────┐   ┌────────┐   ┌────────┐      │
   │ Service A │────┼─▶│ nats-1 │◀─▶│ nats-2 │◀─▶│ nats-3 │      │
   └────┬──────┘     │  └────────┘   └────────┘   └────────┘     │
        │            │        JetStream: file store, R3          │
        │ tx         └────────────────▲───────────▲──────────────┘
        ▼                             │           │
   ┌──────────┐    ┌──────────┐       │           │ pull (at-least-once)
   │ Postgres │◀───│  Relay   │───────┘           │
   │  +outbox │    │ (publish │  publish w/       ▼
   └──────────┘    │  only)   │  Nats-Msg-Id   ┌──────────────┐
                   └──────────┘                │  Consumers   │
                                               │ (idempotent) │
                                               └──────────────┘
```

Rules encoded in the diagram:

1. **Services never publish business events to NATS.** They insert into the outbox inside their own database transaction. This is enforced by credentials (§6.4), not convention.
2. **The relay is the only writer** to business event subjects.
3. **Consumers pull.** Push consumers are not used for business streams.
4. Core NATS request-reply (ephemeral, non-JetStream) is permitted for internal RPC; it carries no durability guarantees and must never carry state-changing commands without an outbox-backed follow-up event.

#### 3. Infrastructure

##### 3.1 Cluster

| Item | Value |
|---|---|
| Nodes | 3, spread across availability zones |
| Server | `nats-server` ≥ 2.11.x, pinned minor, upgraded lab-first |
| Storage | Local NVMe/SSD, dedicated volume for JetStream store dir |
| Sizing (day 0) | 2 vCPU / 4 GB RAM / 100 GB disk per node — revisit at 1k msg/s sustained |
| JetStream `max_file_store` | 80 GB per node (leave 20% disk headroom) |
| JetStream `max_memory_store` | 512 MB per node (memory streams are not used day 0) |
| TLS | Required on client, cluster and monitoring ports; internal CA or ACME |
| Ports | 4222 client / 6222 cluster / 8222 monitoring (localhost or mTLS only) |

`nats-server.conf` skeleton (per node; substitute names/routes):

```hcl
server_name: nats-1
listen: 0.0.0.0:4222

jetstream {
  store_dir: /var/lib/nats/jetstream
  max_file_store: 80GB
  max_memory_store: 512MB
}

cluster {
  name: core
  listen: 0.0.0.0:6222
  routes: [ nats://nats-2:6222, nats://nats-3:6222 ]
  tls { ...cluster mTLS... }
}

tls { cert_file: ..., key_file: ..., ca_file: ... }

# Operator-mode auth (§6): operator JWT + resolver, no static users
operator: /etc/nats/operator.jwt
system_account: <SYS account public key>
resolver: {
  type: full
  dir: /var/lib/nats/resolver
  allow_delete: false
}
resolver_preload: { ... }
```

##### 3.2 Placement and failure expectations

- All business streams: `replicas: 3` (R3). Loss of one node is a non-event; loss of two halts writes (Raft majority) — this is the accepted trade.
- Consumer state is also Raft-replicated; expect brief (<2 s) leader elections on node restart. Clients must use default reconnect with jitter.

##### 3.3 Backups

- Nightly `nats stream backup <STREAM> <dir>` per stream, shipped off-cluster.
- Postgres outbox retention (§7.4) means the last 7 days of events are independently reconstructable from the database — the outbox is the disaster-recovery source of truth, the stream backup is convenience.
- Restore drill: quarterly, restore one stream into a scratch cluster and replay 1k messages through a test consumer. This drill is part of the definition of done (§11).

#### 4. Subject taxonomy (contract — changes require an ADR)

##### 4.1 Grammar

```
{domain}.{kind}.{aggregate}.{action}.{version}

domain    ∈ lowercase, singular, bounded-context name   e.g. orders, identity, billing
kind      ∈ { event, cmd }
aggregate = the entity, lowercase singular              e.g. order, user, invoice
action    = past-tense verb for events, imperative for cmds
version   = v1, v2, ... (major only; minor changes are additive in-schema)
```

Examples:

```
orders.event.order.placed.v1
orders.event.order.cancelled.v1
billing.cmd.invoice.issue.v1
identity.event.user.registered.v1
```

##### 4.2 Rules

1. **No environment, no tenant, no region in the subject.** Environments are separate clusters; tenants are NATS accounts (§6.2).
2. **Version bumps create a new subject** and a new schema file. Producers dual-publish v(n) and v(n+1) during migration; v(n) is retired only when consumer count on it reaches zero (observable via consumer info).
3. Wildcards are for consumers only (`orders.event.>`); producers publish to fully-qualified subjects.
4. Reserved prefixes, never used for business traffic: `$JS.>`, `$SYS.>`, `dlq.>`, `internal.>`.
5. Every new subject is registered in the schema repo (§5.4) before first publish. The repo is the registry.

#### 5. Message contract (contract — changes require an ADR)

##### 5.1 Envelope

CloudEvents 1.0, **binary content mode**: CloudEvents attributes travel as NATS headers, payload is the bare protobuf message. This keeps the payload broker-neutral and the metadata inspectable without deserialising.

Mandatory headers on every business message:

| Header | Content | Source |
|---|---|---|
| `Nats-Msg-Id` | `outbox:{outbox.id}` | relay — JetStream dedupe key |
| `ce-specversion` | `1.0` | relay |
| `ce-id` | same value as outbox id | relay |
| `ce-type` | the subject string | relay |
| `ce-source` | `/{service-name}` | producer, stored in outbox |
| `ce-time` | outbox `created_at`, RFC3339 | relay |
| `ce-dataschema` | schema repo path + git tag, e.g. `orders/order_placed/v1@r2026.34` | producer |
| `traceparent` | W3C trace context of the *originating request* | producer, stored in outbox |
| `tenant-id` | tenant UUID (single-account deployments only; multi-account tenancy carries it implicitly) | producer |

##### 5.2 Payload

- Protobuf 3. One message type per subject version.
- `bytes` on the wire; no JSON for business events. (JSON is permitted for `internal.>` operational messages only.)

##### 5.3 Evolution rules

1. Additive only within a version: new optional fields, never renumber, never change types, never reuse removed field numbers (mark `reserved`).
2. Anything non-additive = new version = new subject (§4.2 rule 2).
3. Consumers must tolerate unknown fields (protobuf default — do not configure strictness that breaks this).

##### 5.4 Schema repository

- Single git repo `platform-schemas`: `/{domain}/{aggregate}_{action}/v{n}.proto` plus a `SUBJECTS.md` index. CI runs `buf breaking` against the previous tag; a breaking diff fails the build.
- Tagged weekly (`r{year}.{week}`); `ce-dataschema` references the tag.

#### 6. Security model

##### 6.1 Operator mode

- `nsc` -managed operator → accounts → users. No accounts or users in server config files. Full NATS-based resolver on the cluster (config in §3.1).
- Operator and account signing keys live in the secrets manager; `nsc` state is committed (JWTs are public) — **seeds are never committed**.

##### 6.2 Account layout (day 0)

| Account | Purpose |
|---|---|
| `SYS` | system account, monitoring only |
| `PLATFORM` | streams, relay, DLQ processor, ops tooling |
| `APP-{domain}` | one per bounded context (e.g. `APP-ORDERS`, `APP-IDENTITY`) |
| `TENANT-{id}` | created per enterprise tenant when external consumers arrive; exports/imports used to share specific streams read-only |

Streams live in `PLATFORM`. Domain accounts get cross-account **imports** of exactly the subjects they may consume, and an export path for their relay publishes. This is more ceremony than one flat account — it is the point: isolation is structural, and adding a paying tenant later is an import grant, not a re-architecture.

##### 6.3 Users (per account, distinct credentials per service instance class)

- `{service}-app` — the service runtime.
- `{service}-relay` — the outbox relay for that service.
- `ops-admin` — humans, short-lived creds via `nsc generate creds`, rotated.

##### 6.4 Permissions (the enforcement of §2 rule 1)

- `{service}-app`: **publish deny** on `*.event.>` and `*.cmd.>`; publish allow on `internal.{service}.>` and `_INBOX.>` (request-reply); subscribe allow on its imported subjects + `_INBOX.>`.
- `{service}-relay`: publish allow **only** on that domain's fully-qualified event/cmd subjects; subscribe allow on `$JS.ACK.>` implicit; nothing else.
- Nobody but `PLATFORM` ops users may touch `$JS.API.>` stream-admin verbs; domain users get consumer-level API only.

A service that tries to bypass the outbox gets a permissions violation, not a code-review comment.

#### 7. Outbox and relay (the publish path)

##### 7.1 Table (one per service database)

```sql
CREATE TABLE outbox (
  id            BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  subject       TEXT        NOT NULL,       -- fully-qualified, §4
  payload       BYTEA       NOT NULL,       -- serialized protobuf
  ce_source     TEXT        NOT NULL,
  ce_dataschema TEXT        NOT NULL,
  traceparent   TEXT,
  tenant_id     UUID,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  published_at  TIMESTAMPTZ
);

CREATE INDEX outbox_unpublished_idx ON outbox (id) WHERE published_at IS NULL;
```

**Invariant:** the outbox INSERT happens in the same transaction as the state change it describes. A domain event with no corresponding state change, or vice versa, is a bug by definition.

##### 7.2 Relay algorithm

One relay process (or goroutine/hosted service) per service database. Horizontal relay instances are safe because of `SKIP LOCKED` + dedupe.

```
loop every POLL_INTERVAL (default 200ms) or on LISTEN/NOTIFY wake:
  BEGIN;
  rows := SELECT id, subject, payload, ce_source, ce_dataschema,
                 traceparent, tenant_id, created_at
          FROM outbox
          WHERE published_at IS NULL
          ORDER BY id
          FOR UPDATE SKIP LOCKED
          LIMIT 100;

  for r in rows:
    ack := jetstream.Publish(r.subject, r.payload, headers per §5.1,
                             MsgId = "outbox:" + r.id)
    // ack.Duplicate == true is SUCCESS (prior attempt landed)
    on error: ROLLBACK; backoff; continue loop   // rows republish next pass

  UPDATE outbox SET published_at = now() WHERE id IN (row ids);
  COMMIT;
```

- Insert trigger fires `NOTIFY outbox_wake` to cut latency; the poll remains as the safety net (NOTIFY is not durable across restarts).
- Publish uses synchronous `Publish` (await the PubAck). Async batching is a later optimisation; do not start there.
- Relay metrics (mandatory): unpublished backlog count, oldest unpublished age, publish error rate, duplicate-ack rate. Alert: backlog age > 30 s.

##### 7.3 Why this is closed

The only crash window is "PubAck received, UPDATE not committed." On restart the row republishes with the same `Nats-Msg-Id`; JetStream's duplicate window drops it and returns `duplicate: true`. Effectively-once into the stream from an at-least-once relay. This depends on §8's `duplicate_window` exceeding the worst-case relay outage — that is why it is 15 minutes, not the 2-minute default.

##### 7.4 Retention

- `DELETE FROM outbox WHERE published_at < now() - interval '7 days'` on a nightly job, or native partitioning by day with partition drop. 7 days of published rows are retained deliberately as the DR replay source (§3.3).

#### 8. Streams and consumers

##### 8.1 Stream per domain

One stream per bounded context, capturing all its event subjects:

```json
{
  "name": "ORDERS_EVENTS",
  "subjects": ["orders.event.>"],
  "storage": "file",
  "num_replicas": 3,
  "retention": "limits",
  "max_age": 2592000000000000,
  "duplicate_window": 900000000000,
  "discard": "old",
  "deny_delete": true,
  "deny_purge": true
}
```

(`max_age` is 30 days in nanoseconds; analytics tail-reads before expiry. `duplicate_window` is 15 minutes in nanoseconds, see §7.3.)

- Commands (`{domain}.cmd.>`) get a separate stream with `"retention": "workqueue"` **only if** exactly-one-handler semantics are required; note WorkQueue streams reject overlapping subject filters across consumers — plan filters before creating them.
- 30-day `max_age` is a cost decision, not an architecture decision: the permanent record is Postgres + outbox. If event replay beyond 30 days becomes a requirement, raise `max_age` or add an object-store tiering consumer — do not treat the stream as the system of record.

##### 8.2 Consumers

- **Durable, pull, explicit ack** for every business consumer. Named `{service}-{purpose}`.
- Defaults: `ack_wait: 30s`, `max_deliver: 5`, `max_ack_pending: 1000`, `ack_policy: explicit`, `deliver_policy: all` (first deploy) then `new`.
- Long-running work (AI/agent tasks): call `msg.InProgress()` on a heartbeat well inside `ack_wait` — do not raise `ack_wait` to 30 minutes.
- Per-aggregate ordering, where required: include the aggregate id as a subject token at publish time and either (a) one filtered ordered consumer per hot aggregate, or (b) `max_ack_pending: 1` on the consumer (throughput trade, acceptable at day-0 volume). Choose per consumer; record the choice.
- Terminal-failure ack: handlers that hit a permanent error call `msg.Term()` (with reason) rather than letting redelivery run to exhaustion.

##### 8.3 Dead letters

JetStream does not move exhausted messages anywhere — it stops delivering and emits an advisory. The platform ships a small **DLQ processor** in the `PLATFORM` account:

1. Subscribes to `$JS.EVENT.ADVISORY.CONSUMER.MAX_DELIVERIES.>` (a stream, `DLQ_ADVISORIES`, captures these so the processor itself can crash safely).
2. On advisory: fetch the message by stream sequence (direct get), republish to `dlq.{original-subject}` into stream `DLQ` (file, R3, 90-day max_age, `Nats-Msg-Id` = `dlq:{stream}:{seq}` for idempotent capture).
3. Alert on every DLQ arrival. DLQ depth > 0 for > 1 h is an incident.
4. Redelivery from DLQ is a manual, audited CLI action (`ops replay`), never automatic.

The same processor and stream capture `msg.Term()` cases via the `$JS.EVENT.ADVISORY.CONSUMER.MSG_TERMINATED.>` advisory.

#### 9. Consumer idempotency (platform primitive)

Shipped as a shared library (first implementations: Go and .NET), not a convention. Handler contract:

```sql
CREATE TABLE processed_messages (
  consumer_name TEXT NOT NULL,
  msg_id        TEXT NOT NULL,          -- Nats-Msg-Id header
  processed_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (consumer_name, msg_id)
);
```

```
handle(msg):
  BEGIN;
  INSERT INTO processed_messages VALUES (consumer, msg.id)
    ON CONFLICT DO NOTHING;
  if conflict: COMMIT; msg.Ack(); return          // already processed
  ... business writes (+ own outbox inserts) ...
  COMMIT;
  msg.AckSync();                                   // double-ack: confirmed by server
```

- The dedupe insert and the business write share one transaction; the ack happens only after commit. Crash after commit, before ack → redelivery hits the conflict branch and acks. At-least-once delivery becomes exactly-once *effect*.
- `processed_messages` pruned past 30 days (must exceed stream `max_age` replay horizon for that consumer).
- Handlers with naturally idempotent effects (pure upserts keyed on event id) may skip the table with a written justification in the consumer's ADR.

#### 10. Observability

- **Tracing:** relay copies `traceparent` from outbox to header; consumer library extracts it and starts a child span. One trace spans HTTP request → DB commit → publish → each consumer.
- **Metrics:** `prometheus-nats-exporter` against port 8222 on all nodes, plus JetStream consumer scrape. Dashboards: stream bytes/msgs, consumer `num_pending`, `num_ack_pending`, redelivery rate, relay backlog (§7.2).
- **Alerts (day 0, complete list):**
  1. Any node down > 2 min.
  2. JetStream store > 70% of `max_file_store`.
  3. Consumer `num_pending` growing for 15 min.
  4. Redelivery rate > 1% of delivery rate.
  5. Relay backlog oldest age > 30 s.
  6. DLQ arrival (any).
  7. Certificate expiry < 21 days.

#### 11. Definition of done (acceptance tests)

Platform is accepted when all pass in a staging environment:

1. **Outbox atomicity:** kill the service between DB commit paths under load (fault injection); zero events without state changes and zero state changes without events, verified by reconciliation script.
2. **Relay crash:** `kill -9` the relay mid-batch, restart; stream contains no duplicates (verify via `Nats-Msg-Id` scan) and no gaps vs outbox.
3. **Node loss:** stop one NATS node during sustained publish; zero publish failures after client reconnect jitter; stop a second node; publishes halt (expected) and resume on restart with no loss.
4. **Consumer crash:** kill a consumer after commit/before ack; redelivered message hits the dedupe branch; effect count unchanged.
5. **Poison message:** handler that always fails reaches `max_deliver`; message appears in `DLQ` with original headers; alert fires; `ops replay` redelivers it successfully after the handler is fixed.
6. **Permissions:** an `{service}-app` credential attempting to publish to `orders.event.>` receives a violation; the attempt is visible in `$SYS` logs.
7. **Schema gate:** a PR with a breaking proto change fails CI.
8. **Restore drill:** stream backup restored to scratch cluster; test consumer replays 1k messages with correct dedupe behaviour.

#### 12. Decision log

| # | Decision | Status | Reversal cost |
|---|---|---|---|
| D1 | Subject grammar (§4) | **Locked** | Very high — treat as API |
| D2 | CloudEvents binary + protobuf (§5) | **Locked** | High |
| D3 | Outbox as sole publish path (§7) | **Locked** | High |
| D4 | Operator mode + account-per-domain (§6) | **Locked** | High |
| D5 | NATS JetStream as broker | Adopted | **Medium — by design.** D1–D4 make this swappable |
| D6 | Self-host vs Synadia Cloud | **Open** — default self-host pending cost review | Low |
| D7 | Pull consumers only | Adopted | Low |
| D8 | 30-day stream retention | Adopted | Low (config) |

#### Appendix A — Bootstrap checklist (ordered)

1. `nsc` operator + accounts + users per §6; commit JWTs, vault the seeds.
2. Provision 3 nodes, TLS, config per §3.1; verify cluster with `nats server check`.
3. Create streams per §8.1 (`nats stream add --config`); `deny_delete/purge` on.
4. Stand up exporter + dashboards + the 7 alerts (§10).
5. Ship the shared libraries: relay, consumer/idempotency, envelope codec.
6. Create `platform-schemas` repo with CI breaking-change gate.
7. DLQ advisories stream + processor + `ops replay` CLI.
8. First real service end-to-end; run §11 acceptance suite.
9. Backup job + first restore drill.

Golang is preferred stack for this day 0 layer.

## Checkpoints

### CP1: Spec, ADR and BDD accepted. This document at `docs/specs/issue-639.md`; ADR `idp/docs/decisions/0012-messaging-day-0.md` recording D1 to D8 and the R1 ruling; the event-bus row in `crew/docs/STANDARDS.md`; one `.feature` per checkpoint under `docs/prose/`. Accept when: `crew/scripts/pr-evidence.py check` passes on the PR and every checkpoint below has a tagged scenario.

Verified by `@pytest.mark.cp1` in `checkpoints/`.

### CP2: Broker on. `platform/event-bus` un-suspended with JetStream file store, TLS on client and cluster ports, operator-mode auth from ExternalSecrets, R1, ports in `catalog/ports.yaml`, Kyverno render clean. Accept when: `nats server check jetstream` from a runner prints ok and `bin/idp-kyverno-dirs platform/event-bus` prints 0 fail.

Verified by `@pytest.mark.cp2` in `checkpoints/`.

### CP3: Contracts gated. Subject grammar gate (`bin/messaging-subject-gate`, good and bad fixtures), schema tree with `buf breaking` in CI, `SUBJECTS.md` index, first stream `ORDERS_EVENTS` (§8.1 values, deny_delete and deny_purge). Accept when: a PR with a breaking proto change fails CI and the bad fixture exits non-zero.

Verified by `@pytest.mark.cp3` in `checkpoints/`.

### CP4: Go relay. `platform/messaging/cmd/relay` implementing §7.2 (SKIP LOCKED, LISTEN/NOTIFY, synchronous publish, `Nats-Msg-Id: outbox:{id}`, headers of §5.1, the four metrics). Accept when: the Go test kills the relay mid-batch a hundred times and the stream shows zero duplicates and zero gaps against the outbox.

Verified by `@pytest.mark.cp4` in `checkpoints/`.

### CP5: Go consumer library. `platform/messaging/consumer` implementing §9 (processed_messages in the handler transaction, AckSync after commit, InProgress heartbeat, Term on permanent error). Accept when: the Go test kills the consumer between commit and ack and the effect count is unchanged after redelivery.

Verified by `@pytest.mark.cp5` in `checkpoints/`.

### CP6: Permissions prove the outbox is the only path. Accounts SYS, PLATFORM, APP-ORDERS; users app, relay, ops-admin; app credential publish-deny on `*.event.>` and `*.cmd.>`. Accept when: a publish with the app credential prints a permissions violation and the violation is visible in the SYS account log on the cluster.

Verified by `@pytest.mark.cp6` in `checkpoints/`.

### CP7: Dead letters. `DLQ_ADVISORIES` and `DLQ` streams, the Go DLQ processor, `ops replay` as an audited command. Accept when: a poison message reaches max_deliver, lands in `DLQ` with its original headers, the alert fires, and `ops replay` redelivers it after the handler is fixed.

Verified by `@pytest.mark.cp7` in `checkpoints/`.

### CP8: Observed. Exporter and relay metrics in SigNoz, one trace spanning request, commit, publish and consumer, the seven alerts as PrometheusRule rows routed to alertmanager. Accept when: `bin/idp-telemetry-coverage` lists every messaging pod as seen and a SigNoz query returns the demo trace by id.

Verified by `@pytest.mark.cp8` in `checkpoints/`.

### CP9: Accepted and demoed. The eight §11 scenarios green on the k3s job, nightly stream backup plus one restore drill green, `bin/idp-messaging-demo` on main printing its receipt, `docs/how-to/onboard-a-service-to-messaging.md`, catalogue entities for the bus, relay and DLQ processor, weekly drill row. Accept when: the drill run id is on this issue and `bin/idp-messaging-demo` prints `ok demo`.

Verified by `@pytest.mark.cp9` in `checkpoints/`.

### CP10: Founder receipt. The founder runs the demo from the portal (one button) and confirms. Accept when: his confirmation is on this issue.

Verified by `@pytest.mark.cp10` in `checkpoints/`.

