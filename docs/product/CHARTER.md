# Product crew: charge, lenses, what exists, market, bootstrap

**Stealth until bootstrap** (founder, 2026-08-28). Private repo only. No public page, post,
listing, waitlist, domain or outreach until the founder writes `bootstrap` on the crew ticket.
Role charter: `roles/product.md`. Sibling function: `docs/research-engine/CHARTER.md` (science).

## The charge, one sentence

Turn the platform, or parts of it, into assets somebody pays for — prospector today, the hermes
personal agent as the business's future, the platform underneath as the thing a founder,
engineer or team buys — and grade every asset's commercial readiness from what runs, under two
lenses, so that a stranger with money can get from first contact to paid and served without one
of us on the call.

## Two lenses, four sub-functions, one ledger

| Lens | Buyer | Assets | Path graded |
|---|---|---|---|
| **A · sold to a founder / engineer / team** | a small engineering org (5–50 devs) buying a run-anywhere estate: catalog, identity, secrets, traces, CI, drills | `idp` (Backstage portal, `platform/*`, `clusters/*`), `claude-guards`, `crew` process | evaluate → install (portability drill receipt) → pay → support → leave with data |
| **B · customer / public facing** | UK entrepreneur (prospector); SMB owner and consumer (hermes personal agent) | `prospector-main` (dossier store), `hermes-v2` (the agent) | hear of it → sign up → pay → promised outcome → help → cancel |

| Sub-function | Owns | Ledger column | Existing agent role |
|---|---|---|---|
| Marketing | who hears of it and why they care | `channel`, `claim` | `~/.claude/agents/roles/marketing.md` |
| Sales | interested → paying | `qualify`, `objection` | `~/.claude/agents/roles/sales.md` |
| Product shaping | what is in the box, price, for whom | `sku`, `price`, `buyer` | none — this charter creates it (`roles/product.md`) |
| Development | the PR that closes a red readiness row | `fix_pr` | `~/.claude/agents/roles/engineering.md` |

One ledger, `docs/product/LEDGER.md` (CP3 generates it). Science's research ledger is linked
by row id, never copied (R37: research is a crew, science is an embedded layer — product is the
same shape).

## What exists today (measured 2026-08-28, commands in `Evidence`)

