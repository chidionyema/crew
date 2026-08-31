---
captured: 2026-08-06T14:09:35+00:00
session: 3f136c3c-7200-46f4-8706-340bb78a7c92
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2715
source: founder prompt, verbatim (founder-doc-capture.py)
---

need to reslve conflict and ship 
  Read 1 file

Done. Summary:

Root cause (proven, not hypothesis). The intermittent production 503 was the API refusing our own storefront. RateLimitPolicy.cs:45 partitions the limiter on client IP, which is the real visitor only for fetches the browser makes directly. A server-rendered page arrives as a fresh connection from the storefront's own egress with no X-Forwarded-For, so all SSR traffic site-wide shared one 120/min bucket (RateLimitPolicy.cs:23). At two API calls per pack view (pack/[id].tsx:1083-1086), the storefront throttled itself at roughly 60 page views a minute, and pack/[id].tsx:1112-1118 renders any non-404/410 as 503 + Retry-After: 60.

The decisive line, from Fly logs at exactly the three test-failure timestamps:
13:53:56Z Error fetching pack details: Error [ApiError] ... status: 429

This kills the wake hypothesis in the handoff. Forcing a request onto a fully stopped app booted it and served a correct 404; the failing tests are 27/28/29, the last three of a 28-test sequential run, ~18s after the machines were warm with 25 tests already passed. It was cumulative request count, never machine state. Your own measurements were consistent with this all along — curling from your IP is a different bucket, which is why it showed a clean 404.

Fix applied, as you directed: RateLimiting__PermitPerMinute=600 set as a Fly secret on prospector-store-api. Rolling restart healthy (1/1), /catalog 200 at t+6s, withdrawn ids still 404.

Verified: re-ran the live smoke — 28 passed, conclusion success, all three withdrawn-pack tests green. Only change was 120 → 600.

Documented in three places: a blind-spot note on RateLimitPolicy.cs where the default lives, a checkpoint at 2026-08-06-withdrawn-pack-503-root-cause.md with a pointer appended to LATEST.md, and a memory file indexed in MEMORY.md.

Two things you should know:

1. The code comment is uncommitted, deliberately. The checkout is mid-merge — .git/MERGE_HEAD present, 11 conflicted paths from the drain session's origin/main → wip/split-v2 merge. git commit --only refuses during a merge, and a bare commit would have swept their conflicted merge into mine. The one-line command to land it afterwards is in the checkpoint. The live mitigation doesn't depend on it.
2. This raised the ceiling, it didn't remove it. The budget is still spent site-wide rather than per visitor, so ~300 page views/min is the new self-throttle point, and the failure mode is still a 503 error page for a real buyer. The structural fix needs the storefront to forward the visitor IP — worth noting that reading Fly-Client-IP API-side is not that fix, since on an SSR call that header is the storefront itself.
