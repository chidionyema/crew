# Fortress stack: LiteLLM, Langfuse/OTel, SPIFFE, MCP, AGENTS.md inside idp

Issue: https://github.com/chidionyema/crew/issues/180
Written by pm-agent on 2026-08-24 from conversation with @founder.

## What the founder asked for

Founder wants the estate to pass an acquirer's technical diligence on five rows,
inside the one platform (~/dev/code/idp), fixing the database first:

(1) Model routing: LiteLLM as the universal API/abstraction layer with fallback
chains and per-agent cost logging; every agent points its base URL at LiteLLM.
(2) Observability & audit: OpenTelemetry GenAI instrumentation on agent code,
routed to Langfuse, giving an immutable audit trail (cost, latency, tokens, tool
invocations) for EU AI Act. (3) Agent identity: SPIFFE/SPIRE issuing short-lived
cryptographic identities to agents as non-human identities. (4) Protocols:
official MCP Python/TypeScript SDKs replacing the proprietary board schemas;
agents reach SQLite databases and internal tools through MCP; Agentgateway
securing agent-to-tool connections. (5) Living specs: AGENTS.md as the
version-controlled boundary/rules format. All running inside docker-compose for
portability.

Full spec, measured state and the strict-bar verdicts on SPIFFE/SPIRE and
Agentgateway: `idp/docs/specs/fortress-stack.md`.

## Checkpoints

### CP1: bin/idp-verify -> last line PASS (today: FAIL, fallback serves 'none' expected 237, db has 236, HTTP 000000)

Verified by `@pytest.mark.cp1` in `checkpoints/`.

### CP2: bin/litellm-status -> proxy up, HTTP 200, real fallback chain configured, hermes-v2 and prospector base URLs both point at 127.0.0.1:4000/v1, STANDARDS row 25 CANDIDATE -> live (today: proxy down, 0 containers, importable in 0 venvs)

Verified by `@pytest.mark.cp2` in `checkpoints/`.

### CP3: bin/langfuse-status -> primary 127.0.0.1:3200 HTTP 200, one real agent trace queryable via the API with non-null cost/latency/tokens/tool-call fields, STANDARDS row 26 partially live -> live (today: primary down, only the OTel fallback answers)

Verified by `@pytest.mark.cp3` in `checkpoints/`.

### CP4: docker ps shows no spire container anywhere on the estate, and crew#78's body records the SPIFFE/SPIRE deferral to the k8s exit plus the interim per-agent-key control (today: neither exists; strict bar verdict: adopting SPIRE now on a one-node laptop estate does not raise the bar, it is a control plane attesting itself)

Verified by `@pytest.mark.cp4` in `checkpoints/`.

### CP5: an MCP server on the official SDK exposes the board and catalog/estate.db as tools, docker compose -f idp/mcp/agentgateway.yml ps shows it running, a tool call for each server round-trips through Agentgateway and returns 200 (today: MCP unimported anywhere, no Agentgateway; strict bar verdict: adopt now, standalone compose mode, scoped to fronting these MCP servers only)

Verified by `@pytest.mark.cp5` in `checkpoints/`.

### CP6: git -C idp show HEAD:AGENTS.md is non-empty and a pre-commit/CI gate reads it, shown passing and refusing in the same run (today: idp carries no AGENTS.md of its own)

Verified by `@pytest.mark.cp6` in `checkpoints/`.

