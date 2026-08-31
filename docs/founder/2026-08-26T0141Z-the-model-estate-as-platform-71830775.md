---
captured: 2026-08-26T01:41:13+00:00
session: 4e5b5e8f-3cc5-400a-92cd-db2cb1dcd790
cwd: /Users/chidionyema/dev/code/hermes-v2
chars: 3628
source: founder prompt, verbatim (founder-doc-capture.py)
---

The Model: Estate-as-Platform
Core principle: The founder is the approving authority, never the implementing operator. Agents are platform engineers with scoped credentials. Every change is a PR. Every approval is a structured message. Nothing touches a GUI.
Five Enterprise Standards (implementable now)
1. Zero-Click Provisioning (ZCP)
Rule: If an agent creates an identity, they also provision its role, secret, and policy binding in the same PR. If they lack privilege, they escalate via a privilege-elevation ticket — not a "please sign in" message.
Tonight: estate-tofu should have been created with the Administrators role in the same tofu plan that created the user. The fix is one block, not a console login.
2. Policy-as-Code Gate (PaC)
Rule: Every operational change — provisioning, deploy, config, secret rotation — passes through an OPA/Rego gate before merge. You already have Rego (6/6, 39/39). Extend it to cover:
provisioning_complete: identity + role + scope in one PR
no_gui_actions: any step requiring a browser click is auto-rejected
founder_approval_required: changes to founder-facing systems need a APPROVE: message, not a click
Tonight: Add the three rules above to your existing Rego policy.
3. Immutable Audit Trail (IAT)
Rule: Every agent action is recorded in two places:
Git commit (what changed)
Langfuse trace (why it changed — the LLM reasoning)
No action exists without both. This is your EU AI Act readiness and your M&A due diligence package.
Tonight: Ensure every agent session logs its reasoning to Langfuse with a crew# tag.
4. Self-Service Catalog (SSC)
Rule: Backstage is the single pane of glass. Every service, every URL, every secret reference, every agent — catalogued with links. The founder never asks "what is the URL?" He looks at the catalog. If it's not there, the catalog gate fails the PR.
Tonight: The bin/catalog-gen you already have must emit links for every entity. The gate you built (crew#269) enforces it.
5. Scoped Agent Identity (SAI)
Rule: Every agent session has a SPIFFE identity (e.g., spiffe://estate.local/session/code-37). That identity carries a role:
platform-engineer: can write tofu, merge infra PRs
application-engineer: can write app code, cannot touch identity
founder-proxy: read-only, reports only
No agent operates as "the founder." No agent uses the founder's credentials. Rogue agents are revoked by rotating their SPIFFE SVID.
Tonight: Start with GitHub App tokens scoped per lane, not the founder's personal token.
The Operating Model: How It Works
Table
Before (friction)    After (enterprise)
"Sign in to OCI console and add a user"    Agent writes tofu block → PR → OPA gate → APPROVE: estate-tofu role → auto-apply
"Create a GitHub OAuth App"    GitHub App with manage_oauth_apps scope → stages app → founder replies APPROVE: oauth app
"4/24 or 2/12 node pool?"    Policy: auto-scale-when-free-full → PR with cost estimate → APPROVE: scale or DENY: stay-free
"Push or delete AwesomeProject?"    Policy: stale-repo-auto-delete-after-7d → deletion staged → APPROVE: delete or DENY: keep
"Review mumchimp.com vs Medusa"    Recon agent posts screenshot diff + Loom → APPROVE: A or APPROVE: B
Phase 0: Stop the Bleeding (tonight)
A. Write idp/docs/policy/enterprise-operating-model.md
The five standards above, plus the operating model table.
B. Fix the three open founder blockers with ZCP:
estate-tofu role assignment → one tofu block, no console
GitHub OAuth App → GitHub App token, no founder clicks
Node pool → auto-default policy with cost estimate
C. Add the three Rego gates:
provisioning_complete
no_gui_actions
founder_approval_required
