# Capability-by-capability: what the crew runs today vs what crewAI 1.9.3 ships

Founder order 2026-08-31: "I WANT A FEATURE BY FEATURE COMPARISON, YOU DONT GET TO DECIDE WHAT STAYS
AND WHAT GOES ... CAPABILITY AND I NEED SOURCES SO I CAN VERIFY." The **stays/goes column is empty —
it is yours.** Every crewAI cell was verified this session by importing the installed package
(`.venv-crewai`, crewai 1.9.3, path `.venv-crewai/lib/python3.11/site-packages/crewai`) and probing
the class fields; the probe printed each field name listed below. Docs URLs are for your own reading.
Every "ours" cell names the file and line you can open.

Coverage words: **FULL** = the mechanism exists in crewAI as shipped; **PARTIAL** = mechanism exists
but our specific behaviour needs an adapter; **NONE** = crewAI has nothing for it.

## 1. Orchestration

| capability | ours today (source) | crewAI 1.9.3 (source) | coverage | stays/goes |
|---|---|---|---|---|
| Turn a brief into a spec + board issue | `crew/crew/cli.py:104` `cmd_plan` (pm-agent) | Agent + Task with `output_pydantic` (Task field, probed; docs.crewai.com/concepts/tasks) | PARTIAL — no GitHub issue writer | |
| Claim a checkpoint | `crew/crew/cli.py:223` `cmd_claim` | Task assignment inside a Crew; no external claim ledger (docs.crewai.com/concepts/crews) | PARTIAL | |
| Post evidence, never tick the box | `crew/crew/cli.py:241` `cmd_evidence` | Task `callback` field (probed; docs.crewai.com/concepts/tasks) | PARTIAL — callback exists, GitHub posting is ours | |
| Independent verify ticks the box | `crew/crew/cli.py:270` `cmd_verify` + `crew/crew/bdd.py:107` feature-file lookup | Task `guardrail` field (probed) validates output; no BDD runner (docs.crewai.com/concepts/tasks#task-guardrails) | PARTIAL | |
| Board state parse/render (three boxes, blockers) | `crew/crew/board.py:93` `parse`, `:119` `render`, `:53` `tick` | none — no issue-board model | NONE | |
| Role charters | `crew/roles/*.md` (4 files, 301 lines) | `Agent(role, goal, backstory)` fields (probed; docs.crewai.com/concepts/agents) | FULL | |
| Manager over workers (Otto) | Otto = a session + checkpoints on crew#717, no code | `Process.hierarchical` + `manager_agent`/`manager_llm` Crew fields (probed; docs.crewai.com/concepts/processes) | FULL | |
| Sequential pipelines | `bin/crew` loop order, prose in CREW_ORCHESTRATION_SPEC.md | `Process.sequential` (probed values: sequential, hierarchical) | FULL | |
| Conditional / branching work | not built (sessions improvise) | `ConditionalTask` (import ok, probed; docs.crewai.com/concepts/conditional-tasks); `Flow` with `@start/@listen/@router/or_/and_/persist` (module `crewai.flow`, probed) | FULL | |
| Delegation between agents | feed OVERLAP lines + human habit | Agent `allow_delegation` field (probed) | FULL | |
| Human approval step | founder APPROVE words, enforced by reply guards | Task `human_input` field (probed; docs.crewai.com/how-to/human-input-on-execution) | PARTIAL — theirs is CLI prompt, ours is board word | |
| Cross-SESSION coordination (lanes, overlap, handoffs) | `~/.claude/scripts/feed-guard.py` (428 lines) + `~/.estate/feed.md` (12,341 lines) | none — coordination is inside one process only | NONE | |
| Task graph across sessions | `~/.claude/scripts/goal_graph.py` (1,657 lines) | `Flow` state machine, single process (docs.crewai.com/concepts/flows) | PARTIAL | |
| Batch same task over inputs | not built | `Crew.kickoff_for_each` / `kickoff_async` (methods probed True) | FULL | |

## 2. Memory & knowledge

| capability | ours today (source) | crewAI 1.9.3 (source) | coverage | stays/goes |
|---|---|---|---|---|
| Durable facts across sessions | 99 files in `~/.claude/projects/.../memory/` + `memory-loop.py` (749 lines) | `LongTermMemory` (import ok; docs.crewai.com/concepts/memory) | PARTIAL — theirs is SQLite auto-summary, ours is curated files | |
| In-run working memory | context window only | `ShortTermMemory` + `EntityMemory` (imports ok) | FULL | |
| Bring rulings to every session | `friction-relay.py` (515 lines) SessionStart hook | `ExternalMemory` (import ok) + `knowledge_sources` on Crew and Agent (fields probed) | PARTIAL | |
| RAG over docs/runbooks | not built (grep by hand) | `Knowledge` + `embedder` Crew field (import + field probed; docs.crewai.com/concepts/knowledge) | FULL | |
| Founder doc capture on arrival | `founder-doc-capture.py` UserPromptSubmit hook | none | NONE | |

## 3. Guards & policy (the 30,328-line harness)

| capability | ours today (source) | crewAI 1.9.3 (source) | coverage | stays/goes |
|---|---|---|---|---|
| Block dangerous commands pre-execution | `rule-guard.py` (1,452 lines), 10 PreToolUse wires in `~/.claude/settings.json` | none — no tool-call interceptor policy engine | NONE | |
| Reply-shape enforcement (DONE means founder receipt) | `dod-guard.py` (202 lines), Stop hook | none | NONE | |
| Output validation per task | same reply guards | Task/Agent `guardrail` fields (probed) | PARTIAL — theirs validates task output, not replies to you | |
| Secret scrub before display | `secret-scrub.py` + `credential-guard.py` hooks | none | NONE | |
| Mistake → permanent regression test | 45 `test_incident_*.py` in `~/.claude/scripts/` | none | NONE | |
| Policy-as-code evaluation | `opa-hook.py` (Stop + PreToolUse) | none | NONE | |
| Agent identity/audit stamp | none | `Fingerprint` (import ok; docs.crewai.com/concepts/security-fingerprints) | crewAI-only gain | |
| Sandboxed code execution | none (sessions run on the Mac) | Agent `allow_code_execution` field, Docker-backed (probed) | crewAI-only gain | |

## 4. LLM plumbing & observability

| capability | ours today (source) | crewAI 1.9.3 (source) | coverage | stays/goes |
|---|---|---|---|---|
| Model routing through one router | LiteLLM at `https://llm.<zone>` (idp platform/llm), lanes incl. claude, claude-fast, embed | `LLM` class takes any LiteLLM model string + base_url (docs.crewai.com/concepts/llms) | FULL — plugs into our router | |
| Second-brand models (kimi, deepseek) | `kimi_bridge.py` daemons, 2 launchd jobs | same `LLM` class via router lane | FULL | |
| Tracing per run | Langfuse via router `litellm_trace_id` (science lane wiring) | event bus `crewai.events` (import ok) + LiteLLM callbacks | FULL — same router carries it | |
| Token/spend metering + cap | `feed_meter.py`, `token-audit.py`, `~/.estate/spend-cap.cache.json` | `usage_metrics` Crew field (probed) — per-run only, no cap | PARTIAL | |
| Rate/iteration caps per agent | Level-10 governor prose in `~/.claude.md` | `max_rpm`, `max_iter` fields on Agent/Crew (probed) | FULL | |
| Prompt/plan improvement loop | none | `Crew.train` / `Crew.test` / `planning` field (all probed True; docs.crewai.com/concepts/training, /testing, /planning) | crewAI-only gain | |
| Replay a failed run from a task | none (re-run by hand) | `Crew.replay` (probed True; docs.crewai.com/concepts/cli#replay) | crewAI-only gain | |
| Response cache | none | `cache` Crew field (probed) | crewAI-only gain | |
| MCP tool servers | idp platform/mcp + estate MCP | `crewai-tools` MCPServerAdapter — **NOT INSTALLED in our venv** (probe: No module named 'crewai_tools') | PARTIAL — extra package needed | |

## 5. Everything crewAI has nothing for (stays ours or dies by your word — it cannot migrate)

Scheduling (Dagster `build_warehouse_hourly` at `science/scheduler/estate_dagster/definitions.py`, Temporal launchd, 5 GitHub crons); CI gates (11 workflows, `scripts/verify.d` 19 rungs); the science warehouse (18,110 lines, 103 files); estate state probes (`estate-state-relay.py`, estate-snapshot); plain-English Vale gate; push notifications (`notify.py`, hermes Telegram); evidence archive (154 files, `docs/evidence/`); board = GitHub issues; spend cap; secret scrub; incident tests; the laws themselves.

## 6. Everything crewAI ships that we have no counterpart for (the gains on the table)

`replay`, `train`, `test`, `planning`, `cache`, `kickoff_for_each`, `kickoff_async`, `ConditionalTask`, `Flow` (start/listen/router/persist), `Fingerprint` audit identity, Docker `allow_code_execution`, `multimodal` agents (all probed on the installed package this session).

---
Probe receipt: the import-and-field probe ran in this session against
`.venv-crewai/lib/python3.11/site-packages/crewai` (version output: 1.9.3); rerun it any time:
`.venv-crewai/bin/python -c "from crewai import Crew; print(sorted(Crew.model_fields))"`.
