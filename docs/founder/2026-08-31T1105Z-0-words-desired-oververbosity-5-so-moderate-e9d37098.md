---
captured: 2026-08-31T11:05:44+00:00
session: ef0354ef-fa6b-4b6b-a5e2-5d6f7889b3b8
cwd: /Users/chidionyema/dev/code/.wt-idp-p0
chars: 2068
source: founder prompt, verbatim (founder-doc-capture.py)
---

0 words? Desired oververbosity 5, so moderate.

Let's write.

You're right to ask. Bootstrapping from scratch only works if the inventory is complete—and right now we've only named a fraction. Scheduled jobs, local automation, external SaaS settings, and Kubernetes CronJobs are exactly the kind of thing that gets forgotten until the first incident.

We need to stop guessing and produce a single platform inventory matrix, then make idp-oke-rebuild --check grade every row.

What's probably still missing
Beyond the six items you listed, here's what I would expect to find in a full estate, and what would break if we rebuilt without them:

Scheduled jobs

Kubernetes CronJob objects (backups, cert renewals, reports)

Flux Kustomization/HelmRelease with schedule annotations

GitHub Actions scheduled workflows (on: schedule)

Cloudflare Workers/CRON triggers or Page Rules with scheduled tasks

Local Mac launchd jobs and crontab entries (you mentioned a few, but there may be more)

CI/CD pipelines

GitHub Actions workflows (build, test, deploy)

Repository secrets and OIDC trust relationships

Branch protection rules and required status checks

Container registry (GHCR) packages and their retention policies

DNS & certificates

All Cloudflare DNS records (A, CNAME, TXT, etc.)

Cloudflare Tunnel configs and associated ingress rules

TLS certificates (origin, edge, and any manually installed ones)

Kubernetes configuration outside Flux

Manually applied manifests (kubectl apply)

CRDs and operators (Kyverno, cert-manager, etc.)

ConfigMaps and Secrets not tracked by Git

Runtime state not in Git (e.g., PVs, PVCs, LoadBalancer IPs)

Backups and restore mechanisms

OCI volume backups or snapshots

Object storage bucket policies and lifecycle rules

Any database dumps or etcd snapshots

Monitoring & alerting

Prometheus/Grafana configs, alert rules, notification channels

Any external uptime checks or health endpoints

Identity & secrets

Root secret values (you already have R52 for that)

OAuth client IDs, API tokens, SSH keys, Vault unseal keys
