---
captured: 2026-08-24T13:55:16+00:00
session: 8dbb3e7d-68ee-49f7-82dd-b10f4fd7c22e
cwd: /Users/chidionyema
chars: 5553
source: founder prompt, verbatim (founder-doc-capture.py)
---

probe adn sudit platfron nd epxose the gaps to get to 
Where the industry is heading. What you build now to be there first.
1. The Five Forces (2026–2028)
Table
Force    Direction    Source
Inference cost collapse    API prices down 30–50% annually. Self-hosting break-even dropped from 120M to 80M tokens/month. MoE models (DeepSeek V3) now run 70B-quality on a single consumer GPU.     GigaGPU, April 2026
Agent governance gap    92% of enterprises lack visibility into agent identities. 95% doubt they could detect a compromised agent. 86–89% of agent pilots fail before production. NIST's first agent-specific deliverables not expected before late 2026.     CSA Research, April 2026
Regulatory hardening    EU AI Act enforceable August 2026. Colorado AI Act July 1, 2026. Both mandate immutable audit trails, human-in-the-loop oversight, and persistent agent identity.     FifthRow, January 2026
Standard protocol consolidation    MCP (Model Context Protocol) and A2A (Agent-to-Agent) are now the interoperability baselines. NIST targeting an AI Agent Interoperability Profile by Q4 2026.     CSA Research, April 2026
Spec-driven development    GitHub Spec Kit, OpenSpec, BMAD-METHOD emerging as standards for agent-coordinated engineering. Static specs drift within hours; "living specs" that agents execute against are winning.     Augment Code, March 2026
2. What an Acquirer Will Probe (Technical Due Diligence 2026)
From M&A practice, the four questions that determine valuation:
Can the platform scale without re-architecting core systems?
Will infrastructure costs behave predictably as usage grows?
How dependent is execution on individuals vs. repeatable systems?
Is the AI layer defensible — proprietary vs. third-party, portable, audited?
The discount triggers:
No agent inventory or audit trail → 40% valuation hit (governance = risk)
Hard dependency on one frontier API with no abstraction layer → vendor lock-in penalty
Documentation = browser tabs + session memory → not a going concern
3. The Fortress Architecture That Wins
Based on the convergence of these forces, the acquirable AI startup in 2028 looks like this:
A. The Intelligence Layer: Abstracted, Not Dependent
Model router (LiteLLM / OpenRouter pattern) with fallback chains. Primary = open-source (Llama, Mistral, Qwen). Frontier = fallback for edge cases only.
Prompt caching + batching as first-class infrastructure. Cuts costs 50–80%.
Self-hosting path proven on Mac → Oracle Free ARM → dedicated GPU. Same containers, different substrate.
B. The Agent Layer: Governed, Not Orchestrated
One human owner per workflow. Every agent has a named founder owner.
Least privilege delegation. Agents don't inherit user rights; they get per-task policies.
Immutable audit trail. Every action logged: who delegated, to whom, for what, at what cost, with what latency.
Kanban-mediated, not chat-mediated. Human approval gates before real-world actions, not after.
C. The Documentation Layer: Living, Not Static
GitHub Spec Kit or OpenSpec as the contract language. Specs version-controlled, agent-agnostic, executable.
ADR folder (docs/adr/) — every architectural decision in 6 lines: context, decision, consequences.
Runbook — one page per service: what it does, how to check health, how to kill it.
D. The Compliance Layer: Built-In, Not Bolted-On
MCP + A2A protocols for all agent-tool and agent-agent communication. No proprietary formats.
Audit logs structured for EU AI Act Article 12 (automatic recording of risk-relevant events).
Human-in-the-loop gates for high-risk outputs (Article 14).
4. What to Build Now vs. What to Wait For
Table
Build Now    Wait For
Model router with open-source primary + frontier fallback    NIST AI Agent Interoperability Profile (Q4 2026)
MCP-compliant tool interfaces for all your agents    Full SP 800-53 agent overlays (2027+)
Living spec format (Spec Kit or OpenSpec)    Enterprise governance SaaS (not needed at your scale)
Agent identity + audit trail (who, what, cost, latency)    Multi-agent orchestration platforms (overkill until you have 10+ agents)
ADR + runbook discipline    Kubernetes (Compose is your platform contract until revenue)
5. The Specific Standards to Adopt Today
Table
Standard    What It Is    Why It Matters for You
MCP    Model Context Protocol — agent-to-tool communication    Makes your tools portable across any agent. No vendor lock-in.
A2A    Agent-to-Agent protocol — peer delegation    Standardizes how your agents talk to each other. Acquirer can inspect the protocol, not your custom code.
GitHub Spec Kit    MIT-licensed spec CLI    Living specs that don't drift. Version-controlled. Agent-agnostic.
MLflow    Open-source experiment tracking    72% enterprise adoption. Proves your research is reproducible.
OpenTelemetry    Observability standard    Every agent action traced. The audit trail acquirers expect.
The Bottom Line
The industry is converging on governed, standard-protocol, spec-driven, open-source-primary AI systems. The startups that get bought are the ones who can hand an acquirer a folder with:
specs/ — living contracts
adrs/ — decision history
agents/ — MCP + A2A compliant, individually owned, fully audited
runbooks/ — one page per service
docker-compose.yml — runs on Mac today, Oracle Free tomorrow, Kubernetes when they hire DevOps
Not browser tabs. Not session memory. Not six Claude windows voting on estate-broadcast.py.
That's the fortress. That's what future-proofs you against both token cost inflation and acquirer due diligence.
What do you want to interrogate next?
