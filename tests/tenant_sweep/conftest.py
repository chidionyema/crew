import sys
from pathlib import Path

# Make `tenant_sweep` importable when pytest runs from the repo root.
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
