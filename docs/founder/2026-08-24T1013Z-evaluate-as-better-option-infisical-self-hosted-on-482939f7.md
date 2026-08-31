---
captured: 2026-08-24T10:13:07+00:00
session: 8ef72725-f30e-4d4b-8cb9-791f03f67fdf
cwd: /Users/chidionyema/.claude/projects/-Users-chidionyema/memory
chars: 2101
source: founder prompt, verbatim (founder-doc-capture.py)
---

evaluate as better option Infisical. Self-hosted on your Mac, zero cost, open source (MIT), YC-backed. It is the secrets team member you hire instead of writing another script.
  Why Infisical Fits Your Constraints
  Table
  Your Rule    Infisical Answer
  R14: £0    Self-hosted = free forever. No paid tier needed.
  Mac substrate    Runs in Docker on your Mac today.
  No sysadmin feel    Web UI, not terminal archaeology.
  K8s later, zero rework    Native K8s operator + External Secrets integration.
  Open source    MIT license. You own it.
  What It Replaces
  Instead of this chaos:
  scripts/secret-add (custom, untested)
  scripts/secret-load (custom, untested)
  sops rotate -i (manual, easy to forget)
  Git blame for audit (who changed what when?)
  You get a platform:
  Add: Web UI or infisical secrets set — one command, audited
  Revoke: Delete in UI, instant, versioned in case you need rollback
  Rotate: Built-in rotation policies + webhook triggers
  Audit: Every read, write, and access logged with timestamp + identity
  Access control: Projects + environments (dev/staging/prod) with role-based access
  Versioning: Every secret change is a version. Roll back in one click.
  The Exact Setup (10 Minutes)
  bash
  cd ~/dev/code/crew

  1. Infisical runs locally — your Mac IS the server

  mkdir -p infisical && cd infisical
  curl -o docker-compose.yml https://raw.githubusercontent.com/Infisical/infisical/main/docker-compose.yml
  docker compose up -d

  2. Web UI at http://localhost:8080

  Create one account (you). Create projects: crew, prospector.

  Create environments: dev, staging, prod.

  3. CLI login (agents use this)

  brew install infisical/get-cli/infisical
  infisical login
  infisical init --projectId=crew
  Migration: Your 25 Legacy Keys
  bash
  One-shot import from your current age blob

  bash deploy/secrets.sh list | while read name; do
    val=$(bash deploy/secrets.sh get "$name")
    infisical secrets set "$name"="$val" --env=dev
  done

  Verify

  infisical secrets --env=dev
  Done. 25 keys imported, encrypted at rest, audited from minu
