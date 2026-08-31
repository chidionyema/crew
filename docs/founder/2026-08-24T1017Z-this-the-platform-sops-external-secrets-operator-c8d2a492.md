---
captured: 2026-08-24T10:17:23+00:00
session: d7dfd2d4-8c4e-4c11-b1a0-a3643af6c41d
cwd: /Users/chidionyema/dev/code/crew
chars: 4009
source: founder prompt, verbatim (founder-doc-capture.py)
---

this 🏗️ The Platform: SOPS + External Secrets Operator
No server. No database. No paid tier. £0 forever.
plain
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Git Repo      │────▶│  ESO Controller  │────▶│  k8s Secret   │
│ secrets/*.yaml  │     │  (reads SOPS)    │     │  (in-cluster) │
│ (encrypted)     │     │                  │     │                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
         │                                               │
         │  Today: age key on Mac                        │  Tomorrow: app reads
         ▼                                               ▼
   sops --decrypt                                  env var / file mount
Same files. Same encryption. The only thing that changes is WHERE the age private key lives.
🔐 Full Lifecycle (No Scripts, One Tool: sops)
Table
Lifecycle    Command    What happens
Add    sops secrets/prod/db.yaml    Opens editor, encrypts on save
Rotate    sops rotate -i secrets/prod/db.yaml    Re-encrypts with new data key
Revoke    git rm secrets/prod/db.yaml + rotate all others    Gone from git, old key useless
Audit    git log --all -- secrets/prod/db.yaml    Who changed what, when
Add recipient    Edit .sops.yaml, sops updatekeys secrets/**/*.yaml    New team member can decrypt
Remove recipient    Edit .sops.yaml, sops updatekeys secrets/**/*.yaml    Old key can't read new files
No custom scripts. No secret-add. No secret-load. Just sops and git.
☸️ K8s Bridge (External Secrets Operator)
ESO is open source, CNCF-adjacent, runs in any cluster. It reads the SAME encrypted files from git.
yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: minimax
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: sops-store
    kind: SecretStore
  target:
    name: minimax-api-key
    creationPolicy: Owner
  data:
    - secretKey: MINIMAX_API_KEY
      remoteRef:
        key: secrets/prod/minimax.yaml
        property: MINIMAX_API_KEY
Your app code doesn't change. It reads MINIMAX_API_KEY from env. Whether that env came from sops --decrypt on your Mac or ESO in a pod — the app can't tell.
🚫 Why Everything Else Is Ruled Out
Table
Tool    Why it dies under R14
HashiCorp Vault    Needs a server, needs HA, needs storage, violates R14
1Password / Doppler    Paid tier for teams, not open source
Sealed Secrets    K8s-only, needs controller running, useless on Mac today
Infisical    Needs PostgreSQL + Redis = infrastructure before proof
AWS/GCP/Azure KMS    Cloud lock-in, costs money, not open source
SOPS + ESO is the only stack that is:
✅ Open source (Mozilla + CNCF)
✅ £0 forever (age = no KMS fees)
✅ Works on Mac today (no server)
✅ Works in k8s tomorrow (ESO controller)
✅ Full audit trail (git history)
✅ Key rotation built in (sops rotate)
🎯 What You Commit Now
bash
cd ~/dev/code/crew

# 1. The .sops.yaml (already done, but clean)
cat > secrets/.sops.yaml << 'EOF'
creation_rules:
  - path_regex: secrets/.*\.yaml$
    age: <ESTATE_PUB_KEY>
EOF

# 2. The ESO SecretStore (for when k8s exists)
mkdir -p deploy/k8s/base
cat > deploy/k8s/base/secretstore.yaml << 'EOF'
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: estate-vault
spec:
  provider:
    sops:
      # age key mounted from a k8s Secret
EOF

# 3. The pre-commit guard (blocks unencrypted)
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
for f in $(git diff --cached --name-only | grep '^secrets/.*\.yaml$'); do
  grep -q "^sops:" "$f" || { echo "UNENCRYPTED: $f"; exit 1; }
done
EOF
chmod +x .git/hooks/pre-commit

git add secrets/ deploy/k8s/base/ .git/hooks/pre-commit
git commit -m "feat: estate secrets platform (SOPS + ESO, R14-clean)"
📋 Handoff
🟢 Guard migration: PR #30 merged, 95/95, 9 rules in Rego
🟡 Awaiting: MINIMAX_API_KEY for first sops secrets/dev/minimax.yaml
🟡 Legacy migration: 25 keys in prospector blob → run when you say
🟢 Platform: SOPS + ESO, no alternatives fit R14
⏸️ K8s: ESO manifests ready, cluster follows proof
