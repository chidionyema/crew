---
captured: 2026-08-09T22:22:31+00:00
session: 2274477d-21ea-48f4-85ed-c8a9bd7fbc66
cwd: /Users/chidionyema/Documents/code/prospector
chars: 3524
source: founder prompt, verbatim (founder-doc-capture.py)
---

Root cause found, and it's precise and fixable — not infrastructure, not the ideas being bad.

The chain, fully traced

1. Not a retrieval outage — ddg is 99.2% healthy today (1081/1090 ok), exa's 6 failures are contained by the circuit breaker, claude_cli-as-retrieval isn't even needed. Ruled out.
2. moat_ungrounded (the dominant kill gate today, 41% of all kills) fires exclusively on buyer_intent, and exclusively in the three lanes — side_hustle, smb, growth — that went live in the daemon on 5175128 (2026-08-01 21:48: "let the daemon generate startups, not just solo side-hustles"). Zero venture kills use this gate, matching venture's unbroken historical pattern.
3. Read all 30 buyer_intent: unverifiable rationales from the last 24h (store/dossiers/*.kill.json). Every single one follows the identical anti-pattern — the query pair is phrased as "<niche topic> search interest UK" / "<niche topic> low search volume niche demand" / "already offered" — literally asking a web search engine to return a page that states search-volume/demand data. That data doesn't live on indexed web pages; it lives in keyword-planner tools, app-store reviews, or paid subreddits. The system prompt's own instruction (prompts/query_gen_batched.md) is explicit: "Ground the precondition, not the pitch" — and for every other check, that's exactly what happens. For buyer_intent specifically, it isn't.
4. Why just this one check: prompts/markets/uk/query_gen_batched_exemplars.md has worked examples for payer_solvency, pain_reality, incumbency — and zero for buyer_intent. The LLM writing queries has a template to imitate for every check except the one that's now load-bearing for 12 of every 15 daemon candidates. It falls back to the literal, ungroundable "ask for the demand statistic itself" pattern.
5. This isn't a hypothesis about what a fix looks like — the fix already exists, just in the wrong file. prompts/markets/us/query_gen_batched_exemplars.md (same commit, 5fa2388, 2026-07-30, never ported to UK) has two worked buyer_intent examples, grounded correctly — in a mandatory regulatory trigger that forces the need to exist, e.g. "DMEPOS supplier enrollment surety bond requirements site:cms.gov". UK never got the equivalent. Since UK is the only market actually running (US never fires — confirmed earlier, every batch today shows markets: ['uk'] only), this gap is live on every single non-venture candidate.

What's confirmed vs. what's still to test

Confirmed: the mechanism, the missing exemplars, the exact commit and date it stopped mattering silently (queries have presumably always been weak here — it only started costing real yield once the daemon began generating at this lane mix on 08-01).

Not yet confirmed: that adding UK-grounded buyer_intent exemplars actually recovers pass rate — that's a testable prediction, not a proven fix. The move would be: write 2-3 UK exemplars in the same style (forum complaint threads, existing paid-competitor pricing pages, or a mandatory UK regulatory trigger — e.g. Section 19 permit requirements, CQC registration, FCA authorisation), then run one batch and re-measure the buyer_intent: unverifiable rate against today's 65% (30/46) baseline.

Want me to write those exemplars into prompts/markets/uk/query_gen_batched_exemplars.md now? It's a prompt-content change, not a money/identity-rail change, but it does touch every future batch's spend, so I'd rather you confirm before I edit a live prompt file.

✻ Sau yes fi quickly and cheaply and prove it works
