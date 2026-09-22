"""Command line entry points for the crew tooling."""
from __future__ import annotations

import argparse
import sys
from typing import List

from crew import board


def _load_tickets(paths: List[str]) -> List[dict]:
    """Load tickets from a list of JSON file paths; tolerate missing files."""
    import json

    tickets: List[dict] = []
    for path in paths:
        try:
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except FileNotFoundError:
            continue
        if isinstance(data, list):
            tickets.extend(data)
    return tickets


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="crew", description="Crew platform CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    search = sub.add_parser("search", help="Search open tickets across all plans")
    search.add_argument("--plan", action="append", required=True, help="Path to a plan JSON file (repeatable)")
    search.add_argument("--query", required=True, help="Free-text search query")

    args = parser.parse_args(argv)

    if args.command == "search":
        tickets = _load_tickets(args.plan)
        for ticket in board.search_tickets(tickets, args.query):
            number = ticket.get("number", "?")
            title = ticket.get("title", "")
            plan = ticket.get("plan", "")
            print(f"#{number}\t[{plan}]\t{title}")
        return 0

    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
