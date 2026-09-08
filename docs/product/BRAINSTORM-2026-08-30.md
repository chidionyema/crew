# Brainstorm 2026-08-30: capabilities we have not switched on, and what the personal and commercial agent needs

Founder ask, 2026-08-30 (crew#686): "any ideas of capabilities, preferably advanced, that exist that we have not yet enabled for our Hermes agents and our to-be-unified models; from a product perspective what features we need to add to personal agents; we want to serve the personal and commercial markets."

Two research runs, one hour, every row with a source. **The last column is the founder's**: write KEEP, TRY or DROP against a row on crew#686 and the TRY rows become tickets with a demo each (LAW 32). Evidence marks: *proven* = shipped by the vendor or verified by two publishers; *single source* = one publisher, a lead not a claim; *unverified* = not checked.

## A. Built into Hermes Agent, switched off in our estate

Evidence is the vendor tree at `hermes-v2/hermes-agent/` against our `hermes-v2/config.yaml` (version 38). Each row is a config change, not code (headline rule 1).

| # | Capability | Where it is | Why it is off | What it gives | Proof test (minutes) | Founder |
|---|---|---|---|---|---|---|
| A1 | Observability plugin: Hermes traces to Langfuse and SigNoz | `hermes-agent/plugins/observability/` | `plugins.enabled` is `[sovereign, guide]` (config.yaml:103) | Closes a LAW 50 gap a buyer's engineer finds first; every other row runs traced | one Langfuse query shows a Hermes trace (15) | |
| A2 | 19 vendor connectors: Stripe, PayPal, Square, Notion, Linear, Sentry, Datadog, Supabase, Vercel, Netlify, Figma, Asana, Atlassian, Intercom, Airtable, n8n, Hugging Face, Webflow, Comfy | `hermes-agent/optional-mcps/` | no `mcp_servers` key in config | The agent reads a customer's real systems: the commercial market in one config block | Stripe test mode + Linear, one traced call each (20) | |
| A3 | 20 more messaging surfaces: Slack, Teams, WhatsApp, Discord, Matrix, SimpleX, email, SMS, Google Chat, Mattermost, Home Assistant, ntfy and more | `hermes-agent/plugins/platforms/` | only `telegram` and `a2a` under `platforms:` (config.yaml:73) | Slack and Teams are the two a commercial buyer asks for by name | `hermes gateway setup` for Slack, one round trip (15) | |
| A4 | Browser and computer use | `hermes-agent/toolsets.py:54-59,91` | no `browser:` or `toolsets:` key | The one demo a sales room understands without explanation | one navigate-and-screenshot (10) | |
| A5 | Voice both ways: five TTS providers, inbound voice-note transcription | `cli-config.yaml.example:1316-1411` | no `tts:` key | The personal-market differentiator (see B8) | Telegram voice note in, audio out (15) | |
| A6 | Sub-agents (`delegate_task`, depth up to 2) | `cli-config.yaml.example:1472-1479` | nothing set | One agent handles a real workload in parallel instead of one long session | three-way fan-out, compare wall clock (20) | |
| A7 | Payments and finance skill packs | `hermes-agent/optional-skills/payments`, `finance` | absent from our `skills/` (25 packs, none of these) | Quote, invoice, reconcile: the difference between a chat toy and a thing with a price; pairs with A2 | Stripe test mode, confirm no live key reachable (30) | |
| A8 | Security skill pack | `hermes-agent/optional-skills/security` | absent | Pairs with the chaos drill and adversarial review lanes (crew#677) | run against one repo (20) | |
| A9 | Context engine: a structured handover on every compaction | `hermes-agent/plugins/context_engine/` | not enabled; compaction at 150k (config.yaml:125) throws context away | Turns the compression incident (crew#496) into an asset | compact one long session, read what survived (30) | |
| A10 | Kanban tools (eleven) | `toolsets.py:83-89`; `kanban.db` last written 2026-08-22 | never wired to the board | Wire it to the crew board or delete the dead surface | `kanban_list` returns rows or not (5) | |
| A11 | Self-evolution (DSPy + GEPA, MIT, ICLR 2026) | `hermes-agent-self-evolution/`, `cron/evolution.jobs` nightly 03:00 | it has run: hermes-v2#41 and #37 "evolution:" PRs on 2026-08-27; `logs/cost/evolution.txt` has no row, so cost is unmeasured | Skills improve from transcripts, as PRs the founder taps | one dated cost row per run (LAW 28) | |
| A12 | Nous Portal tool gateway: one subscription for web search, image generation, TTS and a cloud browser | `hermes-agent/README.md:124-141` | not set up | Replaces four separate keys; **but** it is a second credential root beside LiteLLM, check against R52 before adopting | `hermes portal info` after sign-in (10) | |

## B. Personal agent: features, ranked by demand evidence

| # | Feature | Kind | Evidence | Founder |
|---|---|---|---|---|
| B1 | Memory the person can read, edit and take to another model | differentiator | proven: HN threads on OpenClaw memory breaking and on git-tracked memory (news.ycombinator.com/item?id=47721955, 47783940). Ours is Hindsight (config.yaml:29); the missing part is the user-facing view | |
| B2 | "Explain what you did" receipts per action: model, tool, input, cost | strongest differentiator | proven negative demand: 1,184 malicious skills in the OpenClaw marketplace stealing keys (github.com/joylarkin/openclaw-security-news). A by-product of our own routing and trace store | |
| B3 | A sandbox and permission fence the user can see | differentiator | proven: CVE-2026-35623; HN "full-machine control is too scary" | |
| B4 | One agent on every channel | table stakes | proven: OpenClaw ships 29 channels (digitalocean.com, xtom.com). Row A3 is the switch | |
| B5 | Scheduled proactive daily brief | table stakes | proven: OpenAI folded Pulse into scheduled Tasks (datamation.com; aibusinessweekly.net Jul 2026); unscheduled proactivity was unloved | |
| B6 | Life admin: bills, birthdays, reminders, to-dos | table stakes | proven: documented daily OpenClaw use (thenuancedperspective.substack.com, techradar.com) | |
| B7 | Inbox and calendar autopilot | table stakes | proven: Pulse Gmail and Calendar connectors | |
| B8 | Voice in and out | lead | single source (HN); row A5 is the switch | |
| B9 | Setup a non-engineer survives | differentiator | proven: HN's stated reason nobody they know uses it, "takes effort to set up" | |
| B10 | Purchases with a hard limit | differentiator, demand unproven | grocery ordering documented (techradar.com); the limit is our invention; row A7 | |
| B11 | Health, weight, workout tracking | lead | single source | |
| B12 | Family sharing | unverified | no evidence found; not for a public page | |

## C. Commercial market: features, ranked

| # | Feature | Evidence | Founder |
|---|---|---|---|
| C1 | SSO and role-based access | proven: "security, SSO and audit logs decide the shortlist before accuracy" (ivern.ai, sketricgen.ai) | |
| C2 | Conversation-level audit log tied to identity, exportable | proven (same two) | |
| C3 | Self-hosted or on-premise as the qualifier | proven: cloud-only agents disqualified on sovereignty (ringlyn.com, irisagent.com) | |
| C4 | Data residency by region | proven (same) | |
| C5 | Multi-tenant workspace governance | single source (ivern.ai); readiness row "second tenant" is red (READINESS.md) | |
| C6 | SOC 2 and HIPAA posture | single source; never claimed before held | |
| C7 | Integration depth into systems not built for agents | single source; row A2 | |
| C8 | Predictable cost against Dust credits per seat and Fin per outcome | finance's call | |

## D. Positioning a self-hosted, provider-agnostic, auditable agent can own

1. **The agent that shows its work.** Every action leaves a receipt: model, tool, what it read, what it cost. The vendors' business is the black box; ours emits the receipt as a by-product (B2, A1).
2. **Your agent does not move house when the model does.** Memory and routing are yours, the model is a swappable part. Users already do this by hand with git-tracked memory; we ship it (B1, LAW 34).
3. **The same agent, personal and at work, one vendor, one audit trail.** Fin bills per resolution, Dust per seat; a small business buying both buys twice. An argument until a named customer.

## E. Pricing signals

Personal: $20/month is settled (ChatGPT Plus, Claude Pro, Google AI Pro $19.99; pricepertoken.com, sentisight.ai); power tiers $100–200. Hermes run cost is $22.63/month (READINESS.md, R-H1). Business: Dust $30 and $150 per seat (automationatlas.io, costbench.com); Fin $0.99 per resolution plus $29–139 seats (intercom.com, gleap.io); Lindy $49.99–199.99 (single source). Decagon's contract value: one second-hand source, not printed.

## F. Rejected, with the test that killed each

- **Letta or MemGPT as memory**: duplicates Hindsight (config.yaml:29); a second memory platform is the stitching the headline forbids.
- **LiveKit or Pipecat for realtime voice**: Hermes already ships TTS across five providers plus inbound transcription (A5); sub-second barge-in has no customer asking.
- **FutureAGI for evals and guardrails**: overlaps Langfuse, which runs; its distinct piece (GEPA) is already in A11.
- **Zep or Graphiti as a second memory**: a benchmark lead on one publisher (63.8% vs Mem0 49.0% on LongMemEval) is not a reason for a second memory store; revisit only if Hindsight fails a measured recall test.

## The three to do first

1. **A1**, one config line, because nothing else on this page is safe to run untraced.
2. **A2** with Stripe test mode and Linear, because it is the cheapest proof Hermes reaches a customer's real systems.
3. **A4** the browser, because it is the one demo a person understands without a word.

Stale row found on the way: `approvals.always_ask` in config.yaml still lists four `fly` commands (R1, the platform we left); remove with the A1 change.

Sources beyond those inline: hermes-agent.nousresearch.com/docs, particula.tech agent-memory comparison 2026, arcade.dev MCP gateway guide, aws.amazon.com MCP gateway and registry post.
