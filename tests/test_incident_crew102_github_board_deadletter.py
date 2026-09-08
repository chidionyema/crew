import pytest
import subprocess
import os
import json
from unittest.mock import patch, MagicMock

# Mock the gh command to simulate failures
def mock_gh_issue_comment_fail(*args, **kwargs):
    if "--body" in kwargs:
        # Simulate a 5xx error by raising an exception
        raise subprocess.CalledProcessError(returncode=1, cmd="gh issue comment", stderr="HTTP 500: Internal Server Error")
    return MagicMock(stdout="{}")

def mock_gh_issue_comment_success(*args, **kwargs):
    return MagicMock(stdout="{}")

@pytest.fixture
def setup_deadletter_file(tmp_path):
    # Use a temporary directory for HOME to isolate dead-letter file
    temp_home = tmp_path / "temp_home"
    deadletter_dir = temp_home / ".claude" / "state"
    deadletter_path = deadletter_dir / "board-deadletter.jsonl"
    os.makedirs(deadletter_dir, exist_ok=True)

    with patch.dict(os.environ, {"HOME": str(temp_home)}):
        yield deadletter_path

# This function simulates the core logic of estate-broadcast.py for dead-lettering
def simulate_estate_broadcast_deadletter(payload, mock_gh_function):
    deadletter_file = os.path.expanduser("~/.claude/state/board-deadletter.jsonl")
    
    # Check for idempotency key in existing dead-letter file
    existing_keys = set()
    if os.path.exists(deadletter_file):
        with open(deadletter_file, "r") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if "idempotency_key" in data:
                        existing_keys.add(data["idempotency_key"])
                except json.JSONDecodeError:
                    pass # Ignore malformed lines

    if "idempotency_key" in payload and payload["idempotency_key"] in existing_keys:
        return False # Already dead-lettered, no-op

    try:
        # Simulate the gh issue comment call
        mock_gh_function(
            "102",
            repo="chidionyema/crew",
            _b=json.dumps(payload) # Assuming the payload is passed as a JSON string in the body
        )
    except subprocess.CalledProcessError:
        # If gh call fails, dead-letter the payload
        with open(deadletter_file, "a") as f:
            f.write(json.dumps(payload) + "\n")
        return False
    return True

def test_broadcast_failure_dead_letters_payload(setup_deadletter_file):
    deadletter_path = setup_deadletter_file
    payload = {"ts": "2026-08-29T10:00:00Z", "from": "test", "kind": "info", "message": "Test broadcast"}

    # Simulate gh command failing
    with patch("subprocess.run", side_effect=mock_gh_issue_comment_fail):
        success = simulate_estate_broadcast_deadletter(payload, subprocess.run)
        assert not success

    # Verify payload is in dead-letter file
    with open(deadletter_path, "r") as f:
        dead_letter_content = f.read()
        assert json.dumps(payload) + "\n" in dead_letter_content

def test_retry_with_same_idempotency_key_is_no_op(setup_deadletter_file):
    deadletter_path = setup_deadletter_file
    idempotency_key = "unique-key-123"
    payload_1 = {"ts": "2026-08-29T10:00:00Z", "from": "test", "kind": "info", "message": "First broadcast", "idempotency_key": idempotency_key}
    payload_2 = {"ts": "2026-08-29T10:01:00Z", "from": "test", "kind": "info", "message": "Second broadcast (same key)", "idempotency_key": idempotency_key}
    payload_3 = {"ts": "2026-08-29T10:02:00Z", "from": "test", "kind": "info", "message": "Third broadcast (different key)", "idempotency_key": "another-key"}

    # First broadcast fails and dead-letters
    with patch("subprocess.run", side_effect=mock_gh_issue_comment_fail):
        simulate_estate_broadcast_deadletter(payload_1, subprocess.run)

    # Second broadcast with same key, should be a no-op for dead-lettering
    with patch("subprocess.run", side_effect=mock_gh_issue_comment_fail):
        simulate_estate_broadcast_deadletter(payload_2, subprocess.run)

    # Third broadcast with different key, should dead-letter
    with patch("subprocess.run", side_effect=mock_gh_issue_comment_fail):
        simulate_estate_broadcast_deadletter(payload_3, subprocess.run)

    # Verify dead-letter file content
    with open(deadletter_path, "r") as f:
        dead_letter_lines = f.readlines()
        assert len(dead_letter_lines) == 2 # Only payload_1 and payload_3 should be there
        assert json.dumps(payload_1) + "\n" in dead_letter_lines
        assert json.dumps(payload_3) + "\n" in dead_letter_lines
        assert json.dumps(payload_2) + "\n" not in dead_letter_lines
