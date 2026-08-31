---
captured: 2026-08-29T07:33:14+00:00
session: 2d8b3bd0-3d43-40d9-862b-712be5c41803
cwd: /Users/chidionyema/dev/code
chars: 1906
source: founder prompt, verbatim (founder-doc-capture.py)
---

The Elite Approach: Infrastructure as Code (IaC)Elite teams manage Tailscale exactly like they manage Kubernetes: as code. No Chrome extensions, no manual form filling.1. The Master API Key (The Only Manual Step)An elite team generates exactly one master Tailscale API key when the company is founded. That key goes into a secure vault (like GitHub Secrets or Doppler). From that point on, a human never touches the Tailscale UI again.2. Programmatic Provisioning (Terraform or API)Instead of clicking through a UI, the CI/CD pipeline uses that master API key to run Terraform (or a direct API call) to dynamically generate the scoped credentials it needs.If a pipeline needs to provision a credential with tag:k8s, the automation executes a POST request to the Tailscale API:Bash# How high-tech automation generates a tagged credential instantly
curl -X POST 'https://api.tailscale.com/api/v2/oauth/clients' \
  <redacted> \
  -d '{"description": "estate-k8s-operator", "tags": ["tag:k8s"]}'
This returns the Client ID and Secret instantly to the pipeline, completely bypassing the browser.3. The ACL as TruthFor OIDC specifically, high-tech teams commit their Tailscale ACL (policy.hujson) to a GitHub repository. The CI pipeline automatically syncs it to Tailscale. The ACL is where you declare that the GitHub Actions OIDC identity is legally allowed to assume tag:k8s.How to Fix This Right NowYour agent is stuck trying to force you to do its manual labor using a broken, hallucinated mental model of a webpage. You need to yank it out of the UI and force it to use the API.Tell the agent exactly this:"Stop trying to use the Chrome extension or ClickOps. Tailscale OIDC does not assign tags in the UI. We are managing Tailscale programmatically. Use the Tailscale API to generate the OAuth client with tag:k8s, or update the Tailscale ACL via code to map the GitHub Actions identity."
