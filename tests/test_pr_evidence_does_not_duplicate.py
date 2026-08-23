"""A refused push must not cost the repository another copy of the evidence.

INCIDENT, 2026-08-23. `pr-evidence.py attach` copies the image, commits it, and only
then pushes. Pushes are refused here as a matter of routine — the branch-freshness
fence refuses a branch behind main, the dead-branch guard refuses a branch whose pull
request has already merged. When the push was refused the commit still stood, so the
retry minted a new timestamp and committed the same bytes a second time.

Measured on prospector origin/main that day: docs/evidence/pr-669/ held three
byte-identical 106 KB copies, every one sha256 80291a6991ea..., and pr-674 collected
two the same way. Nobody noticed, because a duplicate screenshot still reads as
evidence.

These tests assert the RULE, not the implementation: attaching bytes that are already
there adds nothing, and attaching genuinely new bytes still adds a file.
"""

from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "pr-evidence.py"


def _load():
    spec = importlib.util.spec_from_file_location("pr_evidence", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _attach(mod, dest: Path, src: Path, stamp: str) -> str:
    """The naming half of one attach run, including the copy it decides on."""
    name, write = mod.evidence_name(dest, src, stamp, 1)
    if write:
        shutil.copyfile(src, dest / name)
    return name


def test_retrying_a_refused_push_adds_no_second_copy(tmp_path):
    mod = _load()
    dest = tmp_path / "pr-674"
    dest.mkdir()
    src = tmp_path / "gate.png"
    src.write_bytes(b"\x89PNG python: PASS (8278 passed, 0 failed)")

    first = _attach(mod, dest, src, "20260823T191647Z")
    # The push is refused. The operator runs the identical command again, later, so the
    # timestamp it would use is different.
    second = _attach(mod, dest, src, "20260823T191712Z")

    assert first == second, "the retry took a new name and duplicated the evidence"
    assert len(list(dest.iterdir())) == 1


def test_a_genuinely_new_image_is_still_added(tmp_path):
    """The fix must not turn the folder into a single-image store."""
    mod = _load()
    dest = tmp_path / "pr-674"
    dest.mkdir()
    gate = tmp_path / "gate.png"
    gate.write_bytes(b"\x89PNG python: PASS")
    deploy = tmp_path / "deploy.png"
    deploy.write_bytes(b"\x89PNG deploy-engine: success")

    a = _attach(mod, dest, gate, "20260823T191647Z")
    b = _attach(mod, dest, deploy, "20260823T191712Z")

    assert a != b
    assert len(list(dest.iterdir())) == 2


def test_the_name_is_reused_whatever_the_source_path_was(tmp_path):
    """Identity is the bytes, not the filename it arrived under.

    The same screenshot re-taken into a different scratch path is the same evidence.
    Keying on the source name would have let that duplicate.
    """
    mod = _load()
    dest = tmp_path / "pr-674"
    dest.mkdir()
    one = tmp_path / "a" / "shot.png"
    one.parent.mkdir()
    one.write_bytes(b"\x89PNG identical")
    two = tmp_path / "b" / "totally-different-name.png"
    two.parent.mkdir()
    two.write_bytes(b"\x89PNG identical")

    assert _attach(mod, dest, one, "20260823T191647Z") == _attach(
        mod, dest, two, "20260823T191712Z"
    )
    assert len(list(dest.iterdir())) == 1
