#!/usr/bin/env python3
import subprocess
import json
import sys

def read_github_board(repo="chidionyema/crew", issue_number=102):
    try:
        cmd = f"gh api -H 'Accept: application/vnd.github.raw' repos/{repo}/issues/{issue_number}/comments"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        comments = json.loads(result.stdout)
        
        board_rows = []
        for comment in comments:
            if comment and 'body' in comment:
                board_rows.append(comment['body'])
        return board_rows
    except subprocess.CalledProcessError as e:
        print(f"Error reading GitHub issue comments: {e.stderr}", file=sys.stderr)
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON from GitHub API response.", file=sys.stderr)
        return []

if __name__ == "__main__":
    rows = read_github_board()
    for row in rows:
        print(row)