| Asset | Lens | Buyer named | Price named | Pay path | Onboarding | Readiness | Evidence |
|---|---|---|---|---|---|---|---|
| prospector dossier store | B | UK entrepreneur, franchisor payer (hypotheses, `docs/research-engine/SCALE_market_2026-08-25.md`) | £19.99–£99.99 rungs, `config.yaml:2112` `rungs: [1999, 2999, 4999, 7999, 9999]`, marked "HYPOTHESIS, not a finding" (`config.yaml:2081`) | real Stripe checkout on 11 packs, 12/12 sessions (`store/launch/checkout-proof.md`, 2026-06-20); storefront API 10/10 (`storefront-proof.md`) | store runs on OKE at mumchimp.com (memory `store-runs-on-oke-mumchimp`) | **amber**: money path proven once, 69 days old; no willingness-to-pay evidence; no help/cancel path graded | `grep -n rungs prospector-main/config.yaml`; `grep -c '^- \[x\]' prospector-main/store/launch/*.md` |
| hermes personal agent | B | none named — README sells "an engineering agent that watches your production estate" to an engineer, not an SMB owner or consumer | none; only its own run cost: WATCH $22.63/month (`hermes-v2/README.md:123`), VPS £5–15/mo (`THE-ARCHITECT.md:61`) | none — no signup, no billing, no tenant; onboarding docs are `claim-gate.md`, `verify_on_stop.md` (operator mechanics) | clone-and-run, Telegram gateway is a launchd job on the founder's Mac (memory `hermes-telegram-is-the-gateway-launchd-job`) | **red**: no buyer, no price, no pay path, single-tenant on one laptop | `grep -ril 'stripe\|billing\|signup\|tenant' hermes-v2` → config/onboarding mechanics only, 0 commercial |
| idp platform | A | none named — `docs/demo/idp-free-tier.md` exists (demo only); `docs/policy/enterprise-operating-model.md` describes the operating model, not an offer | none | none | `docs/onboarding/*`, `docs/SHOWCASE.md` (358 lines, graded per entity), portability drill (idp#648, last run red on edge/k3s) | **red for sale, amber for diligence**: 75 catalog entities, showcase graded, but no SKU, no licence, no support tier, drill not green | `find idp -name catalog-info.yaml \| wc -l` = 75 |
| marketing / sales / pm agents | — | — | — | — | `~/.claude/agents/roles/{marketing,sales,finance}.md`, `pm-agent.md` | **inventory**: role files exist, no product-shaping role, none wired to a ledger | `ls ~/.claude/agents/roles` |

Red is honest. Nothing above is a launch.

## Market facts (web research 2026-08-28, agent af13a29d; every figure with its source; `unverified` where no primary)

**Personal agents, what buyers pay today**
- Lindy $29.99 / $99.99 / $199.99 per user per month, hosted only — lindy.ai/blog/best-ai-agents
- Zapier Agents free 400 activities/mo, ~$33/mo for 1,500 — zapier.com/blog/lindy-vs-zapier
- Microsoft Copilot Business $18/user/mo promo → $21 after 2026-09-30; Copilot Studio $200/mo per 25k credits — moxo.com/blog/best-ai-agents
- Claude Pro $20, Max $100/$200, Team $25–30/seat (5 min) — suprmind.ai/hub/claude/pricing
- Google AI Pro $19.99, Ultra $99.99–$199.99 — felloai.com/gemini-pricing
- Relay.app free 100 runs, Pro $9.99, Growth $29.99 — g2.com/products/relay-app/pricing
- OpenClaw (ex-Clawdbot/Moltbot): open-source MIT, self-hosted, BYO-model, WhatsApp/Telegram/Slack — openclaw.ai; star count unverified
- Open Interpreter, n8n: open-source, self-hosted, BYO-model — contabo.com/blog/best-open-source-ai-agent-frameworks
- Band: personal-grade agents cluster at **$20–50/month**; the self-hosted tier is **£0 + BYO model key**. Hermes' measured run cost ($22.63/month on Haiku) sits inside the paid band — the margin question is CP2's first row.

**Market size (scope differs per analyst; cite one and its scope, never the spread)**
- Grand View Research: AI agents $7.63B 2025 → $10.9B 2026 → $182.97B 2033, 49.6% CAGR — grandviewresearch.com/industry-analysis/ai-agents-market-report
- MarketsandMarkets: $7.84B 2025 → $52.62B 2030, 46.3% CAGR — marketsandmarkets.com/Market-Reports/ai-agents-market-15761548.html
- Gartner $206.5B 2026 agent-software spend: secondary only, **unverified**
- SMB adoption: 55% of US small businesses used AI in 2025 (39% in 2024) — factoryjet.com/blog/ai-adoption-us-small-businesses-2026; 41% of SMB leaders piloting agents for decision support — ringly.io/blog/ai-agent-statistics-2026, publisher **unverified**

**Lens A comparables (what a team pays for a platform)**
- Roadie (managed Backstage) $22/developer/month — encore.dev/articles/backstage-alternatives
- Humanitec from ~$1,979/month, 5 users — encore.dev/articles/platform-engineering-tools
- Port.io $100M Series C at $800M, 2025-12-11 — techcrunch.com/2025/12/11/port-raises-100m-at-800m-valuation-to-take-on-spotifys-backstage
- Cortex $35M Series B 2023, no 2025–26 round found — techcrunch.com/2023/05/31/cortex-raises-35m-series-b-for-its-internal-developer-portal
- No 2025–26 acquisition of Roadie, Cortex or Humanitec found.

**What a buyer's engineer asks for (diligence rows; the platform's readiness scorecard uses these as columns)**
SOC 2 or equivalent attestation; ARR and cohort retention over 18 months; key-person risk;
code and IP ownership incl. contractor assignment; single-model-provider dependency (LAW 34
answers this); regulatory exposure; technical documentation and scalability metrics —
qubit.capital/blog/ai-startup-due-diligence-documents-metrics, blog.promise.legal/ma-due-diligence-ai-products-checklist, fastdatascience.com/ai-due-diligence.

