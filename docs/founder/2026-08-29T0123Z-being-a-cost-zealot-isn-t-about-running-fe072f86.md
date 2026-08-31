---
captured: 2026-08-29T01:23:22+00:00
session: a0d64ea4-d03d-4d1f-84e1-e1739e05c615
cwd: /Users/chidionyema/dev/code/idp/.claude/worktrees/crew459-portal-polish
chars: 3544
source: founder prompt, verbatim (founder-doc-capture.py)
---

Being a cost zealot isn't about running crippled infrastructure—it's about refusing to pay for idle capacity, default configuration bloat, and poor architectural discipline.

Here is how to shred your bill down from $42+/month to $19/month (or $0) while keeping 100% of your developer speed and power.

Step 1: Kill "Request Inflation" (The K8s Default Trap)
Kubernetes doesn't schedule pods based on what they actually use; it schedules based on what they request. Default Helm charts for tools like SigNoz, ClickHouse, Temporal, and Langfuse request absurd defaults (e.g., asking for 1–2 full CPU cores and 2 GB RAM each) just to sit idle 95% of the day.

The Fix:
Set requests to micro-limits, allow limits to burst.

Change internal pod specifications to:

YAML
resources:
  requests:
    cpu: "10m"     # 0.01 core (instead of 500m-1000m)
    memory: "64Mi" # (instead of 1Gi)
  limits:
    cpu: "2000m"   # Let it burst to 2 cores when active!
    memory: "2Gi"  # Let it use RAM when under load
Result: Kubernetes will suddenly fit your entire platform into 2 to 4 cores without killing pods, because scheduling is no longer blocked by imaginary reservations.

Step 2: Put Heavy Platform Tools on a Strict Diet
Off-the-shelf platform tools expect enterprise-scale nodes. You need to restrict them:

ClickHouse (SigNoz): Set memory limits in ClickHouse config (max_server_memory_usage_to_ram_ratio = 0.3). Stop it from grabbing all host RAM.

Temporal: Use a single-process/embedded backend or a lightweight shared SQLite/PostgreSQL instance instead of running heavy multi-node Cassandra/Elasticsearch containers.

Telemetry Retention: Set log and trace retention in SigNoz to 3–7 days maximum. You do not need gigabytes of 30-day debug logs sitting in memory and disk on a lean setup.

Step 3: Right-Size to 4 Cores / 16 GB ($19/mo) or 2 Cores ($0/mo)
Once you strip out fake resource requests:

Run measure it to inspect actual P95 CPU and RAM usage. You will likely find your 6-core node is running at ~10–15% real utilization.

Downsize the OCI Node:

4 Cores / 16 GB RAM = $19/month (uses Oracle's 2 free cores + pays for 2).

4 Cores / 24 GB RAM = $27/month (if you need extra RAM headroom).

2 Cores / 12 GB RAM = $0/month (if you strip requests aggressively enough to fit inside Oracle's Always Free tier).

Step 4: Enforce the 4 Zealot Rules for the Team
Add these operational rules to the team standard immediately:

No Paid Scaling Without Proof: Nobody scales a node or adds cloud resources without showing P95 utilization metrics proving the existing node is 80%+ full.

Zero Public Load Balancers for Staging: Access staging exclusively via Tailscale. Never pay $8.25/mo for an extra OCI public Load Balancer.

No Ephemeral Cluster Boots: All CI runs use sub-minute unit gates. Local dev uses mirrord inside the staging namespace.

Auto-Clean K8s Jobs: Set ttlSecondsAfterFinished: 60 on all Kubernetes jobs so test runs and migration pods delete themselves instantly after execution.

Summary of Impact
Metric    Current State    Cost Zealot Target
Node Size    6 Cores / 24 GB    4 Cores / 16 GB (or 2 Cores)
Monthly OCI Bill    $42 - $78/mo    $19/mo (or $0/mo)
Staging Cost    Proposed +$36/mo    $0/mo (Namespace isolation)
Feedback Loop    13-minute CI wait    60-sec CI + 1-sec mirrord loop
Next Command: Tell your agent measure it, strip pod requests to micro-limits, and downsize the node to 4 Cores / 16 GB ($19/mo) with namespace staging.

Want to inspect resource requests across all running pods right now?

Yes
