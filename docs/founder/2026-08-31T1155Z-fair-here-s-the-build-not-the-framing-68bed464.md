---
captured: 2026-08-31T11:55:23+00:00
session: ef0354ef-fa6b-4b6b-a5e2-5d6f7889b3b8
cwd: /Users/chidionyema/dev/code/.wt-idp-p0
chars: 5796
source: founder prompt, verbatim (founder-doc-capture.py)
---

Fair — here's the build, not the framing.

Ground rule that makes an inventory "true": it is derived from live control-plane APIs, never from git. Git is the thing under audit. Every control plane that can hold state gets enumerated with the provider's own listing API, and the declared side (tofu, Flux) is diffed against that. This is a solved discipline with off-the-shelf tooling — you don't need another bespoke script pile.

Step 1 — enumerate every control plane, read-only, snapshot to a new repo. Your estate has eight places state can live. One command or tool each:

OCI tenancy: oci search resource structured-search --query-text "query all resources" per region/compartment. This returns everything that exists regardless of how it was created — it's the ground truth your tofu state gets compared against. OCI also ships resource discovery in the terraform provider binary (-command=export), which generates HCL + state from a live compartment; keep that for step 3.
Kubernetes: full object dump — kubectl api-resources --verbs=list -o name | xargs -I{} kubectl get {} -A -o json (plus cluster-scoped). Classify each object by ownership: Flux kustomize labels (kustomize.toolkit.fluxcd.io/name), Helm release annotations, controller ownerReferences. Cross-check against Flux's own applied-object inventory (flux tree / Kustomization .status.inventory). Anything with no owner chain back to git is hand-applied.
Cloudflare: API-list zones, DNS records, tunnels, access policies. cf-terraforming (Cloudflare's own tool) generates both the HCL and the import commands from the live account — it exists precisely for your situation.
Tailscale: API — devices, keys, and pull the ACL document itself; the ACL is one HuJSON file, commit it. Tailscale has a first-party terraform provider for adoption.
GitHub: gh api — repo settings, branch protections, Actions secret names, workflows, webhooks, deploy keys, app installations, GHCR packages. Names and existence are inventory; values aren't needed.
The Mac: launchctl list, LaunchAgents/LaunchDaemons dirs, crontab -l, ~/.claude/settings.json hooks, brew services. Snapshot the output as files.
Vendor credentials: list what exists in the OCI vault (already covered by the tenancy search) and enumerate which external accounts hold live keys (Telegram, LLM vendors) — a one-page ledger of where each root secret lives, per your R52 model.
GHCR/images: package list per repo; which tags are referenced by Flux vs orphaned.

If you want one tool instead of eight scripts: Steampipe has plugins for OCI, Kubernetes, GitHub, Cloudflare, and Tailscale — SQL across all of them, so the reconciliation below is a join query, not more Python.

Step 2 — reconcile into one table with four verdicts. One row per resource: (plane, type, id, declared_in, verdict). Verdicts: MANAGED (live and in git, matching), DRIFTED (in git, differs live — tofu plan -refresh-only gives you this for the OCI side), ORPHAN (live, declared nowhere), GHOST (declared, doesn't exist). The definition of done for "true inventory": every enumerated row carries a verdict, and the ORPHAN set is either empty or each entry has an explicit waiver with an expiry date. No "known but unmanaged" category is allowed to persist.

Step 3 — adopt or kill. Every ORPHAN either gets imported into IaC or deleted — nothing stays loose. OpenTofu import blocks with -generate-config-out= write the HCL for you; cf-terraforming does Cloudflare; the tailscale and github providers take those planes. GHOSTs get purged from state/config. At your scale (51 OCI resources, 73 Flux rows, probably tens of DNS records) this is days of import work, not weeks.

On doing it by hand: your instinct is correct for steps 1–2, and I'd tell any client the same — trust in an inventory derives from how it was constructed. The enumeration is ~10 mechanical read-only commands; run them yourself in an afternoon, commit the raw JSON. Where agents are safe to readmit is step 3 only, because import work is self-verifying: the proof is a tofu plan diff that you read before apply, and a wrong import shows as a destructive plan line, not a silent success. That's the property that made you unable to catch them before — their claims weren't mechanically checkable. Only delegate work where the artifact checks itself.

Enforcement — the iron fist, as mechanisms:

Credential separation. The nightly inventory job runs on its own read-only OCI principal, read-only kubeconfig, read-only API tokens — a credential set the writers can't touch. Verification independent of the writer is a permissions boundary, not a policy document.
The nightly job re-runs steps 1–2 and goes red on any new ORPHAN, DRIFT, or GHOST, and red is wired as a required status check across the repos — a delta anywhere freezes merges everywhere until you clear it. That replaces rulings-nobody-receives with a gate nothing can route around.
Kill the ORPHAN class at the source: Kyverno deny on any object in workload namespaces lacking Flux ownership labels (hand-applied manifests become impossible), and OCI IAM policies that give agent principals zero write scope — write exists only behind your apply.
GitHub: branch protection with you as required reviewer, org-level auto-merge disabled, agent tokens scoped so they cannot bypass. You already found and disabled two merge robots; the setting makes the class unrecreatable.

Sequence and honest timeline: snapshots today (your hands, one afternoon); reconciliation table in 2–3 days; Cloudflare/Tailscale/GitHub adoption plus the nightly red gate inside two weeks. The first command worth running before anything else is the OCI structured search — until that output is sitting in a repo next to tofu state list, every other conversation about the estate is speculation.
