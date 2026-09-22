"""Command-line entry point for the crew platform."""

from __future__ import annotations

import argparse
import sys
from typing import Sequence

from . import board as board_mod


def _cmd_board_index(args: argparse.Namespace) -> int:
    payload = board_mod.build_index(args.workspace)
    print(f"indexed {payload['total']}")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="crew")
    sub = parser.add_subparsers(dest="command", required=True)

    board = sub.add_parser("board", help="Board utilities")
    board_sub = board.add_subparsers(dest="board_command", required=True)
    idx = board_sub.add_parser("index", help="Rebuild the board index")
    idx.add_argument("--workspace", required=True, help="Workspace slug to index")
    idx.set_defaults(func=_cmd_board_index)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args) or 0)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())