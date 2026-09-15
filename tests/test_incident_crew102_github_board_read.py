"""Network tests that the GitHub issue page for crew#102 is itself readable.

These tests GET https://github.com/chidionyema/crew/issues/102 and assert
the page carries the expected board header text. They are marked
@pytest.mark.network so the CI default invocation can exclude them with
`-m "not network"`. Each test skips gracefully if the network is
unreachable, so it never fails CI on an offline machine.
"""

from __future__ import annotations

import urllib.error
import urllib.request

import pytest

ISSUE_URL = "https://github.com/chidionyema/crew/issues/102"
EXPECTED_TITLE_PHRASE = "ESTATE BOARD"
EXPECTED_BODY_PHRASE = "This issue IS the estate board"


def _fetch(url: str, timeout: float = 10.0) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "crew-issue-102-read-test/1.0"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # nosec - URL is a constant
        return resp.read()


@pytest.mark.network
def test_issue_102_title_contains_estate_board():
    try:
        body = _fetch(ISSUE_URL)
    except (urllib.error.URLError, OSError, TimeoutError):
        pytest.skip("network unreachable")
    text = body.decode("utf-8", errors="replace")
    assert EXPECTED_TITLE_PHRASE in text, (
        f"expected '{EXPECTED_TITLE_PHRASE}' in issue #102 page"
    )


@pytest.mark.network
def test_issue_102_body_marks_this_issue_as_board():
    try:
        body = _fetch(ISSUE_URL)
    except (urllib.error.URLError, OSError, TimeoutError):
        pytest.skip("network unreachable")
    text = body.decode("utf-8", errors="replace")
    assert EXPECTED_BODY_PHRASE in text, (
        f"expected '{EXPECTED_BODY_PHRASE}' in issue #102 page"
    )
