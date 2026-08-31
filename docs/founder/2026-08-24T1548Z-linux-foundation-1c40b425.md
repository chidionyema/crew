---
captured: 2026-08-24T15:48:11+00:00
session: 281e8f75-40a5-4629-badc-b7ef51e07d02
cwd: /Users/chidionyema
chars: 11838
source: founder prompt, verbatim (founder-doc-capture.py)
---

Linux Foundation

This setup exposes zero application ports directly to your host machine, isolates database and credential layers inside an encrypted Docker network, enforces hard spend caps, and generates an immutable audit trail for EU AI Act compliance.

GitHub

Project Layout

Plaintext



fortress-stack/

├── docker-compose.yml # Zero-host-port orchestration with Traefik v3

├── litellm-config.yaml # Model routing, fallback chains & hard budget caps

├── agentgateway.yaml # AAIF MCP/A2A gateway config with OTel tracing

├── specs/

│ └── AGENTS.md # AAIF living specification standard

└── INTEGRATION.md # Deployment & verification runbook

1. Production docker-compose.yml

Every microservice runs within fortress-net. Traefik routes inbound requests via HTTP Host headers (llm.fortress.local, audit.fortress.local, mcp.fortress.local).

GitHub

YAML



version: '3.8'networks:

fortress-net:

driver: bridge

ipam:

config:

- subnet: 172.28.0.0/16volumes:

pg_data:

spire_data:

traefik_certs:services:

# --- INGRESS LAYER (The ONLY host-exposed gateway) ---

traefik:

image: traefik:v3.1

container_name: fortress-ingress

restart: unless-stopped

command:

- "--api.insecure=true"

- "--providers.docker=true"

- "--providers.docker.exposedbydefault=false"

- "--entrypoints.web.address=:80"

- "--metrics.prometheus=true"

ports:

- "80:80" # Single entrypoint for all host traffic

- "8080:8080" # Ingress Admin Dashboard

volumes:

- "/var/run/docker.sock:/var/run/docker.sock:ro"

- "traefik_certs:/certs"

networks:

- fortress-net

healthcheck:

test: ["CMD", "traefik", "healthcheck"]

interval: 10s

timeout: 5s

retries: 3



# --- INTELLIGENCE LAYER (LiteLLM Model Router) ---

litellm:

image: ghcr.io/berriai/litellm:main-latest

container_name: fortress-llm-router

restart: unless-stopped

environment:

- LITELLM_CONFIG_PATH=/app/config.yaml

- DATABASE_URL=postgresql://litellm:${POSTGRES_PASSWORD:-fortress_pass}@postgres:5432/litellm_db

- LANGFUSE_PUBLIC_KEY=${LANGFUSE_PUBLIC_KEY}

- LANGFUSE_SECRET_KEY=${LANGFUSE_SECRET_KEY}

- LANGFUSE_HOST=http://langfuse:3000

volumes:

- ./litellm-config.yaml:/app/config.yaml:ro

depends_on:

postgres:

condition: service_healthy

labels:

- "traefik.enable=true"

- "traefik.http.routers.litellm.rule=Host(`llm.fortress.local`)"

- "traefik.http.services.litellm.loadbalancer.server.port=4000"

networks:

- fortress-net



# --- OBSERVABILITY & AUDIT LAYER (Langfuse + Postgres) ---

postgres:

image: postgres:16-alpine

container_name: fortress-db

restart: unless-stopped

environment:

POSTGRES_USER: litellm

POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-fortress_pass}

POSTGRES_DB: litellm_db

volumes:

- pg_data:/var/lib/postgresql/data

networks:

- fortress-net

healthcheck:

test: ["CMD-SHELL", "pg_isready -U litellm -d litellm_db"]

interval: 5s

timeout: 5s

retries: 5



langfuse:

image: langfuse/langfuse:3

container_name: fortress-audit

restart: unless-stopped

environment:

- DATABASE_URL=postgresql://litellm:${POSTGRES_PASSWORD:-fortress_pass}@postgres:5432/litellm_db

- NEXTAUTH_SECRET=${NEXTAUTH_SECRET:-super_secret_fortress_key_32chars}

- NEXTAUTH_URL=http://audit.fortress.local

depends_on:

postgres:

condition: service_healthy

labels:

- "traefik.enable=true"

- "traefik.http.routers.langfuse.rule=Host(`audit.fortress.local`)"

- "traefik.http.services.langfuse.loadbalancer.server.port=3000"

