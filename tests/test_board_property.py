"""Property: the issue body survives a round trip.

The board is read from GitHub, changed, and written back on every command. If
parse(render(b)) ever loses a field, one agent silently deletes another agent's
state. One property covers every shape instead of a table of examples.
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from crew import board as B

# GitHub renders markdown, and the crew owns the delimiters: a title or blocker
# containing a newline or a pipe is not a value the board can hold.
text = st.text(
    alphabet=st.characters(blacklist_categories=("Cs", "Cc"), blacklist_characters="|"),
    min_size=1, max_size=60,
).map(str.strip).filter(lambda s: s and not s.startswith("#"))

checkpoints = st.lists(
    st.tuples(st.integers(1, 99), text, st.booleans()),
    min_size=0, max_size=8, unique_by=lambda t: t[0],
).map(lambda ts: [B.Checkpoint(id=f"CP{n}", title=t, done=d) for n, t, d in ts])

rows = st.lists(
    st.tuples(st.integers(1, 99), text, text, text),
    min_size=0, max_size=6,
).map(lambda ts: [B.Row(cp=f"CP{n}", result=r, evidence=e, when=w) for n, r, e, w in ts])

# The crew owns its five section headings the same way it owns the pipe in a
# table row. A brief whose own text is the line "## Checklist" is not a value
# the board can hold, and no other heading is excluded.
def _no_heading_collision(s: str) -> bool:
    return not any(line.strip() in B.KNOWN_HEADINGS for line in s.splitlines())


boards = st.builds(
    B.Board,
    origin=st.text(alphabet=st.characters(blacklist_categories=("Cs", "Cc")), max_size=80)
    .map(str.strip)
    .filter(_no_heading_collision),
    checkpoints=checkpoints,
    rows=rows,
    blockers=st.lists(text, max_size=4, unique=True),
)


@settings(max_examples=300)
@given(boards)
def test_round_trip(b):
    got = B.parse(B.render(b))
    assert got.checkpoints == b.checkpoints
    assert got.rows == b.rows
    assert got.blockers == b.blockers
    assert got.origin == (b.origin or "_not recorded_")


@settings(max_examples=200)
@given(boards)
def test_render_is_idempotent(b):
    once = B.render(b)
    assert B.render(B.parse(once)) == once


@settings(max_examples=200)
@given(boards)
def test_complete_means_every_box_ticked(b):
    assert b.complete == (bool(b.checkpoints) and all(c.done for c in b.checkpoints))
