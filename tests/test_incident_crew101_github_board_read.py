import pytest
import subprocess
import json
from scripts.read_github_board import read_github_board

# Mock data for GitHub API response
MOCK_GITHUB_COMMENTS = [
    {"body": "Comment 1 body"},
    {"body": "Comment 2 body"},
    {"body": "Comment 3 body"}
]

MOCK_GITHUB_RESPONSE_JSON = json.dumps(MOCK_GITHUB_COMMENTS)

def test_read_github_board_success(mocker):
    """
    Tests that read_github_board successfully fetches and parses comments.
    """
    mock_run = mocker.patch('subprocess.run')
    mock_run.return_value.stdout = MOCK_GITHUB_RESPONSE_JSON
    mock_run.return_value.returncode = 0
    mock_run.return_value.stderr = ""

    board_rows = read_github_board(repo="test/repo", issue_number=123)

    assert board_rows == ["Comment 1 body", "Comment 2 body", "Comment 3 body"]
    mock_run.assert_called_once_with(
        "gh api -H 'Accept: application/vnd.github.raw' repos/test/repo/issues/123/comments",
        shell=True, capture_output=True, text=True, check=True
    )

def test_read_github_board_api_error(mocker):
    """
    Tests that read_github_board handles GitHub API errors.
    """
    mock_run = mocker.patch('subprocess.run')
    mock_run.side_effect = subprocess.CalledProcessError(1, "gh api ...", stderr="API Error")

    board_rows = read_github_board(repo="test/repo", issue_number=123)

    assert board_rows == []
    mock_run.assert_called_once()

def test_read_github_board_json_decode_error(mocker):
    """
    Tests that read_github_board handles JSON decoding errors.
    """
    mock_run = mocker.patch('subprocess.run')
    mock_run.return_value.stdout = "invalid json"
    mock_run.return_value.returncode = 0
    mock_run.return_value.stderr = ""

    board_rows = read_github_board(repo="test/repo", issue_number=123)

    assert board_rows == []
    mock_run.assert_called_once()
