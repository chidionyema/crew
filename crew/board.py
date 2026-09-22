"""Board helpers: listing and searching open tickets across all plans."""
from __future__ import annotations

import re
from typing import Iterable, List


def _tokenize(text: str) -> List[str]:
    """Lower-case split on non-word characters so search terms match flexibly."""
    return [t for t in re.split(r"\W+", text.lower()) if t]


def search_tickets(tickets: Iterable[dict], query: str) -> List[dict]:
    """Return tickets whose title or body matches every token in ``query``.

    Matching is case-insensitive and token-based: every whitespace/punctuation
    separated token in ``query`` must appear in either the title or the body of
    the ticket for it to be returned. An empty query returns an empty list so
    that callers must opt-in to a full listing.
    """
    tokens = _tokenize(query)
    if not tokens:
        return []
    hits: List[dict] = []
    for ticket in tickets:
        haystack = " ".join(
            [
                str(ticket.get("title", "")),
                str(ticket.get("body", "")),
            ]
        ).lower()
        if all(token in haystack for token in tokens):
            hits.append(ticket)
    return hits
