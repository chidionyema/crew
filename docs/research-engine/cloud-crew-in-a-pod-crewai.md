# Research: Cloud Crew in a Pod Using CrewAI

**Date:** 2026-09-01  
**Researcher:** estate-agents[bot]  
**Status:** RESEARCH — findings only; no build, no deploy

## The Founder's Ask

Run a cloud crew in its own pod on the production cluster like Otto, using CrewAI as the framework.

## What Already Exists

The crew redesign on CrewAI (docs/plans/2026-08-31-crew-redesign-on-crewai.md) frames the gaps and proposes CrewAI as the orchestration engine. The capability-by-capability map (docs/plans/2026-08-31-crew-vs-crewai-capability-map.md) shows CrewAI covers the full orchestration layer: crews, tasks, processes, memory, knowledge, training and replay. The surface map (docs/plans/2026-08-31-crew-surface-map.md) lists the work items; the custom-builds audit (docs/audit/2026-08-31-custom-builds.md) identifies creeds to fold into CrewAI. The R72 bake-off (docs/rulings/R72-two-harnesses-goose-and-our-own-bake-off.md) documents that Goose is a harness (execution loop + tool sandboxing), while CrewAI is an orchestration framework — different layers; both are adopted for different work.

Otto runs on the Mac today as a Telegram card renderer (sovereign/otto/README.md); the founder has approved Otto as the manager role in the CrewAI redesign, to coordinate department crews. No pod manifest for Otto exists yet — that is a follow-on build.

## CrewAI Platform Findings

### Open-Source Framework

CrewAI is distributed under MIT licence with a mature feature set as of version 1.9.3:

- **Crews, Tasks, Processes:** Role-based agent orchestration with sequential and hierarchical process types (sources: docs.crewai.com/concepts/crews, tasks, processes).
- **Flows:** State machine DAG language for conditional routing and parallel work (docs.crewai.com/concepts/flows).
- **Memory:** Short-term, long-term, and entity memory backed by pluggable stores (docs.crewai.com/concepts/memory).
- **Knowledge:** Retrieval-augmented generation over embedded documents (docs.crewai.com/concepts/knowledge).
- **Training, Testing, Replay:** Built-in methods to improve prompts, validate outputs, and replay failed runs from a checkpoint (docs.crewai.com/concepts/training, testing).
- **Model-Agnostic LLM Interface:** Accepts any LiteLLM model string and base_url, plugging directly into our router at `llm.<ESTATE_ZONE>` (docs.crewai.com/concepts/llms).

### CrewAI AMP (Hosted Platform)

CrewAI offers a managed platform called AMP with the following characteristics:

- **SaaS Offering:** Cloud-hosted execution environment with visual editor and AI copilot (sources: docs.crewai.com/en/enterprise/introduction, 2026).
- **Pricing:** Basic tier free (50 workflow executions/month); Enterprise custom-quoted with flexible overage.
- **Features:** Observability, training, triggers, guardrails, collaboration (sources: Toolworthy.ai CrewAI review, June 2026).
- **Risk:** AMP is a commercial SaaS managed by CrewAI Inc. Using it ties traces, state and execution to CrewAI's infrastructure. For a cloud crew running on the production OKE cluster, we would use the open-source framework and self-host the platform layers (Postgres, S3, Langfuse).

### Kubernetes Pod Deployment Architecture

The CrewAI production deployment guide (fast.io, 2026) and enterprise Helm chart (enterprise-docs.crewai.com) document the architecture for running CrewAI crews as long-lived Kubernetes services:

**Layers:**
1. **Orchestration** (Flows) — work definition and routing.
2. **Execution** (Crews, Agents) — the multi-agent workers.
3. **Persistence** (PostgreSQL, S3) — state and artifact storage.
4. **Observability** (LangSmith, Langfuse) — traces and metrics.

