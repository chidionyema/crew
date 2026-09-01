# R74 — The All-Seeing Eye: boardroom observability, mobile command, durable agents

**Founder, 2026-09-01 ~20:52–20:53Z, via an external bar-raiser consultant, approved with
"Yes".** Verbatim records in this repo:
- `docs/founder/2026-09-01T2052Z-all-seeing-eye-external-consultant-founder-yes.md`
- `docs/founder/2026-09-01T2053Z-digital-twin-uber-elite-spec-founder-verbatim.md`

He added: "see why the claude harness limits us" — the point of this build is that reading
company state never again requires a chat session to be alive. Sister ruling: R73.

## What the founder is buying (the requirements, restated before anything is judged)

1. The whole agent workforce at a glance — cost, velocity, blockages — never typing a command.
2. Mobile command: plain-English alerts with Approve / Deny buttons on his phone.
3. Durable execution: a crashed agent pauses and resumes, never fails silently.
4. A spend-velocity circuit breaker that suspends a runaway agent before money is lost.
5. Every agent thought, tool call and outcome stored as structured data — a proprietary
   training dataset that ends reliance on any one model provider (LAW 34 made physical).
6. Boardroom-grade visuals he can put in front of investors.

## The build, mapped onto the one-of-each-layer law (LAW 39: inventory first)

| Capability | The consultant named | The platform already runs | Decision |
|---|---|---|---|
| Interceptor | Langfuse | **Langfuse** (`idp/platform/oci/langfuse.tf`, router callback, chaos drill) | exists — complete it, second copy forbidden |
| Analytics store | ClickHouse / Hudi | **ClickHouse inside Langfuse v3** | exists — expose it, Hudi deferred |
| Event pipe | Redpanda / Flink | **NATS** (`idp/platform/event-bus/nats.yaml`) | exists — Flink/Redpanda deferred |
| Durable brain | Temporal | **Temporal** (`idp/platform/temporal/`) | exists (enterprise lane per the Windmill ruling) |
| Boardroom glass | Metabase / Superset | none | **BUILD: Metabase** — the smaller road (LAW 23); consultant v1 named it; linked from Backstage, which stays the one front door |
| Mobile buttons | n8n + Telegram | Hermes Telegram gateway | **BUILD: buttons on the existing gateway** — n8n would be a second workflow layer beside the ruled one |
| Circuit breaker | Flink CEP | LiteLLM router budgets (`idp/platform/llm`) | **BUILD: spend-velocity rule + suspend** on the router — the capability without the cluster |
| Training loop | Hudi → Llama fine-tune | Langfuse dataset export | deferred with a named trigger: revisit when the trace corpus passes 100k task rows |

Deferred is not rejected: each deferred piece carries the measurement that summons it
(sustained event volume, trace-corpus size). Building "for thousands of agents" before the
tenth agent exists is the half-stitched habit at boardroom scale — the buyer's engineer
boots the lakehouse and finds it empty (HEADLINE; LAW 41).

## Delivery

Agents build to green and push; the founder releases (his standing rule). Order:
1. **CP1 — the glance:** Metabase on Langfuse's ClickHouse, dashboards: spend per department,
   tasks per hour, autonomy rate, blockages; linked from Backstage; catalog entity; demo+onboarding.
2. **CP2 — the buttons:** Approve/Deny inline buttons on the Telegram gateway, wired to the
   same words R63 defined; the word and the button are one trigger.
3. **CP3 — the breaker:** router-level spend-velocity limit with bounded attempts, cool-off,
   visible open state (his circuit-breaker ruling), alert to his phone.

## Amendment, same hour: voice is in scope now

Founder, ~21:10Z: "we eed to getto our full potential" and "voice also"
(`docs/founder/2026-09-01T2110Z-full-potential-and-voice-also.md`). The CEO had deferred
voice pending a priced answer; the founder's word pulls it forward. The one answer:

4. **CP4 — the voice:** voice notes on the Telegram gateway he already carries. Whisper
   (open source) turns his spoken note into the command; Piper (open source) speaks the
   company's reply back. Both self-hosted on the platform — no new vendor, no per-minute
   fees, price is compute already paid for. Rejected: cloud voice APIs — a per-word meter
   and a provider tie, against LAW 34.
