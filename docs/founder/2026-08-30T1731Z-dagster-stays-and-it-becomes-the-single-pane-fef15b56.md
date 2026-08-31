---
captured: 2026-08-30T17:31:23+00:00
session: a7b41022-3074-43c7-bb13-a1d7e07adff1
cwd: /Users/chidionyema/dev/code/idp
chars: 1827
source: founder prompt, verbatim (founder-doc-capture.py)
---

Dagster stays, and it becomes the single pane of glass for the entire estate.To make Dagster see everything without hitting the "Mac goes to sleep" wall, its control plane (the UI and the scheduler) needs to live in the cluster, while retaining the ability to trigger compute on your Mac when necessary.To give your local AI agent the exact instructions it needs to execute this, copy and paste this command back into your terminal:PlaintextFile the ticket. We are going with a unified Dagster architecture. Dagster must see and orchestrate the whole estate, whether execution happens on the Mac or in the cluster. 

Ticket Spec:
1. Move the Control Plane: Deploy Dagster (Dagit and Daemon) into `platform/` as Kubernetes Deployments. Expose DAGSTER_GRAPHQL_URL so the Backstage catalogue provider can finally see it.
2. Ingest all Estate Clocks: Inventory the 46 Mac jobs, the 9 cluster CronJobs, and the drill-dispatcher. Re-declare all of them as Dagster Schedules/Sensors so Dagster is the sole "clock" for the estate.
3. Enable Hybrid Execution: Configure Dagster to use KubernetesRunLauncher for cluster tasks. For any of the 46 jobs that physically require execution on the Mac, implement Dagster Pipes or set up a local gRPC server on the Mac to receive runs from the cluster.
Why this fixes the root cause:The UI is never blind: By putting the Dagster web server in the cluster, Backstage will always have a live endpoint to read from, even if your laptop is closed.A single source of truth: Kubernetes CronJobs and custom dispatchers get deprecated. If something runs on a schedule, it runs in Dagster.Flexible compute: Using Dagster Pipes allows the centralized cloud scheduler to trigger bash scripts or Python environments directly on your Mac, stream the logs back to the cloud, and keep a unified history. ticket