**Pod Specification (from production deployments, 2026):**
- **Replicas:** 3 for high availability across zones.
- **Resource Requests:** 100m CPU, 256Mi memory per container (conservative); production typically runs 1-6 CPU and 6-12GB memory per pod.
- **Auto-Scaling:** HorizontalPodAutoscaler on CPU utilization (70% threshold recommended).
- **State Management:** External Postgres (connection pooling via PgBouncer), S3-compatible object store, Redis for session state.
- **Networking:** Ingress controller (NGINX, Istio, AWS ALB) with TLS, explicit NetworkPolicy for segmentation, ServiceAccount with minimized RBAC.
- **Health Checks:** Liveness and readiness probes on `/health` endpoint.

**Container Image:** Dockerfile with pinned `crewai==1.9.3` via pip or UV, entrypoint as Python ASGI server (uvicorn) or CLI runner depending on workload type.

### Production Readiness Checklist (Shakudo, 2026)

Deploying AI agents on Kubernetes requires:
1. **RBAC & ServiceAccounts** — dedicated identity per workload, no privilege creep.
2. **Secrets Management** — external vault (OCI Vault via ESO in our stack), never hardcoded; rotation on short cycles.
3. **Network Policies** — explicit segmentation, no default allow.
4. **Human-in-the-Loop Approval** — founder APPROVE words for state-changing actions (already law LAW 47).
5. **Observability** — traces + metrics + decision logs; Langfuse for traces, SigNoz for metrics (already in platform).
6. **GitOps** — agent definitions in git, kustomize for templating, Flux for reconciliation (already our model).
7. **Data Residency** — inference via local model or router-only calls; strip PII before external LLM calls.

## Fit Against the Laws

### LAW 1: Platform is one (one orchestrator, one memory, one knowledge base)

**Fit:** PASS. CrewAI crews run inside the platform layer, not as a second orchestrator. The existing Dagster scheduler (or Windmill if founder approves W8) remains the scheduler. CrewAI tasks are invoked by the scheduler as Python callables or via the CLI. Memory and knowledge use the same Postgres cluster and embed lane already running for the science plane (D2, D3 in the redesign plan).

### LAW 34: Provider-agnostic from day 0

**Fit:** PASS. CrewAI's LLM abstraction accepts any LiteLLM model string. All LLM calls route through `llm.<ESTATE_ZONE>` on the router; no vendor key is held by the crew pod. The framework itself is MIT-licensed open-source; no provider lock-in.

### LAW 50: Every workload emits to the central collector

**Fit:** PASS. CrewAI's event bus (`crewai.events`) and LiteLLM trace callbacks both emit to Langfuse via the router's existing trace path. SigNoz receives metrics via OTEL from the pod. The capability map confirms Langfuse tracing is FULL coverage.

### LAW 21: Secure by default

**Fit:** PASS. Secrets via ESO/OCI Vault (same as idp platform/secret-store); ServiceAccount RBAC; NetworkPolicy ingress restricted; no hardcoded credentials; model access via router key only.

### LAW 24: Everything load-bearing is in git

**Fit:** PASS. Agent definitions, crew specs, task definitions, kustomize overlays for the pod — all in git. Memory and knowledge state live in Postgres, queryable; not a local file.

## Comparisons: CrewAI vs Alternatives

### Goose (Agent Harness)

Goose (Linux Foundation Agentic AI Foundation, since April 2026) is fundamentally an **agent harness**: the execution loop around one model, tool registration and sandboxing, context management, behaviour enforcement hooks. It does not orchestrate multiple agents or workflows. R72 adopted Goose for the "cheap harness" lane where a single strong model with sandboxed tools is the right answer. CrewAI is not a replacement for Goose; they operate at different layers. A crew can use Goose-model endpoints if the router lanes them.

### LangGraph (LangChain)

LangGraph provides a lower-level state machine primitive for control flow but requires hand-rolled agent definitions and lacks built-in roles, memory, knowledge, or training primitives. For a role-based crew (engineering, security, research, operations), CrewAI's Agent, Task, and Crew abstractions require far less code than LangGraph primitives.

