# Standard: scheduling row, docs/STANDARDS.md -- one scheduler, idp/scheduler; this is a code location it loads
# Rejected: a cron or a standalone `dagster dev` -- a second scheduler; the freshness policies must live where the one daemon evaluates them
"""Incident test, rung 4. One bug, named for the bug.

THE BUG
-------
Dagster's freshness evaluator compares now against the timestamp DAGSTER wrote on
the last materialization event, not against any timestamp the event carries
(dagster/_core/definitions/freshness_evaluator.py:65, read at 1.13.19). So any
observer that records "I looked and here is what I saw" marks every asset fresh
forever. The first version of estate_dagster.sources did exactly that on its
first run: all 28 fact files were recorded at once, and a producer that had been
dead for three days would have read PASS for the whole length of its own window.

That is worse than no monitoring, because it answers the question wrongly instead
of not answering it.

WHAT IS ASSERTED
----------------
The rule, not the code: an event is recorded only when the file changed AND the
change is recent enough to be evidence that its producer is alive. Both refusals
are asserted, because a guard only ever seen refusing has never been shown to
permit (LAW 45 step 3, LAW 38).

    python3 -m pytest tests/test_incident_false_green_at_seeding.py -q
"""

from estate_dagster.sources import ALREADY_STALE, RECORD, UNCHANGED, decide

NOW = 1_756_000_000.0
HOUR = 3600.0
WINDOW = 6  # hours; the shortest declared on the estate


def test_a_fresh_change_is_recorded():
    """The permit case. Without this the guard could refuse everything."""
    assert decide(NOW - HOUR, None, WINDOW, NOW) == RECORD
    assert decide(NOW - HOUR, NOW - 5 * HOUR, WINDOW, NOW) == RECORD


def test_seeding_a_producer_that_is_already_dead_records_nothing():
    """The incident. No prior record, file older than its window.

    Recording here would stamp an event at NOW and report the dead producer as
    healthy until the window elapsed again.
    """
    assert decide(NOW - 72 * HOUR, None, WINDOW, NOW) == ALREADY_STALE


def test_a_file_restored_with_an_old_mtime_records_nothing():
    """Same rule, not seeding: the mtime moved but moved backwards in time."""
    assert decide(NOW - 48 * HOUR, NOW - HOUR, WINDOW, NOW) == ALREADY_STALE


def test_an_unchanged_file_records_nothing():
    """The other false-green path: re-recording resets the clock, so the asset
    never crosses its window no matter how long the producer has been dead."""
    assert decide(NOW - HOUR, NOW - HOUR, WINDOW, NOW) == UNCHANGED


def test_the_boundary_belongs_to_stale():
    """A file exactly its window old is out, not in. Equal ages must not flip
    between runs depending on which side of the comparison rounds first."""
    assert decide(NOW - WINDOW * HOUR, None, WINDOW, NOW) == ALREADY_STALE
    assert decide(NOW - (WINDOW * HOUR - 1), None, WINDOW, NOW) == RECORD
