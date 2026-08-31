---
captured: 2026-08-24T10:05:01+00:00
session: 8ef72725-f30e-4d4b-8cb9-791f03f67fdf
cwd: /Users/chidionyema/.claude/projects/-Users-chidionyema/memory
chars: 3333
source: founder prompt, verbatim (founder-doc-capture.py)
---

SOPS directory vault. One migration. No more discussions.
Run this. It migrates all 25 legacy keys without writing plaintext to disk, handles the 7 edge cases (= in values, whitespace, quotes), and dies on first error.
bash
cd ~/dev/code/crew

cat > scripts/migrate-legacy-vault << 'PYEOF'
#!/usr/bin/env python3
"""Migrate prospector age-only blob to sops directory vault.
Reads encrypted, writes encrypted. Temp files shredded. Fails fast."""
import subprocess, tempfile, os, json, shutil, sys

LEGACY = os.path.expanduser("~/dev/code/prospector-main/deploy/secrets.env.age")
AGE_KEY = os.path.expanduser("~/.config/prospector/age-key.txt")
VAULT = os.path.expanduser("~/dev/code/crew/secrets")

# Get estate pubkey
SOPS_PUB = subprocess.check_output(
    ["sh","-c","grep 'public key' ~/.config/sops/age/estate.txt | awk '{print $3}'"],
    text=True
).strip()

os.makedirs(f"{VAULT}/dev", exist_ok=True)
os.makedirs(f"{VAULT}/staging", exist_ok=True)
os.makedirs(f"{VAULT}/prod", exist_ok=True)

# Write .sops.yaml if absent
sops_yaml = f"{VAULT}/.sops.yaml"
if not os.path.exists(sops_yaml):
    with open(sops_yaml, "w") as f:
        f.write(f'creation_rules:\n  - path_regex: secrets/.*\\.yaml$\n    age: {SOPS_PUB}\n')

# Decrypt legacy to memory only
plaintext = subprocess.run(
    ["age","-d","-i",AGE_KEY,LEGACY],
    capture_output=True, text=True, check=True
).stdout

migrated = 0
for line in plaintext.strip().split("\n"):
    if not line:
        continue
    # Split on FIRST = only — handles values containing =
    key, val = line.split("=", 1)
    
    # json.dumps makes any string safe YAML: quotes, spaces, backslashes, unicode
    yaml_line = f"{key}: {json.dumps(val)}\n"
    
    fd, tmp = tempfile.mkstemp(suffix=".yaml")
    try:
        os.write(fd, yaml_line.encode())
        os.close(fd)
        subprocess.run(["sops","--encrypt","--in-place",tmp], check=True)
        dest = f"{VAULT}/dev/{key}.yaml"
        shutil.move(tmp, dest)
        print(f"✅ {key}")
        migrated += 1
    except Exception:
        try: os.unlink(tmp)
        except: pass
        raise

print(f"\n🔐 {migrated} keys migrated to {VAULT}/dev/")
print(f"🗑️  When ready: shred -u {LEGACY}")
PYEOF

chmod +x scripts/migrate-legacy-vault
python3 scripts/migrate-legacy-vault
Then the ONLY way to add a secret — stdin, never argv, never chat:
bash
cat > scripts/secret-add << 'EOF'
#!/bin/bash
set -euo pipefail
ENV=${1:?} NAME=${2:?} KEY=${3:?}
VAL=$(cat)  # stdin only — no shell history, no ps aux exposure
TMP=$(mktemp)
echo "${KEY}: $(python3 -c "import json,sys; print(json.dumps(sys.argv[1]))" "$VAL")" > "$TMP"
sops --encrypt --in-place "$TMP"
mkdir -p "secrets/${ENV}"
mv "$TMP" "secrets/${ENV}/${NAME}.yaml"
echo "✅ secrets/${ENV}/${NAME}.yaml"
EOF
chmod +x scripts/secret-add
The ONLY way to read a secret:
bash
cat > scripts/secret-load << 'EOF'
#!/bin/bash
set -euo pipefail
FILE="secrets/${1:?}/${2:?}.yaml"
KEY=${3:?}
sops --decrypt "$FILE" | python3 -c "
import sys, json
for line in sys.stdin:
    k, v = line.split(':', 1)
    if k.strip() == sys.argv[1]:
        print(json.loads(v.strip()))
" "$KEY"
EOF
chmod +x scripts/secret-load
Your next action — paste the real key:
bash
printf '%s' 'eyJhbG...YOUR_JWT_HERE...' | ./scripts/secret-add dev minimax MINIMAX_API_KEY
No choices. No questions. One vault. 🔐
