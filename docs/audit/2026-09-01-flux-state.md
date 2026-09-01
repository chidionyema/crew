# Flux state of the cluster, read 2026-09-01T14:19Z (read-only)

Founder, 2026-09-01: for each Flux Kustomization and HelmRelease report name, namespace, lastAppliedRevision, the Ready condition and lastTransitionTime; then Flux events from the last hour. Read through `bin/idp-kube` (API-key profile); nothing changed.

## Summary

73 objects: 49 Kustomizations, 24 HelmReleases. Ready: 68. Not Ready: 5.

## Not Ready

| Kind | Namespace | Name | lastAppliedRevision | Ready | Reason | lastTransitionTime | Message |
|---|---|---|---|---|---|---|---|
| Kustomization | flux-system | chaos | main@bee102db | False | ReconciliationFailed | 2026-09-01T14:16:51Z | Schedule/backstage/backstage-pod-kill dry-run failed (InternalError): Internal error occurred: failed calling webhook "vschedule.kb.io": failed to call webhook: Post "https://chaos-mesh-controller-manager.chaos-mesh.svc:443/validate-chaos-mesh-org-v1alpha1-schedule?timeout=5s": EOF  |
| Kustomization | flux-system | commerce | - | - | - | - | - |
| Kustomization | flux-system | commerce-data | - | - | - | - | - |
| Kustomization | flux-system | event-bus | - | - | - | - | - |
| Kustomization | flux-system | temporal | main@1b323ac9 | False | DependencyNotReady | 2026-08-30T05:54:22Z | dependency 'flux-system/edge' is not ready |

## All objects