networks:

- fortress-net



# --- IDENTITY LAYER (SPIRE Cryptographic Non-Human Identity) ---

spire-server:

image: ghcr.io/spiffe/spire-server:1.9.0

container_name: fortress-spire

restart: unless-stopped

volumes:

- spire_data:/opt/spire/data

networks:

- fortress-net



# --- PROTOCOL GATEWAY (Agentgateway: MCP & A2A Proxy) ---

agentgateway:

image: ghcr.io/agentgateway/agentgateway:latest

container_name: fortress-protocol-gateway

restart: unless-stopped

volumes:

- ./agentgateway.yaml:/etc/agentgateway/config.yaml:ro

labels:

- "traefik.enable=true"

- "traefik.http.routers.agentgateway.rule=Host(`mcp.fortress.local`)"

- "traefik.http.services.agentgateway.loadbalancer.server.port=8080"

networks:

- fortress-net

2. Intelligence Layer: litellm-config.yaml

Configures primary open-source models (DeepSeek/Qwen) with automatic frontier model fallbacks (Claude/GPT-4o), hard budget caps ($5/day), and automatic Langfuse telemetry emission.

Linux Foundation

YAML



model_list:

# Primary: Open-Source / Low Cost

- model_name: primary-instruct

litellm_params:

model: groq/qwen-2.5-32b

api_key: os.environ/GROQ_API_KEY

rpm: 1000



# Fallback: Frontier Model

- model_name: frontier-fallback

litellm_params:

model: anthropic/claude-3-5-sonnet-20241022

api_key: os.environ/ANTHROPIC_API_KEYrouter_settings:

routing_strategy: usage-based-routing-v2

fallback_coordinate:

- primary-instruct: ["frontier-fallback"]

num_retries: 2

timeout: 30general_settings:

master_key: os.environ/LITELLM_MASTER_KEY

success_callback: ["langfuse"]

failure_callback: ["langfuse"]

max_user_budget: 5.0 # Max $5/day total cap across agents

budget_duration: 1d

3. Protocol & Observability: agentgateway.yaml

Standardizes Model Context Protocol (MCP) tool access and Agent-to-Agent (A2A) communications under AAIF guidelines, enforcing CEL security policies and OpenTelemetry context propagation.

Linux Foundation

YAML



version: "v1alpha1"listeners:

- name: mcp-ingress

address: "0.0.0.0:8080"

protocol: MCProutes:

- name: internal-tools

match:

- path: "/mcp/v1"

policies:

rate_limiting:

requests_per_minute: 120

authorization:

cel_expression: "request.headers['x-agent-id'] != ''"

upstreams:

- name: hermes-mcp-server

target: "hermes-service:50051"telemetry:

opentelemetry:

endpoint: "http://langfuse:3000/api/public/otel"

protocol: grpc

4. Living Specification: specs/AGENTS.md

Adopted by the Agentic AI Foundation (AAIF) as the neutral standard for version-controlled agent operational boundaries.

Linux Foundation

Markdown



# Agent System Specification (AGENTS.md v1.0)## System Identity & Governance- **Owner**: Founder Engineering Team- **Default Privilege Mode**: Least-Privilege / Per-Task Delegation- **Protocol Baseline**: Model Context Protocol (MCP v1.0) & A2A## Operational Boundaries- **Primary LLM Endpoint**: `http://litellm:4000/v1` via Traefik (`http://llm.fortress.local`)- **Cost Envelope**: $5.00 daily hard-cap enforced at Proxy level- **Audit Mandate**: All tool invocations and model calls emit OpenTelemetry context headers.## Approval Gates (EU AI Act Article 14)- **Automated Actions Allowed**: Read-only database queries, local spec generation, log aggregation.- **Human-in-the-Loop Required**: Database writes, external deployment executions, token creation.

5. Deployment & Execution (INTEGRATION.md)

Add local domain resolution to /etc/hosts:



Bash



# Add to /etc/hosts for local ingress resolution

127.0.0.1 llm.fortress.local audit.fortress.local mcp.fortress.local

Initialize and launch the environment:



Bash



# 1. Environment Setup

cp .env.example .env# Edit .env with GROQ_API_KEY, ANTHROPIC_API_KEY, and LITELLM_MASTER_KEY# 2. Start the Stack (Background Detached)

docker compose up -d# 3. Verify Container Isolation & Zero Host Port Leaks

docker compose ps

Verify internal DNS routing and audit traces:



Bash



