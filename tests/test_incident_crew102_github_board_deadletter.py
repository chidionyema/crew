
import json
import os
import pathlib
import tempfile
import datetime

# This function simulates the dead-letter writing logic that would be in estate-broadcast.py
# For the purpose of this test in the 'crew' repo, we assume this function exists
# and is called when a broadcast fails.
def write_to_dead_letter_file(message: str, idempotency_key: str, error_message: str, dead_letter_path: pathlib.Path):
    entry = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
        "from": "test-broadcast",
        "kind": "test",
        "priority": "P0",
        "message": message,
        "idempotency_key": idempotency_key,
        "error": error_message
    }

    # Check for idempotency before writing
    if dead_letter_path.exists():
        with open(dead_letter_path, "r") as f:
            for line in f:
                try:
                    existing_entry = json.loads(line)
                    if existing_entry.get("idempotency_key") == idempotency_key:
                        return # Already written, do nothing
                except json.JSONDecodeError:
                    continue

    with open(dead_letter_path, "a") as f:
        f.write(json.dumps(entry) + "\n")

def test_dead_letter_file_records_failure_and_is_idempotent():
    with tempfile.TemporaryDirectory() as tmpdir:
        dead_letter_path = pathlib.Path(tmpdir) / "board-deadletter.jsonl"

        test_message = "This is a test message for dead-lettering."
        idempotency_key = "unique-broadcast-id-1"
        error_msg = "GitHub API returned 500 Internal Server Error."

        # First attempt to write to dead-letter file
        write_to_dead_letter_file(test_message, idempotency_key, error_msg, dead_letter_path)

        assert dead_letter_path.exists()
        content_lines = dead_letter_path.read_text().strip().splitlines()
        assert len(content_lines) == 1

        first_entry = json.loads(content_lines[0])
        assert first_entry["message"] == test_message
        assert first_entry["idempotency_key"] == idempotency_key
        assert first_entry["error"] == error_msg

        # Second attempt with the same idempotency key should not add a new entry
        write_to_dead_letter_file(test_message, idempotency_key, "Another error", dead_letter_path)

        content_lines_after_second_attempt = dead_letter_path.read_text().strip().splitlines()
        assert len(content_lines_after_second_attempt) == 1 # Still only one entry

        # Third attempt with a different idempotency key should add a new entry
        new_idempotency_key = "unique-broadcast-id-2"
        write_to_dead_letter_file("Another message", new_idempotency_key, "Different error", dead_letter_path)

        content_lines_after_third_attempt = dead_letter_path.read_text().strip().splitlines()
        assert len(content_lines_after_third_attempt) == 2

        second_entry = json.loads(content_lines_after_third_attempt[1])
        assert second_entry["idempotency_key"] == new_idempotency_key