| Kind | Namespace | Name | lastAppliedRevision | Ready | Reason | lastTransitionTime | Message |
|---|---|---|---|---|---|---|---|
| HelmRelease | cert-manager | cert-manager | chart cert-manager@v1.21.1 | True | UpgradeSucceeded | 2026-08-31T07:10:44Z | Helm upgrade succeeded for release cert-manager/cert-manager.v2 with chart cert-manager@v1.21.1 |
| HelmRelease | chaos-mesh | chaos-mesh | chart chaos-mesh@2.8.4 | True | UpgradeSucceeded | 2026-08-31T07:12:00Z | Helm upgrade succeeded for release chaos-mesh/chaos-mesh.v4 with chart chaos-mesh@2.8.4 |
| HelmRelease | edge | external-dns | chart external-dns@1.21.1 | True | UpgradeSucceeded | 2026-08-31T07:11:28Z | Helm upgrade succeeded for release edge/external-dns.v6 with chart external-dns@1.21.1 |
| HelmRelease | edge | traefik | chart traefik@41.3.0 | True | UpgradeSucceeded | 2026-08-31T07:10:46Z | Helm upgrade succeeded for release edge/traefik.v8 with chart traefik@41.3.0 |
| HelmRelease | external-secrets | external-secrets | chart external-secrets@2.9.0 | True | UpgradeSucceeded | 2026-08-31T07:09:46Z | Helm upgrade succeeded for release external-secrets/external-secrets.v2 with chart external-secrets@2.9.0 |
| HelmRelease | healing | descheduler | chart descheduler@0.36.0 | True | UpgradeSucceeded | 2026-08-31T07:11:29Z | Helm upgrade succeeded for release healing/descheduler.v3 with chart descheduler@0.36.0 |
| HelmRelease | healing | k8sgpt-operator | chart k8sgpt-operator@0.2.29 | True | UpgradeSucceeded | 2026-08-31T07:11:29Z | Helm upgrade succeeded for release healing/k8sgpt-operator.v3 with chart k8sgpt-operator@0.2.29 |
| HelmRelease | hindsight | hindsight | chart hindsight@0.9.2 | True | UpgradeSucceeded | 2026-08-31T07:12:51Z | Helm upgrade succeeded for release hindsight/hindsight.v47 with chart hindsight@0.9.2 |
| HelmRelease | identity | oauth2-proxy | chart oauth2-proxy@10.7.0 | True | UpgradeSucceeded | 2026-08-29T07:33:02Z | Helm upgrade succeeded for release identity/oauth2-proxy.v5 with chart oauth2-proxy@10.7.0 |
| HelmRelease | keda | keda | chart keda@2.20.2 | True | InstallSucceeded | 2026-08-31T07:14:43Z | Helm install succeeded for release keda/keda.v1 with chart keda@2.20.2 |
| HelmRelease | keda | keda-add-ons-http | chart keda-add-ons-http@0.15.0 | True | InstallSucceeded | 2026-08-31T07:14:44Z | Helm install succeeded for release keda/keda-add-ons-http.v1 with chart keda-add-ons-http@0.15.0 |
| HelmRelease | kyverno | kyverno | chart kyverno@3.9.0 | True | UpgradeSucceeded | 2026-08-31T07:09:45Z | Helm upgrade succeeded for release kyverno/kyverno.v2 with chart kyverno@3.9.0 |
| HelmRelease | metrics-server | metrics-server | chart metrics-server@3.14.0 | True | InstallSucceeded | 2026-08-31T07:11:28Z | Helm install succeeded for release metrics-server/metrics-server.v1 with chart metrics-server@3.14.0 |
| HelmRelease | monitoring | blackbox | chart prometheus-blackbox-exporter@11.17.2 | True | UpgradeSucceeded | 2026-08-31T07:12:07Z | Helm upgrade succeeded for release monitoring/blackbox.v3 with chart prometheus-blackbox-exporter@11.17.2 |
| HelmRelease | monitoring | kube-prometheus-stack | chart kube-prometheus-stack@88.6.0 | True | UpgradeSucceeded | 2026-08-31T07:12:05Z | Helm upgrade succeeded for release monitoring/kube-prometheus-stack.v2 with chart kube-prometheus-stack@88.6.0 |
| HelmRelease | observability | langfuse | chart langfuse@2.0.2 | True | UpgradeSucceeded | 2026-08-31T07:14:04Z | Helm upgrade succeeded for release observability/langfuse.v71 with chart langfuse@2.0.2 |
| HelmRelease | observability | signoz | chart signoz@0.138.0 | True | UpgradeSucceeded | 2026-08-31T07:12:44Z | Helm upgrade succeeded for release observability/signoz.v49 with chart signoz@0.138.0 |
| HelmRelease | observability-agent | k8s-infra | chart k8s-infra@0.17.0 | True | UpgradeSucceeded | 2026-08-31T03:17:25Z | Helm upgrade succeeded for release observability-agent/observability-agent-k8s-infra.v3 with chart k8s-infra@0.17.0 |
| HelmRelease | reloader | reloader | chart reloader@2.2.16 | True | UpgradeSucceeded | 2026-08-31T07:11:24Z | Helm upgrade succeeded for release reloader/reloader.v4 with chart reloader@2.2.16 |
| HelmRelease | robusta | robusta | chart robusta@0.48.0 | True | UpgradeSucceeded | 2026-08-31T07:12:01Z | Helm upgrade succeeded for release robusta/robusta.v11 with chart robusta@0.48.0 |
| HelmRelease | spire-mgmt | spire | chart spire@0.30.1 | True | UpgradeSucceeded | 2026-08-31T07:12:31Z | Helm upgrade succeeded for release spire-mgmt/spire.v4 with chart spire@0.30.1 |
| HelmRelease | spire-mgmt | spire-crds | chart spire-crds@0.6.1 | True | InstallSucceeded | 2026-08-31T07:12:02Z | Helm install succeeded for release spire-mgmt/spire-crds.v1 with chart spire-crds@0.6.1 |
| HelmRelease | tailscale | tailscale-operator | chart tailscale-operator@1.102.3 | True | UpgradeSucceeded | 2026-09-01T13:16:55Z | Helm upgrade succeeded for release tailscale/tailscale-operator.v7 with chart tailscale-operator@1.102.3 |
| HelmRelease | temporal | temporal | chart temporal@1.6.0 | True | UpgradeSucceeded | 2026-08-29T19:01:39Z | Helm upgrade succeeded for release temporal/temporal.v25 with chart temporal@1.6.0 |
| Kustomization | flux-system | alerts | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:16:58Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | alerts-github | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:16:51Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | alerts-secret | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:16:28Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | autoscaler | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:17:51Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | backstage | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:17:03Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | backstage-namespace | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:14:53Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | chaos | main@bee102db | False | ReconciliationFailed | 2026-09-01T14:16:51Z | Schedule/backstage/backstage-pod-kill dry-run failed (InternalError): Internal error occurred: failed calling webhook "vschedule.kb.io": failed to call webhook: |
| Kustomization | flux-system | chaos-mesh | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:16:04Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | cluster-state | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:16:36Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | commerce | - | - | - | - | - |
| Kustomization | flux-system | commerce-data | - | - | - | - | - |
| Kustomization | flux-system | dns | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:16:41Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | drills | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:16:40Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | edge | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:16:13Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | estate-catalog | latest@sha256:ebf7e038adf9e04d44d831db0cf4356ed00d82fc6b4db860ff49e45645e548cf | True | ReconciliationSucceeded | 2026-09-01T14:11:01Z | Applied revision: latest@sha256:ebf7e038adf9e04d44d831db0cf4356ed00d82fc6b4db860ff49e45645e548cf |
| Kustomization | flux-system | event-bus | - | - | - | - | - |
| Kustomization | flux-system | external-secrets | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:17:05Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | flux-system | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:15:42Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | gateway-api-crds | v1.5.1@e7677b70 | True | ReconciliationSucceeded | 2026-09-01T14:16:39Z | Applied revision: v1.5.1@sha1:e7677b70ae75d14a4448fba94870e7deea6cf0ad |
| Kustomization | flux-system | guacamole | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:16:19Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | healing | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:16:55Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | healing-analyzer | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:17:39Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | healthchecks | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:16:52Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | hermes-agent | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:10:24Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | hindsight | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:16:11Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | identity | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:16:18Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | image-automation | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:16:23Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | keda | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:17:33Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | kyverno | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:15:56Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | llm | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:17:14Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | mcp | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:16:22Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | metrics-server | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:16:02Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | monitoring | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:17:09Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | monitoring-rules | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:16:09Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | observability | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:15:30Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | observability-collector | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:17:05Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | priority-classes | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:14:44Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | prospector | main@b658a1a8 | True | ReconciliationSucceeded | 2026-09-01T14:12:50Z | Applied revision: main@sha1:b658a1a8eda1700b3787c4005cd5660e8cab09bf |
| Kustomization | flux-system | prospector-platform | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:17:20Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | reloader | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:17:42Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | robusta | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:15:48Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | scheduling | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:16:45Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | science | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:17:05Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | secret-store | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:16:09Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | spire | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:07:50Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | staging | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:15:30Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | tailscale | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:15:58Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |
| Kustomization | flux-system | temporal | main@1b323ac9 | False | DependencyNotReady | 2026-08-30T05:54:22Z | dependency 'flux-system/edge' is not ready |
| Kustomization | flux-system | verification | main@bee102db | True | ReconciliationSucceeded | 2026-09-01T14:16:14Z | Applied revision: main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a |

