"""Incident test, crew#273: a spec, ruling or plan in this repo never makes a vendor-only
channel mandatory (LAW 34). Rung 4: one test, named for the bug. The guard itself is proved
both ways by its --selftest; this asserts the rule over the tree."""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
GUARD = ROOT / ".claude-guards" / "vendor-lock-guard.py"
if not GUARD.is_file():
    GUARD = pathlib.Path.home() / ".claude" / "scripts" / "vendor-lock-guard.py"


def test_incident_crew273_no_spec_mandates_a_vendor_only_channel():
    if not GUARD.is_file():
        import pytest
        pytest.skip("BLIND: vendor-lock-guard not checked out")
    files = [str(f) for top in ("docs", "policy", "roles") for f in (ROOT / top).rglob("*") if f.suffix in {".md", ".feature"}]
    files += [str(f) for f in ROOT.glob("*.md")]
    r = subprocess.run([sys.executable, str(GUARD), "--files", *files], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-2000:]
