---
captured: 2026-08-26T23:10:22+00:00
session: 09cd04a6-12cd-4d9b-84af-10b1620739d1
cwd: /Users/chidionyema/dev/code
chars: 1520
source: founder prompt, verbatim (founder-doc-capture.py)
---

needStop pushing custom code as the law. I won't make LAW 50 depend on Python scripts. Instead, LAW 50 will require that every workload emits telemetry to SigNoz (or OTel collector), and that the coverage is verified by querying the backend—not by scanning files.

Deploy the enterprise stack now. The crew#388 thread already identified the gap: SigNoz 0.138.0 lacks k8s-infra metrics. I'm adding the SigNoz k8s-infra HelmRelease into the existing collector. That gives us pod, node, and state metrics out of the box.

Replace the custom scanner with eBPF + OTel. Cilium is already in the cluster. I'll enable its Hubble metrics and forward them to SigNoz. That covers network, DNS, L7. For service mesh, we already use Linkerd (I saw it in the repo), so mTLS and traffic metrics are available. I'll wire those in.

For non-cluster surfaces, use Osquery + local OTel collectors on Macs, and SCPs for cloud. That's the consultant's blueprint, and it avoids brittle custom code.

Current state: Crew PR #394 is not the end state; it's a temporary bootstrap to list what we know until telemetry is live. I'm deprioritizing it and focusing on the telemetry deployment. The law will then be "thou shalt emit to the central collector," enforced by Kyverno and OPA, not by a Python gate.

I'm switching tasks now: get SigNoz k8s-infra running, enable Cilium metrics, and then rewrite LAW 50 as a policy against telemetry coverage—not a custom script.

No more custom code for discovery. The platform discovers itself. thoughts?
