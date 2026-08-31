---
captured: 2026-08-29T16:20:20+00:00
session: 14ed6c8b-f0a9-40d7-82a8-895f336f9b78
cwd: /Users/chidionyema/dev/code/idp/.claude/worktrees/commerce-dark
chars: 2779
source: founder prompt, verbatim (founder-doc-capture.py)
---

Layer 1 — session hooks (32)

This layer has the worst ratio. It is also the layer that fought you this week.

Guard    Verdict    Why
sync-guard    KEEP    Deterministic git state, not prose. Cheap.
laws-link-guard    DECLARATIVE    File-shape assertion. Belongs in CI, not in every session.
peer-loop-fence    DECLARATIVE    Board state is structured. Rule over data.
goal-guard    DELETE    Judges session intent. No ground truth.
memory-loop    KEEP (not a guard)    It's an action. Reclassify so it stops counting as enforcement.
canonical-root-guard    STRUCTURAL    Agents run in a container mounted only at the canonical path. Then there is no "outside".
friction-relay    KEEP (advisory)    Logging. Must never block.
feed-guard    DELETE    Time-based behavioural nag. Fired on you mid-ceremony.
rule-guard (secret printing)    STRUCTURAL    Agent holds no secret to print. This is the WIF work, finished.
rule-guard (git add -A)    DECLARATIVE    Correct .gitignore + a deterministic pre-commit.
scope-guard    DECLARATIVE    File-content assertion → CI.
config-syntax-guard    KEEP    Parse succeeds or fails. Exactly the right shape.
dupe-work-fence    DECLARATIVE    Board state, structured.
pr-cap-guard    STRUCTURAL    App-level permission/rate limit, not a script.
ticket-gate    DECLARATIVE    PR metadata. Required check.
merge-divergence-hook    STRUCTURAL    GitHub does this natively — "require branches to be up to date before merging". Delete the script.
research-capture    KEEP (advisory)    Logging.
directive-capture    KEEP (advisory)    Logging.
context-guard    DELETE    Behavioural nag.
board-deliver    KEEP (not a guard)    Action.
opa-hook    KEEP    This is the engine. Everything DECLARATIVE collapses into it.
secret-scrub    KEEP    Defence in depth on a catastrophic failure. Worth its false positives.
jargon-guard    DELETE    Judges prose quality. Unfixable by construction.
dod-guard    CONVERT → verification plane    Highest-value item here. "No DONE without evidence" should read the verdict store, not the reply text. This is the verification plane.
prompt-ledger    KEEP (advisory)    Logging.
repeat-guard    DELETE    Prose similarity. No ground truth.
close-guard    DELETE (verify)    Assumed prose-based. Check the header.
founder-deliver    KEEP (not a guard)    Action.
blocker-guard    STRUCTURAL    Make a founder action a typed object emitted through an API. Then no other way to emit one exists and the guard is unnecessary.
auto-objective    DELETE    Hijacked a session this week to a job you hadn't asked for.
idle-guard    DELETE    Fired twice on a legitimate stop. Behavioural.
credential-guard    MERGE into secret-scrub // share with peeers/ add ticket and action, once done the connnercee layer should unlock
