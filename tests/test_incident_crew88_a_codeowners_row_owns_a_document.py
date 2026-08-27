"""crew#88, measured 2026-08-27 09:20Z: 377 of 389 documents name no owner; every one of them fails
the standard on that criterion alone. Rule (rung 4, both ways): a document with no Owner line is
owned when a CODEOWNERS row covers its path; a document nothing covers stays unowned; an Owner
line in the file outranks CODEOWNERS."""
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "science"))
import docsmap


def _repo(tmp_path, codeowners):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "covered.md").write_text("# covered\n" + "x " * 200)
    (tmp_path / "loose.md").write_text("# loose\n" + "x " * 200)
    (tmp_path / "docs" / "inline.md").write_text("Owner: inline-person\n" + "x " * 200)
    if codeowners is not None:
        (tmp_path / "CODEOWNERS").write_text(codeowners)
    subprocess.run(["git", "-C", str(tmp_path), "add", "-A"], check=True)
    return {d.path: d.owner for d in docsmap.scan(str(tmp_path))}


def test_a_codeowners_row_owns_the_document_it_covers_and_nothing_else(tmp_path):
    got = _repo(tmp_path, "# comment\n/docs/ @chidionyema\n")
    assert got["docs/covered.md"] == "@chidionyema"
    assert got["loose.md"] is None
    assert got["docs/inline.md"] == "inline-person"


def test_without_codeowners_nothing_changes(tmp_path):
    got = _repo(tmp_path, None)
    assert got["docs/covered.md"] is None and got["loose.md"] is None and got["docs/inline.md"] == "inline-person"


def test_last_matching_row_wins_like_github():
    rows = [("*", "@a"), ("/docs/", "@b"), ("*.md", "@c")]
    assert docsmap.codeowner_of("docs/x.md", rows) == "@c"
    assert docsmap.codeowner_of("docs/x.txt", rows) == "@b"
    assert docsmap.codeowner_of("bin/run", rows) == "@a"


def test_a_trailing_slash_only_pattern_matches_at_any_depth() -> None:
    # crew#477 REWORK: GitHub matches `docs/` under any parent, the same as `docs`
    rows = [("docs/", "@u")]
    assert docsmap.codeowner_of("a/docs/x.md", rows) == "@u"
    assert docsmap.codeowner_of("docs/x.md", rows) == "@u"
    assert docsmap.codeowner_of("docs/x.md", [("/docs/", "@r")]) == "@r"
    assert docsmap.codeowner_of("a/docs/x.md", [("/docs/", "@r")]) is None
