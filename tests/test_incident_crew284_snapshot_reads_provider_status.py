"""Incident (crew#284, 2026-08-26): 25 minutes of pending CI attributed to our branches.

githubstatus.com reported Actions=major_outage the whole time. The estate snapshot is the
file every session reads first, so it carries the provider's own status: RED when Actions
is anything but operational, NOT RUN when the status page cannot be read, never GREEN by
default. Rung 4; drives github_actions() through a fake sh.
"""
from __future__ import annotations

import importlib.util
import json
from importlib.machinery import SourceFileLoader
from pathlib import Path

SNAP = Path(__file__).resolve().parents[1] / "scripts" / "estate-snapshot"


def _load():
    loader = SourceFileLoader("estate_snapshot_284", str(SNAP))
    spec = importlib.util.spec_from_file_location("estate_snapshot_284", SNAP, loader=loader)
    assert spec is not None, SNAP
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


def _row(monkeypatch, rc, body):
    mod = _load()
    monkeypatch.setattr(mod, "sh", lambda cmd, timeout=30: (rc, body))
    return mod.github_actions()[0]


def _page(status):
    return json.dumps({"components": [{"name": "Git Operations", "status": "operational"}, {"name": "Actions", "status": status}]})


def test_outage_is_a_red_row(monkeypatch) -> None:
    row = _row(monkeypatch, 0, _page("major_outage"))
    assert "RED major_outage" in row


def test_operational_is_green(monkeypatch) -> None:
    assert "GREEN operational" in _row(monkeypatch, 0, _page("operational"))


def test_unreadable_page_is_not_run_never_green(monkeypatch) -> None:
    assert "NOT RUN" in _row(monkeypatch, 7, "")
    assert "NOT RUN" in _row(monkeypatch, 0, "<html>")
