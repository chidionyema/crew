---
captured: 2026-08-26T00:36:58+00:00
session: 9f8f4f5f-1e12-4c54-b7a9-6fca2b737991
cwd: /Users/chidionyema/dev/code/idp
chars: 3405
source: founder prompt, verbatim (founder-doc-capture.py)
---

The "Lazy Consensus" Autonomy Upgrade1. The estate-defaults.yaml (The Organism's Instincts)We place a configuration file at the root of your infrastructure repository. This acts as the "brain stem" for your agents. If an agent hits a fork in the road, it reads this file before it even thinks about messaging you.YAML# ~/.estate/estate-defaults.yaml
# LAW OF AUTONOMY: Do not ask the founder for decisions covered by this matrix.

infrastructure:
  dns_zone: "mesh.estate" # All internal services route here
  compute_tier: "auto-scale-paid" # Never suspend for limits; auto-scale up to $50/mo.

policy:
  stale_repos: "delete-if-no-remote-and-1-commit"
  vendor_lock_in: "hard-reject" # Shadow CTO automatically fails PRs using proprietary SDKs
  oauth_creation: "terraform-automated" # Agents must use TF providers to create OIDC clients

handoff_protocol:
  mode: "lazy_consensus"
  timeout_minutes: 60
2. The New Handoff Protocol (STAGED)Your agents are banned from using the phrase "FOUNDER ACTION:" unless it is a physical hardware requirement (like tapping a YubiKey).Everything else is "STAGED".Old Way: "I need you to delete AwesomeProject." -> Founder is blocked.New Way: "STAGED: AwesomeProject meets stale criteria (no remote, 1 commit). Earmarked for deletion. Reply hold to cancel. Auto-deleting in 60 minutes." -> Founder ignores the message, system cleans itself.3. Killing the OAuth "Friction"KINI's rule #1 is "can this be auto-configured?". The agent asked you to click around the GitHub UI to make an OAuth app. That is a failure of automation.The Enterprise Fix: We don't click UI buttons. The agents should use the Terraform GitHub Provider to programmatically provision GitHub Apps, generate the client secrets, and push those secrets directly into the OCI Vault using the Terraform Vault provider. You do zero clicking. Zero copy-pasting.THE CREW DIRECTIVE (COPY-PASTE)Feed this to KINI and the agents to permanently upgrade their operating parameters and clear the immediate blockages.PlaintextCREW DIRECTIVE: IMPLEMENT KINI'S "LAZY CONSENSUS" PROTOCOL

1. SYSTEM PROMPT OVERRIDE: 
Before asking the founder a question, evaluate: Can this be auto-configured with a safe default? Can it be staged for confirmation? If yes, stage it. The phrase "FOUNDER ACTION:" is now heavily restricted.

2. CREATE DEFAULTS PRIMITIVE:
Create `estate-defaults.yaml` in the repo root. Populate it with KINI's proposed defaults: DNS zone, node pool auto-scaling thresholds, stale repo policies, and vendor lock-in rejections.

3. NEW HANDOFF FORMAT:
All future handoffs must use the STAGED format:
"STAGED: [Action] is ready. Reply 'go' to execute immediately, 'hold' to review. Auto-activating in [X] minutes."

4. IMMEDIATE UNBLOCK (IDP#147 & AwesomeProject):
- AwesomeProject: Apply the new stale policy from defaults.yaml. Delete the directory immediately.
- OAuth App: Do not ask the founder to use the GitHub UI. Write a Terraform script using the `github` and `oci` providers to programmatically create a GitHub App, generate the secret, and inject it into the OCI Vault. If a true OAuth App cannot be fully API-automated, configure a generic OIDC client via Cloudflare Access (which is fully API automatable) instead of GitHub.

DONE WHEN: The agent clears the current queue without requiring the founder to click a single UI button, and the new STAGED protocol is used for the next handoff.
