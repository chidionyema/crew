---
captured: 2026-08-24T22:26:49+00:00
session: 76aaf0e4-b2ce-4ce8-83d2-aec61bc6e553
cwd: /Users/chidionyema/dev/code
chars: 2306
source: founder prompt, verbatim (founder-doc-capture.py)
---

FOUNDER DIRECTIVE: ENVIRONMENT PARITY — FINAL
Principle: This laptop is a dev substrate. It must replicate prod (k3s on Oracle Free Tier) as closely as mechanically possible. Any deviation is drift; drift is a bug.
Colima Configuration
Set network.hostAddresses: true in ~/.colima/default/colima.yaml. This makes Docker -p 127.0.0.1:PORT:PORT bind to actual localhost on the macOS host, not 0.0.0.0 via limactl. Without this, loopback security is theater.
Do NOT restart Colima until a scheduled maintenance window. After restart, verify with lsof -nP -iTCP -sTCP:LISTEN that every ledger-declared 127.0.0.1 binding is kernel-real.
Port Ledger Is Absolute Law
ports.yaml is the single source of truth for all port bindings across all environments. No service binds any port without declaration.
The FOREIGN skip-list in the port gate is too broad. limactl holding *:PORT is a claim, not an exemption. If a process holds a port, it gets checked against the ledger. No exceptions.


No Environment-Specific Hacks in Shared Code
Dockerfile, docker-compose.yml, Kubernetes manifests, and application code must remain environment-agnostic. No Colima-specific flags, no DNS workarounds, no macOS conditionals. Local infrastructure fixes belong in local config only (~/.colima/, local bootstrap scripts), never in the shared repo.
Verification Discipline
Every claim of "localhost-only" or "secure binding" must be independently verified with live kernel probes (lsof, ss), not Docker's self-reported bind address. Audit the ledger after every infrastructure change.
Documentation
Record every substrate property that creates environment asymmetry (e.g., hostAddresses: false voids Docker localhost bindings) in estate docs. The next session starts from your standing point, not from zero.
Handoff
🔴 Colima restart pending — hostAddresses: true set, awaiting maintenance window
🟡 Port gate — FOREIGN rule narrowed, 80/443 correctly FAILING until restart proves fix
🟢 k3d cluster — live, Traefik up, 80/443 registered
🟢 Backstage build — C++ compile fix applied, image building
🟢 Dagster — 40 schedules running
⚪ ArgoCD — crew#191 item 4, footprint measurement pending
⚪ Private repos — 11 repos visibility flip blocked on leak check completion
⚪ SPIFFE — decision pending: k3s DaemonSet, documented skip, or defer
