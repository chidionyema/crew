---
captured: 2026-08-28T10:50:22+00:00
session: a0d64ea4-d03d-4d1f-84e1-e1739e05c615
cwd: /Users/chidionyema/dev/code/idp/.claude/worktrees/crew459-portal-polish
chars: 3003
source: founder prompt, verbatim (founder-doc-capture.py)
---

look for the fucking last tin  before we lost the fucking thraead wtf are we doing on this redits, we have to change our operational playbook. Minimax is not inherently useless, but asking it to do deep architectural reasoning in one shot is why it feels "dumb and slow."

The "exponential way" to build this when using a degraded fallback model is to shift the cognitive load off the LLM and onto deterministic scripts. You don't ask Minimax to figure out the network; you give it a rigid tunnel, hide the complexity behind a single command, and let it act as a simple dispatcher.

Here is how to exponentially accelerate this setup using the tools you already have, compensating for the downgraded brain.

Phase 1: The "Dumb LLM" Bridge (Cluster to Mac)
We need to connect the cluster to your Mac without asking Minimax to write complex Kubernetes manifests.

The Auth Key Bypass: Go to your Tailscale admin console (from your phone or Mac) and generate an Ephemeral Auth Key.

The Injection: Have your team (or you via your terminal) inject that Tailscale Auth Key into the Hermes cluster pod as an environment variable (TAILSCALE_AUTH_KEY).

The One-Liner: Ask Minimax to run exactly this command inside its pod to join your network instantly:
tailscale up --authkey=$TAILSCALE_AUTH_KEY --hostname=hermes-pod

Phase 2: The Trust Anchor
Minimax will hallucinate if it has to negotiate passwords or complex authentications every turn. We need absolute zero-friction execution.

Generate Keys: Tell Minimax to run ssh-keygen -t ed25519 -N "" inside its pod.

Create the Link: Since you have your Moonlight/Tailscale setup working from your iPhone, manually copy the pod's public key (id_ed25519.pub) and paste it into your Mac's ~/.ssh/authorized_keys file.

Now, the agent has permanent, passwordless root-level access to your Mac.

Phase 3: The Exponential Multiplier (The Wrapper)
This is the secret to making a weaker LLM perform like a genius. Do not let Minimax write raw SSH commands; it will mess up the escaping and syntax.

Create the Abstraction: On the cluster pod, create a simple bash script called mac-run.

Bash
#!/bin/bash
ssh -o StrictHostKeyChecking=no founder@100.112.51.80 "$@"
Make it Executable: chmod +x mac-run and move it to /usr/local/bin/.

The Prompting Shift: From now on, you instruct Minimax: "Whenever you need to interact with the codebase, do not use local tools. Write your script, save it to a file, and execute it using mac-run 'cat script.sh | bash'."

Why this is Exponential
By doing this, you have completely isolated the complexity. Minimax doesn't need to understand WireGuard, Tailscale, or SSH. It just knows that if it types mac-run "ls ~/dev/code", it gets the result. You constrain its environment so tightly that its lack of reasoning power doesn't matter—it just becomes a fast, obedient typist executing on your high-powered Mac.

To get this moving, can you easily generate a Tailscale Auth Key from your current device to feed into the cluster pod?
