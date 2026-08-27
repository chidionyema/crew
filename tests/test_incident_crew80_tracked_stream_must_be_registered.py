"""crew#80: law_enforcement tracked a stream whose writer no longer existed, so
the lawenforcement check was red for five days with nothing to fix.

Rule: a tracked stream is a name in science/sources.json. A name not in the
registry raises; a registered one resolves to its path under the home root.
Rung 4, incident test.
"""
import json

import pytest

from science import law_enforcement as le


def test_every_tracked_stream_is_registered_under_home():
    paths = le.stream_paths()
    assert len(paths) == len(le.TRACKED_STREAMS)
    assert all(p.startswith(le.H) for _, p in paths)
    assert not any("one-branch" in n for n, _ in paths)


def test_unregistered_tracked_stream_refuses(tmp_path, monkeypatch):
    reg = tmp_path / "sources.json"
    reg.write_text(json.dumps({"sources": [
        {"name": n, "root": "home", "path": f".claude/{n}.jsonl"}
        for n in le.TRACKED_STREAMS if n != "spend"]}))
    with pytest.raises(KeyError, match="spend"):
        le.stream_paths(sources=str(reg), home=str(tmp_path))
    reg.write_text(json.dumps({"sources": [
        {"name": n, "root": "home", "path": f".claude/{n}.jsonl"}
        for n in le.TRACKED_STREAMS]}))
    got = le.stream_paths(sources=str(reg), home=str(tmp_path))
    assert [n for n, _ in got] == [f".claude/{n}.jsonl" for n in le.TRACKED_STREAMS]