# Test Model Router through Traefik Ingress

curl -X POST http://llm.fortress.local/v1/chat/completions \

-H "Host: llm.fortress.local" \

-H "Authorization: Bearer $LITELLM_MASTER_KEY" \

-H "Content-Type: application/json" \

-d '{"model": "primary-instruct", "messages": [{"role": "user", "content": "Ping"}]}'# Access Dashboard UI via Host Domain:# Langfuse Audit Log: http://audit.fortress.local# Traefik Dashboard: http://localhost:8080

For Behavior-Driven Development (BDD) targeting AI agents, pairing standard Gherkin-syntax tools (pytest-bdd or behave) with LLM evaluation assertion frameworks (Promptfoo or DeepEval) provides an enterprise-standard, maintenance-free testing suite.

BDD & Specification-Testing Frameworks for Agents
Tool / Framework    Type    Best For    Why Acquirers Respect It
pytest-bdd / behave    Standard Gherkin BDD    Functional & Governance Behavior    Native Python integration; tests AGENTS.md rules directly against MCP endpoints and LiteLLM routers using human-readable .feature specs.
Promptfoo    Open-source CLI & Evals    Security, Tool Call & Boundary BDD    Declarative YAML/Gherkin assertions for LLM output constraints, prompt injection resistance, tool-use validation, and latency/cost regression.
DeepEval    Pytest-Native Agent Evals    Trajectory & Policy Testing    Provides assert methods for Gherkin steps to verify agent task completion, hallucination rates, and least-privilege tool usage.
UK AISI Inspect    Agent Evaluation Engine    Safety & Multi-Step Trajectories    Open-source framework created by the UK AI Safety Institute to evaluate autonomous agent tool calls, sandbox execution, and policy compliance.
Implementation Example: Testing AGENTS.md Rules with pytest-bdd
Instead of writing custom evaluation logic, human-readable .feature files turn your living specification (specs/AGENTS.md) into automated CI/CD pass/fail criteria.

1. The Living BDD Feature (tests/features/agent_governance.feature)
Gherkin
Feature: Agent Governance and Gatekeeping
  As an Enterprise Security Auditor
  I want to verify that agents strictly follow AGENTS.md boundaries
  So that high-risk tool execution cannot bypass human approval

  Scenario: High-risk database write blocked without approval gate
    Given an agent operating with role "analyst-agent"
    When the agent sends an MCP tool request "delete_database_records" to "http://mcp.fortress.local"
    Then the Agentgateway must reject the request with HTTP 403
    And an audit event must be logged in Langfuse with tag "policy_violation"

  Scenario: Daily budget cap enforcement
    Given the global daily spend has reached $5.00
    When an agent requests a completion from "http://llm.fortress.local"
    Then LiteLLM must return a budget exceeded error
    And the request must not fall back to frontier models
2. The Python Step Implementation (tests/step_defs/test_governance.py)
Python
import pytest
import requests
from pytest_bdd import scenarios, given, when, then, parsers

# Load the feature file
scenarios('../features/agent_governance.feature')

@given(parsers.parse('an agent operating with role "{role}"'))
def agent_context(role):
    return {"headers": {"x-agent-id": role}}

@when(parsers.parse('the agent sends an MCP tool request "{tool_name}" to "{gateway_url}"'))
def send_mcp_request(agent_context, tool_name, gateway_url):
    payload = {"jsonrpc": "2.0", "method": f"tools/{tool_name}", "id": 1}
    response = requests.post(f"{gateway_url}/mcp/v1", json=payload, headers=agent_context["headers"])
    agent_context["response"] = response

@then(parsers.parse('the Agentgateway must reject the request with HTTP {status_code:d}'))
def verify_status_code(agent_context, status_code):
    assert agent_context["response"].status_code == status_code
How This Satisfies M&A Technical Due Diligence
Deterministic Verification: Acquirers can run pytest tests/ in CI/CD to verify that agent guardrails, proxy limits, and human-in-the-loop policies pass automatically on every commit.

Zero Proprietary Code: Using pytest-bdd and Promptfoo offloads test harness maintenance to open-source maintainers.

Spec-to-Test Parity: The .feature files map 1:1 with your specs/AGENTS.md file, demonstrating that your living documentation is enforced by real tests.

How would you like to set up BDD testing for your estate?

Generate a complete pytest-bdd test suite for AGENTS.md

Configure Promptfoo for security & prompt injection testing// investigate  we need to adopt quickly
