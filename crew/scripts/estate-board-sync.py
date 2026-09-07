import json
import re
import os
from datetime import datetime, timezone

# Regex to parse comments in the format: `ts` **from** (kind/priority): message.
# Handles optional milliseconds in timestamp.
COMMENT_FULL_RE = re.compile(
    r"^`(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\\.\\d+)?Z)`\\s+\\*\\*([^\\*]+?)\\*\\*\\s+\\(([^/]+?)/([^)]+?)\\):\\s+(.*)$"
)
# Regex for comments in the format: `ts` **from**: message (without kind/priority)
COMMENT_SIMPLE_RE = re.compile(
    r"^`(\d{4}-\d{2}-\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d+)?Z)`\\s+\\*\\*([^\\*]+?)\\*\\*:\\s+(.*)$"
)

def parse_comment(comment_body: str) -> dict | None:
    """Parses a GitHub issue comment into a structured dictionary."""
    match = COMMENT_FULL_RE.match(comment_body)
    if match:
        ts_str, from_str, kind_str, priority_str, message_str = match.groups()
        return {
            "ts": ts_str,
            "from": from_str.strip(),
            "kind": kind_str.strip(),
            "priority": priority_str.strip(),
            "message": message_str.strip(),
        }
    
    match = COMMENT_SIMPLE_RE.match(comment_body)
    if match:
        ts_str, from_str, message_str = match.groups()
        return {
            "ts": ts_str,
            "from": from_str.strip(),
            "kind": "unclassified", # Default for comments without explicit kind
            "priority": "info",    # Default for comments without explicit priority
            "message": message_str.strip(),
        }
    
    return None

def sync_estate_board(issue_comments_json: str, output_file: str):
    """
    Syncs the estate board from GitHub issue comments to a local JSONL file.
    
    Args:
        issue_comments_json: A JSON string of a list of dictionaries, each representing a GitHub issue comment.
                             Expected keys: 'body', 'author'.
        output_file: The path to the output JSONL file.
    """
    issue_comments = json.loads(issue_comments_json)
    parsed_rows = []
    for comment in issue_comments:
        # Skip comments that are part of the backfill or not actual board entries
        if comment.get("author") == "chidionyema" and comment.get("body", "").startswith("**Backfill"):
            continue
        
        parsed_data = parse_comment(comment.get("body", ""))
        if parsed_data:
            parsed_rows.append(parsed_data)

    # Sort by timestamp to ensure chronological order
    parsed_rows.sort(key=lambda x: datetime.fromisoformat(x["ts"].replace("Z", "+00:00")))

    with open(output_file, "w") as f:
        for row in parsed_rows:
            f.write(json.dumps(row) + "\\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        sync_estate_board(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python estate-board-sync.py <issue_comments_json_string> <output_file_path>")