## Requirements attached to the platform, retrospectively (R-rows)

Every commercial requirement is a row here and a `product.bytesync.io/requirement` annotation
on the catalog entity it constrains (CP4 adds the annotation and the gate that refuses an
entity or requirement without its pair).

| Id | Requirement | Entity | Source |
|---|---|---|---|
| R-P1 | prospector price rungs backed by willingness-to-pay evidence, not a hypothesis | `prospector-store` | `config.yaml:2081`, SCALE hypothesis 1 |
| R-P2 | prospector help and cancel path exists and is walked | `prospector-store` | this charter, lens B path |
| R-H1 | hermes has a named SMB buyer and a named consumer buyer, each with a price inside the $20–50 band or a self-hosted £0+BYO tier | `hermes-v2` | market facts above |
| R-H2 | hermes multi-tenant: a second person can run it without the founder's Mac | `hermes-v2` | memory `hermes-telegram-is-the-gateway-launchd-job`, LAW 46 |
| R-H3 | hermes signup → pay → served path is commands or URLs, no step blank | `hermes-v2` | lens B path |
| R-A1 | platform has one SKU (what is in the box), a licence and a support tier | `idp` | lens A comparables |
| R-A2 | platform install path is the portability drill receipt, green | `idp` portability-drill | idp#648 |
| R-A3 | diligence columns (SOC 2 posture, IP assignment, provider dependency, docs) are graded rows, not prose | `idp` conscience | diligence list above |

## Bootstrap, in commands, in order

Done-probes are commands; a probe that cannot run is BLIND, not green.

**CP1 · Charter and role exist on main.**
`test -f roles/product.md && test -f docs/product/CHARTER.md` on `origin/main`.

**CP2 · Readiness scorecard, generated.** `bin/product-readiness` reads the prospector proof
files, the hermes tree, the idp catalog and showcase, and prints one row per asset per lens with
`green|amber|red|BLIND|stealth-held` and the reason; writes `docs/product/READINESS.md`.
Probe: `bin/product-readiness --check` exits 0 and the page has ≥ 3 asset rows, hermes rows
first; a row whose source file is missing prints BLIND (mutation test: move
`store/launch/checkout-proof.md`, expect BLIND).

**CP3 · The ledger.** `docs/product/LEDGER.md` with the four sub-function columns, one row per
R-row above, each with `fix_pr` blank or a PR number. Probe: `bin/product-readiness --ledger`
refuses a ledger row with no entity or a red readiness row with no ledger row.

**CP4 · Requirements attached to entities.** `product.bytesync.io/requirement: R-xx` annotation
on the three entities; gate in idp `policy/operating_model.rego` (or a `bin/` check called from
ci.yml) refuses a catalog entity under lens A/B with no R-row and an R-row with no entity.
Probe: `opa test policy/ -v` shows the two new cases; mutation: drop the annotation, expect deny.

**CP5 · First walk of each buyer path, recorded.** For each lens, one recorded walk (asciinema
or a proof `.md` in the shape of `checkout-proof.md`): prospector hear→cancel, hermes
sign-up→served (expected: red at sign-up — that is the finding), platform evaluate→install.
Probe: three files under `docs/product/walks/` each with a `Verdict:` line; the ledger's
`fix_pr` column non-empty for every red step. Stealth: walks use test cards and private URLs.

`bootstrap` is the founder's word on the ticket after CP5; nothing public before it.
