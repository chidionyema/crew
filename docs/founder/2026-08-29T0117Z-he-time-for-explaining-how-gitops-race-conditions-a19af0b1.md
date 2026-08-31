---
captured: 2026-08-29T01:17:52+00:00
session: f3f21d6e-8df9-44b8-ae46-def299e0298c
cwd: /Users/chidionyema/dev/code
chars: 2914
source: founder prompt, verbatim (founder-doc-capture.py)
---

he time for explaining how GitOps race conditions work is over. You are absolutely right—this is an amateur architectural failure. Moving a file in Git should never cause a cascading destruction of a production namespace.Here is exactly how you eliminate this failure mode across the entire platform permanently, ensuring that no agent, no human, and no automated GitOps sync can ever prune a critical namespace again.1. The GitOps Level Fix: Disable Pruning on NamespacesFlux natively supports an annotation that completely exempts a resource from garbage collection. If a namespace has this annotation, Flux will manage it, but will refuse to delete it even if it is removed from the Git repository or moved between Kustomization manifests.  Do not rely on humans to remember this. Force it across all namespaces globally using a Kustomize patch in your base configuration.Add this to your root kustomization.yaml that generates your platform namespaces:YAMLpatches:
  - target:
      kind: Namespace
    patch: |
      apiVersion: v1
      kind: Namespace
      metadata:
        name: not-important
        annotations:
          kustomize.toolkit.fluxcd.io/prune: disabled
This instantly guarantees that Flux will never garbage-collect a namespace during a refactor.2. The Cluster Level Fix: Immutable Namespaces (Kyverno)The GitOps fix protects you from Flux, but it doesn't protect you from a rogue script, an agent, or an accidental kubectl delete ns.Deploy a cluster-wide Kyverno policy that intercepts and physically blocks the DELETE API request for any core platform namespace.YAMLapiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: prevent-namespace-deletion
spec:
  validationFailureAction: Enforce
  rules:
  - name: block-deleting-platform-namespaces
    match:
      any:
      - resources:
          kinds:
          - Namespace
    preconditions:
      any:
      - key: "{{ request.object.metadata.name }}"
        operator: In
        value: 
          - backstage
          - observability
          - identity
          - flux-system
    validate:
      message: "AMATEUR GUARD: Deletion of core platform namespaces is hard-blocked. You must disable this Kyverno policy to proceed."
      deny:
        conditions:
          any:
          - key: "{{ request.operation }}"
            operator: Equals
            value: DELETE
3. CI Pipeline Guard (Preventing the Move)You mentioned writing a guard so "no future move of a namespace between rows can pass CI."If you are validating PRs, add a simple check in your GitHub Actions to fail if a namespace is deleted from a Kustomization list without the prune: disabled annotation being verified in the cluster.  Bash# Add to your CI validation script
if git diff --name-status main | grep '^D.*namespace.yaml'; then
  echo "FATAL: Deleting or moving a namespace manifest in GitOps is banned unless manually intervened."
  exit 1
fi
