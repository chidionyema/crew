#!/usr/bin/env python3

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

# --- Configuration (read from bin/board-target) ---

def get_board_target_config(key):
    try:
        import subprocess
        return subprocess.check_output(['bin/board-target', key], text=True, stderr=subprocess.PIPE).strip()
    except Exception as e:
        print(f"Error reading board-target config for {key}: {e}", file=sys.stderr)
        sys.exit(1)

REPO = get_board_target_config('repo')
ISSUE_NUMBER = int(get_board_target_config('issue'))
DEAD_LETTER_PATH = os.path.expanduser(get_board_target_config('deadletter'))

# --- GitHub API (simplified for demonstration) ---

def github_comment_on_issue(repo, issue_number, body):
    # In a real scenario, this would use a GitHub API client (e.g., PyGithub)
    # and handle authentication. For this simulation, we'll just print.
    print(f"[SIMULATED] Commenting on {repo}#{issue_number}:\n{body}")
    # Simulate success
    return {"html_url": f"https://github.com/{repo}/issues/{issue_number}#comment-simulated"}

# --- Dead-lettering --- 

def dead_letter_message(message, reason):
    timestamp = datetime.now(timezone.utc).isoformat()
    dead_letter_entry = {
        "timestamp": timestamp,
        "reason": reason,
        "message": message
    }
    try:
        with open(DEAD_LETTER_PATH, 'a') as f:
            f.write(json.dumps(dead_letter_entry) + '\n')
        print(f"WARN: Message dead-lettered to {DEAD_LETTER_PATH} due to: {reason}", file=sys.stderr)
    except Exception as e:
        print(f"ERROR: Failed to write to dead-letter file {DEAD_LETTER_PATH}: {e}", file=sys.stderr)
        sys.exit(1)

# --- Main broadcast logic ---

def broadcast_message(message_jsonl_line):
    try:
        message = json.loads(message_jsonl_line)
    except json.JSONDecodeError as e:
        dead_letter_message(message_jsonl_line, f"Invalid JSON: {e}")
        return

    # Ensure message has an idempotency key to prevent duplicate posts on retry
    idempotency_key = message.get('idempotency_key')
    if not idempotency_key:
        idempotency_key = f"broadcast-{hash(message_jsonl_line)}-{time.time()}"
        message['idempotency_key'] = idempotency_key
        message_jsonl_line = json.dumps(message) # Update line with key

    # Check if this message (by idempotency_key) has already been posted
    # In a real system, this would involve checking a persistent store (e.g., a database)
    # For this simulation, we'll assume it's a new message if not found in a simple cache.
    # For the purpose of this test, we'll simulate a simple check.
    # A more robust solution would involve a proper deduplication mechanism.
    # For now, we'll just assume it's new for every run to demonstrate dead-lettering.

    comment_body = f"`{message.get('ts', datetime.now(timezone.utc).isoformat())}` **{message.get('from', '?')}** ({message.get('kind', 'info')}/{message.get('priority', 'info')}): {message.get('message', '')}"

    try:
        # Simulate posting to GitHub issue
        response = github_comment_on_issue(REPO, ISSUE_NUMBER, comment_body)
        print(f"Broadcast successful: {response['html_url']}")
    except Exception as e:
        dead_letter_message(message_jsonl_line, f"GitHub API error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Broadcast a JSONL message to the estate board GitHub issue.")
    parser.add_argument('message', nargs='?', help='The JSONL message to broadcast. If not provided, reads from stdin.')
    args = parser.parse_args()

    if args.message:
        broadcast_message(args.message)
    else:
        for line in sys.stdin:
            broadcast_message(line.strip())
