"""Property: the issue body survives a round trip.

The board is read from GitHub, changed, and written back on every command. If
parse(render(b)) ever loses a field, one agent silently deletes another agent's
state. One property covers every shape instead of a table of examples.
"""

import json

from hypothesis import given, settings
from hypothesis import strategies as st

from crew import board as B
from crew.board_format import parse_comment

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


# ---------------------------------------------------------------------------
# crew#102 — the row parser survives a round trip on its own.
#
# Every broadcast row the estate writes is a GitHub comment, and the cache
# (`~/.claude/ESTATE_BOARD.jsonl`) is a JSONL of the dicts ``parse_comment``
# returns. If the parser ever returns a value that ``json.dumps`` refuses,
# the cache write path silently loses the row; if it ever returns a value
# whose fields drift from the contract, the writer and the reader disagree
# about what a row *is*. This property pins both: that ``parse_comment`` on
# a row-shaped body returns a dict with the five named fields and that the
# dict round-trips through JSON.
# ---------------------------------------------------------------------------

# GitHub renders comment body with no change to backticks, asterisks or
# parentheses, so the row format needs no escaping; ``-`` and ``_`` are the
# only non-alnum allowed in the ``from`` field (the issue templates use both).
from_field = st.from_regex(r"[A-Za-z0-9][A-Za-z0-9_\-]{0,19}", fullmatch=True)
ts_field = st.datetimes(
    allow_imaginary=False,
    min_value=__import__("datetime").datetime(2024, 1, 1),
    max_value=__import__("datetime").datetime(2030, 1, 1),
    timezones=st.just(__import__("datetime").timezone.utc),
).map(lambda dt: dt.strftime("%Y-%m-%dT%H:%M:%SZ"))
kind_field = st.from_regex(r"[A-Za-z0-9][A-Za-z0-9\-]{0,19}", fullmatch=True)
priority_field = st.one_of(
    st.sampled_from(["info"]),
    st.from_regex(r"p[1-9]", fullmatch=True),
)
# A message is a single line: no newlines. The parser strips lines and the
# regex anchors both ends, so a message with an embedded newline would never
# match anyway, but the strategy does not need to model that -- ``st.text``
# without newlines is the simpler and faster pin.
message_field = st.text(
    alphabet=st.characters(
        blacklist_categories=("Cs", "Cc"), blacklist_characters=("\n",)
    ),
    min_size=1,
    max_size=80,
).map(str.strip).filter(lambda s: s)


@settings(max_examples=200)
@given(ts_field, from_field, kind_field, priority_field, message_field)
def test_parse_row_round_trip_full_format(ts, frm, kind, prio, msg):
    """The full shape (`ts` **from** (kind/priority): message) parses and JSONs."""
    body = f"`{ts}` **{frm}** ({kind}/{prio}): {msg}"
    row = parse_comment(body)
    assert row is not None, f"row-shaped body was not parsed: {body!r}"
    assert row == {
        "ts": ts,
        "from": frm,
        "kind": kind,
        "priority": prio,
        "message": msg,
    }
    # The cache write path is ``json.dumps(row) + "\\n"``. If the dict shape
    # ever stops being JSON-serialisable (a set, a bytes, a pathlib.Path),
    # the cache silently loses the row -- so the property is not only that
    # ``parse_comment`` returns a dict but that the dict is safe to JSON.
    assert json.loads(json.dumps(row)) == row


@settings(max_examples=200)
@given(ts_field, from_field, message_field)
def test_parse_row_round_trip_simple_format(ts, frm, msg):
    """The simple (older) shape defaults kind="unclassified" and priority="info"."""
    body = f"`{ts}` **{frm}**: {msg}"
    row = parse_comment(body)
    assert row is not None, f"row-shaped body was not parsed: {body!r}"
    assert row == {
        "ts": ts,
        "from": frm,
        "kind": "unclassified",
        "priority": "info",
        "message": msg,
    }
    assert json.loads(json.dumps(row)) == row


# Not a row: a backfill header a person wrote, an empty body, a plain sentence.
# These are the exact shapes ``tests/test_incident_crew101_..._was_never_refilled.py``
# asserts ``parse_comment`` returns ``None`` for, lifted into a property so the
# pin does not silently narrow as new row shapes are added.
not_a_row = st.sampled_from([
    "**Backfill 1/3 — the 191 rows that existed before the board became this issue.**",
    "",
    "   ",
    "just a note from a human",
    "nothing here to parse",
])


@settings(max_examples=50)
@given(not_a_row)
def test_parse_row_returns_none_for_prose(body):
    """Prose, empty, and whitespace-only bodies are not rows."""
    assert parse_comment(body) is None
