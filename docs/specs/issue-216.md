# Build: Self-aware platform — one MCP voice for the estate's own state

Issue: https://github.com/chidionyema/crew/issues/216
Written by pm-agent on 2026-08-25 from conversation with @founder.

## What the founder asked for

The founder: the platform should be self-aware. It already has all the maps
and internal state to answer any question about itself — think of all the
tool calls and tokens wasted repeating the same actions. He wants one
interface, MCP or otherwise, where an agent just queries and gets an accurate
answer back.

Design substance he pasted: one MCP server is the platform's voice. Backstage
catalog is the map (owner, repo, dependencies). Telemetry (OTel/Prometheus)
is the vitals. Flux/k8s is desired vs actual state. "Why is X down?" should
be one tool call returning structured JSON, not eight shell commands.

Four improvements, each with the failure mode he named and the fix he named:

1. Fat tools — `get_workload_state(app)` returns catalog + metrics + desired
   state in one payload. Failure: payload bloat (raw logs, timeseries) kills
   the context. Fix: summarize by default, drill on demand via a separate
   `get_workload_logs(tail=50)`.
2. Schema-first — the server reads typed `catalog-info.yaml` annotations,
   never string-greps. Failure: "dark matter" — resources applied outside the
   catalog are invisible. Fix: `get_catalog_drift()` compares catalog vs live
   state and lists untracked resources.
3. Event push, not poll — state changes push to a bus the agent subscribes
   to. Failure: alert storms flood the agent's context and cause reaction
   loops. Fix: debounce/aggregate behind Temporal; 50 crashes in 10s arrive
   as one `cascading_failure` event.
4. Split `propose_action()` from `execute_action()` — agent proposes, founder
   approves from the phone. Failure: TOCTOU, the cluster changed between
   proposal and approval. Fix: the proposal carries a state hash; execute
   refuses if the current hash differs and forces re-evaluation.

This EXTENDS the estate MCP server that already exists in `idp/mcp/`
(agentgateway.yaml + estate-mcp.Dockerfile, live as
`mcp__estate__{list_databases,get_database_schema,execute_sql}`). It does not
stand up a second MCP server, a second gateway, or a second event bus — new
tools are new routes/targets behind the one Agentgateway. Improvement 4 lands
on the existing Sovereign Bus (crew#213: Temporal, `bin/sb`, approve/deny
signals, signed receipt chain, Otto Telegram plugin) — that is already the
propose/approve path and the existing event buffer; the state hash goes into
the signed receipt it already writes. The "map" the fat tool reads is
Backstage catalog plus `catalog/ports.yaml`; the vitals come from OTel/
Prometheus per the fortress stack (crew#180); "desired vs actual" on the
laptop substrate (Fly destroyed, OKE not live) is launchd job state and
colima container state standing in for k8s until a cluster exists. The tool
should read `crew/STATE.md` (the hourly, prose-free estate snapshot) rather
than re-measuring the estate itself, to attack the exact waste he named:
repeated tool calls and tokens re-deriving facts the estate already knows.

  from `crew/STATE.md` + the Backstage catalog in one MCP call, no shell-out.
  one JSON payload, summarized by default, under a proven byte ceiling
  (property test over many app sizes).
  fat tool never inlines raw logs or raw timeseries.
  entries against live launchd jobs, colima containers and `catalog/
  ports.yaml`, and lists every resource running but uncataloged.
  identical failure events in T seconds collapse to one `cascading_failure`
  event delivered to the agent, proven by a storm test.
  state hash in the signed receipt; `execute_action()` refuses and forces
  re-evaluation when the live hash no longer matches the proposal's hash
  (TOCTOU test: mutate state between propose and execute, expect refusal).
  tokens for three recurring questions before this MCP surface existed and
  after, and prints both numbers, so the waste he named is a measured number
  and not a claim.
  desired-vs-actual source. Deferred until a cluster exists (OKE is planned,
  not live); this checkpoint is a stub proving the interface the adapter
  will implement, not a live cluster call.

## Checkpoints

### CP1: an inventory tool answers "what is the estate, and what does it run"

Verified by `@pytest.mark.cp1` in `checkpoints/`.

### CP2: `get_workload_state(app)` returns catalog + metrics + desired state as

Verified by `@pytest.mark.cp2` in `checkpoints/`.

### CP3: `get_workload_logs(app, tail=50)` is the separate drill-down tool; the

Verified by `@pytest.mark.cp3` in `checkpoints/`.

### CP4: `get_catalog_drift()` on the laptop — compares Backstage catalog

Verified by `@pytest.mark.cp4` in `checkpoints/`.

### CP5: event aggregation sits behind Temporal on the Sovereign Bus — N

Verified by `@pytest.mark.cp5` in `checkpoints/`.

### CP6: `propose_action()`/`execute_action()` on the Sovereign Bus carry a

Verified by `@pytest.mark.cp6` in `checkpoints/`.

### CP7: a token-and-tool-call receipt — a script measures tool calls and

Verified by `@pytest.mark.cp7` in `checkpoints/`.

### CP8: k8s adapter — swaps the launchd/colima stand-in for a real Flux/k8s

Verified by `@pytest.mark.cp8` in `checkpoints/`.

