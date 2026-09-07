import json
import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the directory containing the script to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

# Import the function to be tested
from read_github_board import read_board_from_github

class TestReadGithubBoard(unittest.TestCase):

    @patch('read_github_board.default_api')
    def test_read_board_from_github_success(self, mock_default_api):
        """Test reading board data from a GitHub issue with valid JSONL comments."""
        mock_default_api.read_issue.return_value = {
            'read_issue_response': {
                'comments': [
                    {'body': '{"id": 1, "status": "open"}'},
                    {'body': '{"id": 2, "status": "closed"}'},
                ]
            }
        }
        
        repo = "crew"
        issue_number = 102
        board_data = read_board_from_github(repo, issue_number)
        
        self.assertEqual(len(board_data), 2)
        self.assertEqual(board_data[0], {"id": 1, "status": "open"})
        self.assertEqual(board_data[1], {"id": 2, "status": "closed"})
        mock_default_api.read_issue.assert_called_once_with(repo=repo, number=issue_number)

    @patch('read_github_board.default_api')
    def test_read_board_from_github_empty_comments(self, mock_default_api):
        """Test reading board data from a GitHub issue with no comments."""
        mock_default_api.read_issue.return_value = {
            'read_issue_response': {
                'comments': []
            }
        }
        
        repo = "crew"
        issue_number = 102
        board_data = read_board_from_github(repo, issue_number)
        
        self.assertEqual(len(board_data), 0)
        mock_default_api.read_issue.assert_called_once_with(repo=repo, number=issue_number)

    @patch('read_github_board.default_api')
    def test_read_board_from_github_invalid_json_comments(self, mock_default_api):
        """Test reading board data from a GitHub issue with invalid JSON comments."""
        mock_default_api.read_issue.return_value = {
            'read_issue_response': {
                'comments': [
                    {'body': '{"id": 1, "status": "open"}'},
                    {'body': 'this is not json'},
                    {'body': '{"id": 3, "status": "pending"}'},
                ]
            }
        }
        
        repo = "crew"
        issue_number = 102
        board_data = read_board_from_github(repo, issue_number)
        
        self.assertEqual(len(board_data), 2)
        self.assertEqual(board_data[0], {"id": 1, "status": "open"})
        self.assertEqual(board_data[1], {"id": 3, "status": "pending"})
        mock_default_api.read_issue.assert_called_once_with(repo=repo, number=issue_number)

    @patch('read_github_board.default_api')
    def test_read_board_from_github_api_error(self, mock_default_api):
        """Test error handling when default_api.read_issue raises an exception."""
        mock_default_api.read_issue.side_effect = Exception("API Error")
        
        repo = "crew"
        issue_number = 102
        board_data = read_board_from_github(repo, issue_number)
        
        self.assertEqual(len(board_data), 0)
        mock_default_api.read_issue.assert_called_once_with(repo=repo, number=issue_number)

    @patch('read_github_board.default_api')
    def test_read_board_from_github_missing_keys(self, mock_default_api):
        """Test handling of missing keys in the API response."""
        mock_default_api.read_issue.return_value = {
            'read_issue_response': {}}
        
        repo = "crew"
        issue_number = 102
        board_data = read_board_from_github(repo, issue_number)
        
        self.assertEqual(len(board_data), 0)
        mock_default_api.read_issue.assert_called_once_with(repo=repo, number=issue_number)

if __name__ == '__main__':
    unittest.main()
