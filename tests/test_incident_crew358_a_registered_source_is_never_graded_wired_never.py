"""crew#358: the register graded mac/*jobs/* WIRED_NEVER ("no code refers to any of them") while
science/sources.json already held source job_timelines over the same directory and the
warehouse held 1,445 of its rows. A hand-written verdict disagreed with the collector for a
week. Rule: an entry whose key falls under a registered source's path can never be graded
WIRED_NEVER; it is COLLECTED with the source as reader, or EXCLUDED with a reason. Rung 4,
incident test, both ways."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _sources_and_verdicts():
    reg = json.loads((ROOT / "science/sources.json").read_text())["sources"]
    ver = json.loads((ROOT / "science/verdicts.json").read_text())["entries"]
    return reg, ver


def _covered_by_source(key, sources):
    # register keys look like mac/*jobs/* ; a source path .claude/jobs covers keys whose glob
    # tail names its last directory component.
    tail = key.split("*")[-2] if key.count("*") >= 2 else key.rsplit("/", 1)[-1]
    return [s for s in sources if tail and Path(s["path"]).name == tail.strip("/")]


def test_no_register_entry_under_a_registered_source_is_graded_wired_never():
    sources, verdicts = _sources_and_verdicts()
    stale = [e["key"] for e in verdicts
             if e["verdict"] == "WIRED_NEVER" and _covered_by_source(e["key"], sources)]
    assert stale == []


def test_the_jobs_entry_names_its_source_and_the_matcher_still_fires_on_a_stale_grade():
    sources, verdicts = _sources_and_verdicts()
    jobs = next(e for e in verdicts if e["key"] == "mac/*jobs/*")
    assert jobs["verdict"] == "COLLECTED" and "job_timelines" in jobs["reader"]
    assert [s["name"] for s in _covered_by_source("mac/*jobs/*", sources)] == ["job_timelines"]
    assert _covered_by_source("mac/*nothing-registered/*", sources) == []
