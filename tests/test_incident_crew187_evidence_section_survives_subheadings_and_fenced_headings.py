"""Incident test, crew#187 (idp#17, 2026-08-24): the evidence gate stopped reading its own
section at the first sub-heading, and a heading-shaped line inside a code fence closed it too.

Both ways: a `###` sub-heading and a fenced `# comment` line stay inside the section; the next
`##` heading outside a fence ends it.
"""
import importlib.util
import pathlib

HERE = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("pr_evidence", HERE / "scripts" / "pr-evidence.py")
assert spec is not None and spec.loader is not None
pe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pe)


def test_subheading_and_fenced_heading_do_not_end_the_section():
    tail = "### run one\n```\n# a shell comment\n$ pytest -q\n3 passed\n```\n### run two\n```\n$ x\n```\n"
    assert pe.section_end(tail, 2) is None


def test_next_same_level_heading_ends_the_section():
    tail = "```\n$ pytest -q\n3 passed\n```\n## Architecture laws\n- LAW 1\n"
    end = pe.section_end(tail, 2)
    assert end is not None and tail[end:].startswith("## Architecture laws")
