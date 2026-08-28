"""Incident, crew#537 (2026-08-28): the board could not see the checkpoints
of a pm-agent issue, and would have erased the issue on its first write.

Two causes, both in crew/board.py:
  1. CP_RE demanded `CPn:`; the issue (and 30 lines over 20 open issues)
     wrote `- [ ] CP4 title`, so `crew verify`/`claim`/`evidence` answered
     "CP4 is not on the checklist".
  2. The list sat under `## Checkpoints`, which _split_sections did not know,
     so every line of the issue was "preamble" and render() emitted none of
     it: the founder verbatim, the requirements and the checklist would have
     vanished on the next `crew` command.

The guard: a pm-agent-shaped body parses to its checkpoints, and every
non-blank line of it survives parse -> render.
"""

from crew import board as B

CREW537 = """\
# crew#537 Ideas on the science page

## Founder verbatim

> we need the research engine to make forecasts and grade them

## Requirements

- Three graded ideas rows on SHOWCASE.md
- Ledger rows carry kind/forecast/outcome

## Checkpoints

- [x] CP1 Ledger schema carries kind, forecast, outcome (receipt: crew#540)
- [x] CP2 Showcase renders the Ideas section
- [ ] CP3 Verify gate refuses an idea without a forecast
- [ ] CP4 Three graded ideas rows on SHOWCASE.md
- [ ] CP5 First idea from the engine on the ledger

Closes-when: `python3 science/datamap.py --row prospector.ideas_graded`

Author-session: 09cd04a6
"""


def _content_lines(text: str) -> list[str]:
    return [ln.strip() for ln in text.splitlines() if ln.strip()]


def test_pm_agent_issue_checkpoints_are_visible():
    b = B.parse(CREW537)
    assert [c.id for c in b.checkpoints] == ["CP1", "CP2", "CP3", "CP4", "CP5"]
    assert b.get("CP4").title == "Three graded ideas rows on SHOWCASE.md"
    assert b.get("CP1").done and not b.get("CP4").done
    assert b.get("CP1").title.endswith("(receipt: crew#540)")


def test_colon_and_no_colon_lines_parse_the_same():
    with_colon = B.parse("## Checklist\n\n- [ ] CP7: do the thing\n")
    without = B.parse("## Checklist\n\n- [ ] CP7 do the thing\n")
    assert with_colon.checkpoints == without.checkpoints
    assert with_colon.get("CP7").title == "do the thing"


def test_checkpoints_heading_with_parenthetical_is_the_checklist():
    b = B.parse("## Checkpoints (each is a generated artefact + a gate, zero spend)\n\n- [ ] CP1 x\n")
    assert [c.id for c in b.checkpoints] == ["CP1"]


def test_write_back_keeps_every_line_of_a_pm_agent_issue():
    b = B.parse(CREW537)
    out = B.render(b.tick("CP4"))
    rendered = _content_lines(out)
    for line in _content_lines(CREW537):
        if line.startswith("- [") or line.startswith("## Checkpoints"):
            continue  # canonicalised: `CPn:` lines under `## Checklist`
        assert line in rendered, f"write-back dropped: {line!r}"
    assert "- [x] CP4: Three graded ideas rows on SHOWCASE.md" in rendered
    assert "## Founder verbatim" in rendered
    assert "Closes-when: `python3 science/datamap.py --row prospector.ideas_graded`" in rendered
    # the preamble comes first, before the crew's own sections
    assert out.index("## Founder verbatim") < out.index(B.H_ORIGIN)


def test_second_write_is_stable():
    once = B.render(B.parse(CREW537))
    assert B.render(B.parse(once)) == once


def test_crew_shaped_body_unchanged():
    body = B.render(B.Board(origin="Distilled.", checkpoints=[B.Checkpoint("CP1", "one")]))
    assert B.parse(body).preamble == ""
    assert B.parse(body).notes == []
    assert B.render(B.parse(body)) == body


def test_brief_without_a_checklist_heading_still_has_checkpoints():
    body = "Brief line.\n\n- [ ] CP1 first\n- [x] CP2 second\n\nOwner: someone.\n"
    b = B.parse(body)
    assert [(c.id, c.done) for c in b.checkpoints] == [("CP1", False), ("CP2", True)]
    assert b.preamble == "Brief line.\n\n\nOwner: someone."
    out = B.render(b)
    assert "Owner: someone." in out and "- [x] CP2: second" in out
    assert B.render(B.parse(out)) == out
