# Demo infrastructure: the research and the one answer (founder order 2026-09-01, crew#805)

Founder, verbatim (claude-estate `docs/founder/2026-09-01T2221Z` and `...T22xxZ-own-elite-demo-infrastructure.md`):
"we need demo infrastructure not claude code — our own standardised demo needs to be elite.
research the web, we have a lot to demo to investors and buyers."

Two web-research lanes ran 2026-09-01 (sources linked throughout; every claim carries its URL).

## Lane 1 — the paid demo-platform market, measured and rejected

| Product | What it makes | 2026 price | Self-hostable? |
|---|---|---|---|
| Arcade | simulated clickable demo | free (3) → $32/user/mo → $297.50/mo | no |
| Navattic | simulated clickable demo | free (1) → $125 → $500 → $1,000/mo, sales-gated | no |
| Storylane | simulated clickable demo | free (1) → $40 → $500/mo (5-seat min) → $1,200/mo | no |
| Supademo | simulated demo + replicas | free (5, branded) → $39/user/mo → $149/user/mo | no |
| Walnut / Reprise / Demostack / Saleo | enterprise sales-demo suites | $20k–$50k+/yr, sales-led | no |
| Guideflow | simulated clickable demo | free → $40 → $599 → $1,799/mo | no |
| Floik | simulated demo + video | free tier, <$130/mo | unclear |
| Stepshots (runner-up) | screenshot-stitched demo, OSS capture CLI | CLI free; hosting ~€19/mo | capture yes, artifact no |

Sources: arcade.software/post/arcade-pricing · getsmartcue.com/blog/navattic-pricing-2026 ·
supademo.com/blog/storylane-pricing · getsmartcue.com/blog/supademo-pricing-2026 ·
getsmartcue.com/blog/walnut-full-pricing-2026 · coldiq.com/blog/guideflow-pricing ·
naoma.ai/en/blog/best-demo-automation-platforms · stepshots.com/cli

**Why the whole category loses:** every one of these produces a *facsimile* — a screenshot-stitched
simulation of the UI. That is exactly what a buyer's adversarial engineer takes apart in one
sitting: it is discoverably not the real system. The cost curve also breaks the estate's
$150/month ceiling at every serious tier. ("LiveDemo"/livedemo.ai claims to be an open-source
alternative; two independent searches found no repository, licence or self-host docs — not
evidence, not used.)

## Lane 2 — what elite developer-facing companies actually do

None of Stripe, Temporal, HashiCorp or Supabase use a simulated-demo builder. The pattern is two
things, everywhere:

1. **The real product, live, time-boxed.** HashiCorp's Terraform Sandbox: free, no signup,
   in-browser, real Terraform, expires after 1 hour (developer.hashicorp.com/terraform/sandbox).
   Stripe: the real product in test mode (docs.stripe.com/stripe-apps/enable-sandbox-support).
2. **Recorded video plus runnable open-source code.** Temporal: live-coding recordings + example
   repos a buyer clones and runs (temporal.io/resources/on-demand/demo-failure-handling).
   Supabase: real example repos on CodeSandbox (codesandbox.io/examples/package/supabase).

## The one answer: the Demo Standard, three tiers, $0 recurring

**Tier 1 — every feature ships a recorded demo that is code.**
CLI features: a VHS `.tape` file (charmbracelet/vhs, MIT, 20.8k stars, official CI action) in the
same change as the feature; CI replays it and renders MP4/GIF. UI features: a Playwright
`*.demo.spec.ts` using Playwright's own video + trace capture (Microsoft-maintained, already our
e2e tool). Rendered artifacts are committed under `docs/demos/`; the tape/script is the source of
truth. A scheduled drift job re-renders and fails red if the demo no longer matches the software —
a demo cannot lie. Rejected: asciinema+agg (recorded session, not a checked-in script — drifts
silently); playwright-recast (57 stars, one maintainer — too thin for diligence).

**Tier 2 — one surface, the portal.** TechDocs is mkdocs-material; the maintainers' answer is a
plain HTML5 video tag pointing at the committed file (github.com/squidfunk/mkdocs-material/
discussions/3984; iframes are sanitised away, github.com/backstage/backstage/issues/11537). Each
demo page has one standard shape: what it proves, the watchable demo, the command a buyer can run
himself. R66 Telegram pin on release, unchanged.

**Tier 3 — the buyer clicks the real thing.** A time-boxed sandbox in the HashiCorp shape: a
vCluster (Apache 2.0, OSS mode — vcluster.com/docs/vcluster/introduction/oss-vs-free) spun up
inside the existing cluster, Flux reconciles the demo manifests in, fixed demo data seeds it, a
scoped URL lives for 60 minutes, then it is torn down. Seconds to start, nothing survives to
accrue cost. Rejected: Okteto (per-environment pricing the ceiling has no room for).

**Everything runs in CI or on the cluster; nothing on the founder's Mac. New recurring cost: $0.**

## Checkpoints (build waits on the founder's word: GO: demo-stack)

- [ ] CP1 decision record in idp docs/decisions/ (this design)
- [ ] CP2 VHS + Playwright render jobs in CI; first tape = the intent compiler (crew#804)
- [ ] CP3 ship-gate extension: a feature push without a watchable demo is refused; graded against
      every existing feature doc before it lands (new-gate rule)
- [ ] CP4 TechDocs demo pages live; R66 pin flow
- [ ] CP5 the 60-minute sandbox (vCluster + seed data + expiring URL)
- [ ] CP6 backfill: every existing docs/demo/*.md gains its watchable demo