### AutoGen (Microsoft)

AutoGen is a conversation-based multi-agent framework, simpler than CrewAI for two-agent chats but weaker for workflows with dependencies, conditional routing, and external task state. Crew orchestration is stronger in CrewAI than in AutoGen.

The audit already found this: capability map section 1 (Orchestration) marks CrewAI FULL for the turns we need; no other framework ships that breadth without hand-rolling orchestration on top.

## Risk Assessment

**Single point of failure:** A pod running all departments (engineering, security, research, operations, audit) under one manager (Otto) means one pod crash blocks all crew work. Mitigation: replicate to 3+ pods with PodDisruptionBudget; separate department crews to separate pods (separate deployments) if high availability is critical; add a circuit breaker and manual override so the founder can pause the crew without losing the pod.

**State in a database:** Long-term memory and knowledge move from files in `~/.claude/` to Postgres rows. If the Postgres connection breaks, the crew halts. Mitigation: use connection pooling (PgBouncer), read-replica fallback, backup Postgres restores tested monthly.

**LLM routing dependency:** All model calls go through the router at `llm.<ESTATE_ZONE>`. If the router is down, no inference happens. Mitigation: already a platform risk (LAW 34 provider-agnostic means the router is the trust boundary); add health checks and circuit breaker on router availability before the crew spins a task.

## Recommendation

**Adopt CrewAI as the open-source framework layer for the cloud crew redesign, running it as three replicas in a Kubernetes Deployment on the production OKE cluster.** CrewAI provides all orchestration and memory primitives the redesign plan requires (crews, tasks, flows, memory, knowledge, training, replay); integrates with our router, Langfuse, and SigNoz; supports our provider-agnostic law; and uses the same Postgres and object store the platform already runs. The risk is orchestration complexity in a single pod cluster — mitigated by replicas, separate department deployments if needed, and circuit breakers on router/database availability.

**Alternative rejected:** CrewAI AMP (commercial SaaS) ties execution and state to CrewAI Inc.'s infrastructure — vendor lock-in (LAW 34 fails; LAW 50 evidence comes from their SaaS, not our collector). Do not use AMP; use the open-source framework on our cluster.

## Smallest Next Step (If Approved)

1. **Scope:** Build the foundation layer only (no department crews yet).
   - Postgres + S3 connectivity from a test pod (already running; probe queries work).
   - CrewAI config module reading estate-config (W0 from the redesign plan).
   - Router + Langfuse wiring so one test crew's trace lands in Langfuse and memory writes are queryable in Postgres.
   - Kustomize overlay for a CrewAI pod deployment spec (3 replicas, resource requests, liveness/readiness, RBAC).

2. **Proof:** One crew of two agents (e.g., a planner and an executor) completes a real task end-to-end. Its trace, memory write, and knowledge retrieval are each queryable in the backend.

3. **Acceptance:** Same one as step 1 of the redesign build order (crew#717 D1 acceptance test).

## Sources

- [CrewAI Framework Documentation](https://docs.crewai.com)
- [CrewAI AMP Enterprise Platform](https://docs.crewai.com/en/enterprise/introduction)
- [CrewAI Production Deployment Guide 2026](https://fast.io/resources/crewai-production-deployment/)
- [CrewAI Enterprise Kubernetes Helm Configuration](https://enterprise-docs.crewai.com/configuration/configuration)
- [How to Deploy AI Agents on Kubernetes (Shakudo, 2026)](https://www.shakudo.io/blog/deploy-ai-agents-on-kubernetes)
- [Goose Moves to Agentic AI Foundation (April 2026)](https://goose-docs.ai/blog/2026/04/07/goose-moves-to-aaif/)
- [Linux Foundation Agentic AI Foundation Announcement](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)
- [A Comparison of AI Agent Harnesses in 2026 (Winder AI)](https://winder.ai/ai-agent-harness-comparison/)
