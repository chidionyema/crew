# R38: the founder dashboard is Backstage, god's view across all

Founder, 2026-08-27, verbatim: "why cant we have founders dashboard in backstage rather than nother ui" ... "gids view renenber and nevr niss a beat" ... "across all".

He also pasted a plan from another tool (a GitHub App, the Kubernetes Dashboard with a cluster-admin token behind `kubectl proxy`, a GitHub Project, `platform_bootstrap.sh` / `platform_inventory.py` / `platform_predictor.py`, `git add -A`) and said: "this is an idea but i know we can do exponentially better".

## Meaning

- The founder's dashboard is the Backstage portal in `idp`. Never a second UI.
- God's view: every repo, service, cluster, board and science page is reachable from the founder entities in the catalog. Pages render through TechDocs; the cluster through the Kubernetes plugin; the board through GitHub issues on the entity.
- Remember: it is durable and generated from what runs. Nothing hand-drawn, nothing that lives in one session.
- Never miss a beat: an estate surface that is not in the catalog is a defect. The crew#401 gate refuses it.
- A proposal that adds a K8s Dashboard, a GitHub Project or a glue script beside Backstage is the stitched version, and is refused.

## Tracked item

crew#412, one row per surface.
