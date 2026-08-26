"""Incident, 2026-08-26 (crew#319, crew#320): `datamap.py` graded 38 Mac stores from a
hand-typed table while 279 inventory rows, every cluster workload, every hostname, every
hook, every MCP server and every workflow had no verdict at all. The transcript row sat
diagnosed in source for two days because nothing failed.

The rule, not the code: every discovered producer carries a verdict or the gate is red;
every gap carries a ticket or the gate is red; a discoverer that goes blind says so or the
census catches it. Rung 4 (incident) with a rung 2 property inside: the closed world holds
for any producer, not the ones listed today.
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

import pytest

SCIENCE = pathlib.Path(__file__).resolve().parents[1] / "science"
sys.path.insert(0, str(SCIENCE))
import datamap  # noqa: E402
import producers  # noqa: E402

REG = {"version": 1, "blind_allowed": {},
       "entries": [
           {"key": "mac/ledger/*", "verdict": "COLLECTED", "reader": "collect.py", "why": ""},
           {"key": "act/x", "verdict": "NEVER_EMITTED", "why": "nothing writes it", "ticket": "crew#1"},
       ]}


def _prod(key: str, kind: str = "ledger") -> dict:
    return {"domain": key.split("/")[0], "key": key, "kind": kind, "measures": ["rows"], "evidence": "t"}


def test_a_producer_the_register_does_not_name_is_unexplained_and_fails_the_gate():
    graded = datamap.grade([_prod("mac/ledger/a"), _prod("mac/data/b", "data"), _prod("act/x", "act")], REG)
    verdicts = {g["key"]: g["verdict"] for g in graded}
    assert verdicts == {"mac/ledger/a": "COLLECTED", "mac/data/b": "UNEXPLAINED", "act/x": "NEVER_EMITTED"}
    bad = datamap.violations(graded, {}, REG, [])
    assert any("1 producer(s) UNEXPLAINED" in b for b in bad), bad


def test_the_same_gate_is_green_when_every_producer_has_a_verdict_and_every_gap_a_ticket():
    graded = datamap.grade([_prod("mac/ledger/a"), _prod("act/x", "act")], REG)
    assert datamap.violations(graded, {}, REG, []) == []


def test_a_gap_without_a_ticket_is_red_even_when_nothing_is_unexplained():
    reg = {**REG, "entries": [{"key": "act/x", "verdict": "NEVER_EMITTED", "why": "w", "ticket": ""}]}
    graded = datamap.grade([_prod("act/x", "act")], reg)
    bad = datamap.violations(graded, {}, reg, [])
    assert bad and "without a ticket" in bad[0], bad


def test_a_blind_domain_is_red_unless_the_register_allows_it_by_name():
    graded = datamap.grade([_prod("mac/ledger/a")], REG)
    assert any("BLIND and not allowed" in b for b in datamap.violations(graded, {"cluster_live": "no oci"}, REG, []))
    allowed = {**REG, "blind_allowed": {"cluster_live": "crew#345"}}
    assert datamap.violations(graded, {"cluster_live": "no oci"}, allowed, []) == []


def test_a_discoverer_that_returns_nothing_without_raising_is_caught(tmp_path, monkeypatch):
    monkeypatch.setattr(datamap, "CENSUS", tmp_path / "census.json")
    (tmp_path / "census.json").write_text('{"domains": {"mac": 100, "hook": 34}}')
    graded = datamap.grade([_prod("mac/ledger/a")] * 10, REG)   # mac: 10 of 100, hook: 0
    msgs = datamap.census_check(graded, blind={})
    assert any(m.startswith("mac: 10 members, was 100") for m in msgs), msgs
    assert any(m.startswith("hook: 0 members and not BLIND") for m in msgs), msgs
    # ... and the same shrink is fine when the domain said BLIND
    assert not [m for m in datamap.census_check(graded, blind={"mac": "x", "hook": "y"}) if m.startswith(("mac:", "hook:"))]


def test_every_domain_raises_rather_than_answering_partially_when_its_world_is_missing(monkeypatch, tmp_path):
    """Property over the domain table: point each world at nothing and it must raise (become
    BLIND), never return []. A silent [] is the class of failure this file exists for."""
    monkeypatch.setattr(producers, "INVENTORY", tmp_path / "none.json")
    monkeypatch.setattr(producers, "WAREHOUSE", tmp_path / "none.db")
    monkeypatch.setattr(producers, "IDP", tmp_path / "no-idp")
    monkeypatch.setattr(producers, "OKE_KUBECONFIG", tmp_path / "no-kube")
    monkeypatch.setattr(producers, "CLAUDE_HOME", tmp_path / "no-claude")
    monkeypatch.setattr(producers, "HOME", tmp_path)
    for name in ("mac", "warehouse", "cluster", "cluster_live", "endpoint", "hook", "transcript"):
        with pytest.raises((OSError, RuntimeError, KeyError, ValueError, StopIteration)):
            producers.DOMAINS[name]()


def test_the_shipped_register_is_well_formed():
    reg = datamap.register()
    assert reg["entries"], "an empty register explains nothing"
    keys = [e["key"] for e in reg["entries"] if e["key"].startswith("act/")]
    assert len(keys) == len(set(keys))


def test_the_cli_grades_the_act_domain_offline():
    r = subprocess.run([sys.executable, str(SCIENCE / "datamap.py"), "--domains", "act"],
                       capture_output=True, text=True, timeout=120, check=False)
    assert r.returncode == 0, r.stderr[-800:]
    assert "DATA MAP" in r.stdout and "act " in r.stdout
