"""crew#274: a workflow that checks out another repository pins it by a full 40-hex sha.

`actions/checkout` with `repository:` set fetches `ref:` from that repository. A short sha
that is not on the default branch cannot be fetched (`fatal: couldn't find remote ref`),
so the job fails before the guard it wanted to run. crew-qa run 33118866962 red on
`ref: 7204084`; the fix was the full sha. A branch name would work but floats, and a
floating pin means a change in the other repository reds this one without a diff here.

Every cross-repository checkout in this repo pins a 40-hex sha, or an expression the
workflow computes (`${{ ... }}`).
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")


def _cross_repo_checkouts():
    for wf in sorted((ROOT / ".github" / "workflows").glob("*.y*ml")):
        doc = yaml.safe_load(wf.read_text(encoding="utf-8")) or {}
        for job_name, job in (doc.get("jobs") or {}).items():
            for step in job.get("steps") or []:
                uses = str(step.get("uses", ""))
                with_ = step.get("with") or {}
                if uses.startswith("actions/checkout") and with_.get("repository"):
                    yield wf.name, job_name, with_.get("repository"), str(with_.get("ref", ""))


def test_every_cross_repo_checkout_pins_a_full_sha() -> None:
    bad = [
        (wf, job, repo, ref)
        for wf, job, repo, ref in _cross_repo_checkouts()
        if not (FULL_SHA.match(ref) or ref.startswith("${{"))
    ]
    assert not bad, f"cross-repo checkout not pinned to a 40-hex sha: {bad}"


def test_the_guard_refuses_a_short_sha() -> None:
    assert not FULL_SHA.match("7204084")
    assert FULL_SHA.match("dc97bcf5ffc174ec371443875b7f785736cbac87")
