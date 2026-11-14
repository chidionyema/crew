"""The estate-guards files vendored into crew are byte-for-byte the pinned commit's (estate-guards is private)."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIN = json.loads((ROOT / ".estate-guards-pin.json").read_text())


def test_every_vendored_file_matches_its_pin():
    assert len(PIN["commit"]) == 40 and PIN["sha256"]
    for rel, digest in PIN["sha256"].items():
        assert hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() == digest, f"{rel} drifted from {PIN['commit']}"


def test_no_workflow_checks_out_the_private_repository():
    for wf in (ROOT / ".github" / "workflows").glob("*.y*ml"):
        text = wf.read_text()
        assert "repository: chidionyema/claude-guards" not in text and "repository: chidionyema/estate-guards" not in text, wf.name
