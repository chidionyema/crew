import subprocess
import os
import pytest

# Define the agent commit trailer
AGENT_TRAILER = "Co-authored-by: Agent Workforce <agent-workforce@example.com>"
GUARD_SCRIPT = "scripts/verify.d/20-agent-commit-guard.sh"

# Helper function to run a git command
def run_git_command(repo_path, command, env=None):
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    return subprocess.run(command, cwd=repo_path, capture_output=True, text=True, check=False, env=full_env)

# Helper function to run the guard script
def run_guard_script(repo_path):
    return subprocess.run([os.path.join(repo_path, GUARD_SCRIPT)], cwd=repo_path, capture_output=True, text=True, check=False)

@pytest.fixture
def temp_git_repo(tmp_path):
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()
    run_git_command(repo_path, ["git", "init"])
    run_git_command(repo_path, ["git", "config", "user.email", "test@example.com"])
    run_git_command(repo_path, ["git", "config", "user.name", "Test User"])
    return repo_path

def test_founder_commit_without_trailer_succeeds(temp_git_repo):
    # Simulate a founder commit (no agent trailer)
    run_git_command(temp_git_repo, ["touch", "file1.txt"])
    run_git_command(temp_git_repo, ["git", "add", "file1.txt"])
    run_git_command(temp_git_repo, ["git", "commit", "-m", "Founder commit"])

    # Run the guard script
    result = run_guard_script(temp_git_repo)
    assert result.returncode == 0, f"Guard failed for valid founder commit: {result.stderr}"
    assert "SUCCESS: Commit attribution check passed for 'Test User'." in result.stdout

def test_agent_commit_with_trailer_succeeds(temp_git_repo):
    # Simulate an agent commit (with agent trailer)
    run_git_command(temp_git_repo, ["git", "config", "user.email", "agent@example.com"])
    run_git_command(temp_git_repo, ["git", "config", "user.name", "Agent Workforce"])
    run_git_command(temp_git_repo, ["touch", "file2.txt"])
    run_git_command(temp_git_repo, ["git", "add", "file2.txt"])
    run_git_command(temp_git_repo, ["git", "commit", "-m", f"Agent commit\n\n{AGENT_TRAILER}"])

    # Run the guard script
    result = run_guard_script(temp_git_repo)
    assert result.returncode == 0, f"Guard failed for valid agent commit: {result.stderr}"
    assert "SUCCESS: Agent commit by 'Agent Workforce' has the required trailer." in result.stdout

def test_agent_commit_without_trailer_fails(temp_git_repo):
    # Simulate an agent commit (missing agent trailer)
    run_git_command(temp_git_repo, ["git", "config", "user.email", "agent@example.com"])
    run_git_command(temp_git_repo, ["git", "config", "user.name", "Agent Workforce"])
    run_git_command(temp_git_repo, ["touch", "file3.txt"])
    run_git_command(temp_git_repo, ["git", "add", "file3.txt"])
    run_git_command(temp_git_repo, ["git", "commit", "-m", "Agent commit without trailer"])

    # Run the guard script
    result = run_guard_script(temp_git_repo)
    assert result.returncode == 1, f"Guard succeeded for invalid agent commit: {result.stdout}"
    assert "ERROR: Agent commit by 'Agent Workforce' is missing the required 'Co-authored-by: Agent Workforce <agent-workforce@example.com>' trailer." in result.stderr

def test_founder_commit_with_trailer_fails(temp_git_repo):
    # Simulate a founder commit (with agent trailer)
    run_git_command(temp_git_repo, ["touch", "file4.txt"])
    run_git_command(temp_git_repo, ["git", "add", "file4.txt"])
    run_git_command(temp_git_repo, ["git", "commit", "-m", f"Founder commit with agent trailer\n\n{AGENT_TRAILER}"])

    # Run the guard script
    result = run_guard_script(temp_git_repo)
    assert result.returncode == 1, f"Guard succeeded for invalid founder commit: {result.stdout}"
    assert "ERROR: Non-agent commit by 'Test User' includes the agent trailer 'Co-authored-by: Agent Workforce <agent-workforce@example.com>'." in result.stderr