## Flux events, last hour (13:19Z to 14:19Z): 370 events on 126 distinct object/reason pairs (event store holds 12263 events)

| Kind/Namespace/Name | Type | Reason | Count | Last seen (UTC) | Revision | Outcome / message |
|---|---|---|---|---|---|---|
| Kustomization/flux-system/chaos | Warning | ReconciliationFailed | 1 | 14:16:50 | main@bee102dbf8c92ac69 | Schedule/backstage/backstage-pod-kill dry-run failed (InternalError): Internal error occurred: failed calling webhook "vschedule.kb.io": failed to call webhook: Post "https://chaos-mesh-controller-manager.chaos-mesh.svc: |
| Kustomization/flux-system/edge | Warning | ReconciliationFailed | 1 | 13:20:17 | main@163d6cd80ed13f49f | PolicyException/kyverno/provider-edge-load-balancer dry-run failed (InternalError): Internal error occurred: failed calling webhook "kyverno-svc.kyverno.svc": failed to call webhook: Post "https://kyverno-svc.kyverno.svc |
| GitRepository/flux-system/flux-system | Normal | GarbageCollectionSucceeded | 1 | 13:36:32 | - | garbage collected 1 artifacts |
| GitRepository/flux-system/flux-system | Normal | GitOperationSucceeded | 2 | 14:17:17 | main@sha1:bee102dbf8c9 | no changes since last reconciliation: observed revision 'main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a' |
| GitRepository/flux-system/idp-writer | Normal | GitOperationSucceeded | 2 | 14:15:50 | main@sha1:bee102dbf8c9 | no changes since last reconciliation: observed revision 'main@sha1:bee102dbf8c92ac69b0ff9fe466355034050cb4a' |
| GitRepository/flux-system/idp-writer | Normal | NewArtifact | 1 | 13:35:26 | main@bee102dbf8c92ac69 | stored artifact for commit 'fix(edge): let cert-manager's HTTP-01 solver past ...' |
| GitRepository/flux-system/prospector | Normal | GitOperationSucceeded | 1 | 14:14:14 | main@sha1:b658a1a8eda1 | no changes since last reconciliation: observed revision 'main@sha1:b658a1a8eda1700b3787c4005cd5660e8cab09bf' |
| HelmChart/cert-manager/cert-manager-cert-manager | Normal | ArtifactUpToDate | 1 | 14:14:31 | - | artifact up-to-date with remote revision: 'v1.21.1' |
| HelmChart/chaos-mesh/chaos-mesh-chaos-mesh | Normal | ArtifactUpToDate | 1 | 14:14:47 | - | artifact up-to-date with remote revision: '2.8.4' |
| HelmChart/edge/edge-external-dns | Normal | ArtifactUpToDate | 1 | 14:15:37 | - | artifact up-to-date with remote revision: '1.21.1' |
| HelmChart/edge/edge-traefik | Normal | ArtifactUpToDate | 1 | 14:14:34 | - | artifact up-to-date with remote revision: '41.3.0' |
| HelmChart/external-secrets/external-secrets-external-secrets | Normal | ArtifactUpToDate | 1 | 14:14:30 | - | artifact up-to-date with remote revision: '2.9.0' |
| HelmChart/healing/healing-descheduler | Normal | ArtifactUpToDate | 1 | 14:09:37 | - | artifact up-to-date with remote revision: '0.36.0' |
| HelmChart/healing/healing-k8sgpt-operator | Normal | ArtifactUpToDate | 1 | 14:09:44 | - | artifact up-to-date with remote revision: '0.2.29' |
| HelmChart/hindsight/hindsight-hindsight | Normal | ArtifactUpToDate | 1 | 14:15:13 | - | artifact up-to-date with remote revision: '0.9.2' |
| HelmChart/identity/identity-oauth2-proxy | Normal | ArtifactUpToDate | 1 | 14:08:41 | - | artifact up-to-date with remote revision: '10.7.0' |
| HelmChart/keda/keda-keda | Normal | ArtifactUpToDate | 1 | 14:13:28 | - | artifact up-to-date with remote revision: '2.20.2' |
| HelmChart/keda/keda-keda-add-ons-http | Normal | ArtifactUpToDate | 1 | 14:10:34 | - | artifact up-to-date with remote revision: '0.15.0' |
| HelmChart/kyverno/kyverno-kyverno | Normal | ArtifactUpToDate | 1 | 14:16:57 | - | artifact up-to-date with remote revision: '3.9.0' |
| HelmChart/metrics-server/metrics-server-metrics-server | Normal | ArtifactUpToDate | 1 | 14:16:46 | - | artifact up-to-date with remote revision: '3.14.0' |
| HelmChart/monitoring/monitoring-blackbox | Normal | ArtifactUpToDate | 1 | 14:14:12 | - | artifact up-to-date with remote revision: '11.17.2' |
| HelmChart/monitoring/monitoring-kube-prometheus-stack | Normal | ArtifactUpToDate | 1 | 14:10:03 | - | artifact up-to-date with remote revision: '88.6.0' |
| HelmChart/observability/observability-langfuse | Normal | ArtifactUpToDate | 1 | 14:17:24 | - | artifact up-to-date with remote revision: '2.0.2' |
| HelmChart/observability/observability-signoz | Normal | ArtifactUpToDate | 1 | 14:15:03 | - | artifact up-to-date with remote revision: '0.138.0' |
| HelmChart/observability-agent/observability-agent-k8s-infra | Normal | ArtifactUpToDate | 1 | 14:15:36 | - | artifact up-to-date with remote revision: '0.17.0' |
| HelmChart/reloader/reloader-reloader | Normal | ArtifactUpToDate | 1 | 14:16:25 | - | artifact up-to-date with remote revision: '2.2.16' |
| HelmChart/robusta/robusta-robusta | Normal | ArtifactUpToDate | 1 | 14:17:51 | - | artifact up-to-date with remote revision: '0.48.0' |
| HelmChart/spire-mgmt/spire-mgmt-spire | Normal | ArtifactUpToDate | 1 | 14:12:25 | - | artifact up-to-date with remote revision: '0.30.1' |
| HelmChart/spire-mgmt/spire-mgmt-spire-crds | Normal | ArtifactUpToDate | 1 | 14:10:05 | - | artifact up-to-date with remote revision: '0.6.1' |
| HelmChart/tailscale/tailscale-tailscale-operator | Normal | ArtifactUpToDate | 1 | 14:18:21 | - | artifact up-to-date with remote revision: '1.102.3' |
| HelmChart/temporal/temporal-temporal | Normal | ArtifactUpToDate | 1 | 14:01:00 | - | artifact up-to-date with remote revision: '1.6.0' |
| ImagePolicy/flux-system/sovereign-worker | Normal | Succeeded | 1 | 13:39:58 | - | Latest image tag for ghcr.io/chidionyema/sovereign-worker resolved to main-3199-bee102dbf8c92ac69b0ff9fe466355034050cb4a (previously ghcr.io/chidionyema/sovereign-worker:main-3190-163d6cd80ed13f49faf85032005e6580fa070501 |
| ImageRepository/flux-system/backstage | Normal | Succeeded | 1 | 14:16:31 | - | tags did not change, next scan in 1m0s |
| ImageRepository/flux-system/estate-mcp | Normal | Succeeded | 1 | 14:17:42 | - | tags did not change, next scan in 5m0s |
| ImageRepository/flux-system/hermes-agent | Normal | Succeeded | 1 | 14:17:37 | - | tags did not change, next scan in 5m0s |
| ImageRepository/flux-system/prospector-store-api | Normal | Succeeded | 1 | 14:14:59 | - | tags did not change, next scan in 5m0s |
| ImageRepository/flux-system/prospector-store-web | Normal | Succeeded | 1 | 14:14:59 | - | tags did not change, next scan in 5m0s |
| ImageRepository/flux-system/sovereign-worker | Normal | Succeeded | 2 | 14:15:02 | - | tags did not change, next scan in 5m0s |
| ImageUpdateAutomation/flux-system/backstage | Normal | Succeeded | 1 | 14:18:24 | - | repository up-to-date |
| Kustomization/flux-system/alerts | Normal | DependencyNotReady | 1 | 13:36:40 | main@bee102dbf8c92ac69 | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/alerts | Normal | ReconciliationSucceeded | 7 | 14:16:58 | main@bee102dbf8c92ac69 | Reconciliation finished in 583.063372ms, next run in 10m0s |
| Kustomization/flux-system/alerts-github | Normal | DependencyNotReady | 1 | 13:36:05 | main@bee102dbf8c92ac69 | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/alerts-github | Normal | ReconciliationSucceeded | 7 | 14:16:51 | main@bee102dbf8c92ac69 | Reconciliation finished in 861.98294ms, next run in 10m0s |
| Kustomization/flux-system/alerts-secret | Normal | DependencyNotReady | 1 | 13:36:05 | main@bee102dbf8c92ac69 | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/alerts-secret | Normal | ReconciliationSucceeded | 7 | 14:16:29 | main@bee102dbf8c92ac69 | Reconciliation finished in 572.446056ms, next run in 10m0s |
| Kustomization/flux-system/autoscaler | Normal | DependencyNotReady | 1 | 13:36:05 | main@bee102dbf8c92ac69 | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/autoscaler | Normal | ReconciliationSucceeded | 7 | 14:17:51 | main@bee102dbf8c92ac69 | Reconciliation finished in 612.143089ms, next run in 10m0s |
| Kustomization/flux-system/backstage | Normal | DependencyNotReady | 1 | 13:36:02 | main@163d6cd80ed13f49f | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/backstage | Normal | ReconciliationSucceeded | 6 | 14:17:03 | main@bee102dbf8c92ac69 | Reconciliation finished in 1.751537861s, next run in 10m0s |
| Kustomization/flux-system/backstage-namespace | Normal | ReconciliationSucceeded | 7 | 14:14:53 | main@bee102dbf8c92ac69 | Reconciliation finished in 534.733924ms, next run in 10m0s |
| Kustomization/flux-system/chaos | Normal | DependencyNotReady | 1 | 13:36:38 | main@163d6cd80ed13f49f | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/chaos | Normal | ReconciliationSucceeded | 5 | 14:06:50 | main@bee102dbf8c92ac69 | Reconciliation finished in 727.142506ms, next run in 10m0s |
| Kustomization/flux-system/chaos-mesh | Normal | DependencyNotReady | 1 | 13:36:02 | main@163d6cd80ed13f49f | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/chaos-mesh | Normal | ReconciliationSucceeded | 6 | 14:16:04 | main@bee102dbf8c92ac69 | Reconciliation finished in 600.054797ms, next run in 10m0s |
| Kustomization/flux-system/cluster-state | Normal | DependencyNotReady | 1 | 13:36:02 | main@163d6cd80ed13f49f | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/cluster-state | Normal | ReconciliationSucceeded | 6 | 14:16:36 | main@bee102dbf8c92ac69 | Reconciliation finished in 1.180034496s, next run in 10m0s |
| Kustomization/flux-system/dns | Normal | DependencyNotReady | 1 | 13:36:02 | main@163d6cd80ed13f49f | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/dns | Normal | ReconciliationSucceeded | 6 | 14:16:41 | main@bee102dbf8c92ac69 | Reconciliation finished in 573.244945ms, next run in 10m0s |
| Kustomization/flux-system/drills | Normal | DependencyNotReady | 1 | 13:36:38 | main@bee102dbf8c92ac69 | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/drills | Normal | ReconciliationSucceeded | 7 | 14:16:40 | main@bee102dbf8c92ac69 | Reconciliation finished in 688.040719ms, next run in 10m0s |
| Kustomization/flux-system/edge | Normal | DependencyNotReady | 1 | 13:35:31 | main@bee102dbf8c92ac69 | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/edge | Normal | Progressing | 3 | 14:16:13 | main@1b9d2cfc31b972835 | ClusterPolicy/secrets-not-from-env-vars configured |
| Kustomization/flux-system/edge | Normal | ReconciliationSucceeded | 5 | 14:16:13 | main@bee102dbf8c92ac69 | Reconciliation finished in 1.399802577s, next run in 10m0s |
| Kustomization/flux-system/estate-catalog | Normal | ReconciliationSucceeded | 6 | 14:11:02 | latest@sha256:ebf7e038 | Reconciliation finished in 509.998134ms, next run in 10m0s |
| Kustomization/flux-system/external-secrets | Normal | ReconciliationSucceeded | 7 | 14:17:05 | main@bee102dbf8c92ac69 | Reconciliation finished in 591.538864ms, next run in 10m0s |
| Kustomization/flux-system/flux-system | Normal | ReconciliationSucceeded | 7 | 14:15:42 | main@bee102dbf8c92ac69 | Reconciliation finished in 2.090830288s, next run in 10m0s |
| Kustomization/flux-system/gateway-api-crds | Normal | ReconciliationSucceeded | 7 | 14:16:39 | v1.5.1@e7677b70ae75d14 | Reconciliation finished in 2.95476969s, next run in 10m0s |
| Kustomization/flux-system/guacamole | Normal | DependencyNotReady | 1 | 13:35:35 | main@2f0a1012d6f3e3e6a | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/guacamole | Normal | Progressing | 1 | 13:30:29 | main@163d6cd80ed13f49f | Namespace/guacamole created ConfigMap/guacamole/guacamole-env created ConfigMap/guacamole/guacamole-seed created Service/guacamole/founder-mac-vnc created Service/guacamole/guacamole created Service/guacamole/guacamole-d |
| Kustomization/flux-system/guacamole | Normal | ReconciliationSucceeded | 4 | 14:16:19 | main@bee102dbf8c92ac69 | Reconciliation finished in 1.704044301s, next run in 10m0s |
| Kustomization/flux-system/healing | Normal | DependencyNotReady | 1 | 13:36:34 | main@163d6cd80ed13f49f | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/healing | Normal | ReconciliationSucceeded | 6 | 14:16:55 | main@bee102dbf8c92ac69 | Reconciliation finished in 686.30918ms, next run in 10m0s |
| Kustomization/flux-system/healing-analyzer | Normal | DependencyNotReady | 1 | 13:36:37 | main@163d6cd80ed13f49f | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/healing-analyzer | Normal | ReconciliationSucceeded | 6 | 14:17:39 | main@bee102dbf8c92ac69 | Reconciliation finished in 546.642173ms, next run in 10m0s |
| Kustomization/flux-system/healthchecks | Normal | DependencyNotReady | 1 | 13:36:02 | main@163d6cd80ed13f49f | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/healthchecks | Normal | ReconciliationSucceeded | 6 | 14:16:52 | main@bee102dbf8c92ac69 | Reconciliation finished in 1.371261385s, next run in 10m0s |
| Kustomization/flux-system/hermes-agent | Normal | DependencyNotReady | 1 | 13:36:36 | main@163d6cd80ed13f49f | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/hermes-agent | Normal | ReconciliationSucceeded | 5 | 14:10:24 | main@bee102dbf8c92ac69 | Reconciliation finished in 1.577424917s, next run in 10m0s |
| Kustomization/flux-system/hindsight | Normal | DependencyNotReady | 1 | 13:36:33 | main@163d6cd80ed13f49f | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/hindsight | Normal | ReconciliationSucceeded | 6 | 14:16:11 | main@bee102dbf8c92ac69 | Reconciliation finished in 845.230276ms, next run in 10m0s |
| Kustomization/flux-system/identity | Normal | DependencyNotReady | 1 | 13:36:02 | main@163d6cd80ed13f49f | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/identity | Normal | ReconciliationSucceeded | 6 | 14:16:18 | main@bee102dbf8c92ac69 | Reconciliation finished in 1.116519881s, next run in 10m0s |
| Kustomization/flux-system/image-automation | Normal | DependencyNotReady | 1 | 13:36:05 | main@bee102dbf8c92ac69 | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/image-automation | Normal | ReconciliationSucceeded | 7 | 14:16:23 | main@bee102dbf8c92ac69 | Reconciliation finished in 812.905164ms, next run in 10m0s |
| Kustomization/flux-system/keda | Normal | DependencyNotReady | 1 | 13:36:39 | main@bee102dbf8c92ac69 | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/keda | Normal | ReconciliationSucceeded | 7 | 14:17:33 | main@bee102dbf8c92ac69 | Reconciliation finished in 648.455286ms, next run in 10m0s |
| Kustomization/flux-system/kyverno | Normal | ReconciliationSucceeded | 7 | 14:15:56 | main@bee102dbf8c92ac69 | Reconciliation finished in 609.46178ms, next run in 10m0s |
| Kustomization/flux-system/llm | Normal | DependencyNotReady | 1 | 13:36:02 | main@163d6cd80ed13f49f | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/llm | Normal | ReconciliationSucceeded | 6 | 14:17:14 | main@bee102dbf8c92ac69 | Reconciliation finished in 1.152829278s, next run in 10m0s |
| Kustomization/flux-system/mcp | Normal | DependencyNotReady | 1 | 13:36:34 | main@163d6cd80ed13f49f | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/mcp | Normal | ReconciliationSucceeded | 6 | 14:16:22 | main@bee102dbf8c92ac69 | Reconciliation finished in 1.364006546s, next run in 10m0s |
| Kustomization/flux-system/metrics-server | Normal | DependencyNotReady | 1 | 13:36:34 | main@163d6cd80ed13f49f | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/metrics-server | Normal | ReconciliationSucceeded | 6 | 14:16:02 | main@bee102dbf8c92ac69 | Reconciliation finished in 570.612595ms, next run in 10m0s |
| Kustomization/flux-system/monitoring | Normal | DependencyNotReady | 1 | 13:36:02 | main@163d6cd80ed13f49f | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/monitoring | Normal | ReconciliationSucceeded | 6 | 14:17:09 | main@bee102dbf8c92ac69 | Reconciliation finished in 909.159815ms, next run in 10m0s |
| Kustomization/flux-system/monitoring-rules | Normal | DependencyNotReady | 1 | 13:36:02 | main@163d6cd80ed13f49f | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/monitoring-rules | Normal | ReconciliationSucceeded | 6 | 14:16:09 | main@bee102dbf8c92ac69 | Reconciliation finished in 785.491584ms, next run in 10m0s |
| Kustomization/flux-system/observability | Normal | DependencyNotReady | 1 | 13:36:02 | main@163d6cd80ed13f49f | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/observability | Normal | Progressing | 1 | 13:46:13 | main@bee102dbf8c92ac69 | Job/observability/langfuse-clickhouse-database created |
| Kustomization/flux-system/observability | Normal | ReconciliationSucceeded | 6 | 14:15:30 | main@bee102dbf8c92ac69 | Reconciliation finished in 1.796913876s, next run in 10m0s |
| Kustomization/flux-system/observability-collector | Normal | DependencyNotReady | 1 | 14:06:16 | main@163d6cd80ed13f49f | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/observability-collector | Normal | ReconciliationSucceeded | 6 | 14:17:05 | main@bee102dbf8c92ac69 | Reconciliation finished in 880.915667ms, next run in 10m0s |
| Kustomization/flux-system/priority-classes | Normal | ReconciliationSucceeded | 7 | 14:14:44 | main@bee102dbf8c92ac69 | Reconciliation finished in 647.233913ms, next run in 10m0s |
| Kustomization/flux-system/prospector | Normal | Progressing | 1 | 14:12:50 | main@cf53d01945b892ed5 | ClusterPolicy/secrets-not-from-env-vars configured |
| Kustomization/flux-system/prospector | Normal | ReconciliationSucceeded | 6 | 14:12:50 | main@b658a1a8eda1700b3 | Reconciliation finished in 6.407367218s, next run in 10m0s |
| Kustomization/flux-system/prospector-platform | Normal | DependencyNotReady | 1 | 13:36:02 | main@163d6cd80ed13f49f | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/prospector-platform | Normal | ReconciliationSucceeded | 6 | 14:17:20 | main@bee102dbf8c92ac69 | Reconciliation finished in 648.605968ms, next run in 10m0s |
| Kustomization/flux-system/reloader | Normal | DependencyNotReady | 1 | 13:36:05 | main@bee102dbf8c92ac69 | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/reloader | Normal | ReconciliationSucceeded | 7 | 14:17:42 | main@bee102dbf8c92ac69 | Reconciliation finished in 502.617573ms, next run in 10m0s |
| Kustomization/flux-system/robusta | Normal | DependencyNotReady | 1 | 13:35:35 | main@bee102dbf8c92ac69 | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/robusta | Normal | ReconciliationSucceeded | 7 | 14:15:48 | main@bee102dbf8c92ac69 | Reconciliation finished in 956.493852ms, next run in 10m0s |
| Kustomization/flux-system/scheduling | Normal | DependencyNotReady | 1 | 13:36:02 | main@163d6cd80ed13f49f | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/scheduling | Normal | ReconciliationSucceeded | 6 | 14:16:45 | main@bee102dbf8c92ac69 | Reconciliation finished in 726.759182ms, next run in 10m0s |
| Kustomization/flux-system/science | Normal | DependencyNotReady | 1 | 13:36:38 | main@163d6cd80ed13f49f | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/science | Normal | ReconciliationSucceeded | 6 | 14:17:05 | main@bee102dbf8c92ac69 | Reconciliation finished in 955.217638ms, next run in 10m0s |
| Kustomization/flux-system/secret-store | Normal | DependencyNotReady | 1 | 13:35:34 | main@bee102dbf8c92ac69 | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/secret-store | Normal | ReconciliationSucceeded | 7 | 14:16:09 | main@bee102dbf8c92ac69 | Reconciliation finished in 785.232821ms, next run in 10m0s |
| Kustomization/flux-system/spire | Normal | DependencyNotReady | 1 | 13:36:02 | main@163d6cd80ed13f49f | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/spire | Normal | ReconciliationSucceeded | 6 | 14:18:16 | main@bee102dbf8c92ac69 | Reconciliation finished in 735.616039ms, next run in 10m0s |
| Kustomization/flux-system/staging | Normal | ReconciliationSucceeded | 7 | 14:15:30 | main@bee102dbf8c92ac69 | Reconciliation finished in 802.196166ms, next run in 10m0s |
| Kustomization/flux-system/tailscale | Normal | DependencyNotReady | 1 | 13:36:05 | main@bee102dbf8c92ac69 | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/tailscale | Normal | Progressing | 1 | 13:22:20 | main@163d6cd80ed13f49f | Health check passed in 44.602007ms |
| Kustomization/flux-system/tailscale | Normal | ReconciliationSucceeded | 7 | 14:15:58 | main@bee102dbf8c92ac69 | Reconciliation finished in 620.773944ms, next run in 10m0s |
| Kustomization/flux-system/verification | Normal | DependencyNotReady | 1 | 13:36:05 | main@bee102dbf8c92ac69 | Dependencies do not meet ready condition, retrying in 30s |
| Kustomization/flux-system/verification | Normal | ReconciliationSucceeded | 7 | 14:16:14 | main@bee102dbf8c92ac69 | Reconciliation finished in 479.355758ms, next run in 10m0s |
| OCIRepository/flux-system/estate-catalog | Normal | ArtifactUpToDate | 1 | 14:14:35 | - | artifact up-to-date with remote revision: 'latest@sha256:ebf7e038adf9e04d44d831db0cf4356ed00d82fc6b4db860ff49e45645e548cf' |
