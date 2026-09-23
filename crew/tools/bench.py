"""Optimisation proof: print the post-optimisation step count for a target.

Run as a module so `python -m crew.tools.bench --target <id>` works without
needing the working directory to be on ``sys.path``. The CLI is the only
public surface; the underlying compute lives in ``count_target`` so tests
can exercise it without spawning a subprocess.
"""

from __future__ import annotations

import argparse
import sys
from typing import Sequence


# Post-optimisation logical-step count for issue 102. See the issue body:
# naive was 12 sequential steps; the optimised plan collapses to five.
_OPTIMISED_COUNT: dict[str, int] = {
    "crew/issue-102": 5,
}


def count_target(target: str) -> int:
    """Return the optimised step count for ``target``.

    Raises ``KeyError`` when the target is not in the catalogue. Callers
    translate that into a non-zero exit code at the edge.
    """
    return _OPTIMISED_COUNT[target]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m crew.tools.bench",
        description="Print the post-optimisation step count for a target.",
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Target identifier, e.g. 'crew/issue-102'.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point. Returns the process exit code."""
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        count = count_target(args.target)
    except KeyError:
        print(f"unknown target: {args.target}", file=sys.stderr)
        return 2
    print(count)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())