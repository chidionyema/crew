---
captured: 2026-08-31T04:14:43+00:00
session: 80471694-3138-4645-a870-868210b81120
cwd: /Users/chidionyema/dev/code/hermes-v2
chars: 1554
source: founder prompt, verbatim (founder-doc-capture.py)
---

Run these two and paste the output:

kubectl top nodes
kubectl get nodes -o custom-columns=NAME:.metadata.name,ALLOC_CPU:.status.allocatable.cpu,ALLOC_MEM:.status.allocatable.memory
kubectl get deploy,sts -A -o custom-columns=\
KIND:.kind,NS:.metadata.namespace,NAME:.metadata.name,REPLICAS:.spec.replicas,\
CPU_REQ:.spec.template.spec.containers[*].resources.requests.cpu,\
MEM_REQ:.spec.template.spec.containers[*].resources.requests.memory

The second one is the load-bearing query. Every row with REPLICAS: 1 is a candidate, and its request values are exactly what a second copy costs. I'll sum them against allocatable and tell you what fits.

While you pull it, the thing that will decide the answer more than the arithmetic: for resilience on two nodes, replicas: 2 alone buys you nothing unless the replicas land on different nodes. Kubernetes will happily schedule both on the same one, and then a node loss takes out both copies — you've paid double for identical exposure. Every workload you scale to 2 needs a topologySpreadConstraint with topologyKey: kubernetes.io/hostname and whenUnsatisfiable: DoNotSchedule. That part is free, it's a field, and without it the spend is wasted.

Second thing the numbers will surface: if both replicas must sit on different nodes, then losing a node means the survivors need to run everything alone. So the real capacity test isn't "do second replicas fit across 16.7 GB" — it's "does the full working set fit on one node." That's the number that means resilience. Paste the output and I'll compute both.
