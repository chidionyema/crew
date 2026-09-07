import subprocess
import os

def run_commit_guard(commit_message):
    # Create a temporary file for the commit message
    with open("temp_commit_message.txt", "w") as f:
        f.write(commit_message)
    
    # Run the guard script, feeding the commit message to stdin
    try:
        result = subprocess.run(
            ["bash", "scripts/verify.d/20-agent-commit-guard.sh"],
            input=commit_message.encode('utf-8'),
            capture_output=True,
            check=False
        )
        return result.returncode, result.stdout.decode('utf-8'), result.stderr.decode('utf-8')
    finally:
        # Clean up the temporary file
        if os.path.exists("temp_commit_message.txt"):
            os.remove("temp_commit_message.txt")

def test_valid_agent_commit():
    commit_message = "feat: My agent commit\n\nAgent-ID: test-agent-123"
    returncode, stdout, stderr = run_commit_guard(commit_message)
    assert returncode == 0, f"Guard failed for valid commit. Stdout: {stdout}, Stderr: {stderr}"
    assert "Error" not in stdout and "Error" not in stderr, f"Guard produced error for valid commit. Stdout: {stdout}, Stderr: {stderr}"

def test_invalid_agent_commit_no_trailer():
    commit_message = "feat: My agent commit without trailer"
    returncode, stdout, stderr = run_commit_guard(commit_message)
    assert returncode == 1, f"Guard passed for invalid commit. Stdout: {stdout}, Stderr: {stderr}"
    assert "Error: Agent commits must include the 'Agent-ID:' trailer." in stderr, f"Incorrect error message. Stdout: {stdout}, Stderr: {stderr}"

# To run these tests, you would typically use pytest.
# For this exercise, we'll just call them directly.
if __name__ == "__main__":
    print("Running test_valid_agent_commit...")
    test_valid_agent_commit()
    print("test_valid_agent_commit passed.")
    
    print("Running test_invalid_agent_commit_no_trailer...")
    test_invalid_agent_commit_no_trailer()
    print("test_invalid_agent_commit_no_trailer passed.")

