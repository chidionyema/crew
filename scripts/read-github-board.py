import json
import sys

# This script expects `default_api` to be available in its execution environment.
# If running outside such an environment, `default_api` would need to be imported
# or mocked. For the purpose of this task, we assume it's provided.

def read_board_from_github(repo: str, issue_number: int) -> list[dict]:
    """
    Reads board data from GitHub issue comments.
    Each comment body is expected to be a JSONL entry.
    """
    board_data = []
    try:
        # Assuming default_api is globally available or accessible
        issue_data = default_api.read_issue(repo=repo, number=issue_number)
        comments = issue_data.get('read_issue_response', {}).get('comments', [])
        for comment in comments:
            try:
                # Assuming each comment body is a single JSONL entry
                entry = json.loads(comment['body'])
                board_data.append(entry)
            except json.JSONDecodeError:
                # Skip comments that are not valid JSON
                continue
    except Exception as e:
        # In a production script, you might want more robust error logging
        print(f"Error reading issue {issue_number} from {repo}: {e}", file=sys.stderr)
    return board_data

if __name__ == "__main__":
    # The repository and issue number are hardcoded as per the task description.
    # In a more general solution, these might be command-line arguments or config.
    repo_name = "crew"
    issue_num = 102
    
    board_entries = read_board_from_github(repo=repo_name, issue_number=issue_num)
    for entry in board_entries:
        print(json.dumps(entry))
