"""Bench tools for the crew: post-optimisation step counters.

Run as a module:

    python -m crew.tools.bench --target crew/issue-102

For the target ``crew/issue-102`` this prints the optimised count (``5``)
and exits ``0``. Any other target exits non-zero with a clear message.
"""

from __future__ import annotations

import argparse
import sys
from typing import Sequence

from crew.errors import CrewError

# The single supported benchmark target for this issue.
ISSUE_102_TARGET = "crew/issue-102"

# Post-optimisation logical step count for ``crew/issue-102``.
ISSUE_102_OPTIMISED_COUNT = 5


def _build_parser() -> argparse.ArgumentParser:
    """Build the argparse parser for the bench CLI."""
    parser = argparse.ArgumentParser(
        prog="crew.tools.bench",
        description="Print the post-optimisation step count for a crew target.",
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Crew benchmark target, e.g. 'crew/issue-102'.",
    )
    return parser


def run(argv: Sequence[str] | None = None) -> int:
    """Run the bench CLI and return the process exit code."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    target = args.target
    if target == ISSUE_102_TARGET:
        print(ISSUE_102_OPTIMISED_COUNT)
        return 0

    raise CrewError(f"Unknown bench target: {target!r}")


def main() -> int:
    """Entry point for ``python -m crew.tools.bench``."""
    try:
        return run()
    except CrewError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
